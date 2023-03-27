import re
from duckduckgo_search import ddg

class DDGSearch:
    def __init__(self, keyword='[SEARCH]') -> None:
        self.keyword = '[SEARCH]'
        self.searchRegex = r"\[SEARCH\](.*)$"
        self.noresultResponse = "There are no results for this query. Try a different [SEARCH] query."
        pass

    def extractQuery(self, query: str):
        if self.keyword not in query:
            return None

        match = re.search(self.searchRegex, query, re.MULTILINE)
        if match:
            result = match.group(1).strip()
            return result
        else:
            print("Error matching regex in query\n", query)

        return None

    def constructPrompt(self, results):
        prompt = "[RESULTS]\n"
        for i, r in enumerate(results):
            prompt += f"""Result {i+1}:\nTitle: {r['title']}\nBody: {r['body']}\n"""
        return prompt


    def performSearch(self, query, max_results=3):
        searchResults = ddg(query, max_results=max_results)
        if len(searchResults) == 0:
            return self.noresultResponse

        prompt = self.constructPrompt(searchResults)
        return prompt
    
if __name__ == "__main__":
    ddgsearch = DDGSearch()
    query = """Lemme look that shiii up
    [SEARCH] Kanye West recent news?
    Hold up a sec
    """
    extractedQuery = ddgsearch.extractQuery(query)
    if extractedQuery is not None:
        response = ddgsearch.performSearch(extractedQuery)
    print(response)