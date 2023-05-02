# ws additions
import csv
#working

# imports
import openai

# langchain tools
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.openai import _convert_message_to_dict
from langchain import PromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate

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
from rich.style import Style
from pick import pick

# Version checks
assert openai.version.VERSION >= "0.27.0", "Update OpenAI API version"

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

def chat_agent_tui(chat_path: str):
    api_config="~/.cfg/openai.cfg"
    prompts_dir="./prompts/chat_instructions1.txt"
    seed_openai_key(cfg=api_config)
    agent = ChatOpenAI(temperature=0)
    message_history = []
    with open(Path(chat_path)) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['identity'] == 'ego':
                message = AIMessage(content=row['text'])
                message_history.append(message)
            elif row['identity'] == 'alter':
                message = HumanMessage(content=row['text'])
                message_history.append(message)
    message_history.append(SystemMessage(content=Path('./questions/rel_hyp.txt').read_text()))
    token_usage = []
    #console = Console()
    system_prompt = SystemMessagePromptTemplate(prompt=PromptTemplate(template="{system_instructions}", input_variables=["system_instructions"])).format(system_instructions=Path(prompts_dir).read_text())
    messages = [[system_prompt] + message_history]
    result = agent.generate(messages)
    token_usage.append({'time': dt.now().strftime('%Y%m%d-%H%M%S'), 'tokens_used': result.llm_output['token_usage']['total_tokens']})
    message_history.append(result.generations[0][0].message)
    #console.print("[bold][Robo-Enumerator][/bold]\n" + result.generations[0][0].text, style=Style(color="magenta")))
    history = [_convert_message_to_dict(message) for message in [system_prompt] + message_history]
    filename = Path(chat_path).stem
    savefile = Path("logs/{}_chatbot_log_{}.json".format(filename[:-4], dt.now().strftime('%Y%m%d-%H%M%S')))
    savefile.write_text(json.dumps(history))
    savefile = Path("logs/{}_chatbot_token-usage_{}.json".format(filename[:-4], dt.now().strftime('%Y%m%d-%H%M%S')))
    savefile.write_text(json.dumps(token_usage))

# chat_paths = ["./chats/628fae689230c4e1882ac772.csv", './chats/628fae959230c4e1882ac777.csv']
# for chat_path in chat_paths:
#     chat_agent_tui(chat_path)

chat_dir = "./chats/"
for filename in os.listdir(chat_dir):
    if filename.endswith(".csv"):
        chat_path = os.path.join(chat_dir, filename)
        chat_agent_tui(chat_path)

