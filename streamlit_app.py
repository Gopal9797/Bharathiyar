import streamlit as st

st.set_page_config(
    page_title="Bharathiyar",
    page_icon=":material/auto_stories:",
    layout="centered",
)

CAPTIONS = {
    "Bharathiyar": "Poems, essays, stories, life writing, and a published speech. Search in Tamil or English.",
    "Pictures": "Portraits, a photograph from 1921, the 1960 stamp, and his signature.",
    "Films": "The 2000 biographical film, a television promo, and songs from the film.",
    "Library": "Browse the shelf by kind and collection.",
    "Search": "Find works from one keyword or several.",
    "Read": "The full text of the work you opened.",
    "Books": "Lives of Bharati written by his wife, a friend, and later scholars.",
    "About": "His life, where these texts come from, and how search works.",
}

page = st.navigation(
    [
        st.Page(
            "app_pages/home.py",
            title="Bharathiyar",
            icon=":material/auto_stories:",
            default=True,
            url_path="home",
            help=(
                "Start here for a short introduction, collection counts, and "
                "a few well-known poems."
            ),
        ),
        st.Page(
            "app_pages/pictures.py",
            title="Pictures",
            icon=":material/portrait:",
            help=(
                "Public-domain portraits, the 1921 photograph, the 1960 stamp, "
                "and Bharati's signature, each with its source."
            ),
        ),
        st.Page(
            "app_pages/films.py",
            title="Films",
            icon=":material/movie:",
            help=(
                "Watch the 2000 film Bharathi, the Doordarshan promo, "
                "and songs from the film on YouTube."
            ),
        ),
        st.Page(
            "app_pages/library.py",
            title="Library",
            icon=":material/library_books:",
            help=(
                "Browse poems, articles, stories, speeches, and life writing. Filter by "
                "kind or collection, then open a work."
            ),
        ),
        st.Page(
            "app_pages/search.py",
            title="Search",
            icon=":material/search:",
            help=(
                "Search by Tamil or English keywords. Match any word or every "
                "word, then add a related theme."
            ),
        ),
        st.Page(
            "app_pages/read.py",
            title="Read",
            icon=":material/menu_book:",
            url_path="read",
            help="Read the full Tamil text of one work, with related pieces beside it.",
        ),
        st.Page(
            "app_pages/books.py",
            title="Books",
            icon=":material/book:",
            help=(
                "Five published lives of Bharati, from Chellamma and Va. Ra. "
                "to later studies by Prema Nandakumar and S. Vijaya Bharati."
            ),
        ),
        st.Page(
            "app_pages/about.py",
            title="About",
            icon=":material/info:",
            help=(
                "Dates from his life, the public-domain sources, "
                "and how keyword search is matched."
            ),
        ),
    ],
    position="top",
)

st.title(page.title, icon=page.icon)
st.caption(CAPTIONS[page.title])
page.run()
