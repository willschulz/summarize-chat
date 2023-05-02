#! /usr/bin/python

"""
@author: Musashi Jacobs-Harukawa
@title: ChatAgent TUI

Terminal user interface (TUI)-based tool for developing OpenAI Chat Agent.

"""

# ws additions
import csv

# imports
import openai
import wandb

# langchain tools
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.openai import _convert_message_to_dict
from langchain import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# standard tools
import os
import argparse
import json
from configparser import ConfigParser
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime as dt

# CLI
from rich import print
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.style import Style
from pick import pick

# Version checks
assert openai.version.VERSION >= "0.27.0", "Update OpenAI API version"

# Argparse
def parse_args():
    parser = argparse.ArgumentParser(
        description="Simple Terminal User Interface (TUI) for OpenAI Chat API.")
    parser.add_argument("--api-config", type=str, default="~/.cfg/openai.cfg",
                        help=("Provide config path for credentials options"))
    parser.add_argument("--prompts-dir", type=Path, default='./prompts',
                        help=("Directory with prompts"))
    parser.add_argument("--wandb-project", type=str,
                        default='robo-enumerator',
                        help=("W&B project title"))
    parser.add_argument("--disable-wandb", action='store_true')
    args = parser.parse_args()
    return args

# Setup OpenAI Key
def seed_openai_key(cfg: str="~/.cfg/openai.cfg"):
    """
    Reads OpenAI key from config file and adds it to environment.
    Assumed config location is "~/.cfg/openai.cfg"
    """
    # Get OpenAI Key
    config = ConfigParser()
    try:
        config.read(Path(cfg).expanduser())
    except:
        raise ValueError(f"Could not using read file at: {cfg}. Please contact me on how to set up your OpenAI config.")
    openai_key = config['API_KEY']['secret']
    openai.api_key = openai_key
    os.environ['OPENAI_API_KEY'] = openai_key
    return openai_key

# Styling
style_user = Style(color="green")
style_bot = Style(color="magenta")
style_help = Style(color="blue")

# Prompt templates
initial_instructions = SystemMessagePromptTemplate(
    prompt = PromptTemplate(
        template = "{system_instructions}",
        input_variables=["system_instructions"]))

class ChatAgentTUI():
    def __init__(self, args):
        self.args = args
        self.agent = ChatOpenAI(temperature=0)
        if not args.disable_wandb:
            self.wandb_run = wandb.init(project=args.wandb_project)
        self.message_history = []
        #try adding message history
        # Load messages from CSV file
        with open('./chats/chat1.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['identity'] == 'ego':
                    message = AIMessage(content=row['text'])
                    self.message_history.append(message)
                elif row['identity'] == 'alter':
                    message = HumanMessage(content=row['text'])
                    self.message_history.append(message)
        
        self.message_history.append(SystemMessage(content="Now you will act like you are answering a survey about your political attitudes.  Please answer the following question: 'How much more hypocritical are Republicans, compared to Democrats?  Please respond with a number from 0 to 10, where 5 means that Republicans are equally hypocritical as Democrats.'  Please respond with a number from 0 to 10."))

        self.token_usage = []
        self.console = Console()
        self.start_process()
        self.save_conversation(wandb_log=not self.args.disable_wandb, local_log=True)
        exit(0)

    def start_process(self):
        "Get ball rolling by asking for system prompt."
        prompt_file, _ = pick(
            options = list(Path(self.args.prompts_dir).iterdir()),
            title = "Please choose a prompt template.")
        if Confirm.ask(f"Do you want to see the contents of [bold]{prompt_file.stem}[/bold]?", default=False):
            print(prompt_file.read_text())
        self.system_prompt = initial_instructions.format(
            system_instructions = prompt_file.read_text())
        self.call_agent() 

    def call_agent(self):
        messages = [[self.system_prompt] + self.message_history]
        result = self.agent.generate(messages)
        self.token_usage.append({'time': dt.now().strftime('%Y%m%d-%H%M%S'),
                                 'tokens_used': result.llm_output['token_usage']['total_tokens']})
        self.message_history.append(result.generations[0][0].message)
        self.console.print(
            "[bold][Robo-Enumerator][/bold]\n"+
            result.generations[0][0].text, style=style_bot)

    def save_conversation(self, wandb_log: bool=True, local_log: bool=True):
        # Write message_history to file
        history = [_convert_message_to_dict(message)
                   for message in
                   [self.system_prompt] + self.message_history]
        # Construct token usage
        if wandb_log:
            table = wandb.Table(
                columns=["role", "content"],
                data=[[msg["role"], msg["content"]]
                      for msg in history])
            self.wandb_run.log({"System Instruction": self.system_prompt.content})
            self.wandb_run.log({"Message History": table})
        # Create local log
        if local_log:
            savefile = Path(
                "logs/chatbot_log_{}.json".format(
                    dt.now().strftime('%Y%m%d-%H%M%S')))
            savefile.write_text(json.dumps(history))
            savefile = Path(
                "logs/chatbot_token-usage_{}.json".format(
                    dt.now().strftime('%Y%m%d-%H%M%S')))
            savefile.write_text(json.dumps(self.token_usage))

def main():
    args = parse_args()
    seed_openai_key(cfg=args.api_config)
    ChatAgentTUI(args)

if __name__ == "__main__":
    main()

