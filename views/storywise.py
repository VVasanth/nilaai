import streamlit as st
import pandas as pd  # pip install pandas
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = "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"
hf_endpoint_url = "https://dl5gegyfgn6puaab.us-east-1.aws.endpoints.huggingface.cloud"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

template = """
<s>[INST] <<SYS>> You are a helpful QA architect, who has an expertise in writing test cases for api. From the given api documentation, you generate comprehensive test cases. You also have expertise in python and java languages and write quality code. <</SYS>> [INST]

{question} [/INST]
"""

def generate_response(input_text):
    """
    Returns a language model for HuggingFace inference.

    Parameters:
    - model_id (str): The ID of the HuggingFace model repository.
    - max_new_tokens (int): The maximum number of new tokens to generate.
    - temperature (float): The temperature for sampling from the model.

    Returns:
    - llm (HuggingFaceEndpoint): The language model for HuggingFace inference.
    """
    # Wrap it with LangChain
    llm_hf = HuggingFaceEndpoint(
        endpoint_url=hf_endpoint_url,
        max_new_tokens=1024,
        top_k=50,
        top_p=0.9,
        temperature=0.6,
        repetition_penalty=1.2,
        streaming=True
    )
    
    # Create a simple prompt template
    prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template="Q: {user_input}\nA:"
    )

    # Create a chain
    chain = LLMChain(llm=llm_hf, prompt=prompt_template)

    response = chain.run(user_input=input_text)
    
    return response

st.title(f"StoryWise - User Story Assessor", anchor=False)


st.write("\n")
st.subheader("Your GenAI partner for bulletproof user stories", anchor=False)
st.write(
    """
    StoryWise is a GenAI-powered assistant that reviews user stories in real time, providing instant, actionable feedback to improve clarity, completeness, and testability. It identifies ambiguous language, missing acceptance criteria, and vague requirements — helping teams write better stories, faster. 
    
    The result? 
    
    Stronger specs, fewer bugs, and a smoother handoff from idea to execution.
    """
)

st.write("\n")
st.divider()
st.write("\n")

with st.form("my_form"):

    user_story_title = st.text_input("User Story Title", "")

    st.write("\n")
    user_story_desc = st.text_area(
        "User Story Description",
        "",height=150
    )

    st.write("\n")
    acceptance_criteria = st.text_area(
        "Acceptance Criteria",
        "",height=100
    )

    st.write("\n")
    submitted = st.form_submit_button("Evaluate User Story")
    #st.button("Evaluate User Story", type="primary")
    if submitted:
        print(user_story_desc)
        response = generate_response(user_story_desc)
        st.success("Here's the answer:")
        st.write(response)