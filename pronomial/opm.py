from ovos_plugin_manager.coreference import CoreferenceSolverEngine

import pronomial


class PronomialCoreferenceSolver(CoreferenceSolverEngine):
    @classmethod
    def solve_corefs(cls, text, lang="en"):
        return pronomial.replace_corefs(text, lang=lang)
