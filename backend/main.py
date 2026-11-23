import asyncio

from fastapi import FastAPI
from pydantic import BaseModel, Field

from agent import agent, ResearchDeps, explain_relevance
from models import ResearchResult, Paper


# Create our API so users can send requests
app = FastAPI(title="AI Research Agent")


# The user must write a search request
class ResearchRequest(BaseModel):
    query: str = Field(min_length=1)


# A simple page to check if our API is working
@app.get("/")
def home():
    return {"message": "AI Research Agent API is running"}


# This starts when the user searches for papers
@app.post("/research", response_model=ResearchResult)
async def research(request: ResearchRequest):

    # Make an empty place to save found papers
    deps = ResearchDeps()

    # Ask our main AI to understand the request and find papers
    result = await agent.run(
        request.query,
        deps=deps,
    )

    # Take only the first 10 papers
    selected_papers = deps.papers[:10]

    # If no papers were found, say so
    if not selected_papers:
        return ResearchResult(
            papers=[],
            summary=(
                "No papers matching your criteria were found "
                "in the OpenAlex search results."
            ),
        )

    # Ask our second AI to explain each paper
    explanations = []

    for paper in selected_papers:
        explanation = await explain_relevance(
            request.query,
            paper,
        )

        # Save the explanation
        explanations.append(explanation)

        # Wait 2 seconds to avoid too many Groq requests
        await asyncio.sleep(2)

    # Make an empty list for our final papers
    papers = []

    # Put each paper together with its AI explanation
    for paper, explanation in zip(
        selected_papers,
        explanations,
    ):
        paper_data = {
            **paper,
            "relevance": explanation,
        }

        # Check the paper using our model from models.py
        papers.append(
            Paper.model_validate(paper_data)
        )

    # Send the final papers and summary back to the user
    return ResearchResult(
        papers=papers,
        summary=(
            f"Found {len(papers)} matching papers "
            "in the OpenAlex search results."
        ),
    )
