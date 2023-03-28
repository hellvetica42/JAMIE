import os
import openai
import logging
openai.organization = "org-h2JY1eLn7JLboZJneMfsMGUb"
openai.api_key = os.getenv("OPENAI_API_KEY")

class GPT:
    def __init__(self) -> None:
        self.usage = 0
        self.resetHistory()

    def resetHistory(self):
        self.messages = []
        with open('promptv3.txt', 'r') as f:
            self.messages.append({'role':'user', 'content':f.read()})
        self.messages.append({'role':'assistant', 'content':'Hi, I am Jamie. How can I help you?'})

    def query(self, query):
        logging.info(f"Input message:\n{query}")
        self.messages.append({'role':'user', 'content':query})
        results = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            messages=self.messages
        )
        resultMsg = results['choices'][0]['message']['content']
        resultRole = results['choices'][0]['message']['role']
        self.messages.append({'role':resultRole, 'content':resultMsg})
        self.usage += results['usage']['total_tokens']
        logging.info(f"Output message:\n{resultMsg}")
        return resultMsg
