import os
import io
import contextlib
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables for Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set Streamlit page configuration
st.set_page_config(page_title="AI Powered Data Analyst", layout="wide")

# Optional: CSS to push the chat input to the bottom
st.markdown("""
    <style>
    .block-container {
        display: flex;
        flex-direction: column;
        height: 100vh;
    }
    .element-container:has(input) {
        margin-top: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Gemini model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

st.title("📊 AI-Powered Data Analyst")
st.markdown("Upload a CSV and ask questions about your data in natural language.")

# Session state for chat history and clearing input
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# File upload section
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        #st.warning("Non-UTF8 file detected. Trying fallback encoding...")
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")

    # Show preview of data
    st.subheader("Preview of your data")
    st.dataframe(df.head())

    # Prepare summary info for prompt
    col_info = df.dtypes.apply(lambda x: x.name).to_dict()
    shape_info = f"DataFrame shape: {df.shape[0]} rows, {df.shape[1]} columns"
    desc_stats = df.describe(include='all').fillna('N/A').to_dict()
    sample_data = df.head(5).to_dict(orient="records")

    # Show chat history before input
    for i, chat in enumerate(st.session_state.chat_history):
        st.markdown(f"### Question {i+1}:")
        st.write(chat["query"])

        st.markdown("**Generated Code:**")
        st.code(chat["code"], language="python")

        if chat["output"]:
            st.markdown("**Output:**")
            st.text(chat["output"])

        if chat["plot"]:
            st.markdown("**Plot:**")
            st.pyplot(chat["plot"])

    # Clear the input box after query submission
    if st.session_state.clear_input:
        st.session_state.query_input = ""
        st.session_state.clear_input = False

    # Input section at the bottom
    st.markdown("---")
    query = st.text_input("💬 Ask a question about your data:", key="query_input", placeholder="Type your question and press Enter...")

    if st.button("Submit Query") and query.strip():
        prompt = f"""
            You are a Python data analyst.

            You have the following DataFrame `df`:

            - {shape_info}
            - Column Info (column name: dtype): {col_info}
            - Summary statistics: {desc_stats}
            - Sample Rows: {sample_data}

            Write **robust, well-commented Python code** using pandas (and matplotlib if visualization is needed) to answer the user's query.

            User Query: "{query}"

            Only return valid Python code. Do not include any text outside of the code block.
        """

        with st.spinner("Generating code..."):
            response = model.generate_content(prompt)
            code = response.text.strip()
            if code.startswith("```python"):
                code = code[len("```python"):].strip()
            if code.endswith("```"):
                code = code[:-3].strip()
            if not code.strip():
                st.error("❌ AI returned empty or invalid code.")
                st.stop()


        # Execute generated code safely
        output_text = ""
        plot_figure = None
        try:
            local_vars = {"df": df, "plt": plt}
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exec(code, {}, local_vars)

            output_text = stdout.getvalue()
            if plt.get_fignums():
                plot_figure = plt.gcf()
                plt.clf()

        except Exception as e:
            output_text = f"⚠️ Error executing generated code: {e}"

        # Save chat
        st.session_state.chat_history.append({
            "query": query,
            "code": code,
            "output": output_text,
            "plot": plot_figure,
        })

        st.session_state.clear_input = True
        st.rerun()

else:
    st.info("Please upload a CSV file to get started.")
