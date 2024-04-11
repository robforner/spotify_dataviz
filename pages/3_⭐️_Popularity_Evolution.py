import pandas as pd
import plotly.express as px
import streamlit as st
import Homepage as dataset

st.set_page_config(page_title="Artist Popularity Evolution", page_icon="⭐️", layout='wide',)

playlist_appearances = dataset.groupby('track_artist')['playlist_name'].nunique().reset_index(name='unique_playlists')

# Sorting artists by the number of unique playlist appearances
playlist_appearances_sorted = playlist_appearances.sort_values(by='unique_playlists', ascending=False)

# Creating the bar chart
fig = px.bar(playlist_appearances_sorted, x='track_artist', y='unique_playlists',
             title='Most Playlist Appearances per Artist',
             labels={'track_artist': 'Artist', 'unique_playlists': 'Number of Unique Playlists'},
             height=600)

# Improving layout
fig.update_xaxes(tickangle=-45)

# Display the figure
st.plotly_chart(fig)