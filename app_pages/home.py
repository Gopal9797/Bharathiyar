import streamlit as st

from bharathi.catalog import KIND_ORDER, preview
from bharathi.media import ASSETS, PICTURES
from bharathi.store import get_works
from bharathi.view import render_work_card

works = get_works()
counts = {kind: sum(1 for work in works if work.kind == kind) for kind in KIND_ORDER}

portrait = PICTURES[0]

photo, words = st.columns([1, 2], vertical_alignment="center")
with photo:
    st.image(
        ASSETS / portrait["file"],
        caption="Subramania Bharati",
        alt=portrait["alt"],
        width="stretch",
    )
with words:
    fearless = next((work for work in works if work.title == "அச்சமில்லை"), None)
    if fearless is not None:
        opening = next(
            (
                line.strip()
                for line in fearless.text.splitlines()
                if line.strip() and not line.strip().startswith("(")
            ),
            "",
        )
        st.markdown(f"> {opening}")
    st.caption("அச்சமில்லை · There is no fear")

with st.grid(5, min_column_width=120):
    st.metric("Works", f"{len(works):,}")
    st.metric("Poems", f"{counts['poem']:,}")
    st.metric("Articles", f"{counts['article']:,}")
    st.metric("Stories", f"{counts['story']:,}")
    st.metric("Speech texts", f"{counts['speech']:,}")

st.caption(
    f"Also on the shelf: {counts['life']} pieces of life writing. "
    "The speech count is printed text in this edition. "
    "He addressed many meetings; About lists the ones still remembered."
)

st.subheader("Longer works")
st.caption("Poems, stories, and his own account of the last journey, now on the shelf.")
longer_titles = (
    "விநாயகர் நான்மணிமாலை",
    "என் ஈரோடு யாத்திரை",
)
longer = [work for title in longer_titles for work in works if work.title == title]
for needle in ("கண்ணன் பாட்டு", "பாஞ்சாலி சபதம்", "கதைக் கொத்து", "பகவத் கீதை"):
    match = next((work for work in works if needle in work.collection), None)
    if match is not None:
        longer.append(match)

with st.grid(3, min_column_width=240):
    for work in longer:
        render_work_card(work, snippet=preview(work.text, 140), key_prefix="home_long")

st.subheader("Open a well-known poem")
featured_titles = (
    "செந்தமிழ் நாடு",
    "அச்சமில்லை",
    "பாப்பாப் பாட்டு",
    "பாரத தேசம்",
    "காணி நிலம் வேண்டும்",
    "பெண் விடுதலை",
)
featured = []
for title in featured_titles:
    match = next((work for work in works if work.title == title and work.kind == "poem"), None)
    if match is not None:
        featured.append(match)

with st.grid(3, min_column_width=240):
    for work in featured:
        render_work_card(work, snippet=preview(work.text, 140), key_prefix="home")

st.subheader("Try a keyword")
st.caption("These open Search with the word already filled in.")
examples = (
    ("விடுதலை", "Freedom"),
    ("பெண்", "Women"),
    ("தமிழ்", "Tamil"),
    ("சாதி", "Caste"),
    ("கல்வி", "Learning"),
)
with st.container(horizontal=True):
    for token, label in examples:
        if st.button(f"{label}", key=f"home_kw_{token}", help=token):
            st.switch_page("app_pages/search.py", query_params={"q": token})
