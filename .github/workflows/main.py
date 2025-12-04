
from fastapi import FastAPI
import openai

app = FastAPI()

@app.get("/")
def home():
    return {"message": "PolicyPal API is running"}

@app.post("/ask")
def ask_compliance(question: str):
    openai.api_key = "9dea955c3ebb9aa71040ca135a4b732e"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}]
    )
    return {"answer": response.choices[0].message.content}
