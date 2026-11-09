"""Download public portraits and make the short Tamil greeting."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

import edge_tts

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

COMMONS = "https://commons.wikimedia.org/w/api.php"
FILES = (
    "File:Subramanya_Bharathi.jpg",
    "File:Subramanya_Bharathi_with_his_wife_Chellamma.jpg",
    "File:Subramanya_Bharathi_1960_stamp_of_India.jpg",
    "File:Subramanya_Bharathi_Signature.jpg",
    "File:Bharathiyar_Photograph.jpg",
)
YOUTUBE = (
    "OLePZtChkPE",
    "DvrFMYFBdCM",
    "gKhzQDZaKrY",
    "v_4fPHTk0aw",
    "KNf3NUQ1_Uc",
    "KPj5Uv27z1c",
)
GREETING = (
    "அச்சமில்லை, அச்சமில்லை. "
    "அச்சமில்லை, அச்சமில்லை. "
    "அச்சமில்லை, அச்சமில்லை."
)


def get_json(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "BharathiyarArchive/1.0 (educational archive)"})
    with urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def download(url: str, dest: Path) -> None:
    request = Request(url, headers={"User-Agent": "BharathiyarArchive/1.0 (educational archive)"})
    with urlopen(request, timeout=120) as response:
        dest.write_bytes(response.read())


def commons() -> None:
    titles = "|".join(FILES)
    url = (
        f"{COMMONS}?action=query&format=json&titles={titles}"
        "&prop=imageinfo&iiprop=url|extmetadata|mime|size&iiurlwidth=900"
    )
    payload = get_json(url)
    pages = payload["query"]["pages"]
    credits = []
    for page in pages.values():
        info = page["imageinfo"][0]
        meta = info.get("extmetadata", {})
        title = page["title"].removeprefix("File:")
        artist = meta.get("Artist", {}).get("value", "Unknown")
        license_name = meta.get("LicenseShortName", {}).get("value", "")
        license_url = meta.get("LicenseUrl", {}).get("value", "")
        credit = meta.get("Credit", {}).get("value", "")
        thumb = info.get("thumburl") or info["url"]
        dest = ASSETS / title.replace(" ", "_")
        download(thumb, dest)
        credits.append(
            {
                "file": dest.name,
                "title": title,
                "artist": artist,
                "license": license_name,
                "license_url": license_url,
                "source": info["descriptionurl"],
                "bytes": dest.stat().st_size,
            }
        )
        print(dest.name, dest.stat().st_size, license_name)
    (ASSETS / "credits.json").write_text(
        json.dumps(credits, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


async def greeting() -> None:
    dest = ASSETS / "achchamillai.mp3"
    communicate = edge_tts.Communicate(GREETING, "ta-IN-PallaviNeural", rate="-25%")
    last = 0
    await communicate.save(str(dest))
    # A second pass records the last word boundary so we know the length.
    communicate = edge_tts.Communicate(GREETING, "ta-IN-PallaviNeural", rate="-25%")
    async for chunk in communicate.stream():
        if chunk["type"] == "WordBoundary":
            last = chunk["offset"] + chunk["duration"]
    seconds = last / 10_000_000
    print(f"greeting {dest.stat().st_size} bytes, about {seconds:.1f}s")


def youtube() -> None:
    for video_id in YOUTUBE:
        url = (
            "https://www.youtube.com/oembed?format=json&url="
            f"https://www.youtube.com/watch?v={video_id}"
        )
        try:
            data = get_json(url)
            print("OK", video_id, data.get("title"), data.get("author_name"))
        except Exception as error:  # noqa: BLE001 - report dead links and continue
            print("FAIL", video_id, error)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    commons()
    asyncio.run(greeting())
    youtube()


if __name__ == "__main__":
    main()
