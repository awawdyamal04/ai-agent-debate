"""Pre-written demo arguments used when running in --demo mode (no API key needed)."""
from datetime import datetime
from src.debate.protocol import DebateMessage, EvidenceItem, ToolMetadata

PRO_ARGS = [
    "Smartphones demonstrably shorten our attention spans. Research by Microsoft in 2015 found that the average human attention span dropped from 12 seconds to 8 seconds — coinciding precisely with the smartphone era. When we compulsively check our devices every few minutes, we train our brains for interruption rather than sustained concentration, making deep work increasingly difficult.",
    "Our reliance on smartphones for instant answers is quietly eroding our capacity for independent recall. When we Google instead of remember, we prevent the consolidation of information into long-term memory. A 2011 study by Betsy Sparrow at Columbia found that people are less likely to remember information if they believe it will remain digitally accessible — a phenomenon called 'cognitive offloading' that weakens our natural memory systems.",
    "Smartphone notifications create a state of continuous partial attention that fundamentally hinders learning. Research by Gloria Mark at UC Irvine found that after an interruption, it takes an average of 23 minutes to regain full concentration. With the average user receiving 80+ notifications daily, meaningful intellectual engagement becomes nearly impossible.",
    "Longitudinal studies increasingly link heavy smartphone use to lower academic achievement. A 2019 study published in Computers in Human Behavior found that students who used their phones more than four hours per day scored significantly lower on standardised tests than moderate users. The correlation is not accidental — distracted studying produces shallower learning.",
    "Smartphones are systematically replacing the cognitive effort required for problem-solving. GPS navigation has measurably impaired our spatial reasoning — a 2017 study in Nature Communications showed that London taxi drivers who switched to GPS showed atrophied hippocampal activity compared to those who memorised routes. What we don't use, we lose.",
    "Social media on smartphones exploits our dopamine systems, creating compulsive engagement loops that crowd out reflective thought. The very design of these platforms — variable reward schedules, infinite scrolling, likes and reactions — is engineered to maximise time-on-device at the direct expense of sustained intellectual focus.",
    "The evidence on adolescent smartphone use is particularly alarming. Jean Twenge's landmark research in 'iGen' documents that teens who spend more than 5 hours per day on smartphones are 66% more likely to have at least one suicide risk factor, and show significantly lower critical thinking scores. The developing brain is especially vulnerable to these disruptions.",
    "Smartphones train us to expect immediate answers, degrading our tolerance for productive struggle. When students reach for a device at the first sign of difficulty, they deprive themselves of the effortful retrieval practice that builds deep understanding. Struggle is where learning happens — smartphones circumvent that process entirely.",
    "Reading comprehension deteriorates when we read on screens, according to extensive research. A 2018 meta-analysis of 54 studies found that digital reading produced significantly worse comprehension than print reading. Smartphones, with their fractured reading environment and competing notifications, represent the worst possible medium for deep text engagement.",
    "The cumulative evidence is overwhelming: smartphones, through attentional fragmentation, memory offloading, problem-solving shortcuts, and addictive design, are systematically degrading the cognitive capabilities that define human intelligence. The Pro position stands: smartphones make us less smart, and the data makes this undeniable.",
]

