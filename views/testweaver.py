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
#hf_endpoint_url = "https://dl5gegyfgn6puaab.us-east-1.aws.endpoints.huggingface.cloud"
hf_endpoint_url = "https://ydx9vu47ixt3vcs8.us-east-1.aws.endpoints.huggingface.cloud"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

# Define prompt
template = """### Instruction:
{instruction}

### API Name:
{input_1}

### API Brief Description:
{input_2}

### Endpoint URL:
{input_3}

### Parameter_details:
{input_4}


### Response:"""

instruction = """"
As a Quality Engineer, generate a detailed and structured set of test cases — including positive, negative, and edge cases — for validating a REST API endpoint. The goal is to ensure correctness, robustness, error handling, and resilience against edge conditions.

Actor: Quality Engineer (QE)
Responsible for:
* Validating all input parameters (required/optional)
* Simulating real-world usage and failure scenarios
* Ensuring the endpoint handles invalid or unexpected input gracefully
* Confirming compliance with spec, business rules, and security expectations

Expected Output (from Assistant):
🔢 Test Case Summary:
* Total Positive Cases: X
* Total Negative Cases: Y
* Total Edge Cases: Z
✅ Positive Test Cases
(Valid scenarios that should succeed)
❌ Negative Test Cases
(Invalid or missing inputs that should fail predictably)
🧪 Edge Test Cases
(Boundary or rare conditions to test robustness)

📋 Test Case Format (for each case):
* Test Case ID
* Description
* Input Parameters (with example values)
* Expected Outcome

🔍 QE Test Strategy Coverage Checklist:
* Required vs optional parameter handling
* Data type mismatches and nulls
* Missing parameters
* Invalid or unsupported enum values
* Format violations (e.g., malformed URL)
* Boundary values and limits
* Extra/unknown fields
* Wrong HTTP methods
* Authentication/authorization errors (if applicable)
* Duplicate/replay handling
* Business logic constraints

📝 API Detail input to generate test cases:

"""

def process_response(response_str):
    start_index = response_str.find("🔢 Test Case Summary:")
    processed_response = response_str[start_index:]
    return processed_response



def generate_response(input_1, input_2, input_3, input_4):
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
        max_new_tokens=3000,
        streaming=True
    )
    
    # Create a simple prompt template
    prompt_template = PromptTemplate(
         input_variables=["instruction", "input_1", "input_2", "input_3", "input_4"],
         template=template,
    )
    print(prompt_template)
    # Create a chain
    chain = LLMChain(llm=llm_hf, prompt=prompt_template)

    response = chain.run(
        {
            "instruction": instruction,
            "input_1": input_1,
            "input_2": input_2,
            "input_3": input_3,
            "input_4": input_4
        })
    
    return response

st.title(f"TestWeaver - Generate test cases and scripts", anchor=False)

st.subheader("Total API test coverage, woven in a snap.", anchor=False)
st.write(
"""
***TestWeaver transforms your API specs into comprehensive test cases and Python test scripts***, covering both positive and negative scenarios. It ensures complete API test coverage — from happy paths to edge cases, and error handling.

🔥 Key Features:

🛠️ Automated Test Generation: Instantly generate Python test scripts from your API specifications.

✅ Positive & Negative Scenarios: Full-spectrum testing, covering success and failure paths.

🔍 Comprehensive Coverage: Validates every edge case, error, and boundary condition.

⚙️ Easy Integration: Plug directly into your testing pipeline with ready-to-run Python scripts.

💥 Benefits:

📈 Boosts Test Coverage: No more missed edge cases or error paths.

⏳ Saves Time: Automatically generates test cases — no manual scripting required.

🚫 Reduces Errors: Ensures comprehensive testing without human oversight.

🔒 Increases Confidence: Reliable, repeatable tests for thorough API validation.

    """
)

st.divider()

st.subheader("🧠 Experiment Zone: AI Generated Test Cases from API details")  # This acts as the form title

with st.form("my_form"):

    api_name = st.text_input("API Name *", placeholder="Enter api name/title here...")

    st.write("\n")
    api_desc = st.text_area(
        "API Brief Description *",
        placeholder="Enter brief description about the API here...",height=100
    )

    st.write("\n")
    endpoint_url = st.text_input("Endpoint URL *", placeholder="Enter endpoint url here...")

    st.write("\n")
    parameter_details = st.text_area(
        "Parameter Details *",
        placeholder="Enter api parameter details here...",height=300
    )

    st.write("\n")
    submitted = st.form_submit_button("Generate Test Cases")
    #st.button("Evaluate User Story", type="primary")
    if submitted:
        if not api_name or not api_desc or not endpoint_url or not parameter_details:
            st.error("API Title, Description, Endpoint URL and Parameter details are required. Please fill in all fields.")
        else:
            with st.spinner("Generating..."):
                print(api_name)
                print(parameter_details)
                response = generate_response(api_name, api_desc, endpoint_url, parameter_details)
            print(response)
            st.success("Generated Test Cases are:")
            processed_response = process_response(response)
            st.write(processed_response)
