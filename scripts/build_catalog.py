"""Build data/works.json from Project Madurai Unicode editions."""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bharathi.catalog import english_title_for, tag_themes

SOURCE_DIR = ROOT / "data" / "sources"
OUT_PATH = ROOT / "data" / "works.json"

SOURCES: tuple[dict[str, str], ...] = (
    {
        "key": "national",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0012_01.html",
        "file": "pmuni0012_01.html",
        "default_kind": "poem",
        "credit": "Project Madurai, pmuni0012 — தேசிய கீதங்கள்",
    },
    {
        "key": "devotional",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0012_02.html",
        "file": "pmuni0012_02.html",
        "default_kind": "poem",
        "credit": "Project Madurai, pmuni0012 — தெய்வப் பாடல்கள்",
    },
    {
        "key": "songs",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0021.html",
        "file": "pmuni0021.html",
        "default_kind": "poem",
        "credit": "Project Madurai, pmuni0021 — ஞானம், பல்வகை, சுயசரிதை",
    },
    {
        "key": "essays",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0542.html",
        "file": "pmuni0542.html",
        "default_kind": "article",
        "credit": "Project Madurai, pmuni0542 — கட்டுரைகள் தொகுப்பு 1",
    },
    {
        "key": "kannan",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0049.html",
        "file": "pmuni0049.html",
        "default_kind": "poem",
        "credit": "Project Madurai, pmuni0049 — கண்ணன் பாட்டு, குயில் பாட்டு",
    },
    {
        "key": "panchali-1",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0091.html",
        "file": "pmuni0091.html",
        "default_kind": "poem",
        "credit": "Project Madurai, pmuni0091 — பாஞ்சாலி சபதம், பாகம் 1",
    },
    {
        "key": "panchali-2",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0888.html",
        "file": "pmuni0888.html",
        "default_kind": "poem",
        "split": "h3",
        "credit": "Project Madurai, pmuni0888 — பாஞ்சாலி சபதம், பாகம் 2",
    },
    {
        "key": "vinayagar",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0245.html",
        "file": "pmuni0245.html",
        "default_kind": "poem",
        "split": "single",
        "start": "விநாயகர் நான்மணிமாலை",
        "credit": "Project Madurai, pmuni0245 — விநாயகர் நான்மணிமாலை",
    },
    {
        "key": "gita",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0014.html",
        "file": "pmuni0014.html",
        "default_kind": "article",
        "credit": "Project Madurai, pmuni0014 — பகவத் கீதை",
    },
    {
        "key": "gita-preface",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0529.html",
        "file": "pmuni0529.html",
        "default_kind": "article",
        "split": "h3",
        "credit": "Project Madurai, pmuni0529 — பகவத் கீதை",
    },
    {
        "key": "chandrikai",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0095.html",
        "file": "pmuni0095.html",
        "default_kind": "story",
        "split": "h3",
        "credit": "Project Madurai, pmuni0095 — சந்திரிகையின் கதை",
    },
    {
        "key": "stories",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0536.html",
        "file": "pmuni0536.html",
        "default_kind": "story",
        "split": "h3",
        "credit": "Project Madurai, pmuni0536 — கதைக் கொத்து",
    },
    {
        "key": "navatantra",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0630.html",
        "file": "pmuni0630.html",
        "default_kind": "story",
        "split": "h3",
        "credit": "Project Madurai, pmuni0630 — நவதந்திரக் கதைகள்",
    },
    {
        "key": "sankaran",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0631.html",
        "file": "pmuni0631.html",
        "default_kind": "story",
        "credit": "Project Madurai, pmuni0631 — சின்னச் சங்கரன் கதை",
    },
    {
        "key": "gnanaratham",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0632.html",
        "file": "pmuni0632.html",
        "default_kind": "article",
        "split": "h3",
        "credit": "Project Madurai, pmuni0632 — ஞானரதம்",
    },
    {
        "key": "stories-1",
        "url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0633.html",
        "file": "pmuni0633.html",
        "default_kind": "story",
        "credit": "Project Madurai, pmuni0633 — சிறுகதைகள், பாகம் 1",
    },
)

