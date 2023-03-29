import re
import os, sys
import json
import openai
import logging
from datetime import date

from AgentPrompt import PREFIX, FORMAT_INSTRUCTIONS, SUFFIX, FINAL_ANSWER, THOUGHT, SCRATCHPAD_PREFIX, ACTION
from DDGSearch import DDGSearch
from BashAPI import BashAPI

openai.organization = "org-h2JY1eLn7JLboZJneMfsMGUb"
openai.api_key = os.getenv("OPENAI_API_KEY")


class JAMIE:
    def __init__(self) -> None:
        self.tools = [DDGSearch(), BashAPI()]
        self.tool_map = {t.name:t for t in self.tools}


        self.match_json = r"```\{(.|\n)*\}```"

        self.tool_list = ", ".join([f"{t.name}: {t.description}" for t in self.tools])
        self.tool_names = ",".join([t.name for t in self.tools])

        instructions = FORMAT_INSTRUCTIONS.format(tool_names=self.tool_names)
        self.prompt = "\n".join([PREFIX, self.tool_list, instructions, SUFFIX.format(current_date=date.today())])

        #List of dicts of Thought, Action, Observation
        self.scratchpad : str = ""
        self.messages :list[dict] = [{'role':'user', 'content':self.prompt}]

        logging.basicConfig(level=logging.INFO,
            handlers=[
#                logging.FileHandler('jamie.log'),
                logging.StreamHandler()
            ]
        )

    def run(self, question):
        self.messages.append({'role':'user', 'content':f"Question: {question}"})
        self.scratchpad += question + SCRATCHPAD_PREFIX

        while True:
            msg = self.query(self.messages)

            chain = self.extract_action_and_thought(msg)

            if chain[0] == "Final Answer":
                return chain[1]

            if chain[0] in self.tool_names:
                tool_output = self.tool_map[chain[0]].run(chain[1])
                logging.info(f"TOOL OUTPUT:'\n {tool_output}")
                self.scratchpad += "Observation: " + tool_output

            self.messages[1]['content'] = self.scratchpad
            input('OK?')




    def extract_action_and_thought(self, text):
        if FINAL_ANSWER in text and ACTION not in text and '```' not in text:
            logging.info(text)
            return ("Final Answer", text.split(FINAL_ANSWER)[-1].strip())

        try:
            elements = text.split("```")
            thought, action = elements[0], elements[1]
            thought = thought.split("\n")[0]
            actionJson = json.loads(action.strip())


            if THOUGHT in thought:
                logging.info(thought.strip())
                self.scratchpad += thought.strip()
            elif len(thought.strip()) > 0:
                logging.info(f"Thought: {thought.strip()}")
                self.scratchpad += f"Thought: {thought.strip()}"
            else:
                raise ValueError(f"No Thought in LLM output: {text}")

            logging.info(f"Action: {action}")
            self.scratchpad += f"```\n{action}\n```\n"
            return (actionJson['action'], actionJson['action_input'])

        except Exception:
            raise ValueError(f"Could not parse LLM output: {text}")

    def query(self, queries):
        #print("INPUT MESSAGES: \n",queries)
        results = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=queries
        )
        msg = results['choices'][0]['message']['content']
        #print("OUTPUT MESSAGES: \n", msg)
        return msg 

if __name__ == "__main__":
    question = sys.argv[1]
    jamie = JAMIE()
    result = jamie.run(question)
    print("JAMIE:", result)
