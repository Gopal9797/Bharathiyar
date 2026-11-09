import streamlit as st

from bharathi.media import ASSETS, PICTURES

st.caption("These pictures are stored with the app. Each caption names the license.")

with st.grid(2, min_column_width=260):
    for picture in PICTURES:
        with st.container(border=True):
            st.image(
                ASSETS / picture["file"],
                caption=picture["caption"],
                alt=picture["alt"],
                width="stretch",
            )
