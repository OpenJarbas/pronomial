import unittest
from unittest.mock import patch

from pronomial.opm import PronomialCoreferenceEngine


class TestPronomialCoreferenceEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = PronomialCoreferenceEngine()

    def test_contains_corefs_true_for_pronouns(self):
        self.assertIs(
            self.engine.contains_corefs("the dog ran it was fast", "en"),
            True
        )

    def test_contains_corefs_false_for_no_pronouns(self):
        self.assertIs(
            self.engine.contains_corefs("what is a dog", "en"),
            False
        )

    def test_contains_corefs_false_for_unknown_lang(self):
        self.assertIs(
            self.engine.contains_corefs("it they them", "zz"),
            False
        )

    def test_contains_corefs_bcp47_tag(self):
        self.assertIs(
            self.engine.contains_corefs("the dog ran it was fast", "en-US"),
            True
        )

    def test_solve_corefs_returns_string(self):
        result = self.engine.solve_corefs("the dog ran. it was fast.", "en")
        self.assertIsInstance(result, str)

    def test_solve_corefs_bcp47_tag(self):
        result = self.engine.solve_corefs("it ran.", "en-US")
        self.assertIsInstance(result, str)

    def test_solve_corefs_replaces_pronoun(self):
        self.assertEqual(
            self.engine.solve_corefs("Inês said she loves me!", "en"),
            "Inês said Inês loves me !"
        )

    def test_resolve_returns_string(self):
        result = self.engine.resolve("what is it", "en")
        self.assertIsInstance(result, str)

    def test_resolve_passthrough_on_failure(self):
        engine = PronomialCoreferenceEngine()
        with patch.object(PronomialCoreferenceEngine, "solve_corefs",
                          side_effect=RuntimeError("crash")):
            self.assertEqual(engine.resolve("what is it", "en"),
                             "what is it")

    def test_entry_point_loads_correct_class(self):
        import importlib.metadata
        eps = {ep.name: ep for ep in
               importlib.metadata.entry_points(group="opm.agents.coref")}
        self.assertIn("pronomial", eps)
        self.assertIs(eps["pronomial"].load(), PronomialCoreferenceEngine)


if __name__ == "__main__":
    unittest.main()
