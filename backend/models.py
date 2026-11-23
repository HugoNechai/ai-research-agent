from pydantic import BaseModel, Field

# What one research paper looks like
class Paper(BaseModel):
    title: str
    authors: list[str]
    year: int
    citations: int
    citation_source: str
    url: str
    relevance: str = ""


# What the full search result looks like
class ResearchResult(BaseModel):
    papers: list[Paper] = Field(default_factory=list)
    summary: str = ""
