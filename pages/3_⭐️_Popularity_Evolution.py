import pandas as pd
import plotly.express as px
import streamlit as st
from Homepage import dataset

st.set_page_config(page_title="Artist Popularity Evolution", page_icon="⭐️", layout='wide',)


st.markdown('# ⭐️ Artist Popularity Evolution')

dataset['track_album_release_date'] = pd.to_datetime(dataset['track_album_release_date'])

# Extract the year from the release date
dataset['year'] = dataset['track_album_release_date'].dt.year

# Filter the data for the specified artists
filtered_data = dataset[dataset['track_artist'].isin(['Ed Sheeran', 'Ariana Grande', 'The Chainsmokers'])]

# Group by artist and year, then count the number of unique playlists
playlist_appearances_by_year = filtered_data.groupby(['track_artist', 'year'])['playlist_name'].nunique().reset_index(name='unique_playlists')

# Sorting the data for plotting
playlist_appearances_by_year_sorted = playlist_appearances_by_year.sort_values(by=['track_artist', 'year'])

# Creating the line chart
fig = px.line(playlist_appearances_by_year_sorted, x='year', y='unique_playlists', color='track_artist',
              title='Evolution of Artist Popularity Through Time',
              labels={'year': 'Year', 'unique_playlists': 'Number of Unique Playlists', 'track_artist': 'Artist'},
              markers=True, # Adding markers to points for clarity
              height=600)

# Improving layout
fig.update_xaxes(tickangle=-45)

# Display the figure with Streamlit
st.plotly_chart(fig)