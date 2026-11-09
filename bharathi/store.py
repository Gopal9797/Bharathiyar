"""Cached access to the catalog for the Streamlit app."""

from __future__ import annotations

import streamlit as st

from bharathi.catalog import WORKS_PATH, Work, load_works


@st.cache_data
def _load_works(_stamp: float) -> tuple[Work, ...]:
    return load_works()


def get_works() -> tuple[Work, ...]:
    stamp = WORKS_PATH.stat().st_mtime if WORKS_PATH.exists() else 0
    return _load_works(stamp)
