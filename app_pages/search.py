import streamlit as st

from bharathi.catalog import KIND_LABELS, KIND_ORDER, THEME_LABELS, related_keywords, search
from bharathi.store import get_works
from bharathi.view import render_work_card

works = get_works()
theme_ids = tuple(THEME_LABELS)
theme_labels = [THEME_LABELS[theme] for theme in theme_ids]
label_to_theme = {THEME_LABELS[theme]: theme for theme in theme_ids}
kind_labels = [KIND_LABELS[kind] for kind in KIND_ORDER]
label_to_kind = {label: kind for kind, label in zip(KIND_ORDER, kind_labels, strict=True)}

EXAMPLES = ("விடுதலை", "பெண்", "தமிழ்", "அச்சம்", "freedom")

if "search_limit" not in st.session_state:
    st.session_state.search_limit = 12


def apply_example() -> None:
    picked = st.session_state.get("example_keyword")
    if picked:
        st.session_state.q = picked
        st.session_state.search_limit = 12


def add_keyword(token: str) -> None:
    current = str(st.session_state.get("q") or "").strip()
    words = current.split()
    if token not in words:
        st.session_state.q = f"{current} {token}".strip()
    st.session_state.search_limit = 12


def show_more_search() -> None:
    st.session_state.search_limit = st.session_state.get("search_limit", 12) + 12


query = st.text_input(
    "Keywords",
    key="q",
    type="search",
    placeholder="விடுதலை, பெண், freedom, caste",
    help="Separate words with spaces or commas. Tamil and English both work.",
    icon=":material/search:",
    live=True,
    bind="query-params",
)

st.pills(
    "Examples",
    EXAMPLES,
    key="example_keyword",
    on_change=apply_example,
    help="Fills the keyword box with one starting word.",
)

match_label = st.segmented_control(
    "Match",
    ["Any keyword", "All keywords"],
    default="Any keyword",
    key="match",
    bind="query-params",
    help="Any keyword finds a work if one word hits. All keywords requires every word.",
)
match = "all" if match_label == "All keywords" else "any"

picked_kinds = st.pills(
    "Kind",
    kind_labels,
    selection_mode="multi",
    key="search_kind",
    persist_state="session",
    help="Leave this empty to search every kind.",
)
picked_themes = st.multiselect(
    "Themes",
    theme_labels,
    key="search_themes",
    persist_state="session",
    help="A work is kept if it carries any theme you pick.",
    placeholder="Any theme",
)

kinds = [label_to_kind[label] for label in (picked_kinds or [])]
themes = [label_to_theme[label] for label in (picked_themes or [])]
has_filter = bool(query.strip() or kinds or themes)

if not has_filter:
    st.info(
        "Try விடுதலை, பெண், தமிழ், or an English word such as freedom, women, or caste.",
        title="Enter a keyword",
        icon=":material/travel_explore:",
    )
else:
    hits = search(works, query, match=match, kinds=kinds, themes=themes)
    st.caption(f"{len(hits)} matches · {match} keyword")
    if not hits:
        st.info(
            "Try a shorter Tamil stem, switch to Any keyword, or clear a theme.",
            title="No matches",
            icon=":material/search_off:",
        )
    else:
        suggestions = related_keywords(hits, query)
        if suggestions:
            st.markdown("**Related keywords**")
            st.caption("Adds a theme word from these results.")
            with st.container(horizontal=True):
                for label, token in suggestions:
                    st.button(
                        label,
                        key=f"related_{token}",
                        on_click=add_keyword,
                        args=(token,),
                    )
        shown = hits[: st.session_state.search_limit]
        with st.grid(2, min_column_width=280):
            for hit in shown:
                render_work_card(hit.work, snippet=hit.snippet, key_prefix="search")
        if len(hits) > len(shown):
            st.button(
                f"Show more · {len(hits) - len(shown)} left",
                key="search_more",
                on_click=show_more_search,
                icon=":material/expand_more:",
            )
