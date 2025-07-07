import streamlit as st
import pandas as pd  # pip install pandas
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import re

load_dotenv()
#hf_endpoint_url = "https://dl5gegyfgn6puaab.us-east-1.aws.endpoints.huggingface.cloud"
hf_endpoint_url = "https://ydx9vu47ixt3vcs8.us-east-1.aws.endpoints.huggingface.cloud"
hf_endpoint_url_resassured = "https://pawadchurisr44it.us-east-2.aws.endpoints.huggingface.cloud"

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


# Define prompt
template_restassured = """### Instruction:
{instruction}

### API Name:
{input_1}

### API Brief Description:
{input_2}

### Test Case Content:
{input_3}


### Response:"""


rest_assured_instruction = """
As a RestAssured Automation Script engineer, generate a functioning, well formatted restassured script with proper comments for the below mentioned api test case details.

"""

instruction = """

As a Quality Engineer (QE), generate a comprehensive and strictly structured set of REST API test cases — covering positive, negative, and edge scenarios — to ensure complete validation of the endpoint’s correctness, robustness, error handling, and resilience under edge conditions.

🎯 Role: Quality Engineer (QE)
Responsible for:

Exhaustively validating all input parameters (required & optional)
Simulating realistic and failure-prone usage scenarios
Ensuring the API gracefully handles invalid, missing, or unexpected input
Verifying compliance with functional spec, business logic, and security expectations

🔒 ‼️ Output Requirements — Strict Adherence is Mandatory
You MUST follow the exact structure and format below — no deviations, no omissions. Responses that do not conform will be considered non-compliant.

🔢 Test Case Summary Section (Top of Output):
Total Positive Cases: X  
Total Negative Cases: Y  
Total Edge Cases: Z

✅ Positive Test Cases

❌ Negative Test Cases

🧪 Edge Test Cases

📋 Test Case Format (Each Case Must Include):
Test Case ID
Description
Input Parameters (with sample values)

Expected Outcome
🔍 QE Test Strategy Coverage Checklist — All Must Be Addressed:
 Required vs optional parameters
 Missing or null parameters
 Incorrect data types
 Invalid or unsupported enum values
 Malformed formats (e.g., bad URL, wrong date/time)
 Boundary limits (min/max, string lengths, etc.)
 Unexpected/extra fields
 Invalid HTTP methods
 Auth/authz failures (if applicable)
 Replay attacks or duplicate handling
 Violations of business logic or constraints

🔁 Final Note: You must generate the test cases in the above format without skipping any structural requirement. Do not improvise or restructure the layout. This is a formal QA artifact and format consistency is non-negotiable.

📝 API Detail input to generate test cases:
"""

instruction_old = """"
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

Pls be sure to generate test cases in the format mentioned above and always stick to the defined format.

📝 API Detail input to generate test cases:

"""

pos_instruction = """Positive Test Cases
(Valid scenarios that must succeed)"""

neg_instruction = """Negative Test Cases
(Invalid/missing inputs that must fail predictably)"""

edge_instruction = """Edge Test Cases
(Boundary values, rare conditions, or stress tests)"""

def process_response(response_str):
    start_index = response_str.find("Test Case Summary Section")
    end_index = response_str.find("QE Test Strategy Coverage Checklist")
    processed_response = response_str[start_index:end_index]
    return processed_response


