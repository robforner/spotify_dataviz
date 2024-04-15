# streamlit run "Homepage.py"
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Homepage", page_icon="🏠", layout='wide')

# Import Datasets
dataset = pd.read_csv('prep_songs.csv', sep=',')

st.markdown("""<style>
a:link {
  color: green;
  background-color: transparent;
  text-decoration: none;
}

a:visited {
  color: green;
  background-color: transparent;
  text-decoration: underline;
}
            
a:hover {
  color: green;
  background-color: transparent;
  text-decoration: underline;
}

a:active {
  color: green;
  background-color: transparent;
  text-decoration: underline;
}""", unsafe_allow_html=True)


st.sidebar.header('🏠 Homepage')
with st.sidebar:
    st.markdown("Select one of the pages above to start visualizing the data related to song data on :green[Spotify]!")

st.markdown('<h1 style = "text-align:center">Analyzing and Comparing Artists and Songs</h1>', unsafe_allow_html=True)
st.markdown('<h1 style = "text-align:center">Interactive Data Visualization Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<h1 style = "text-align:center"><a href="https://www.spotify.com">Spotify</a></h1>', unsafe_allow_html=True)
st.markdown('<h3 style = "text-align:center">DeusVult</h3>', unsafe_allow_html=True)
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')


col1, col2, col3 = st.columns([0.5, 0.5, 0.5])
with col2:
    st.image('spotifylogo.png', use_column_width='always')



