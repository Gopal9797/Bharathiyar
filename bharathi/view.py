"""Shared cards for opening a work."""

from __future__ import annotations

import streamlit as st

from bharathi.catalog import Work, preview

_RULES = set("-—–=*")


def render_body(text: str, *, verse: bool) -> None:
    """Show the writing without letting edition rules become Markdown headings."""
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and set(stripped) <= _RULES:
            lines.append("")
            continue
        if verse and stripped:
            lines.append(stripped + "  ")
        else:
            lines.append(stripped)
    st.markdown("\n".join(lines))


def render_work_card(work: Work, *, snippet: str, key_prefix: str) -> None:
    with st.container(border=True, height="stretch"):
        st.badge(work.kind_label)
        st.markdown(f"**{work.title}**")
        if work.english_title:
            st.caption(work.english_title)
        else:
            st.caption(work.collection)
        excerpt = snippet or preview(work.text)
        if "**" in excerpt:
            st.markdown(excerpt)
        else:
            st.caption(excerpt)
        if st.button(
            "Read",
            key=f"{key_prefix}_{work.id}",
            icon=":material/menu_book:",
            width="stretch",
        ):
            st.switch_page("app_pages/read.py", query_params={"work": work.id})