CON_ARGS = [
    "The claim that smartphones reduce intelligence fundamentally misunderstands what intelligence means in the 21st century. A smartphone gives any person access to the sum of human knowledge in seconds. This is not cognitive atrophy — it is cognitive amplification. UNESCO data shows that smartphone-enabled internet access has dramatically improved educational outcomes in developing nations where traditional schooling is limited.",
    "The 'cognitive offloading' argument actually supports the Con position. Freeing working memory from rote recall allows the brain to engage in higher-order thinking — analysis, synthesis, creative problem-solving. Calculators did not make us worse at mathematics; they freed us from arithmetic so we could tackle harder problems. Smartphones do the same at civilisational scale.",
    "Attention is not a fixed resource that smartphones simply drain. Studies by the Pew Research Center show that smartphone users are more likely to engage with news, participate in civic discourse, and seek continuing education than non-users. The real picture is one of expanded cognitive engagement, not impoverishment.",
    "Smartphones have been transformative for learning outcomes when used appropriately. The Khan Academy — accessed primarily via smartphone — has delivered high-quality mathematics and science education to 150 million learners globally, many of whom had no prior access to qualified teachers. This is intelligence expansion at a scale no previous technology achieved.",
    "The GPS-versus-hippocampus argument proves too much. We do not lament that writing weakened our capacity for oral tradition, or that maps weakened our reliance on landmarks. Cognitive tool use is not cognitive decline — it is cognitive evolution. Smartphones are today's external scaffolding for an enlarged effective intelligence.",
    "The extended mind theory (Clark and Chalmers, 1998) argues that cognition is not confined to the skull. When information is reliably accessible via smartphone, it functionally becomes part of our cognitive system. The question is not whether we hold facts in biological memory, but whether our total cognitive capability — biological plus digital — has increased. It has.",
    "Regarding adolescent data: the research is deeply contested. A 2019 re-analysis by Andrew Przybylski at Oxford found that the effect size of smartphone use on adolescent wellbeing is no larger than that of wearing glasses or eating potatoes. Correlation studies cannot establish that smartphones cause academic decline; confounders abound.",
    "Smartphones enable real-time collaboration that multiplies intellectual capacity. Google Docs, Slack, shared research databases, and instant translation tools mean that a team of smartphone users can produce work that no individual — regardless of innate intelligence — could achieve alone. Collective intelligence has never been higher.",
    "Multilingual translation via smartphones has extended cognitive reach across language barriers. Accessibility features have empowered people with disabilities to participate fully in intellectual life. These are not marginal benefits — they represent profound expansions of who gets to be intelligent.",
    "The evidence as a whole supports the Con position: smartphones extend rather than diminish human intelligence. They democratise access to knowledge, scaffold higher-order thinking, enable global collaboration, and adapt to diverse cognitive needs. Any harms from misuse do not negate the overwhelming cognitive benefits of responsible smartphone use. The Con position prevails.",
]

JUDGE_OPENING = (
    "Welcome to this structured debate on the topic: 'Do smartphones make us less smart?' "
    "I am your Judge and Moderator. This debate will proceed over ten rounds. "
    "The Pro side will argue that YES, smartphones make us less smart. "
    "The Con side will argue that NO, smartphones do not make us less smart. "
    "Both sides must maintain their positions, use evidence, and rebut their opponent directly. "
    "After all rounds I will evaluate six criteria — evidence quality, relevance, consistency, "
    "rebuttal strength, use of sources, and logical clarity — and declare one winner. "
    "No ties are permitted. Pro side, please begin."
)

JUDGE_EVALS = [
    "Round 1: Pro cited the Microsoft attention-span study effectively; Con countered with UNESCO access data. Edge to Con for citing more concrete impact metrics. Pro: 7/10, Con: 8/10.",
    "Round 2: Pro's cognitive offloading argument was strong. Con's counter — that offloading frees higher cognition — was equally compelling and logically sound. Near tie; slight edge to Con. Pro: 7/10, Con: 7.5/10.",
    "Round 3: Pro's notification-interruption research (Gloria Mark) was specific and credible. Con cited Pew engagement data but was less focused. Edge to Pro. Pro: 8/10, Con: 6.5/10.",
    "Round 4: Pro cited Computers in Human Behavior study; Con countered with Khan Academy impact. Both strong. Edge to Con for concrete scale of educational benefit. Pro: 7/10, Con: 8/10.",
    "Round 5: Pro's GPS-hippocampus evidence from Nature Communications was excellent. Con's extended-mind reframing was philosophically sound. Edge to Con for reframing the debate productively. Pro: 7.5/10, Con: 8/10.",
    "Round 6: Pro focused on dopamine/social media design; Con invoked Clark-Chalmers extended mind theory. Both excellent. Slight edge to Con for theoretical depth. Pro: 7.5/10, Con: 8/10.",
    "Round 7: Pro cited Jean Twenge's iGen research; Con cited Przybylski's Oxford re-analysis directly refuting Twenge. Con's direct rebuttal was more persuasive. Edge to Con. Pro: 7/10, Con: 8.5/10.",
    "Round 8: Pro argued smartphones eliminate productive struggle. Con countered with collective intelligence evidence. Both solid. Edge to Con for practical evidence. Pro: 7/10, Con: 7.5/10.",
    "Round 9: Pro cited screen vs. print reading meta-analysis. Con cited translation and accessibility benefits. Con's breadth of impact was more persuasive. Pro: 7/10, Con: 8/10.",
    "Round 10: Both sides delivered strong closing summaries. Con's cumulative argument — democratisation, augmentation, collaboration — was more coherent and evidence-rich. Final round to Con. Pro: 7/10, Con: 8.5/10.",
]

