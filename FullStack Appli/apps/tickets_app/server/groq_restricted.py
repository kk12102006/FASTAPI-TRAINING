import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set")

client = Groq(api_key=api_key)




app = FastAPI(
    title="Groq FastAPI Test",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """
You are a technical assistant for a web application.

You are ONLY allowed to answer questions related to:

1. React
2. FastAPI
3. MongoDB

You may also answer questions where these technologies are used together,
such as React with FastAPI, FastAPI with MongoDB, CRUD applications,
authentication and JWT, REST APIs, frontend/backend integration, and Docker
deployment of React, FastAPI and MongoDB.

If the question is unrelated to these technologies, respond exactly with:

"I can answer only questions related to React, FastAPI and MongoDB."

Keep answers clear and suitable for a beginner.
"""


class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    response: str
    model: str


@app.get("/")
def root():
    return {
        "message": "Groq FastAPI server is running",
        "model": model,
    }


@app.post("/chat", response_model=PromptResponse)
def chat(request: PromptRequest):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": request.prompt,
                },
            ],
        )

        return PromptResponse(
            response=completion.choices[0].message.content,
            model=model,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Groq API error: {str(e)}",
        )