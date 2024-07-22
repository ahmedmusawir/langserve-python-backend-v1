# app/server.py
from decouple import config
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()


app = FastAPI()

# -------------- CORS MIDDLWARE START ----------------
# CORS middleware configuration
origins = [
    "http://localhost:4001",  # Add your frontend URL here
    "http://127.0.0.1:4001",
    "http://localhost:8501"
    "http://127.0.0.1:8501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------- DEFAULT ROUTE START ----------------                

model = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"))
prompt = ChatPromptTemplate.from_template("Give me a summary about {topic} in a paragraph or less.")

chain = prompt | model

add_routes(app, chain, path="/openai")

# ------------- DEFAULT ROUTE ENDS ----------------                

# ------------- MOOSE ROUTE OPENAI STARTS ----------------    
moose_model = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"), streaming=True, temperature=0.7)
moose_prompt = ChatPromptTemplate.from_template("{input}")
print('Moose Prompt', moose_prompt)

add_routes(
    app,
    moose_prompt | moose_model,
    path="/chat",
    playground_type="default",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
)

print('INPUT', input)
# ------------- MOOSE ROUTE OPENAI ENDS ---------------- 

# ------------- MOOSE ROUTE CLAUDE STARTS ----------------    
claude_model = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    api_key=os.getenv("ANTHROPIC_API_KEY"),  # Pass the API key here
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
    # other params...
)
moose_prompt = ChatPromptTemplate.from_template("{input}")
print('Moose Prompt', moose_prompt)

add_routes(
    app,
    moose_prompt | claude_model,
    path="/claude",
    playground_type="default",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
)

print('INPUT', input)
# ------------- MOOSE ROUTE CLAUDE ENDS ---------------- 

# ------------- MOOSE ROUTE GOOGLE STARTS ----------------    

google_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    api_key=os.getenv("GOOGLE_API_KEY"),  # Pass the API key here
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
    # other params...
)
google_prompt = ChatPromptTemplate.from_template("{input}")
print('Google Prompt', google_prompt)

add_routes(
    app,
    google_prompt | google_model,
    path="/gemini",
    playground_type="default",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
)

# ------------- MOOSE ROUTE GOOGLE ENDS ----------------

# ------------- MOOSE ROUTE GROQ STARTS ----------------    

groq_model = ChatGroq(
    model="llama3-70b-8192",
    api_key=os.getenv("GROQ_API_KEY"),  # Pass the API key here
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
    # other params...
)
groq_prompt = ChatPromptTemplate.from_template("{input}")
print('Groq Prompt', groq_prompt)

add_routes(
    app,
    groq_prompt | groq_model,
    path="/groq",
    playground_type="default",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
)

# ------------- MOOSE ROUTE GROQ ENDS ----------------


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)