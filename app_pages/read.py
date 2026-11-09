import streamlit as st

from bharathi.catalog import preview, related_works, work_by_id
from bharathi.store import get_works
from bharathi.view import render_body, render_work_card

works = get_works()
work_id = str(st.query_params.get("work", ""))
work = work_by_id(works, work_id) if work_id else None

if work is None:
    st.info(
        "Open a poem, article, or speech from the library or from search.",
        title="Nothing open",
        icon=":material/menu_book:",
    )
    if st.button("Go to the library", icon=":material/library_books:"):
        st.switch_page("app_pages/library.py")
else:
    st.header(work.title)
    st.badge(work.kind_label)
    if work.english_title:
        st.markdown(f"**{work.english_title}**")
    st.caption(work.collection)
    if work.themes:
        with st.container(horizontal=True):
            for label in work.theme_labels:
                st.badge(label, color="gray")
    if work.note:
        st.info(work.note, title="About this text", icon=":material/record_voice_over:")

    render_body(work.text, verse=work.kind == "poem")

    download = (
        f"{work.title}\n"
        f"{work.english_title}\n\n"
        f"{work.text}\n\n"
        f"Source: {work.source}\n"
        f"{work.source_url}\n"
    )
    st.download_button(
        "Download text",
        data=download,
        file_name=f"{work.id}.txt",
        mime="text/plain",
        icon=":material/download:",
    )
    st.caption(f"{work.source}. {work.source_url}")

    others = related_works(works, work)
    if others:
        st.subheader("Related works")
        with st.grid(3, min_column_width=220):
            for other in others:
                render_work_card(other, snippet=preview(other.text, 120), key_prefix="related")
