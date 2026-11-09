import unittest

from bharathi.catalog import Work, load_works, related_keywords, search


def work(work_id: str, title: str, text: str, kind: str = "poem", themes: tuple[str, ...] = ()) -> Work:
    return Work(
        id=work_id,
        title=title,
        english_title="",
        kind=kind,
        collection="test",
        themes=themes,
        text=text,
        note="",
        source="test",
        source_url="",
    )


class SearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.works = (
            work("1", "சுதந்திர தாகம்", "என்று தணியும் இந்த சுதந்திர தாகம்", themes=("freedom",)),
            work("2", "பெண் விடுதலை", "விடுதலைக்கு மகளிரெல்லோரும் பெண் விடுதலை", themes=("freedom", "women")),
            work("3", "செந்தமிழ் நாடு", "தென்பெண்ணை பாலாறு தமிழ்நாடு", themes=("tamil",)),
            work("4", "கல்வி", "நாட்டுக் கல்வி வேண்டும்", kind="article", themes=("education",)),
        )

    def test_english_freedom_finds_tamil(self) -> None:
        hits = search(self.works, "freedom")
        self.assertEqual({hit.work.id for hit in hits}, {"1", "2"})

    def test_all_keywords_are_narrower_than_any(self) -> None:
        any_hits = search(self.works, "பெண் கல்வி", match="any")
        all_hits = search(self.works, "பெண் கல்வி", match="all")
        self.assertEqual({hit.work.id for hit in any_hits}, {"2", "4"})
        self.assertEqual(all_hits, [])

    def test_tamil_stem_does_not_match_inside_another_word(self) -> None:
        hits = search(self.works, "பெண்")
        self.assertEqual([hit.work.id for hit in hits], ["2"])

    def test_kind_filter(self) -> None:
        hits = search(self.works, "கல்வி", kinds=("poem",))
        self.assertEqual(hits, [])
        hits = search(self.works, kinds=("article",))
        self.assertEqual([hit.work.id for hit in hits], ["4"])

    def test_related_keywords_skip_the_active_theme(self) -> None:
        hits = search(self.works, "freedom")
        suggestions = related_keywords(hits, "freedom")
        tokens = [token for _label, token in suggestions]
        self.assertIn("பெண்", tokens)
        self.assertNotIn("விடுதலை", tokens)
        self.assertNotIn("சுதந்திர", tokens)

    def test_archive_contains_known_poems(self) -> None:
        archive = load_works()
        self.assertGreater(len(archive), 200)
        titles = {hit.work.title for hit in search(archive, "செந்தமிழ்")}
        self.assertIn("செந்தமிழ் நாடு", titles)
        speech_hits = search(archive, kinds=("speech",))
        self.assertEqual(len(speech_hits), 1)
        self.assertIn("இஸ்லாம்", speech_hits[0].work.title)


if __name__ == "__main__":
    unittest.main()
