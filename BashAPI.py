import re
import subprocess
import logging

class BashAPI:
    def __init__(self, keyword='[BASH]') -> None:
        self.name = "BashCLI"
        self.description = "useful for then you need to run commands to answer questions about the system you're running on or run calculations. The input to this should be a valid BASH command."
        self.outputCharLimit = 1000
        pass


    def constructResponse(self, results):
        return results[:self.outputCharLimit] 


    def run(self, command):
        output = subprocess.run(command, capture_output=True, shell=True, executable='/bin/zsh')
        if len(output.stdout.decode()) != 0:
            results = output.stdout.decode()
        elif len(output.stderr.decode()) != 0:
            results = output.stderr.decode()
        else:
            results = "No output"
        prompt = self.constructResponse(results)
        #logging.info(f"Constructed prompt:\n{prompt}")
        return prompt
    
if __name__ == "__main__":
    print("NOT IMPLEMENTED")