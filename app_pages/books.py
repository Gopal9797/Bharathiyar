import streamlit as st

from bharathi.life import BOOKS

st.caption(
    "Several people wrote a life of him. They knew him in different ways, "
    "and they do not agree on every story."
)

for book in BOOKS:
    with st.container(border=True):
        st.markdown(f"**{book['title']}**")
        st.caption(f"{book['english']} · {book['author']}")
        st.markdown(book["about"])
