import streamlit as st

from bharathi.catalog import KIND_ORDER
from bharathi.life import EVENTS, SPEECHES
from bharathi.store import get_works

works = get_works()
counts = {kind: sum(1 for work in works if work.kind == kind) for kind in KIND_ORDER}

st.subheader("Subramania Bharati")
st.markdown(
    """
Subramania Bharati (1882–1921), known in Tamil as Bharathiyar, was born in
Ettayapuram. He wrote poems, songs, essays, and stories for the freedom
movement, for women's emancipation, against caste, and in devotion. He edited
the journals *India* and later wrote for *Swadesamitran*.

The Madras government nationalised his writings in 1949. They are in the
public domain.
"""
)

st.subheader("Life")
st.caption(
    "These dates follow the Puducherry museum, the Government of India note, "
    "and the standard English accounts. A few early years are still told differently from book to book."
)
for year, detail in EVENTS:
    st.markdown(f"**{year}.** {detail}")

if st.button("Read his own account, கனவு", icon=":material/menu_book:"):
    st.switch_page("app_pages/read.py", query_params={"work": "songs-037"})

st.subheader("Speeches")
st.markdown(
    """
He spoke often, at public gatherings, nationalist rallies, and literary
meetings. Books dwell on the last speech, which can make it look like the
only one. This shelf prints one speech summary, from an address in 1920,
and his own account of the Erode visit, published in *Swadesamitran* on
4 August 1921. The occasions below are ones the records still name.
"""
)
for speech in SPEECHES:
    with st.container(border=True):
        st.markdown(f"**{speech['title']}**")
        st.caption(speech["when"])
        st.markdown(speech["about"])

with st.container(horizontal=True):
    if st.button("Read the printed speech summary", icon=":material/record_voice_over:"):
        st.switch_page("app_pages/read.py", query_params={"work": "essays-049"})
    if st.button("Read his Erode account", icon=":material/menu_book:"):
        st.switch_page("app_pages/read.py", query_params={"work": "erode-001"})

st.subheader("What is on this shelf")
st.markdown(
    f"""
This shelf holds {len(works):,} pieces. {counts["poem"]:,} are poems, including
கண்ணன் பாட்டு, குயில் பாட்டு, பாஞ்சாலி சபதம், and விநாயகர் நான்மணிமாலை.
{counts["article"]:,} are articles, including his பகவத் கீதை commentary and
என் ஈரோடு யாத்திரை. {counts["story"]:,} are stories, including கதைக் கொத்து,
நவதந்திரக் கதைகள், and சந்திரிகையின் கதை. {counts["speech"]:,} is the printed
summary of a 1920 address. {counts["life"]:,} are pieces of life writing.

Most of the wording follows Project Madurai electronic editions, including
their line breaks and any transcription slips. என் ஈரோடு யாத்திரை is his
article from *Swadesamitran*, 4 August 1921. English lines under a title are
short glosses of the title, not verse translations.
"""
)

st.subheader("How search works")
st.markdown(
    """
Type one word or several. Spaces and commas separate keywords.

- **Any keyword** keeps a work when one of the words appears.
- **All keywords** keeps a work only when every word appears.
- A Tamil word matches from the start of a word, so பெண் finds பெண்மை and
  பெண்கள்.
- These English words also search the Tamil text: freedom, liberty, tamil,
  nation, india, women, woman, courage, fearless, devotion, krishna,
  education, learning, caste, labor, labour, poverty, leader, gandhi, tilak.
- **Related keywords** offers themes that show up in the current results.
  Choosing one adds that Tamil word to the query.
- Kind and theme filters narrow the same results. A theme filter keeps a
  work if it has any theme you selected.

A search such as `?q=விடுதலை` can be shared. The Match control is stored in
the page address as well.
"""
)

st.subheader("Sources")
st.markdown(
    """
The Project Madurai texts may be shared when this acknowledgement stays with
them. Project Madurai is an open initiative that prepares electronic texts of
Tamil literature and distributes them free of charge.
"""
)
seen_urls: set[str] = set()
for work in works:
    if not work.source_url or work.source_url in seen_urls:
        continue
    seen_urls.add(work.source_url)
    st.markdown(f"- [{work.source}]({work.source_url})")
st.subheader("Pictures and films")
st.markdown(
    """
The pictures are historical images from Wikimedia Commons. The licenses are
on each caption. The films and songs open from YouTube; this app does not
host those videos.
"""
)
st.caption("Electronic editions © Project Madurai, 1998–2016. Bharati's own writings are in the public domain.")