def split_processed_response(proc_response_str):
    pos_test_case_start_index = proc_response_str.find("Positive Test Cases")
    neg_test_case_start_index = proc_response_str.find("Negative Test Cases")
    edge_test_case_start_index = proc_response_str.find("Edge Test Cases")
    test_summary_content = proc_response_str[:(pos_test_case_start_index-5)]
    pos_test_cases_content = proc_response_str[pos_test_case_start_index:(neg_test_case_start_index-5)]
    neg_test_cases_content = proc_response_str[neg_test_case_start_index:(edge_test_case_start_index-5)]
    edge_test_cases_content = proc_response_str[edge_test_case_start_index:]
    print("printing test case content")
    print(pos_test_cases_content)
    print(neg_test_cases_content)

    pos_test_cases_content_x = re.sub(r'^Positive Test Cases\s*', '', pos_test_cases_content)
    # Split on **Test Case ID but keep it in the result
    pos_test_cases_0 = re.split(r'(?=Test Case ID:)', pos_test_cases_content_x.strip())
    # Strip each chunk and drop empty ones
    pos_test_cases = [case.strip() for case in pos_test_cases_0 if case.strip()][1:]
    pos_test_cases = [s.replace("**", "") for s in pos_test_cases]
    print("printing splitted test cases")
    print(pos_test_cases)
    print(len(pos_test_cases))

    neg_test_cases_content_x = re.sub(r'^Negative Test Cases\s*', '', neg_test_cases_content)
    # Split on **Test Case ID but keep it in the result
    neg_test_cases_0 = re.split(r'(?=Test Case ID:)', neg_test_cases_content_x.strip())
    # Strip each chunk and drop empty ones
    neg_test_cases = [case.strip() for case in neg_test_cases_0 if case.strip()][1:]
    neg_test_cases = [s.replace("**", "") for s in neg_test_cases]

    edge_test_cases_content_x = re.sub(r'^Edge Test Cases\s*', '', edge_test_cases_content)
    # Split on **Test Case ID but keep it in the result
    edge_test_cases_0 = re.split(r'(?=Test Case ID:)', edge_test_cases_content_x.strip())
    # Strip each chunk and drop empty ones
    edge_test_cases = [case.strip() for case in edge_test_cases_0 if case.strip()][1:]
    edge_test_cases = [s.replace("**", "") for s in edge_test_cases]

    #pos_test_cases = re.split(r'\s\d+\.\s', pos_test_cases_content.strip())
    #neg_test_cases = re.split(r'\s\d+\.\s', neg_test_cases_content.strip())
    #edge_test_cases = re.split(r'\s\d+\.\s', edge_test_cases_content.strip())
    return test_summary_content, pos_test_cases, neg_test_cases, edge_test_cases


def gen_rest_assured_script(api_name, api_desc, test_case_content):
    # Wrap it with LangChain
    llm_hf_rest_assured = HuggingFaceEndpoint(endpoint_url=hf_endpoint_url_resassured,max_new_tokens=6000,streaming=True)
    
    # Create a simple prompt template
    prompt_template = PromptTemplate(
         input_variables=["rest_assured_instruction", "input_1", "input_2", "input_3"],
         template=template_restassured,
    )
    # Create a chain
    chain = LLMChain(llm=llm_hf_rest_assured, prompt=prompt_template)

    response = chain.run(
        {
            "instruction": rest_assured_instruction,
            "input_1": api_name,
            "input_2": api_desc,
            "input_3": test_case_content,
        })
    
    return response    


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

with st.expander("Total API test coverage, woven in a snap."):
#st.subheader("Total API test coverage, woven in a snap.", anchor=False)
    st.write(
    """
    ***TestWeaver transforms your API specs into comprehensive test cases and RestAssured test scripts***, covering both positive and negative scenarios. It ensures complete API test coverage — from happy paths to edge cases, and error handling.

    🔥 Key Features:

    🛠️ Automated Test Generation: Instantly generate RestAssured test scripts from your API specifications.

    ✅ Positive & Negative Scenarios: Full-spectrum testing, covering success and failure paths.

    🔍 Comprehensive Coverage: Validates every edge case, error, and boundary condition.

    ⚙️ Easy Integration: Plug directly into your testing pipeline with ready-to-run RestAssured scripts.

    💥 Benefits:

    📈 Boosts Test Coverage: No more missed edge cases or error paths.

    ⏳ Saves Time: Automatically generates test cases — no manual scripting required.

    🚫 Reduces Errors: Ensures comprehensive testing without human oversight.

    🔒 Increases Confidence: Reliable, repeatable tests for thorough API validation.

        """
    )

st.divider()

st.subheader("🧠 Experiment Zone: AI Generated Test Cases from API details")  # This acts as the form title

