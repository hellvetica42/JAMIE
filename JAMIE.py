import logging
import sys

from GPT import GPT
from DDGSearch import DDGSearch
from BashAPI import BashAPI

class JAMIE:
    def __init__(self) -> None:
        self.gpt = GPT()
        self.search = DDGSearch()
        self.bash = BashAPI()
        self.APIs = [self.search, self.bash]
        logging.basicConfig(level=logging.INFO,
            handlers=[
                logging.FileHandler('jamie.log'),
                logging.StreamHandler()
            ]
        )
        self.ecnourageSearch = " If you don't know the answer to this question search the web using the [SEARCH DDG] keyword or run a command using the [BASH] keyword."

    def ask(self, question):
        self.gpt.resetHistory()

        #logging.info(f"Asking question: {question}")
        response = self.gpt.query(question + self.ecnourageSearch)
        #response = self.gpt.query(question)
        #logging.info(f"Got response: {response}")

        # Find api keywords and apply
        num_i = 0
        while True:
            num_i += 1
            prompt = None
            queries = [api.extractQuery(response) for api in self.APIs]

            # If multiple API calls were made
            if len([q for q in queries if q is not None]) > 1:
                prompt = "Jamie cannot use multiple API calls in a single message"
            else:
                for q, api in zip(queries, self.APIs):
                    if q is not None:
                        prompt = api.execute(q)
                        break

            if prompt is None:
                return response

            if num_i > 4:
                print("JAMIE STUCK IN LOOP")
                return response

            response = self.gpt.query(prompt)



if __name__ == "__main__":
    question = sys.argv[1]
    jamie = JAMIE()
    print(f"USER: {question}")
    response = jamie.ask(question)
    print(f"JAMIE: {response}")
    print(f"Usage:", jamie.gpt.usage)
