#! /usr/bin/python

"""
@author: Musashi Jacobs-Harukawa
@title: Local Log Parser/Viewer
"""

import json
import argparse
from pathlib import Path
from rich import print
from rich.panel import Panel
from rich.style import Style

# Styling
styles = dict(
    user        = Style(color="green"),
    assistant   = Style(color="blue"),
    system      = Style(color="red", bold=True)
)

def parse_args():
    parser = argparse.ArgumentParser(
        description=(
        "Tool for unpacking and viewing previous conversations with "
        "the OpenAI Chat API. Takes logfile as an argument. Defaults "
        "to most recent file."
        ))
    parser.add_argument("--logfile", type=str, default=None)
    args = parser.parse_args()
    return args


def parse_message(msg):
    print(Panel(msg['content'],
          title=msg['role'].upper(),
          style=styles.get(msg['role'])))
    

def main():
    args = parse_args()
    if args.logfile is None:
        logfile = sorted(Path("./logs").glob("*.json"))[-1]
    else:
        logfile = Path(args.logfile)
    
    dialogue = json.loads(logfile.read_text())
    for msg in dialogue:
        parse_message(msg)

if __name__=='__main__':
    main()