dummy_response = """


Test Case Summary:
- **Total Positive Cases:** 10
- **Total Negative Cases:** 10
- **Total Edge Cases:** 6

---

### ✅ Positive Test Cases

#### 1. **Valid Request with All Parameters**
- **Description:** Test with all valid parameters.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `type = "public", sort = "updated", direction = "desc", per_page = 50, page = 2`
- **Expected Outcome:** 200 OK with 50 public repos, sorted by updated in descending order.

#### 2. **Default Parameters**
- **Description:** Omit all query parameters to use defaults.
- **Input Parameters:**
  - Path: `org = "test-org"`
- **Expected Outcome:** 200 OK with 30 repos, sorted by created descending.

#### 3. **All Repo Types**
- **Description:** Request all repo types.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `type = "all"`
- **Expected Outcome:** 200 OK with all repo types.

#### 4. **Private Repositories**
- **Description:** Request private repos.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `type = "private"`
- **Expected Outcome:** 200 OK with private repos.

#### 5. **Sort by Full Name Ascending**
- **Description:** Sort by full_name in ascending order.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `sort = "full_name", direction = "asc"`
- **Expected Outcome:** 200 OK, repos sorted by full_name ascending.

#### 6. **Max Per Page**
- **Description:** Use max per_page value.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `per_page = 100`
- **Expected Outcome:** 200 OK with up to 100 repos.

#### 7. **Multiple Pages**
- **Description:** Test pagination with page=2.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `page = 2`
- **Expected Outcome:** 200 OK with second page of repos.

#### 8. **Forks Only**
- **Description:** Request forks only.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `type = "forks"`
- **Expected Outcome:** 200 OK with forked repos.

#### 9. **Sort by Pushed Date**
- **Description:** Sort by pushed date.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `sort = "pushed"`
- **Expected Outcome:** 200 OK, repos sorted by pushed date.

#### 10. **Member Repositories**
- **Description:** Request member repos.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `type = "member"`
- **Expected Outcome:** 200 OK with member repos.

---

### ❌ Negative Test Cases

#### 1. **Invalid Org Name**
- **Description:** Use a non-existent org.
- **Input Parameters:**
  - Path: `org = "invalid-org"`
- **Expected Outcome:** 404 Not Found.

#### 2. **Invalid Type Value**
- **Description:** Use an invalid type.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `type = "invalid"`
- **Expected Outcome:** 422 Unprocessable Entity.

#### 3. **Invalid Sort Value**
- **Description:** Use an invalid sort parameter.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `sort = "invalid"`
- **Expected Outcome:** 422 Unprocessable Entity.

#### 4. **Invalid Direction**
- **Description:** Use invalid direction.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `direction = "invalid"`
- **Expected Outcome:** 422 Unprocessable Entity.

#### 5. **Non-Integer Per Page**
- **Description:** Use string for per_page.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `per_page = "abc"`
- **Expected Outcome:** 422 Unprocessable Entity.

#### 6. **Negative Per Page**
- **Description:** Use negative per_page.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `per_page = -1`
- **Expected Outcome:** 422 Unprocessable Entity.

#### 7. **Invalid Page Number**
- **Description:** Use negative page.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `page = -1`
- **Expected Outcome:** 422 Unprocessable Entity.

#### 8. **Unauthenticated Request**
- **Description:** Omit authentication token.
- **Input Parameters:**
  - Path: `org = "test-org"`
- **Expected Outcome:** 401 Unauthorized.

#### 9. **Insufficient Permissions**
- **Description:** User lacks access to org.
- **Input Parameters:**
  - Path: `org = "test-org"`
- **Expected Outcome:** 403 Forbidden.

#### 10. **Invalid HTTP Method**
- **Description:** Use POST instead of GET.
- **Input Parameters:**
  - Path: `org = "test-org"`
- **Expected Outcome:** 405 Method Not Allowed.

---

### 🧪 Edge Test Cases

#### 1. **Max Per Page Value**
- **Description:** Use per_page=100.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `per_page = 100`
- **Expected Outcome:** 200 OK with up to 100 repos.

#### 2. **Zero Per Page**
- **Description:** Set per_page=0.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `per_page = 0`
- **Expected Outcome:** 422 Unprocessable Entity.

#### 3. **Invalid Parameter Format**
- **Description:** Send null in parameters.
- **Input Parameters:**
  - Path: `org = "test-org"`
  - Query: `type = null`
- **Expected Outcome:** 422 Unprocessable Entity.

#### 4. **Rate Limit Exceeded**
- **Description:** Make too many requests.
- **Input Parameters:**
  - Path: `org = "test-org"`
- **Expected Outcome:** 429 Too Many Requests.

#### 5. **Non-Existent Organization**
- **Description:** Use an invalid org name.
- **Input Parameters:**
  - Path: `org = "nonexistent-org"`
- **Expected Outcome:** 404 Not Found.

#### 6. **Unauthenticated Request**
- **Description:** Omit authentication token.
- **Input Parameters:**
  - Path: `org = "test-org"`
- **Expected Outcome:** 401 Unauthorized.

---

### 

"""


