import re
from duckduckgo_search import ddg
import logging

class DDGSearch:
    def __init__(self) -> None:
        self.name = "Current search"
        self.description = "useful for when you need to answer questions about current events or the current state of the world. The input to this should be a single search term. You should break up your questions into multiple searches if you need to find more than one bit of information"
        self.noresultResponse = "There are no results for this query. Try a different query."

    def constructResponse(self, results):
        prompt = f""
        for i, r in enumerate(results):
            prompt += f"""Title: {r['title']}\nBody: {r['body']}\n"""
        return prompt


    def run(self, query, max_results=3):
        searchResults = ddg(query, max_results=max_results)
        if len(searchResults) == 0:
            return self.noresultResponse

        prompt = self.constructResponse(searchResults)
        #logging.info(f"Performed search and constructed prompt:\n{prompt}")
        return prompt
    
if __name__ == "__main__":
    print("NOT IMPLEMENTED")