from src.agents.debater import DebaterAgent
from src.config.settings import SKILLS_DIR
from src.gatekeeper import Gatekeeper


_QUERIES = [
    "smartphones reduce attention span scientific research",
    "smartphone use impairs memory cognitive function study",
    "smartphone dependency reduces problem solving ability",
    "smartphone screen time linked academic performance decline",
    "social media notifications distract deep thinking focus",
    "digital distraction cognitive load research evidence",
    "smartphone addiction brain development impact study",
    "excessive smartphone use working memory impairment",
    "smartphones replace mental effort outsourcing cognition",
    "smartphone overuse linked lower IQ test scores",
]


class ProAgent(DebaterAgent):
    """Pro debater: YES, smartphones make us less smart.

    Skill: src/skills/pro_skill.md defines the fixed position and argument themes.
    Tool: SearchTool provides evidence; Claude API generates arguments.
    """

    speaker: str = "Pro"
    stance: str = "PRO"

    def __init__(self, gatekeeper: Gatekeeper) -> None:
        super().__init__(SKILLS_DIR / "pro_skill.md", gatekeeper)

    def _get_search_query(self, context: dict) -> str:
        idx = (context.get("round_number", 1) - 1) % len(_QUERIES)
        return _QUERIES[idx]
