import streamlit as st

from bharathi.catalog import KIND_LABELS, KIND_ORDER, preview, search
from bharathi.store import get_works
from bharathi.view import render_work_card

works = get_works()
collections = tuple(sorted({work.collection for work in works}))

if "library_limit" not in st.session_state:
    st.session_state.library_limit = 12


def reset_library_limit() -> None:
    st.session_state.library_limit = 12


def show_more_library() -> None:
    st.session_state.library_limit = st.session_state.get("library_limit", 12) + 12


kind_labels = [KIND_LABELS[kind] for kind in KIND_ORDER]
label_to_kind = {label: kind for kind, label in zip(KIND_ORDER, kind_labels, strict=True)}

with st.container(horizontal=True, vertical_alignment="bottom"):
    picked_labels = st.pills(
        "Kind",
        kind_labels,
        selection_mode="multi",
        key="library_kind",
        persist_state="session",
        on_change=reset_library_limit,
        help="Leave this empty to show every kind.",
    )
    collection = st.selectbox(
        "Collection",
        ("All collections", *collections),
        key="library_collection",
        persist_state="session",
        on_change=reset_library_limit,
    )

kinds = [label_to_kind[label] for label in (picked_labels or [])]
chosen_collection = None if collection == "All collections" else collection
hits = search(
    works,
    kinds=kinds,
    collection=chosen_collection,
)
# search() returns nothing when every filter is empty, so an unfiltered shelf
# is the whole catalog in shelf order.
if not kinds and chosen_collection is None:
    hits_works = list(works)
else:
    hits_works = [hit.work for hit in hits]

st.caption(f"{len(hits_works)} works")
shown = hits_works[: st.session_state.library_limit]
with st.grid(2, min_column_width=280):
    for work in shown:
        render_work_card(work, snippet=preview(work.text, 160), key_prefix="library")

if len(hits_works) > len(shown):
    st.button(
        f"Show more · {len(hits_works) - len(shown)} left",
        key="library_more",
        on_click=show_more_library,
        icon=":material/expand_more:",
    )