TOKEN_RE = re.compile(r"(?is)<h3[^>]*>(.*?)</h3>|<strong>\s*(.*?)\s*</strong>")
SPEECH_MARKERS = (
    "பாரதி செய்த பிரசங்க",
    "பாரதியார் செய்த பிரசங்க",
    "சுப்பிரமணிய பாரதி செய்த பிரசங்க",
)
LIFE_TITLES = {"கனவு", "பாரதி - அறுபத்தாறு"}


def tamil_count(value: str) -> int:
    return sum(1 for char in value if "\u0b80" <= char <= "\u0bff")


def strip_tags(value: str) -> str:
    value = re.sub(r"(?is)<br\s*/?>\s*", "\n", value)
    value = re.sub(r"(?is)</p\s*>", "\n\n", value)
    value = re.sub(r"(?is)<[^>]+>", "", value)
    return html.unescape(value)


def clean_title(value: str) -> str:
    lines = [line.strip() for line in strip_tags(value).splitlines() if line.strip()]
    numbered = [line for line in lines if re.match(r"^\d+\.", line)]
    chosen = numbered[-1] if numbered else " ".join(lines)
    title = " ".join(chosen.split())
    title = re.sub(r"^\d+\.\s*", "", title)
    return title.strip(" .")


def collection_name(heading: str) -> str:
    title = clean_title(heading)
    for name in (
        "தேசிய கீதங்கள்",
        "தெய்வப் பாடல்கள்",
        "ஞானப் பாடல்கள்",
        "பல்வகைப் பாடல்கள்",
        "சுயசரிதை",
        "கட்டுரைகள்",
        "கண்ணன் பாட்டு",
        "குயில் பாட்டு",
        "பாஞ்சாலி சபதம்",
        "விநாயகர் நான்மணிமாலை",
        "பகவத் கீதை",
        "கதைக் கொத்து",
        "சந்திரிகையின் கதை",
        "நவதந்திர",
        "சின்னச் சங்கரன்",
        "ஞானரதம்",
        "சிறுகதை",
        "தமிழ்நாடு",
        "தேசிய இயக்கப் பாடல்கள்",
        "தேசீயத் தலைவர்கள்",
        "பிற நாடுகள்",
    ):
        if name in title:
            return name
    return title


def to_text(fragment: str) -> str:
    text = strip_tags(fragment).replace("\r\n", "\n").replace("\r", "\n")
    lines = [" ".join(line.split()) for line in text.split("\n")]
    collapsed = "\n".join(lines)
    collapsed = re.sub(r"\n{3,}", "\n\n", collapsed).strip()
    return collapsed


def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 1000:
        return
    request = Request(url, headers={"User-Agent": "BharathiyarArchive/1.0"})
    with urlopen(request, timeout=180) as response:
        dest.write_bytes(response.read())


def is_book_heading(title: str) -> bool:
    folded = title.lower()
    if tamil_count(title) < 4:
        return True
    if any(marker in title for marker in ("உள்ளடக்கம்", "முற்றிற்று", "Acknowledgements")):
        return True
    if "acknowledgement" in folded or "project madurai" in folded:
        return True
    if title.startswith(("சி. சுப்", "சி.சுப்", "மகாகவி பாரதியார் எழுதிய")):
        return True
    if "songs of" in folded:
        return True
    return False


def make_work(
    spec: dict[str, str],
    index: int,
    title: str,
    text: str,
    collection: str,
) -> dict[str, object]:
    kind = spec["default_kind"]
    note = ""
    if title in LIFE_TITLES or "சுயசரிதை" in collection:
        kind = "life"
    elif any(marker in text[:800] or marker in title for marker in SPEECH_MARKERS):
        kind = "speech"
        note = (
            "Published summary of an address by Bharati, "
            "as printed in the Project Madurai essay edition."
        )
    return {
        "id": f"{spec['key']}-{index:03d}",
        "title": title,
        "english_title": english_title_for(title),
        "kind": kind,
        "collection": collection,
        "themes": list(tag_themes(title, text)),
        "text": text,
        "note": note,
        "source": spec["credit"],
        "source_url": spec["url"],
    }


