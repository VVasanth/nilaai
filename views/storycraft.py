import streamlit as st
import pandas as pd  # pip install pandas
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

load_dotenv()
hf_endpoint_url = "https://dl5gegyfgn6puaab.us-east-1.aws.endpoints.huggingface.cloud"

# Define prompt
template = """### Instruction:
{instruction}

### User Story Title:
{input_1}

### User Story Description:
{input_2}

### Acceptance Criteria:
{input_3}


### Response:"""

instruction = """"
Can you help me in evaluating the user story on the below defined objective with regard to its quality?

Objective: Evaluate a user story against best practices to determine its clarity, feasibility, and alignment with business goals.

Evaluation Criteria:

INVEST Principles:

✅ Independent: Can the story be developed without heavy dependencies?

✅ Negotiable: Is there room for discussion and refinement?

✅ Valuable: Does it deliver clear value to the user or business?

✅ Estimable: Can developers estimate the effort required?

✅ Small: Can it fit within a single sprint or iteration?

✅ Testable: Are there clear success criteria?

User-Centric Format:

🎯 Does the story clearly identify the user, action, and benefit?

🎯 Is it free from unnecessary technical jargon?

Acceptance Criteria:

📌 Are the conditions clear, specific, and measurable?

📌 Do they cover both normal and edge cases?

Business Alignment:

📊 Does the story align with product or business goals?

📊 Does it contribute to engagement, efficiency, or revenue?

Collaboration & Refinement:

🔄 Does the story invite discussion among stakeholders?

🔄 Can it be refined based on feedback?

Output Format (AI Response Example):

Evaluation Summary:

Strengths: (Highlight what is well-defined.)

Areas for Improvement: (Identify gaps and suggest refinements.)

Overall Assessment: (Rate the story as Strong, Needs Refinement, or Weak based on criteria.)

If the user story input does not meet the defined template, pls respond back asking user to provide user story in the proper template.

User Story to be evaluated:

"""
# reset the session state variables associated with testweaver page
if 'download_test_cases' in st.session_state:
    st.session_state.download_test_cases = False

if 'generate_test_cases' in st.session_state:
    st.session_state.generate_test_cases = False

if 'processed_response' in st.session_state:
    st.session_state.processed_response = ""

if 'show_generated_test_cases' in st.session_state:
    st.session_state.show_generated_test_cases = False

if 'show_generate_script' in st.session_state:
    st.session_state.show_generate_script = False

def generate_response(input_1, input_2, input_3):
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
         input_variables=["instruction", "input_1", "input_2", "input_3"],
         template=template,
    )

    # Create a chain
    chain = LLMChain(llm=llm_hf, prompt=prompt_template)

    response = chain.run(
        {
            "instruction": instruction,
            "input_1": input_1,
            "input_2": input_2,
            "input_3": input_3
        })
    
    return response

st.title(f"StoryCraft - User Story Refiner", anchor=False)

st.subheader("From vague to valuable — instantly", anchor=False)
st.write(
"""
***StoryCraft – GenAI-Powered User Story Refiner***
**Refine. Rewrite. Ready-to-Build.**

StoryCraft uses Generative AI to transform messy, vague, or bloated user stories into lean, sprint-ready gold — all aligned with the INVEST principles.

🔧 ***What it does:***
    
💡 Polishes raw stories into Independent, Negotiable, Valuable, Estimable, Small, and Testable units.

💡 Flags ambiguity and fills in missing context using smart, domain-aware prompts.

💡 Streamlines collaboration by delivering crystal-clear stories that reduce back-and-forth.

💡 Accelerates grooming so product and dev teams can move faster with fewer blockers.

💡 Uplevels backlog quality — no more "meh" stories dragging sprints down.

💥 ***Why it matters:***

🕒 Cuts refinement time in half

✅ Boosts story acceptance on first pass

🧠 Reduces cognitive load for devs & QAs

🚀 Improves sprint velocity and predictability

    """
)

st.divider()

st.subheader("🛠️Coming soon: A smarter way to refine stories. Hang tight!")  # This acts as the form title
