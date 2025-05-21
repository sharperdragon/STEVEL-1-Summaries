import os
import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


class Suggestion(BaseModel):
    suggestion: str

GITHUB_TOKEN = os.getenv("GH_TOKEN")
REPO = "sharperdragon/STEVEL-1-Summaries"

@app.post("/api/suggest")
def create_suggestion(s: Suggestion):
    url = f"https://api.github.com/repos/{REPO}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "title": "User Suggestion",
        "body": s.suggestion
    }
    r = requests.post(url, json=data, headers=headers)
    return {"status": r.status_code, "detail": r.json()}