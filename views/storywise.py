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

Provide each of the strengths and Areas for improvements as a bulletted points, with clear specific details.

If the user story input does not meet the defined template, pls respond back asking user to provide user story in the proper template.

User Story to be evaluated:

"""


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

st.title(f"StoryWise - User Story Assessor", anchor=False)

st.subheader("Your GenAI partner for bulletproof user stories", anchor=False)
st.write(
"""
***StoryWise is your GenAI-powered story coach — instantly slicing through fuzz, tightening clarity, and flagging gaps before weak specs become real problems.*** It catches vagueness, missing criteria, and half-baked requirements before they hit your backlog.

💡 How it aligns with the INVEST principles:

✅ ***Independent*** – Encourages writing stories that stand alone by spotting dependencies or entanglements.

✅ ***Negotiable*** – Flags overly prescriptive language to keep the story open for team discussion.

✅ ***Valuable*** – Ensures each story has clear business value, not just busywork.

✅ ***Estimable*** – Highlights missing detail or ambiguity that blocks accurate estimation.

✅ ***Small*** – Detects bloated stories and suggests splitting logic to keep them manageable.

✅ ***Testable*** – Validates the presence of concrete acceptance criteria so QA can hit the ground running.

The result? \n
📉 **Fewer bugs.** \n
🚀 **Faster cycles.** \n
🤝 **Cleaner handoffs from product to engineering.** \n

\n
StoryWise: From fuzzy ideas to rock-solid user stories — in real time.
    """
)

# Initialize session variable if it doesn't exist
if 'download_test_cases' in st.session_state:
    st.session_state.download_test_cases = False

if 'generate_test_cases' in st.session_state:
    st.session_state.generate_test_cases = False

if 'show_generated_test_cases' in st.session_state:
    st.session_state.show_generated_test_cases = False

if 'show_generate_script' in st.session_state:
    st.session_state.show_generate_script = False


st.divider()

st.subheader("🧠 Experiment Zone: Validate Your User Stories with AI")  # This acts as the form title

with st.form("my_form"):

    user_story_title = st.text_input("User Story Title *", placeholder="Enter your user story title here...")

    st.write("\n")
    user_story_desc = st.text_area(
        "User Story Description *",
        placeholder="Enter your user story description here...",height=150
    )

    st.write("\n")
    acceptance_criteria = st.text_area(
        "Acceptance Criteria *",
        placeholder="Enter your acceptance criteria here...",height=100
    )

    st.write("\n")
    submitted = st.form_submit_button("Evaluate User Story")
    #st.button("Evaluate User Story", type="primary")
    if submitted:
        if not user_story_title or not user_story_desc or not acceptance_criteria:
            st.error("Title, Description and Acceptance Criteria are required. Please fill in all fields.")
        else:
            print(user_story_desc)
            with st.spinner("Evaluating..."):
                response = generate_response(user_story_title, user_story_desc, acceptance_criteria)
            st.success("Here's the answer:")
            st.write(response)