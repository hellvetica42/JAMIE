import re
import os
import json
import openai

from AgentPrompt import PREFIX, FORMAT_INSTRUCTIONS, SUFFIX
from DDGSearch import DDGSearch

openai.organization = "org-h2JY1eLn7JLboZJneMfsMGUb"
openai.api_key = os.getenv("OPENAI_API_KEY")


class Agent:
    def __init__(self) -> None:
        self.tools = [DDGSearch()]
        self.tool_map = {t.name:t for t in self.tools}


        self.match_json = r"```((.|\n)*)```"
        self.match_thought = r"^Thought:(.*)$"
        self.match_action = r"^Action:(.|\n)*```((.|\n)*)```$"
        self.match_observation = r"^Observation:(.*)$" 

        self.tool_list = ", ".join([f"{t.name}: {t.description}" for t in self.tools])
        self.tool_names = str([t.name for t in self.tools])

        instructions = FORMAT_INSTRUCTIONS.format(tool_names=self.tool_names)
        self.prompt = "\n".join([PREFIX, self.tool_list, instructions, SUFFIX])

        #List of dicts of Thought, Action, Observation
        self.scratchpad : list[dict] = [{'role':'user', 'content':self.prompt}]
        self.messages :list[dict] = [{'role':'user', 'content':self.prompt}]


    def run(self, input):
        question = {'role':'user', 'content':f"Question: {input}"}
        self.scratchpad.append(question)
        self.messages.append(question)

        chain = self.query(self.scratchpad)
        for link in chain:
            if link['type'] == 'thought':
                self.scratchpad.append({'role':'assistant', 'content':f"Thought: {link['content']}"})

                #self.messages.append({'role':'assistant', 'content':f"Thought: {link['content']}"})

            if link['type'] == 'action':
                self.scratchpad.append({'role':'assistant', 'content':f"Action: {link['content']}"})
                #self.messages.append({'role':'assistant', 'content':f"Thought: {link['content']}"})
                action_json = json.loads(link['content'])

                #Run Tool
                tool = self.tool_map[action_json['action']]
                tool_result = tool.run(action_json['action_input'])
                #self.messages.append({'role':'user', 'content':{tool_result}})

                chain = self.query(self.scratchpad + [{'role':'user', 'content':tool_result}])
                for link in chain:
                    if link['type'] == 'observation':
                        self.scratchpad.append({'role':'assistant', 'content':f"Observation: {link['content']}"})


    def query(self, queries):
        print("QUERIES", "\n".join([str(q) for q in queries]))
        results = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=queries
        )
        msg = results['choices'][0]['message']['content']
        print("MSG:\n", msg)
        chain = self.parseResponse(msg)
        return chain

    def parseResponse(self, response):
        results = []

        thought_match = re.search(self.match_thought, response, re.MULTILINE)
        if thought_match:
            print("THOUGHT:", thought_match.group(1))
            results.append({'type':'thought', 'content':{thought_match.group(1).strip()}})

        action_match = re.search(self.match_action, response, re.MULTILINE)
        if action_match:
            print("ACTION:", action_match.group(2))
            results.append({'type':'action', 'content':action_match.group(2).strip()})

        observation_match = re.search(self.match_observation, response, re.MULTILINE)
        if observation_match:
            results.append({'type':'observation', 'content':{observation_match.group(1).strip()}})

        return results

    def parseJson(self, response):
        match = re.search(self.matchJson, response, re.MULTILINE)
        if match:
            agentDict = json.loads(match.group(1))
            return agentDict
        else:
            return None

if __name__ == "__main__":
    agent = Agent()
    agent.run("What is Brad Pitt's height?")