def parse_source(spec: dict[str, str]) -> list[dict[str, object]]:
    raw = (SOURCE_DIR / spec["file"]).read_text(encoding="utf-8", errors="replace")
    collection = spec["credit"].split("—", 1)[-1].strip()
    if spec.get("split") == "single":
        marker = spec.get("start") or collection
        start = 0
        for heading in re.finditer(r"(?is)<h3[^>]*>.*?</h3>", raw):
            plain = strip_tags(heading.group(0))
            if marker in plain and "புனைந்த" not in plain:
                start = heading.end()
        for match in re.finditer(r"(?is)<strong>\s*(.*?)\s*</strong>", raw[start:]):
            label = clean_title(match.group(1))
            if label in {"வெண்பா", "கலித்துறை", "விருத்தம்", "அகவல்"}:
                start += match.start()
                break
        text = to_text(raw[start:])
        if text.startswith(marker):
            text = text[len(marker) :].lstrip(" :-—\n")
        if len(text) < 120:
            return []
        return [make_work(spec, 1, collection, text, collection)]

    matches = list(TOKEN_RE.finditer(raw))
    works: list[dict[str, object]] = []
    index = 0
    use_h3 = spec.get("split") == "h3"
    for position, match in enumerate(matches):
        heading, strong = match.group(1), match.group(2)
        if heading is not None:
            title = clean_title(heading)
            if is_book_heading(title):
                named = collection_name(heading)
                if not is_book_heading(named):
                    collection = named
                continue
            if not use_h3:
                named = collection_name(heading)
                if not is_book_heading(named):
                    collection = named
                continue
            end = matches[position + 1].start() if position + 1 < len(matches) else len(raw)
            text = to_text(raw[match.end() : end])
            if text.startswith(title):
                text = text[len(title) :].lstrip(" :-—\n")
            if len(text) < 80:
                continue
            index += 1
            works.append(make_work(spec, index, title, text, collection))
            continue
        if use_h3:
            continue
        title = clean_title(strong or "")
        if tamil_count(title) < 2 or is_book_heading(title):
            continue
        end = matches[position + 1].start() if position + 1 < len(matches) else len(raw)
        text = to_text(raw[match.end() : end])
        if text.startswith(title):
            text = text[len(title) :].lstrip(" :-—\n")
        if len(text) < 120:
            continue
        index += 1
        works.append(make_work(spec, index, title, text, collection))
    return _prefer_longer(works)


def _prefer_longer(works: list[dict[str, object]]) -> list[dict[str, object]]:
    best: dict[tuple[str, str], dict[str, object]] = {}
    order: list[tuple[str, str]] = []
    for work in works:
        key = (str(work["kind"]), str(work["title"]))
        current = best.get(key)
        if current is None:
            best[key] = work
            order.append(key)
            continue
        if len(str(work["text"])) > len(str(current["text"])):
            work["id"] = current["id"]
            best[key] = work
    return [best[key] for key in order]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    collected: list[dict[str, object]] = []
    for spec in SOURCES:
        dest = SOURCE_DIR / spec["file"]
        download(spec["url"], dest)
        parsed = parse_source(spec)
        print(f"{spec['file']}: {len(parsed)} works")
        collected.extend(parsed)
    collected = _prefer_longer(collected)
    erode_path = SOURCE_DIR / "erode_yathirai.txt"
    erode_text = erode_path.read_text(encoding="utf-8").strip()
    erode_title = "என் ஈரோடு யாத்திரை"
    if not any(work["title"] == erode_title for work in collected):
        collected.append(
            {
                "id": "erode-001",
                "title": erode_title,
                "english_title": "My journey to Erode",
                "kind": "article",
                "collection": "சுதேசமித்திரன்",
                "themes": list(tag_themes(erode_title, erode_text)),
                "text": erode_text,
                "note": (
                    "Published in Swadesamitran on 4 August 1921 under the name "
                    "சக்திதாசன். Bharati describes the Karungalpalayam library meeting "
                    "and says he agreed to speak the next day on the future state of India."
                ),
                "source": "Swadesamitran, 4 August 1921",
                "source_url": "https://porulputhithu.com/2022/05/27/bharathisprosearticle-5/",
            }
        )
    OUT_PATH.write_text(json.dumps(collected, ensure_ascii=False, indent=2), encoding="utf-8")
    kinds: dict[str, int] = {}
    for work in collected:
        kind = str(work["kind"])
        kinds[kind] = kinds.get(kind, 0) + 1
    print(f"wrote {len(collected)} works to {OUT_PATH}")
    print(kinds)


if __name__ == "__main__":
    main()
