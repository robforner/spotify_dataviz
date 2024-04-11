import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Artist Popularity Evolution", page_icon="⭐️", layout='wide',)

# Load the processed dataset
df = pd.read_csv('yearly_popularity.csv')

# Filter the dataset for the specific artists and ensure chronological sorting
artists = ['Eminem', 'Ariana Grande', 'Ed Sheeran', 'The Chainsmokers']
df_filtered = df[df['Artist'].isin(artists)].sort_values('Year')

# Streamlit app layout
st.markdown("# ⭐️ Artist Popularity Evolution")
# Convert 'Year' to string for animation_frame in Plotly
df_filtered['Year'] = df_filtered['Year'].astype(str)

# Create a custom color map for the artists
color_map = {'Eminem': 'aquamarine', 'Ariana Grande': 'darkmagenta', 'Ed Sheeran': 'goldenrod', 'The Chainsmokers': 'color4'}

# Create the moving graph using Plotly Express
fig = px.bar(df_filtered,
             x="Popularity",
             y="Artist",
             color="Artist",
             animation_frame="Year",
             orientation='h',
             range_x=[0, df_filtered['Popularity'].max() + 10],
             color_discrete_map=color_map)

# Update layout for the custom appearance
fig.update_layout(
    showlegend=False,
    xaxis_title="Yearly certified record sales (+digital singles)",
    yaxis_title=None,
    yaxis={'categoryorder':'total ascending'},
    updatemenus=[dict(type='buttons', showactive=False, y=1, x=0.8, xanchor='left', yanchor='bottom')],
)

# Update traces for custom bar styling
fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)

# Display the figure in the Streamlit app
st.plotly_chart(fig)
