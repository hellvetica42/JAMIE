import re
from duckduckgo_search import ddg
import logging

class DDGSearch:
    def __init__(self, keyword='[SEARCH]') -> None:
        self.keyword = '[SEARCH DDG]'
        self.searchRegex = r"^\[SEARCH DDG\](.*)$"
        self.noresultResponse = "There are no results for this query. Try a different [SEARCH DDG] query."
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

    def constructResponse(self, results, query):
        prompt = f"[RESULTS] {query}\n"
        for i, r in enumerate(results):
            prompt += f"""[RESULT {i+1}]\nTitle: {r['title']}\nBody: {r['body']}\n"""
        return prompt


    def execute(self, query, max_results=2):
        logging.info(f"Running search query: {query}")
        input("OK?")
        searchResults = ddg(query, max_results=max_results)
        if len(searchResults) == 0:
            return self.noresultResponse

        prompt = self.constructResponse(searchResults, query)
        #logging.info(f"Performed search and constructed prompt:\n{prompt}")
        return prompt
    
if __name__ == "__main__":
    ddgsearch = DDGSearch()
    query = """Lemme look that shiii up
    [SEARCH DDG] Kanye West recent news
    Hold up a sec
    """
    extractedQuery = ddgsearch.extractQuery(query)
    if extractedQuery is not None:
        response = ddgsearch.performSearch(extractedQuery)
    print(response)