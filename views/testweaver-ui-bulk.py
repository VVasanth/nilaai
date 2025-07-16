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


selenium_instruction_pom_old = """
As a Selenium Test Automation architect, generate a functioning, well formatted, Page Object Model scripts with validation steps across the multiple test cases mentioned in the json array format...ensure to generate the test scripts for individual test cases as a separate script with the Page object classes created as a common one...pls use the value present under XPath column for the identifiers in the test automation script:

"""

selenium_instruction_pom_new = """

You are a Test Automation Engineer.
Generate a Selenium-based Python test automation suite using the Page Object Model (POM) pattern.
Test cases are defined by a JSON array of JSON Array - where the inner JSON Array constitute the individual manual test case. You need to refer the manual test case to generate the automation scripts, following OOPS principles.
Use "Step_No" field of the individual test case to identify the sequence number, "Step" field to identify the step, "Data" field to identify the data used and "XPath" to use as a locator.

Each test case must be implemented as a standalone test method, and all test cases should be organized into a test class using Python’s unittest framework.
Use webdriver.Chrome() for browser automation and ensure test setup and teardown are handled using a BaseTest class.
Create reusable page object classes under a pages/ folder.

🧾 Input JSON Format:
[
  [
      {"Step_No": 1, "Step": "Open website", "Data": "https://github.com/", "XPath": NaN},
      {"Step_No": 2, "Step": "Click on \"Enterprises\", "Data": NaN, "XPath": "//a[normalize-space()='Enterprises']"},
      {"Step_No": 3, "Step": "Scroll down", "Data": NaN, "XPath": NaN},
  ],
  [
      {"Step_No": 1, "Step": "Open website", "Data": "https://github.com/", "XPath": NaN},
      {"Step_No": 2, "Step": "Click on \"Enterprises\", "Data": NaN, "XPath": "//a[normalize-space()='Enterprises']"},
      {"Step_No": 3, "Step": "Scroll down", "Data": NaN, "XPath": NaN},
    ]
]

🛠️ Output Requirements:
Use Page Object Model (separate LoginPage in pages/login_page.py)

Create BaseTest class to handle browser setup/teardown (setUp/tearDown)

Dynamically generate test methods in tests/test_login.py based on test names and steps

Use unittest.TestCase for structure

Use selenium.webdriver.common.by.By for locators

Handle unsupported actions with meaningful comments or exceptions

🔄 Each step type should be implemented with reusable helper methods where appropriate (e.g., enter_text(), click_element(), assert_in_url(), etc.).

✅ Ensure all generated code is Pythonic, readable, modular, and ready to run.

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



def gen_selenium_suite(test_suite_content):
    # Wrap it with LangChain
    llm_hf_selenium = HuggingFaceEndpoint(endpoint_url=hf_endpoint_url_qwencode,max_new_tokens=3000,streaming=True)
    
    # Create a simple prompt template
    prompt_template = PromptTemplate(
         input_variables=["selenium_instruction", "input_1", "input_2", "input_3"],
         template=template_selenium,
    )
    # Create a chain
    chain = LLMChain(llm=llm_hf_selenium, prompt=prompt_template)


    base_script_instruction = selenium_instruction_pom_new
    
    json_content = ""
    for test_case_content in test_suite_content:
        json_content = json_content + json.dumps(test_case_content, indent=2)

    print(json_content)
    script_instruction = base_script_instruction + json_content
    
    response = chain.run(
        {
            "instruction": script_instruction
        })
    
    return response    


st.title(f"TestWeaver - Generate test automation suite", anchor=False)

with st.expander("Generate Page Object Model (POM) mode Selenium automation scripts in a snap."):
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

st.subheader("🧠 Test Automation Suite Generation")  # This acts as the form title


#with st.form("my_form"):
# Upload a file
uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)
print(uploaded_files)
# If a file is uploaded
if len(uploaded_files) !=0:
    proc_files = []
    payload_files = []
    for uploaded_file in uploaded_files:
        df=pd.read_csv(uploaded_file)
        payload_df = df[['#', 'Step', 'Data', 'XPath']]
        payload_df.rename(columns={'#': 'Step_No'}, inplace=True)
        proc_df = df[['Step', 'Data', 'XPath']]
        proc_files.append(proc_df)
        payload = payload_df.to_dict(orient='records')    
        payload_files.append(payload)
    prefix = "TestCase_"
    options = [f"{prefix}{i+1}" for i in range(0, len(proc_files))]
    selected_option = st.selectbox("Preview Test Case:", options)
    selected_index = options.index(selected_option)
    st.dataframe(proc_files[selected_index], width=1800, height=800)
submitted = st.button("Generate Test Suite")
if submitted:
    with st.spinner("Generating..."):
        gen_selenium_script = gen_selenium_suite(payload_files)
        print("response...")
        #print(gen_selenium_script)
        #proc_response = process_response(gen_selenium_script)
        st.write(gen_selenium_script)
