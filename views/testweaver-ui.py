import streamlit as st
import pandas as pd  # pip install pandas
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import re
import json

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = "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"
hf_endpoint_url_qwencode = "https://pawadchurisr44it.us-east-2.aws.endpoints.huggingface.cloud"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN


# Define prompt
template_selenium = """### Instruction:
{instruction}

### Response:"""


selenium_instruction_testng = """
As a Selenium Test Automation architect, generate a functioning, well formatted, TestNG script with validation steps based on the below test steps captured in the json format...pls use the value present under XPath column for the identifiers in the test automation script:

"""

selenium_instruction_pom = """
As a Selenium Test Automation architect, generate a functioning, well formatted, Page Object Model script with validation steps based on the below test steps captured in the json format...pls use the value present under XPath column for the identifiers in the test automation script:

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


def process_response(response_str):
    start_index = response_str.find("Response:")
    processed_response = response_str[start_index:]
    return processed_response



def gen_selenium_script(test_case_content, test_mode):
    # Wrap it with LangChain
    llm_hf_selenium = HuggingFaceEndpoint(endpoint_url=hf_endpoint_url_qwencode,max_new_tokens=3000,streaming=True)
    
    # Create a simple prompt template
    prompt_template = PromptTemplate(
         input_variables=["selenium_instruction", "input_1", "input_2", "input_3"],
         template=template_selenium,
    )
    # Create a chain
    chain = LLMChain(llm=llm_hf_selenium, prompt=prompt_template)

    if(test_mode == "***TestNG***"):
        base_sel_instruction = selenium_instruction_testng
    else:
       base_sel_instruction = selenium_instruction_pom

    selenium_instruction = base_sel_instruction + json.dumps(test_case_content, indent=2)
    

    response = chain.run(
        {
            "instruction": selenium_instruction
        })
    
    return response    


st.title(f"TestWeaver - Generate test cases and scripts", anchor=False)

with st.expander("Generate selenium automation scripts in a snap."):
#st.subheader("Total API test coverage, woven in a snap.", anchor=False)
    st.write(
    """
    ***TestWeaver*** turns plain English test steps into robust, Selenium-based test automation scripts — no manual coding needed. From UI clicks to validations, it captures every step, covering functional flows, negative paths, and boundary scenarios with precision.

    🔥 Key Features:

    🧠 Natural Language to Automation: Generate Selenium test scripts directly from plain English test steps.

    🔄 Page Object Model Support: Clean, maintainable code following industry-standard best practices.

    ✅ End-to-End Coverage: From happy paths to failure flows — every click, input, and assertion is automated.

    ⚙️ Framework Friendly: Output scripts in TestNG or PyTest format, ready to plug into your CI/CD pipeline.

    💥 Benefits:

    ⏱️ Accelerates Automation: Say goodbye to hours of manual scripting — go from spec to script in seconds.

    🧪 Improves Test Reliability: Standardized scripts reduce flaky tests and increase coverage.

    🧼 Simplifies Maintenance: POM structure makes script updates a breeze when UI changes.

    🚀 Empowers Teams: Enables non-technical stakeholders to contribute to automation with plain-language test cases.

        """
    )

st.divider()

st.subheader("🧠 Test Automation Script Generation from test steps")  # This acts as the form title


#with st.form("my_form"):
# Upload a file
uploaded_file = st.file_uploader("Choose a file", type=['csv'])
sel_test_mode = st.radio("Select Selenium Test Script Mode", ["***TestNG***", "***Page Object Model***"])
# If a file is uploaded
if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    payload_df = df[['#', 'Step', 'Data', 'XPath']]
    payload_df.rename(columns={'#': 'Step_No'}, inplace=True)
    proc_df = df[['Step', 'Data', 'XPath']]
    st.dataframe(proc_df, width=1800, height=800)
    payload = payload_df.to_dict(orient='records')    
submitted = st.button("Generate Test Scripts")
if submitted:
    with st.spinner("Generating..."):
        gen_selenium_script = gen_selenium_script(payload, sel_test_mode)
        proc_response = process_response(gen_selenium_script)
        st.write(proc_response)