# Initialize session variable if it doesn't exist
if 'download_test_cases' not in st.session_state:
    st.session_state.download_test_cases = False

if 'processed_response' not in st.session_state:
    st.session_state.processed_response = ""

if 'generate_test_cases' not in st.session_state:
    st.session_state.generate_test_cases = False

if 'show_generated_test_cases' not in st.session_state:
    st.session_state.show_generated_test_cases = False

if 'show_generate_script' not in st.session_state:
    st.session_state.show_generate_script = False


processed_response = st.session_state.processed_response
response = ""
restassured_automation_scripts = []
api_name = ""
api_desc = ""
pos_test_cases_len = 0
neg_test_cases_len = 0
edge_test_cases_len = 0
total_test_cases_len = 0


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
    if submitted:
        st.session_state.generate_test_cases = True
        if not api_name or not api_desc or not endpoint_url or not parameter_details:
            st.error("API Title, Description, Endpoint URL and Parameter details are required. Please fill in all fields.")
        else:
            with st.spinner("Generating..."):
                print(api_name)
                print(parameter_details)
                response = generate_response(api_name, api_desc, endpoint_url, parameter_details)
            print(response)
            

if(st.session_state.generate_test_cases == True):
    st.session_state.download_test_cases = True
    st.session_state.show_generate_script = True
    st.session_state.show_generated_test_cases = True
    processed_response = process_response(response)
    st.session_state.processed_response = processed_response


@st.dialog("Generate RestAssured Scripts", width="large")
def generate_rest_assured_scripts():
    print("setting rest assured state")
    test_summary_content, pos_test_cases, neg_test_cases, edge_test_cases = split_processed_response(processed_response)
    print(pos_test_cases)
    pos_test_cases_len, neg_test_cases_len, edge_test_cases_len = len(pos_test_cases), len(neg_test_cases), len(edge_test_cases)
    total_test_cases_len = pos_test_cases_len + neg_test_cases_len + edge_test_cases_len
    pos_test_indices = [f"Positive-{i}" for i in range(1, pos_test_cases_len+1)]
    neg_test_indices = [f"Negative-{i}" for i in range(1, neg_test_cases_len+1)]
    edge_test_indices = [f"Edge-{i}" for i in range(1, edge_test_cases_len+1)]
    test_indices = pos_test_indices + neg_test_indices + edge_test_indices
    test_indices = list(dict.fromkeys(test_indices))
    test_case_contents = pos_test_cases + neg_test_cases + edge_test_cases
    test_case_option = st.selectbox(
    "Test Case ID",
    test_indices)
    test_case_ind = test_indices.index(test_case_option)
    st.divider()
    st.write("Selected Test Case Details:")
    st.write(test_case_contents[test_case_ind])
    if st.button("Generate Rest Assured Scripts", type="primary"):
        with st.spinner("Generating Automation Scripts..."):
            rest_assured_script = gen_rest_assured_script(api_name, api_desc, test_case_contents[test_case_ind])
            st.divider()
            st.write(rest_assured_script)
    #st.session_state.generate_restassured_scripts = True


bt_cols = st.columns((2,3,3), gap="medium")

with bt_cols[0]:
    
    if(st.session_state.download_test_cases == True):
            # Convert string to bytes
            print("inside if")
            #print("rest assured state value" + str(st.session_state.generate_restassured_scripts))
            text_bytes = processed_response.encode('utf-8')
            # Download button
            st.download_button(
                label="Download as .txt",
                data=text_bytes,
                file_name="sample.txt",
                mime="text/plain"
            )

with bt_cols[1]:
    if(st.session_state.show_generate_script == True):
        st.button("Generate Rest Assured Scripts", type="primary", on_click=generate_rest_assured_scripts)


if(st.session_state.show_generated_test_cases == True):
    st.success("Generated Test Cases are:")        
    st.write(processed_response)
    st.session_state.generate_test_cases = False
