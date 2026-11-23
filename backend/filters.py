# Remove papers that do not match the user's request
def filter_papers(
    papers: list[dict],              # All papers from OpenAlex
    year_after: int | None = None,   # Papers after this year
    year_before: int | None = None,  # Papers before this year
    min_citations: int | None = None, # Minimum citations
    max_citations: int | None = None, # Maximum citations
) -> list[dict]:

    # Create an empty list for matching papers
    filtered = []

    # Check papers one by one
    for paper in papers:

        # Get the year and citation count
        year = paper.get("year")
        citations = paper.get("citations")

        # Skip papers with missing information
        if year is None or citations is None:
            continue

        # Skip if the paper is too old
        if year_after is not None and year <= year_after:
            continue

        # Skip if the paper is too new
        if year_before is not None and year >= year_before:
            continue

        # Skip if the paper has too few citations
        if min_citations is not None and citations < min_citations:
            continue

        # Skip if the paper has too many citations
        if max_citations is not None and citations > max_citations:
            continue

        # Keep the paper if it passed all checks
        filtered.append(paper)

    # Return only the matching papers
    return filtered
