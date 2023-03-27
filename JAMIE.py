import logging
import sys

from GPT import GPT
from DDGSearch import DDGSearch

class JAMIE:
    def __init__(self) -> None:
        self.gpt = GPT()
        self.search = DDGSearch()
        logging.basicConfig(level=logging.INFO,
            handlers=[
                logging.FileHandler('jamie.log'),
                logging.StreamHandler()
            ]
        )
        self.ecnourageSearch = " If you don't know the answer to this question or are unsure, search the web using the [SEARCH] keyword."

    def ask(self, question):
        self.gpt.resetHistory()

        logging.info(f"Asking question: {question}")
        response = self.gpt.query(question + self.ecnourageSearch)
        logging.info(f"Got response: {response}")

        query = self.search.extractQuery(response)
        if query is None:
            logging.info(f"No search query in response")
            print(response)
            return

        logging.info(f"Found search query in response: {query}")
        prompt = self.search.performSearch(query)
        logging.info(f"Performed search and constructed prompt: {prompt}")

        response = self.gpt.query(prompt)
        #logging.info(f"Received parsed response: {response}")
        return response

if __name__ == "__main__":
    question = sys.argv[1]
    jamie = JAMIE()
    print(f"USER: {question}")
    response = jamie.ask(question)
    print(f"JAMIE: {response}")
