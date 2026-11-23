import os
import httpx
from dotenv import load_dotenv

# Get our secret API key from the .env file
load_dotenv()


# Find research papers about a topic
def search_papers(topic: str, limit: int = 10):

    # This is where we ask OpenAlex for papers
    url = "https://api.openalex.org/works"

    # Send our topic and API key to OpenAlex
    response = httpx.get(
        url,
        params={
            "search": topic,
            "per_page": limit,
            "api_key": os.environ["OPENALEX_API_KEY"],
        },
        timeout=20,
    )

    # Stop if OpenAlex gives us an error
    response.raise_for_status()

    # Make an empty list for the papers
    papers = []

    # Look at each paper OpenAlex found
    for work in response.json()["results"]:

        # Put the paper's short description back into normal text
        abstract_index = work.get("abstract_inverted_index") or {}

        words = {}

        for word, positions in abstract_index.items():
            for position in positions:
                words[position] = word

        abstract = " ".join(
            words[position] for position in sorted(words)
        )

        # Save the important information about this paper
        papers.append({
            "title": work.get("title"),
            "authors": [
                a["author"]["display_name"]
                for a in work.get("authorships", [])
                if a.get("author")
            ],
            "year": work.get("publication_year"),
            "citations": work.get("cited_by_count"),
            "citation_source": "OpenAlex",
            "url": work.get("doi") or work.get("id"),
            "abstract": abstract,
        })

    # Give all the found papers back to our program
    return papers
