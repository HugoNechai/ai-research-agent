from dataclasses import dataclass, field

from pydantic_ai import Agent, RunContext

from openalex import search_papers
from filters import filter_papers


# A place to save the papers we find
@dataclass
class ResearchDeps:
    papers: list[dict] = field(default_factory=list)


# Our main AI: understands the user's request and starts the search
agent = Agent(
    "groq:openai/gpt-oss-120b",
    deps_type=ResearchDeps,

    # Rules that tell our main AI what to do
    instructions=(
        "You are an AI research assistant. "
        "Always call find_research_papers to search for academic papers. "
        "Extract the topic, publication year, and citation constraints "
        "from the user's request. "
        "Use year_after and year_before for strict year boundaries. "
        "Never invent papers, authors, years, or citation counts. "
        "Only recommend papers returned by the tool. "
        "Use paper abstracts when explaining relevance. "
        "Never invent information missing from abstracts. "
        "If no papers match, clearly say so. "
        "Do not claim that you searched the entire OpenAlex database. "
        "Keep the final answer concise."
    ),
)


# Our second AI: explains why each paper matches the topic
relevance_agent = Agent(
    "groq:openai/gpt-oss-120b",

    # Rules for explaining papers without making things up
    instructions=(
        "You explain why an academic paper is relevant "
        "to a research topic. "
        "Use the supplied title and abstract to assess relevance. "
        "The publication year and citation count are verified "
        "by OpenAlex and must be treated as reliable metadata. "
        "If the abstract is unavailable, explain relevance "
        "cautiously using only the title. "
        "Never invent findings, methods, or conclusions. "
        "Do not question verified publication years or citation counts. "
        "Focus on the paper's actual subject and contribution. "
        "Write one or two concise sentences in English. "
        "Return only the explanation."
    ),
)


# A tool our main AI can use to find papers
@agent.tool
def find_research_papers(
    ctx: RunContext[ResearchDeps],
    topic: str,
    year_after: int | None = None,
    year_before: int | None = None,
    min_citations: int | None = None,
    max_citations: int | None = None,
) -> list[dict]:
    """Search OpenAlex and filter academic papers by year and citations."""

    # First, ask OpenAlex for up to 50 papers
    papers = search_papers(topic, limit=50)

    # Then, remove papers that do not match the user's rules
    filtered_papers = filter_papers(
        papers,
        year_after=year_after,
        year_before=year_before,
        min_citations=min_citations,
        max_citations=max_citations,
    )

    # Save the matching papers so our program can use them later
    ctx.deps.papers = filtered_papers

    # Give our AI information about up to 10 matching papers
    return [
        {
            "title": paper["title"],
            "authors": paper["authors"],
            "year": paper["year"],
            "citations": paper["citations"],
            "url": paper["url"],
            "abstract": (paper.get("abstract") or "")[:1000],
        }
        for paper in filtered_papers[:10]
    ]


# Ask our second AI to explain one paper
async def explain_relevance(
    topic: str,
    paper: dict,
) -> str:
    """Generate an individual relevance explanation using AI."""

    # Get the paper's title and short description
    title = paper.get("title") or ""
    abstract = paper.get("abstract") or ""

    # If there is no description, give a safe answer
    if not abstract:
        return (
            f"The title '{title}' suggests relevance to the "
            "requested research topic, but OpenAlex does not "
            "provide an abstract to confirm its specific contribution."
        )

    # Give the paper's information to our second AI
    prompt = (
        f"Research topic: {topic}\n"
        f"Paper title: {title}\n"
        f"Publication year (verified by OpenAlex): {paper['year']}\n"
        f"Citation count (verified by OpenAlex): {paper['citations']}\n"
        f"Paper abstract: {abstract[:3000]}\n\n"
        "Explain why the paper is relevant to the research topic. "
        "Focus on its actual subject and contribution. "
        "Publication year and citation count are verified by OpenAlex. "
        "Do not question these values or invent research findings."
    )

    # Send the prompt to our second AI and wait for its answer
    result = await relevance_agent.run(prompt)

    # Return only the AI's explanation
    return result.output.strip()
