"""Portraits and film links."""

from __future__ import annotations

from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"

PICTURES: tuple[dict[str, str], ...] = (
    {
        "file": "Subramanya_Bharathi.jpg",
        "alt": "Painted portrait of Subramania Bharati",
        "caption": (
            "The familiar portrait. Public domain, made before 1921. "
            "Wikimedia Commons."
        ),
    },
    {
        "file": "Subramanya_Bharathi_with_his_wife_Chellamma.jpg",
        "alt": "Subramania Bharati seated with his wife Chellamma",
        "caption": (
            "Bharati with Chellamma. Public domain photograph. "
            "Wikimedia Commons."
        ),
    },
    {
        "file": "Bharathiyar_Photograph.jpg",
        "alt": "Photograph of Bharati taken in 1921, when he was 39",
        "caption": (
            "Photograph taken in 1921, when he was 39. "
            "Commons file by Balogic, CC BY-SA 4.0."
        ),
    },
    {
        "file": "Subramanya_Bharathi_1960_stamp_of_India.jpg",
        "alt": "1960 Indian postage stamp showing Subramania Bharati",
        "caption": (
            "India Post commemorative stamp, 1960. "
            "Government Open Data License, India."
        ),
    },
    {
        "file": "Subramanya_Bharathi_Signature.jpg",
        "alt": "Handwritten signature of Subramania Bharati",
        "caption": "His signature. Public domain. Wikimedia Commons.",
    },
)

FILMS: tuple[dict[str, str], ...] = (
    {
        "title": "Bharathi (2000), full film",
        "detail": (
            "Gnana Rajasekaran's Tamil biographical film. "
            "Sayaji Shinde plays Bharati, Devayani plays Chellamma, "
            "and Ilaiyaraaja wrote the music. Posted on YouTube by WAM India Tamil."
        ),
        "url": "https://www.youtube.com/watch?v=OLePZtChkPE",
    },
    {
        "title": "Mahakavi Bharathi, series promo",
        "detail": (
            "Promo for the Doordarshan Tamil series on his life and poems. "
            "Posted by DD Tamil."
        ),
        "url": "https://www.youtube.com/watch?v=gKhzQDZaKrY",
    },
    {
        "title": "Vande Mataram, from the film",
        "detail": "Song from Bharathi (2000). Posted by Mango Music Tamil.",
        "url": "https://www.youtube.com/watch?v=v_4fPHTk0aw",
    },
    {
        "title": "Ethilum ingu, from the film",
        "detail": "Song from Bharathi (2000). Posted by Mango Music Tamil.",
        "url": "https://www.youtube.com/watch?v=KNf3NUQ1_Uc",
    },
    {
        "title": "Mayil pola ponnu, from the film",
        "detail": "Song from Bharathi (2000), sung by Bhavatharini. Posted by Mango Music Tamil.",
        "url": "https://www.youtube.com/watch?v=KPj5Uv27z1c",
    },
)
