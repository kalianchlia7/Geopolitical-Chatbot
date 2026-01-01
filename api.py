from fastapi import FastAPI
from pydantic import BaseModel
from main import safety_filter, generate_response  
from prompt_templates import SYSTEM_PROMPT

app = FastAPI(title="Geopolitical Policy Chatbot API")

# Allow CORS so the browser can connect
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # use ["*"] for testing
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request format
class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_api(query: Query):
    user_input = query.question

    # Safety layer
    safety = safety_filter(user_input)
    if safety.get("blocked"):
        return {"answer": safety["response"], "blocked": True}

    system_prompt = SYSTEM_PROMPT
    if "prepend" in safety:
        system_prompt = safety["prepend"] + SYSTEM_PROMPT

    answer = generate_response(user_input, system_prompt)

    full_answer = (answer +
        "\n\n"
        "📌 NOTE:\n" 
        "Instructions for querying sanctions datasets:\n"
        "- Specify the Dataset (OFAC sanctions CSV or WTO trade CSV).\n"
        "- Include the Country/Entity you are interested in.\n"
        "- Include the Year if applicable.\n\n"
        "⚠️ Disclaimers & warnings:\n"
        "- I cannot provide instructions for illegal activity, sanctions evasion, "
        "money laundering, hacking, or bioweapons.\n"
        "- Responses about sensitive geopolitical topics are for educational purposes only.\n\n"
    )



    return {"answer": full_answer, "blocked": False}

# The API could be called from anywhere: a web app, a mobile app, or even malicious scripts.
# You cannot trust external input, so you reapply the safety filter before generating a response.

