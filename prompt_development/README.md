# Notes

## Meeting 11 April 2023

After our last meeting and discussions with Brandon, I wanted to test the following concerns/hypotheses:

1. Using GPT to ask questions about sensitive issues would trigger its internal content filters.
2. GPT would be unable to hide the fact that it is an AI language model.
3. GPT would continue to exhibit behavior of making statements that weren't entailed by the prompt.
4. Summarizing responses back at the end.

I made some modifications to the application to allow selection of text files to use as prompts. This has helped with trying various prompts.

The first test I made for hypothesis 1 was using it to conduct interviews about gender-based violence. This is a challenging topic requiring sensitivity from the interviewer, with potential to cause the respondent harm. I thought this potential may have triggered "guard rails" on GPT's behavior.

The questionnaire (`prompts/questions_gbv.txt`) contains a short battery of questions from the [CIRCABC EU Workplace Sexual Harrassment Questionnaire](https://circabc.europa.eu/sd/a/5ffc3f71-38ae-4b7f-a998-73a1dfeff8ed/Questionnaire%20for%20pilot%20%20survey%20VER2(0).pdf). Using GPT to ask these questions did not appear to trigger content filters. I experimented with three things in this interview:

- _Asking about confidentiality_: the agent made up that these responses would be kept private. In a separate run, it justified this as being "standard practice" and ethical, thus likely even if had not been told by the researcher that this would be the case. However, the agent likewise doubted the possibility that this survey was being conducted by the employer and pressed on.
- _Using slang/obscenity_: this created no issues.
- _Saying I was uncomfortable/experiencing harm_: the agent offered to end the interview, and let me do so.

I then used some [questions about conspiracy thinking](https://www.frontiersin.org/articles/10.3389/fpsyg.2013.00225/full) to test another possibly sensitive area. Additionally I asked it to hide the fact that it an AI in order to not affect the responses of conspiracy-minded respondents. The behavior was a bit unstable and unpredictable.

- In log `...075549.json`, there's initial deflection on the issue 

# Ideas to Try


Gary: Please write a paragraph by somebody like this. Back-and-forth iteration with respondent until they're happy with it.

Uma: Can we use this to elicit the most relevant features to predict a particular outcome?

BMS: At the end, fill out the questionnaire based on the conversation.