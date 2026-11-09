import streamlit as st

from bharathi.media import FILMS

titles = [film["title"] for film in FILMS]
choice = st.selectbox("Choose a film or song", titles)
film = next(item for item in FILMS if item["title"] == choice)

st.caption(film["detail"])
st.video(film["url"], alt=film["title"])
st.link_button(
    "Open on YouTube",
    film["url"],
    icon=":material/open_in_new:",
)
