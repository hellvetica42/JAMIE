import re
import subprocess
import logging

class BashAPI:
    def __init__(self, keyword='[BASH]') -> None:
        self.keyword = keyword
        self.searchRegex = r"^\[BASH\](.*)$"
        self.outputCharLimit = 1000
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

    def constructResponse(self, results):
        prompt = f"[RESULTS]\n{results}"
        return prompt


    def execute(self, command):
        logging.info(f"Running bash command: {command}")
        input("OK?")
        output = subprocess.run(command, capture_output=True, shell=True, executable='/bin/zsh')
        if len(output.stdout.decode()) != 0:
            results = output.stdout.decode()[:self.outputCharLimit]
        elif len(output.stderr.decode()) != 0:
            results = output.stderr.decode()[:self.outputCharLimit]
        else:
            results = "No output"
        prompt = self.constructResponse(results)
        #logging.info(f"Constructed prompt:\n{prompt}")
        return prompt
    
if __name__ == "__main__":
    bashapi = BashAPI()
    query = """Lemme look that shiii up
    [BASH] date
    Hold up a sec
    """
    extractedQuery = bashapi.extractQuery(query)
    if extractedQuery is not None:
        response = bashapi.execute(extractedQuery)
    print(response)