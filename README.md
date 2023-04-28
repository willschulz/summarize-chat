# Robo-Enumerator

Project to use LLMs for better surveying.

## Installation

You will need git, Python and pip installed on your computer.

1. Clone this github repository into your preferred location.

```
cd /PATH/TO/GITHUB/PROJECTS
git clone git@github.com:muhark/robo-enumerator.git
cd robo-enumerator
```

If you have `conda` installed (preferred method, [see installation instructions here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)):

2. Create a `conda` environment for this project and install project requirements.

```
conda create -n robo-enumerator -c conda-forge python=3.9 -y
conda activate robo-enumerator
pip install -r requirements.txt
```

If you do not have `conda` installed, we can use python virtu
al environments. (Less preferred just because I am not developing with this as the default. I'll try to make both solutions work equivalently.)

2. Create a `venv` virtual environment.

```
python -m venv project_env
source project_env/bin/activate
pip install -r requirements.txt
```

## OpenAI Configuration

My code assumes that you keep your openai API key in a file called `~/.cfg/openai.cfg` that has the followings tructure:

```
[API_KEY]
secret=<OPENAI_API_KEY_HERE>
```

Let me know if you have any questions about this or if this causes issues--I can make this code more flexible.


## Wandb Configuration

This project uses weights and biases to track experiments (although, this behavior can be disabled). If you don't already have one, create an account and get access to this project from me.


## Usage

Short version, assuming you are already `cd`'d into this repository and you have the correct python environment activated:

```
cd prompt_development
python tui.py
```

This will begin the session using the system instructions contained in `prompt_development/prompts/system_instructions.txt`. I'll be working on some more modular logic for this prompt so that we can separate out the questions into another file.


Current structure:

```
prompt_development
├── prompts
│   └── system_instructions.txt
├── tui.py
└── view_logs.py
```
