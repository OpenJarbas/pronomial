from typing import Optional

from ovos_plugin_manager.coreference import CoreferenceSolverEngine
from ovos_plugin_manager.templates.agents import CoreferenceEngine

import pronomial
from pronomial.utils import word_tokenize


class PronomialCoreferenceSolver(CoreferenceSolverEngine):
    """Coreference solver plugin for the deprecated OPM solver API.

    Deprecated: use :class:`PronomialCoreferenceEngine` instead.
    """

    @classmethod
    def solve_corefs(cls, text, lang="en"):
        """Replace pronouns in ``text`` with their referent nouns.

        Args:
            text (str): Input text to resolve.
            lang (str): Language code of the text.

        Returns:
            str: Text with coreferences replaced.
        """
        return pronomial.replace_corefs(text, lang=lang)


class PronomialCoreferenceEngine(CoreferenceEngine):
    """OPM agent engine exposing pronomial's rule-based coreference solver.

    Wraps :func:`pronomial.replace_corefs` behind the
    :class:`ovos_plugin_manager.templates.agents.CoreferenceEngine` contract.
    Language tags are accepted as full BCP-47 codes (e.g. ``en-US``) and
    reduced internally to the base language pronomial keys its wordlists on.
    """

    @staticmethod
    def _normalize_lang(lang: Optional[str]) -> str:
        """Reduce a BCP-47 language tag to its lowercase base language.

        Args:
            lang (Optional[str]): Language tag, e.g. ``"en-US"`` or ``"pt"``.

        Returns:
            str: Base language code, e.g. ``"en"``. Empty string if ``lang``
                is falsy.
        """
        return (lang or "").lower().split("-")[0]

    @classmethod
    def _get_pronouns(cls, lang: str) -> dict:
        """Fetch pronomial's pronoun wordlists for a language.

        Args:
            lang (str): Base language code, e.g. ``"en"``.

        Returns:
            dict: Mapping of pronoun category (``"male"``, ``"female"``,
                ``"neutral"``, ``"plural"``, ``"first"``) to word lists.
                Empty dict for unsupported languages.
        """
        resources = pronomial.PronomialCoreferenceSolver._load_lang_resources(lang)
        return resources[-2]  # PRONOUNS

    def contains_corefs(self, text: str, lang: str) -> bool:
        """Check if ``text`` contains pronouns that may need resolving.

        Args:
            text (str): Input text to inspect.
            lang (str): BCP-47 language code of the text.

        Returns:
            bool: True if any known pronoun for ``lang`` appears in the text.
                False for languages without pronoun wordlists.
        """
        lang = self._normalize_lang(lang)
        pronouns = {w.lower()
                    for words in self._get_pronouns(lang).values()
                    for w in words}
        if not pronouns:
            return False
        return any(tok.lower() in pronouns for tok in word_tokenize(text))

    def solve_corefs(self, text: str, lang: str) -> str:
        """Replace pronouns in ``text`` with their referent nouns.

        Args:
            text (str): Input text to resolve.
            lang (str): BCP-47 language code of the text.

        Returns:
            str: Text with coreferences replaced.
        """
        lang = self._normalize_lang(lang)
        return pronomial.replace_corefs(text, lang=lang)

    def resolve(self, text: str, lang: Optional[str] = None,
                use_memory: bool = False) -> str:
        """Resolve coreferences, never raising on failure.

        Args:
            text (str): Input text to resolve.
            lang (Optional[str]): BCP-47 language code. Defaults to the
                configured/session language.
            use_memory (bool): Whether to apply and learn cross-utterance
                context (see :meth:`CoreferenceEngine.resolve`).

        Returns:
            str: Resolved text, or ``text`` unchanged if resolution fails
                for any reason.
        """
        try:
            return super().resolve(text, lang=lang, use_memory=use_memory)
        except Exception:
            return text
