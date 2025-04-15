import streamlit as st

from forms.contact import contact_form


@st.experimental_dialog("Contact Me")
def show_contact_form():
    contact_form()


# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/QEforAILogo.jpeg", width=350)

with col2:
    st.title("QE for AI", anchor=False)
    st.write(
        "Transforming Quality Engineering with GenAI-powered tools that validate, refine, and auto-generate — accelerating delivery while raising the bar on quality."
    )
    

# --- EXPERIENCE & QUALIFICATIONS ---
st.write("\n")
st.subheader("Reimagining Quality Engineering with GenAI", anchor=False)
st.write(
    """
    Bringing GenAI into the heart of Quality Engineering to boost speed, precision, and impact.
    We're building smart solutions like:

    🔍 User Story Validator – Instantly flags gaps in clarity, coverage, and testability

    ✍️ User Story Refiner – Sharpens messy stories into dev-ready requirements

    ⚙️ Test Case Generator – Auto-generates test cases with context-aware intelligence

    The result? 
    
    Faster cycles, fewer bugs, and a smarter path to quality.
    """
)
