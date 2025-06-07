# AI-Powered Data Analyst Documentation
## Project Overview
This project provides an AI-powered data analysis tool using Streamlit, pandas, matplotlib, and Google's Gemini AI model. Users can upload a CSV file and ask questions about their data in natural language. The application generates Python code to answer the questions, executes the code, and displays the results, including any generated plots.
**Key Features:**
*   **CSV Upload:** Allows users to upload CSV files for analysis.
*   **Data Preview:** Displays a preview of the uploaded data.
*   **Natural Language Querying:** Enables users to ask questions about the data in natural language.
*   **AI-Powered Code Generation:** Uses the Gemini AI model to generate Python code to answer user queries.
*   **Code Execution:** Executes the generated code and captures the output.
*   **Result Display:** Displays the output of the code execution, including text and plots.
*   **Chat History:** Maintains a history of user queries and AI responses.
  
**Requirements:**
*   Python 3.6+
*   Streamlit
*   pandas
*   matplotlib
*   google-generativeai
*   python-dotenv
*   A Google Gemini API key
## Getting Started
### Installation
1.  **Clone the repository** 
2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```
    
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    
4.  **Set up environment variables:**
    *   Create a `.env` file in the project directory.
    *   Add your Google Gemini API key to the `.env` file:
               
        ```
        GEMINI_API_KEY=YOUR_GEMINI_API_KEY
        ```
        Replace `YOUR_GEMINI_API_KEY` with your actual API key.
### Running the Application
1.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    
2.  **Access the application:** Open your web browser and navigate to the URL displayed in the terminal (usually `http://localhost:8501`).
## Code Structure
The project consists of the following files:
*   `.gitignore`: Specifies intentionally untracked files that Git should ignore.
*   `app.py`: The main Streamlit application file.
*   `requirements.txt`: Lists the Python packages required to run the application.
### Key Components in `app.py`:
*   **Import Statements:** Imports necessary libraries, including `os`, `io`, `contextlib`, `streamlit`, `pandas`, `matplotlib`, `dotenv`, and `google.generativeai`.
*   **Environment Variable Loading:** Loads the Gemini API key from the `.env` file using `load_dotenv()`.
*   **Gemini Model Initialization:** Initializes the Gemini model using `genai.GenerativeModel()`.
*   **Streamlit UI:** Creates the user interface using Streamlit components, including file uploader, data preview, chat history, and input box.
*   **Prompt Generation:** Constructs a prompt for the Gemini model based on the user's query and the data.
*   **Code Execution:** Executes the generated Python code using `exec()` and captures the output.
*   **Result Display:** Displays the output of the code execution, including text and plots.
*   **Session State Management:** Uses Streamlit's session state to maintain chat history and clear input.
## FAQ
**Q: I am getting an error when running the application.**

A: Ensure that you have installed all the required dependencies using `pip install -r requirements.txt` and that your Gemini API key is correctly set in the `.env` file. Also, check the error message in the terminal for more specific information.

**Q: The AI is returning empty or invalid code.**

A: This can happen if the user query is too complex or ambiguous. Try rephrasing the query or providing more context.

**Q: The generated code is throwing an error.**

A: The AI-generated code may not always be perfect. Review the code and try to identify and fix any errors. The error message displayed in the application can help you debug the code.

**Q: How do I clear the chat history?**

A: The current implementation does not have a dedicated button to clear the chat history. You can clear the chat history by restarting the Streamlit application.
