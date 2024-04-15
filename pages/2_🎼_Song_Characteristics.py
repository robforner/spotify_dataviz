import streamlit as st
import datetime
import pandas as pd
import altair as alt
import plotly.express as px
from Homepage import dataset
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
from savestate import load_selections, save_selections
from featuredesc_txt import feature_desc_txt

st.set_page_config(page_title="Song Characteristics", page_icon="🎼", layout='wide')
saved_artists = "saved_artists.json"
saved_tracktype = 'saved_tracktype_2.json'

st.markdown("# 🎼 Song Characteristics")
help = st.toggle('Help', value=True)
if help:
    st.markdown("Select visualization options from the sidebar on the left. If no options are visible visible please click on the arrow at the top left of the screen.")

feature_desc = st.toggle('Song Feature Descriptions')
if feature_desc:
    for k, v in feature_desc_txt.items():
        if st.checkbox(k):
            st.markdown(v)

dataset['track_popularity'] = dataset['track_popularity'].astype(float)
dataset = dataset.drop(['playlist_name', 'playlist_genre', 'playlist_subgenre', 'track_album_name','track_album_release_date'], axis=1)
dataset = dataset.drop_duplicates()
song_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
selected_artists = load_selections(saved_artists)

def plot_song_features(df, artist, features, song_choice):
    scaler = MinMaxScaler()
    df = df[df['track_artist'].isin(selected_artists)]
    columns = ['track_name', 'track_artist', 'mode', 'key'] + song_features
    df_toplot = df[columns]
    df_toplot[song_features] = scaler.fit_transform(df_toplot[song_features])
    df_toplot['mode'] = df_toplot['mode'].apply(lambda x: 'major' if x == 1 else 'minor' if x == 0 else x)

    pitch_class_mapping = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"}
    df_toplot['key'] = df_toplot['key'].apply(lambda x: pitch_class_mapping.get(x, x))
    df_toplot = df_toplot.loc[df_toplot['track_artist'] == artist]

    df_toplot = df_toplot[['track_name'] + features]
    df_toplot = df.loc[df['track_name'].isin(song_choice)]
    
    ft_toshow = ', '.join(sorted(features))

    fig = go.Figure()
    for i, song_data in enumerate(df_toplot[features].values.tolist()):
        fig.add_trace(go.Scatterpolar(
            r=song_data,
            theta=features,
            fill='toself',
            name=df_toplot.iloc[i]['track_name']
        ))

    # Update the layout
    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 1]
        )),
    showlegend=True,
    title = f"Comparison of {ft_toshow} in selected songs"
    )
    # st.dataframe(df_toplot)
    st.plotly_chart(fig)

st.sidebar.header("🎤 Song Releases by Artist")
with st.sidebar:
    help = st.toggle('Info', key=7, value=True)
    if help:
        st.markdown("Select the features and the songs from the artists selected in the previous page to visualize and compare them. Up to 5 different features are allowed.")

    track_options = ['Original and Remixed Tracks', 'Original Tracks', 'Remixed Tracks']
    track_type = st.radio('Select the kind of track:', track_options, index=track_options.index(load_selections(saved_tracktype)))
    if 'track_type' not in st.session_state:
        st.session_state['track_type'] = track_type
    if st.button("Show and Save", help='Shows and saves the selected type of track', key=100):
        save_selections(saved_tracktype, track_type)
        st.success("Selections saved!")


for artist in selected_artists:
    df_artist = dataset.loc[dataset['track_artist'] == artist]
    
    st.markdown(f'<h2>{artist}</h2>', unsafe_allow_html=True)
    features = st.multiselect('Select the song features to be visualized', song_features, key=artist, max_selections=5, default=['energy', 'speechiness', 'liveness', 'valence'])
    
    if load_selections(saved_tracktype) == 'Original Tracks':
        filtered_df = df_artist[~df_artist['track_name'].str.contains('remix', case=False)]
        artist_songs = sorted(list(set(filtered_df['track_name'].values.tolist())))
        song_choice = st.multiselect('Select the songs', artist_songs, key=artist+'1', max_selections=5)
        plot_song_features(filtered_df, artist, features, song_choice)

    if load_selections(saved_tracktype) == 'Remixed Tracks':
        filtered_df = df_artist[df_artist['track_name'].str.contains('remix', case=False)]
        artist_songs = sorted(list(set(filtered_df['track_name'].values.tolist())))
        song_choice = st.multiselect('Select the songs', artist_songs, key=artist+'1', max_selections=5)
        plot_song_features(filtered_df, artist, features, song_choice)

    if load_selections(saved_tracktype) == 'Original and Remixed Tracks':
        artist_songs = sorted(list(set(df_artist['track_name'].values.tolist())))
        song_choice = st.multiselect('Select the songs', artist_songs, key=artist+'1', max_selections=5)
        plot_song_features(df_artist, artist, features, song_choice)
    
