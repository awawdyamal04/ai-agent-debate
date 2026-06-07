from src.agents.debater import DebaterAgent
from src.config.settings import SKILLS_DIR
from src.gatekeeper import Gatekeeper


_QUERIES = [
    "smartphones increase knowledge access learning benefits",
    "educational apps smartphones improve student outcomes",
    "smartphones boost productivity cognitive tools research",
    "mobile technology democratises education global access",
    "smartphone use enhance communication collaboration study",
    "extended mind theory smartphones cognitive augmentation",
    "moderate smartphone use cognitive benefits research",
    "smartphones support lifelong learning adult education",
    "mobile internet access reduce inequality information gap",
    "smartphone tools improve memory recall organisation",
]


class ConAgent(DebaterAgent):
    """Con debater: NO, smartphones do not make us less smart.

    Skill: src/skills/con_skill.md defines the fixed position and argument themes.
    Tool: SearchTool provides evidence; Claude API generates arguments.
    """

    speaker: str = "Con"
    stance: str = "CON"

    def __init__(self, gatekeeper: Gatekeeper) -> None:
        super().__init__(SKILLS_DIR / "con_skill.md", gatekeeper)

    def _get_search_query(self, context: dict) -> str:
        idx = (context.get("round_number", 1) - 1) % len(_QUERIES)
        return _QUERIES[idx]
