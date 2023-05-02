

import openai
import re
import os

from configparser import ConfigParser

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
    openai.api_key = openai_key g
    os.environ['OPENAI_API_KEY'] = openai_key
    return openai_key

#openai.api_key = "YOUR_API_KEY" # You will need to set up an OpenAI API key first
openai.api_key = seed_openai_key() # You will need to set up an OpenAI API key first

def summarize_chat(file_path):
    """
    This function takes a file path to a transcript of a dyadic text-based chat as input and uses GPT text completion to generate a summary of the conversation.
    """
    
    # Read the chat transcript from the specified file path
    with open(file_path, 'r') as f:
        chat_transcript = f.read()
    
    # Preprocess the chat transcript by removing any special characters and splitting it into individual messages
    chat_messages = re.split(r'[^\w\s]+', chat_transcript)
    
    # Join the last few messages to provide context to the GPT text completion model
    #context = ' '.join(chat_messages[-5:])
    context = ' '.join(chat_messages)
    #context = context + '\n If I were to summarize the above chat, I would say that '
    context = context + "\nPerson A: If I were to express my dislike for Republicans on a scale from 1 to 10, I would say I'm a "
    
    preamble = "Here is a transcript of a chat between two random strangers, who were instructed to discuss whether Democrats or Republicans are more hypocritical.\n"
    context = preamble + context
    print(context)

    # Use GPT text completion to generate a summary of the conversation
    response = openai.Completion.create(
      engine="davinci",
      prompt=context,
      max_tokens=10,
      n=1,
      stop=None,
      temperature=0.5
    )
    
    # Extract the generated summary from the GPT text completion response
    summary = response.choices[0].text.strip()
    
    # Save the summary to a file in the rep_dislike directory
    directory = "prompt_development/labels/rep_dislike/A"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = os.path.basename(file_path).split('.')[0]
    summary_file_path = os.path.join(directory, file_name + "_summary.txt")
    with open(summary_file_path, 'w') as f:
        f.write(summary)
    
    return summary

file_path = "prompt_development/chats_txt/628faee19230c4e1882ac78d.txt"
summary = summarize_chat(file_path)
print(summary)

# directory = "prompt_development/chats_txt/"
# for filename in os.listdir(directory):
#     file_path = directory + '/' + filename
#     summary = summarize_chat(file_path)
#     print(f"Summary of {filename}: {summary}")

