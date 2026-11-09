"""Catalog and keyword search for Bharathiyar's public-domain writings."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKS_PATH = ROOT / "data" / "works.json"

KIND_LABELS: dict[str, str] = {
    "poem": "Poem · பாடல்",
    "article": "Article · கட்டுரை",
    "story": "Story · கதை",
    "speech": "Speech · உரை",
    "life": "Life · சுயசரிதை",
}

KIND_ORDER: tuple[str, ...] = ("poem", "article", "story", "speech", "life")

THEME_LABELS: dict[str, str] = {
    "freedom": "Freedom · விடுதலை",
    "tamil": "Tamil · தமிழ்",
    "nation": "Nation · பாரதம்",
    "women": "Women · பெண்",
    "courage": "Courage · வீரம்",
    "devotion": "Devotion · பக்தி",
    "education": "Learning · கல்வி",
    "caste": "Caste · சாதி",
    "labor": "Labor · உழைப்பு",
    "leaders": "Leaders · தலைவர்கள்",
}

# Stems used both to tag works and to expand English queries into Tamil.
THEME_STEMS: dict[str, tuple[str, ...]] = {
    "freedom": ("சுதந்திர", "விடுதலை", "freedom", "liberty"),
    "tamil": ("தமிழ்", "செந்தமிழ்", "tamil"),
    "nation": ("பாரத", "தேசிய", "சுதேச", "nation", "india"),
    "women": ("பெண்", "மாதர்", "விதவை", "ஸ்திரீ", "women", "woman"),
    "courage": ("அச்சமில்லை", "அச்சம்", "வீரம்", "தைரியம்", "courage", "fearless"),
    "devotion": (
        "பக்தி",
        "பராசக்தி",
        "காளி",
        "கண்ணன்",
        "நந்தலாலா",
        "முருகன்",
        "devotion",
        "krishna",
    ),
    "education": ("கல்வி", "பள்ளி", "சாத்திர", "education", "learning"),
    "caste": ("சாதி", "ஜாதி", "caste"),
    "labor": ("உழைப்பு", "தொழில்", "வறுமை", "labor", "labour", "poverty"),
    "leaders": ("திலகர்", "காந்தி", "லாஜபதி", "சிவாஜி", "நௌரோஜி", "leader", "gandhi", "tilak"),
}

ENGLISH_TITLES: dict[str, str] = {
    "வந்தே மாதரம்": "I bow to the mother",
    "ஜய வந்தே மாதரம்": "Victory, vande mataram",
    "நாட்டு வணக்கம்": "Salute to the country",
    "பாரத நாடு": "The country of Bharat",
    "பாரத தேசம்": "The land of Bharat",
    "எங்கள் நாடு": "Our country",
    "ஜயபாரத": "Victory to Bharat",
    "பாரத மாதா": "Mother Bharat",
    "எங்கள் தாய்": "Our mother",
    "செந்தமிழ் நாடு": "The Tamil country",
    "தமிழ்த்தாய்": "Mother Tamil",
    "தமிழ்": "Tamil",
    "தமிழ்மொழி வாழ்த்து": "Praise of the Tamil language",
    "வாழிய செந்தமிழ்": "Long live Tamil",
    "சுதந்திரப் பெருமை": "The greatness of freedom",
    "சுதந்திரப் பயிர்": "The crop of freedom",
    "சுதந்திர தாகம்": "Thirst for freedom",
    "சுதந்திர தேவியின் துதி": "Hymn to the goddess of freedom",
    "விடுதலை": "Freedom",
    "சுதந்திரப் பள்ளு": "Harvest song of freedom",
    "அச்சமில்லை": "There is no fear",
    "விடுதலை-சிட்டுக்குருவி": "Freedom, little sparrow",
    "விடுதலை வேண்டும்": "Freedom is what we need",
    "பாப்பாப் பாட்டு": "Song to a child",
    "புதுமைப் பெண்": "The new woman",
    "பெண்மை": "Womanhood",
    "பெண்கள் விடுதலைக் கும்பி": "Kummi for women's freedom",
    "பெண் விடுதலை": "Women's freedom",
    "நாட்டுக் கல்வி": "Education for the country",
    "தொழில்": "Labor",
    "கனவு": "A dream",
    "பாரதி - அறுபத்தாறு": "Bharati at sixty-six",
    "காணி நிலம் வேண்டும்": "A small plot of land",
    "நந்த லாலா": "Nandalala",
    "நந்தலாலா": "Nandalala",
    "பாரத சமுதாயம்": "The community of Bharat",
}


@dataclass(frozen=True)
class Work:
    id: str
    title: str
    english_title: str
    kind: str
    collection: str
    themes: tuple[str, ...]
    text: str
    note: str
    source: str
    source_url: str

    @property
    def kind_label(self) -> str:
        return KIND_LABELS.get(self.kind, self.kind)

    @property
    def theme_labels(self) -> tuple[str, ...]:
        return tuple(THEME_LABELS[theme] for theme in self.themes if theme in THEME_LABELS)


@dataclass(frozen=True)
class Hit:
    work: Work
    score: int
    snippet: str


def tag_themes(*parts: str) -> tuple[str, ...]:
    haystack = "\n".join(parts)
    found: list[str] = []
    for theme, stems in THEME_STEMS.items():
        if any(_contains(haystack, stem) for stem in stems):
            found.append(theme)
    return tuple(found)


def english_title_for(title: str) -> str:
    key = title.strip(" .!?,;:\"'“”‘’")
    return ENGLISH_TITLES.get(key, "")


def load_works(path: Path | None = None) -> tuple[Work, ...]:
    payload = json.loads((path or WORKS_PATH).read_text(encoding="utf-8"))
    works: list[Work] = []
    for item in payload:
        works.append(
            Work(
                id=item["id"],
                title=item["title"],
                english_title=item.get("english_title", ""),
                kind=item["kind"],
                collection=item.get("collection", ""),
                themes=tuple(item.get("themes", ())),
                text=item.get("text", ""),
                note=item.get("note", ""),
                source=item.get("source", ""),
                source_url=item.get("source_url", ""),
            )
        )
    return tuple(works)


def work_by_id(works: tuple[Work, ...] | list[Work], work_id: str) -> Work | None:
    for work in works:
        if work.id == work_id:
            return work
    return None


def _tokens(query: str) -> list[str]:
    parts = re.split(r"[\s,;|/]+", query.strip())
    tokens: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.isascii() and len(part) < 3:
            continue
        tokens.append(part)
    return tokens


def _expansions(token: str) -> tuple[str, ...]:
    folded = token.casefold()
    for stems in THEME_STEMS.values():
        folded_stems = {stem.casefold() for stem in stems}
        if folded in folded_stems:
            return stems
    return (token,)


def _contains(haystack: str, needle: str) -> bool:
    """Match a keyword at the start of a word, so பெண் hits பெண்கள் but not தென்பெண்ணை."""
    if not needle:
        return False
    if needle.isascii():
        pattern = rf"(?<![A-Za-z0-9]){re.escape(needle)}"
        return re.search(pattern, haystack, flags=re.IGNORECASE) is not None
    pattern = rf"(?<![\u0b80-\u0bff]){re.escape(needle)}"
    return re.search(pattern, haystack) is not None


def _snippet(work: Work, needles: tuple[str, ...]) -> str:
    flat = re.sub(r"\s+", " ", work.text).strip()
    if not flat:
        return work.english_title or work.collection
    folded = flat.casefold()
    at = -1
    found = ""
    for needle in needles:
        if not needle:
            continue
        if needle.isascii():
            spot = folded.find(needle.casefold())
        else:
            spot = flat.find(needle)
        if spot >= 0 and (at < 0 or spot < at):
            at = spot
            found = needle
    if at < 0:
        window = flat[:220]
    else:
        start = max(0, at - 70)
        end = min(len(flat), at + 150)
        window = flat[start:end]
        if start > 0:
            window = "…" + window
        if end < len(flat):
            window = window + "…"
    if found:
        window = _emphasize(window, found)
    return window


def _emphasize(text: str, needle: str) -> str:
    safe = text.replace("*", "").replace("_", "").replace("`", "")
    if needle.isascii():
        pattern = re.compile(re.escape(needle), re.IGNORECASE)
        return pattern.sub(lambda match: f"**{match.group(0)}**", safe, count=1)
    if needle in safe:
        return safe.replace(needle, f"**{needle}**", 1)
    return safe


def search(
    works: tuple[Work, ...] | list[Work],
    query: str = "",
    *,
    match: str = "any",
    kinds: tuple[str, ...] | list[str] | None = None,
    themes: tuple[str, ...] | list[str] | None = None,
    collection: str | None = None,
) -> list[Hit]:
    """Find works by one or more keywords.

    `match` is \"any\" (a work matches if one keyword hits) or \"all\".
    English theme words expand to Tamil stems, so \"freedom\" finds சுதந்திரம்.
    Theme and kind filters apply in addition to the query.
    """
    selected_kinds = set(kinds or ())
    selected_themes = set(themes or ())
    tokens = _tokens(query)
    phrase = " ".join(tokens)
    hits: list[Hit] = []

    for work in works:
        if selected_kinds and work.kind not in selected_kinds:
            continue
        if collection and work.collection != collection:
            continue
        if selected_themes and not selected_themes.intersection(work.themes):
            continue

        title_blob = f"{work.title}\n{work.english_title}"
        theme_blob = " ".join((*work.theme_labels, *work.themes))
        score = 0
        matched_needles: list[str] = []
        token_hits = 0
        for token in tokens:
            expansions = _expansions(token)
            weight, needle = _best_needle(title_blob, theme_blob, work.text, expansions)
            if weight:
                token_hits += 1
                score += weight
                if needle:
                    matched_needles.append(needle)
        if tokens and match == "all" and token_hits < len(tokens):
            continue
        if tokens and match != "all" and token_hits == 0:
            continue
        if phrase and len(tokens) > 1 and _contains(f"{title_blob}\n{work.text}", phrase):
            score += 3
        if not tokens and not selected_kinds and not selected_themes and not collection:
            continue
        hits.append(Hit(work=work, score=score, snippet=_snippet(work, tuple(matched_needles))))

    kind_rank = {"poem": 0, "speech": 1, "story": 2, "life": 3, "article": 4}
    hits.sort(key=lambda hit: (-hit.score, kind_rank.get(hit.work.kind, 9), hit.work.title))
    return hits


def _best_needle(
    title_blob: str,
    theme_blob: str,
    body: str,
    expansions: tuple[str, ...],
) -> tuple[int, str | None]:
    """Score a keyword: title 8, theme 3, body 1."""
    for needle in expansions:
        if _contains(title_blob, needle):
            return 8, needle
    for needle in expansions:
        if _contains(theme_blob, needle):
            return 3, needle
    for needle in expansions:
        if _contains(body, needle):
            return 1, needle
    return 0, None


def related_works(works: tuple[Work, ...] | list[Work], work: Work, limit: int = 3) -> list[Work]:
    ranked: list[tuple[int, str, Work]] = []
    themes = set(work.themes)
    for other in works:
        if other.id == work.id:
            continue
        overlap = len(themes.intersection(other.themes))
        same_kind = 1 if other.kind == work.kind else 0
        if overlap == 0 and other.collection != work.collection:
            continue
        same_collection = 3 if other.collection == work.collection else 0
        ranked.append((overlap * 2 + same_collection + same_kind, other.title, other))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in ranked[:limit]]


def related_keywords(hits: list[Hit], query: str, limit: int = 8) -> list[tuple[str, str]]:
    """Suggest theme keywords that sit next to the current results.

    Each item is (label, query token to add).
    """
    used = {token.casefold() for token in _tokens(query)}
    counts: dict[str, int] = {}
    for hit in hits:
        for theme in hit.work.themes:
            counts[theme] = counts.get(theme, 0) + 1
    ranked = sorted(counts, key=lambda theme: (-counts[theme], theme))
    suggestions: list[tuple[str, str]] = []
    for theme in ranked:
        stems = THEME_STEMS[theme]
        tamil = next((stem for stem in stems if not stem.isascii()), stems[0])
        if tamil.casefold() in used or theme.casefold() in used:
            continue
        if any(stem.casefold() in used for stem in stems):
            continue
        suggestions.append((THEME_LABELS[theme], tamil))
        if len(suggestions) >= limit:
            break
    return suggestions


def preview(text: str, limit: int = 180) -> str:
    flat = re.sub(r"\s+", " ", text).strip()
    if len(flat) <= limit:
        return flat
    return flat[: limit - 1].rstrip() + "…"
