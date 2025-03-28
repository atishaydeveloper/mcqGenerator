import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
import PyPDF2

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash")

TEMPLATE = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
    create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
    Make sure the questions are not repeated and check all the questions to be conforming the text as well.
    Ensure to mke {number} MCQs with 4 options each.
    ### Response_JSON ###
    {response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template = TEMPLATE
)

quiz_chain = LLMChain(
    llm = llm,
    prompt = quiz_generation_prompt,
    output_key = "quiz",
    verbose = True
)

TEMPLATE2 = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of teh question and give a complete analysis of the quiz. only use at max 50 words for complexity, 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student's ability.
Quiz_MCQs:
{quiz}     

Check from an expert English writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(input_variables = ["subject","quiz"], template=TEMPLATE2)

review_chain = LLMChain(llm=llm, prompt = quiz_evaluation_prompt,output_key="review", verbose=True)

generate_evaluate_chain = SequentialChain(chains = [quiz_chain,review_chain], input_variables=["text","number","subject","tone","response_json"], output_variables = ["quiz", "review"], verbose =True)


    