JUDGE_VERDICT = """After ten rounds of rigorous debate, I have evaluated both sides on six dimensions: factual evidence quality, relevance, consistency, rebuttal strength, use of external sources, and logical clarity.

**Factual Evidence Quality**: The Con side consistently cited diverse, high-impact evidence — UNESCO access data, Khan Academy reach, Przybylski's Oxford reanalysis, and the extended-mind theoretical framework. The Pro side presented credible research (Microsoft attention span, Gloria Mark, Nature Communications GPS study) but relied more heavily on correlational data without addressing confounders.

**Rebuttal Strength**: Con systematically dismantled Pro's key claims — responding to cognitive offloading by inverting the argument, directly countering the Twenge adolescent data with Przybylski, and reframing GPS dependency as cognitive evolution rather than atrophy. Pro's rebuttals, while competent, did not land as directly.

**Logical Clarity and Consistency**: Both sides maintained their positions throughout. Con's framework — that intelligence is not purely biological recall but total cognitive capability including tool use — was internally consistent and more coherent across all ten rounds.

**Overall Assessment**: The Con side presented a more comprehensive, evidence-rich, and logically coherent case. The democratisation of knowledge access, the extended-mind framework, and the direct refutation of Pro's strongest studies together constitute a stronger cumulative argument.

WINNER: Con"""


def get_demo_pro_msg(round_num: int, exchange_num: int) -> dict:
    idx = min(round_num - 1, len(PRO_ARGS) - 1)
    from src.tools.search import _FALLBACK
    items = [EvidenceItem(s["snippet"], s["url"], "fallback", "fallback/demo") for s in _FALLBACK["pro"][:2]]
    msg = DebateMessage(
        round_number=round_num, exchange_number=exchange_num,
        speaker="Pro", stance="PRO", claim=PRO_ARGS[idx],
        evidence=items,
        tool_metadata=ToolMetadata(tools_used=["search(demo)", "demo"], search_queries=["demo"], fallback_used=True),
        rebuttal_target="", confidence_score=0.9,
        timestamp=datetime.now().isoformat(), status="complete",
    )
    return msg.to_dict()


def get_demo_con_msg(round_num: int, exchange_num: int, pro_claim: str = "") -> dict:
    idx = min(round_num - 1, len(CON_ARGS) - 1)
    from src.tools.search import _FALLBACK
    items = [EvidenceItem(s["snippet"], s["url"], "fallback", "fallback/demo") for s in _FALLBACK["con"][:2]]
    msg = DebateMessage(
        round_number=round_num, exchange_number=exchange_num,
        speaker="Con", stance="CON", claim=CON_ARGS[idx],
        evidence=items,
        tool_metadata=ToolMetadata(tools_used=["search(demo)", "demo"], search_queries=["demo"], fallback_used=True),
        rebuttal_target=pro_claim[:120], confidence_score=0.9,
        timestamp=datetime.now().isoformat(), status="complete",
    )
    return msg.to_dict()
