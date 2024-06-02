# app/server.py
from decouple import config
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes


app = FastAPI()

# -------------- CORS MIDDLWARE START ----------------
# CORS middleware configuration
origins = [
    "http://localhost:4001",  # Add your frontend URL here
    "http://127.0.0.1:4001",
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

# ------------- MOOSE ROUTE STARTS ----------------    
moose_model = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"), streaming=True, temperature=0.7)
moose_prompt = ChatPromptTemplate.from_template("{input}")

add_routes(
    app,
    moose_prompt | moose_model,
    path="/chat",
    playground_type="default",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
)
# ------------- MOOSE ROUTE ENDS ----------------                

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)