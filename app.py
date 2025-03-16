import os
import certifi  # Import certifi
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set SSL certificate file path using certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

#####################################################################
## debugging tracking Section for streamlit

import os
from langsmith import Client

# Set environment variables for langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")   # Use a valid API key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot with OPENAI"

# Initialize LangSmith Client
client = Client()

# Debugging: Check if the project exists
print("Existing LangSmith Projects:", client.list_projects())

print("LangChain API Key:", os.getenv("LANGCHAIN_API_KEY"))
print("LangSmith Project:", os.getenv("LANGCHAIN_PROJECT"))



#####################################################################

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY") # LangSmith API key
os.environ["LANGCHAIN_TRACKING_V2"] = "true"  # Enable tracking
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot with OPENAI"  # Project name in LangSmith

# Prompt template for LLM
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a highly knowledgeable AI assistant. Provide long, detailed, and well-structured responses to user queries."),
    ("user", "{question}")
])

def generate_response(question, api_key, llm, temperature, max_tokens):
    """
    Generates a response from an OpenAI language model based on the input question.
    """
    # Initialize the OpenAI chat model
    llm = ChatOpenAI(model=llm, api_key=api_key, temperature=temperature, max_tokens=max_tokens)

    # Format the response for human readability
    output_parser = StrOutputParser()

    # Define a processing chain using the prompt, LLM, and output parser
    chain = prompt | llm | output_parser

    # Invoke the chain with the user's question
    answer = chain.invoke({"question": question})

    return answer

#### Streamlit Application Design ####

# App title
st.title("Enhanced Q&A Chatbot with OpenAI")

#side bar name 
st.sidebar.title("Settings")

#side bar box 
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

#side bar drop down select 
engine = st.sidebar.selectbox("Select an OpenAI Model", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"])

#side bar slider selects
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=600, value=150)

# Main Interface for user input
st.write("Go ahead and ask any question")
user_input = st.text_input("You:")

if user_input and api_key:
    response = generate_response(user_input, api_key, engine, temperature, max_tokens)
    st.write(response)
elif user_input:
    st.warning("Please enter the OpenAI API Key in the sidebar")
else:
    st.write("Please provide the user input")