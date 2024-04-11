import streamlit as st
import datetime
import pandas as pd
import altair as alt
import plotly.express as px
from Homepage import dataset
from savestate import load_selections, save_selections

st.set_page_config(page_title="Song Releases by Artist", page_icon="🎤", layout='wide')

# Savefiles 
saved_artists = 'saved_artists.json'
saved_tracktype = 'saved_tracktype_1.json'

# Preliminary Preprocessing
artists = sorted(list(set(dataset['track_artist'].values.tolist())))
dataset['track_album_release_date'] = pd.to_datetime(dataset['track_album_release_date'])
dataset['track_popularity'] = dataset['track_popularity'].astype(float)

def artist_song_plot(df):
    df = df[df['track_artist'].isin(load_selections(saved_artists))]
    artist_names = ', '.join(sorted(set(df['track_artist'])))

    # Creating the Plotly visualization
    fig = px.scatter(
        df,
        x='track_album_release_date',
        y='track_artist',
        color='track_popularity',
        color_continuous_scale='deep',
        size_max=60,
        hover_name='track_name',
        hover_data={
            'track_album_name': True,
            'track_album_release_date': True,
            'track_popularity': True,
            # Since y-axis is categorical (artist names), it doesn't make sense to have it in the tooltip
            'track_artist': False
        },
        title=f"Song Release Timeline for {artist_names}",
        height=600,
        width = 950
    )

    fig.update_layout(
        yaxis_categoryorder='total ascending',  # Sort artists based on the number of songs
        xaxis_title='Release Date',
        yaxis_title='Artist',
        coloraxis_colorbar=dict(title='Track Popularity'),
    )

    st.plotly_chart(fig)


st.markdown("# 🎤 Song Releases by Artist")
help = st.toggle('Help', value=True)
if help:
    st.markdown("Select visualization options from the sidebar on the left. If no options are visible visible please click on the arrow at the top left of the screen.")

st.sidebar.header("🎤 Song Releases by Artist")
with st.sidebar:
    help = st.toggle('Info', key=7, value=True)
    if help:
        st.markdown("Visualize the number of guests who visited a specific ride in a single day or in a range of days.")
    
    selected_artists = st.multiselect("Select one or more artists:", artists, default=load_selections(saved_artists), key='arts')
    if 'selected_artists' not in st.session_state:
        st.session_state['selected_artists'] = selected_artists
    if st.button("Show and Save", help='Shows the information and saves the selected artists'):
        save_selections(saved_artists, selected_artists)
        st.success("Selections saved!")

    track_options = ['Original and Remixed Tracks', 'Original Tracks', 'Remixed Tracks']
    track_type = st.radio('Select the kind of track:', track_options, index=track_options.index(load_selections(saved_tracktype)))
    if 'track_type' not in st.session_state:
        st.session_state['track_type'] = track_type
    if st.button("Show and Save", help='Shows and saves the selected type of track', key=100):
        save_selections(saved_tracktype, track_type)
        st.success("Selections saved!")


if load_selections(saved_tracktype) == 'Original Tracks':
    filtered_df = dataset[~dataset['track_name'].str.contains('remix', case=False)]
    artist_song_plot(filtered_df)
if load_selections(saved_tracktype) == 'Remixed Tracks':
    filtered_df = dataset[dataset['track_name'].str.contains('remix', case=False)]
    artist_song_plot(filtered_df)
if load_selections(saved_tracktype) == 'Original and Remixed Tracks':
    artist_song_plot(dataset)

