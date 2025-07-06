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
hf_endpoint_url_qwencode = "https://pawadchurisr44it.us-east-2.aws.endpoints.huggingface.cloud"


# Define prompt
template_selenium = """### Instruction:
{instruction}

### Response:"""


selenium_instruction_testng = """
As a Selenium Test Automation architect, generate a functioning, well formatted, TestNG script with validation steps based on the below test steps captured in the json format...pls use the value present under XPath column for the identifiers in the test automation script:

"""

selenium_instruction_testng = """
As a Test Automation Engineer, generate a robust Selenium TestNG automation script in Java, based on the test steps provided below in json format.
Your response must strictly follow the guidelines below:
    ✅ Use the value present under XPath column for the identifiers
    ✅ Add inline comments explaining each key part of the code
    ✅ Implement validations using Assert.* statements for expected UI behavior
    ✅ Use explicit waits (WebDriverWait) instead of hardcoded sleep
    ✅ Follow TestNG annotations like @BeforeMethod, @AfterMethod, @Test
    ✅ Ensure code quality: proper naming, structure, and exception handling
    ✅ Assume XPath locators are provided unless specified otherwise
    ✅ Add negative scenario handling if any step might fail

⚠️ IMPORTANT:
    The response must be pure, production-ready Java code that can be directly used.
    Do not include any introductory text, explanation, or markdown formatting.
"""


cypress_instruction_testng = """
As a Test Automation Engineer, generate a robust Cypress automation script in JavaScript (ES6), based on the test steps provided below in JSON format.
Your response must strictly follow the guidelines below:

✅ Use the value present under the XPath column for element identification (wrap with cy.xpath() — assume the xpath plugin is installed)
✅ Add inline comments explaining each key part of the code
✅ Implement assertions using should() or expect() for expected UI behaviour
✅ Rely on Cypress’s built‑in retry mechanism and command chaining instead of hard‑coded waits; when network sync is needed, alias the call with cy.intercept() and cy.wait('@alias')
✅ Structure the test with Mocha hooks: beforeEach, afterEach, and it blocks
✅ Ensure code quality: clear naming, modular commands (use cypress/support/commands.js if helper actions are needed), and proper error handling with cy.on('uncaught:exception', …)
✅ Assume XPath locators are provided unless specified otherwise
✅ Include negative‑path checks for any step that might fail (e.g., asserting an error message or element absence)

⚠️ IMPORTANT:
The response must be pure, production‑ready Cypress JavaScript code that can be used directly.
Do not include any introductory text, explanation, or markdown formatting.
"""


selenium_instruction_pom_old = """
As a Selenium Test Automation architect, generate a functioning, well formatted, Page Object Model script with validation steps based on the below test steps captured in the json format...pls use the value present under XPath column for the identifiers in the test automation script:

"""

selenium_instruction_pom = """
As a Test Automation Engineer, generate a robust Selenium Page Object Model automation script in Java, based on the test steps provided below in json format.
Your response must strictly follow the guidelines below:
    ✅ Use Page Object Model (POM) structure
    ✅ Use the value present under XPath column for the identifiers
    ✅ Add inline comments explaining each key part of the code
    ✅ Implement validations using Assert.* statements for expected UI behavior
    ✅ Use explicit waits (WebDriverWait) instead of hardcoded sleep
    ✅ Follow TestNG annotations like @BeforeMethod, @AfterMethod, @Test
    ✅ Ensure code quality: proper naming, structure, and exception handling
    ✅ Assume XPath locators are provided unless specified otherwise
    ✅ Add negative scenario handling if any step might fail

⚠️ IMPORTANT:
    The response must be pure, production-ready Java code that can be directly used.
    Do not include any introductory text, explanation, or markdown formatting.
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

    if(test_mode == "***Selenium***"):
        base_script_instruction = selenium_instruction_testng #selenium_instruction_testng
    else:
       base_script_instruction = cypress_instruction_testng

    script_instruction = base_script_instruction + json.dumps(test_case_content, indent=2)
    

    response = chain.run(
        {
            "instruction": script_instruction
        })
    
    return response    


st.title(f"TestWeaver - Generate test cases and scripts", anchor=False)

with st.expander("Generate Selenium and Cypress automation scripts in a snap."):
#st.subheader("Total API test coverage, woven in a snap.", anchor=False)
    st.write(
    """
    ***TestWeaver*** turns plain English test steps into robust, Selenium-based test automation scripts — no manual coding needed. From UI clicks to validations, it captures every step, covering functional flows, negative paths, and boundary scenarios with precision.

    🔥 Key Features:

    🧠 Natural Language to Automation: Generate Selenium test scripts directly from plain English test steps.

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
sel_test_mode = st.radio("Select Automation Test Script Framework", ["***Selenium***", "***Cypress***"])
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
        print("response...")
        #print(gen_selenium_script)
        #proc_response = process_response(gen_selenium_script)
        st.write(gen_selenium_script)
