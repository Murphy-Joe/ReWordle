from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# pylint: disable=no-name-in-module
from pydantic import BaseModel

import service
from utils import Utils
import coroutine_call

app = FastAPI()
origins = [
    "https://www.nytimes.com",
    "chrome-extension://*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class PostBody(BaseModel):
    guesses: list[str]
    next_guess: Optional[str]
    target: Optional[str]

class TargetsLeftResponse(BaseModel):
    count: int
    targets: list[str]

@app.post("/targetsleft", response_model=TargetsLeftResponse)
async def _(body: PostBody) -> list[str]:
    targets_left = service.get_targets_left_for_api(body.guesses, body.target)
    return TargetsLeftResponse(count=len(targets_left), targets=targets_left[:30])

@app.post("/bestletters")
async def _(body: PostBody):
    return service.get_middling_letters_for_api(body.guesses, body.target)

@app.post("/game")
async def _(body: PostBody):
    algo = service.create_algo(body.guesses, body.target)
    return algo.narrowing_score_per_guess(body.next_guess)

@app.post("/onecall")
async def _(body: PostBody):
    words_left = service.get_targets_left_for_api(body.guesses, body.target)
    if not body.guesses or len(words_left) > 500:
        return Utils.get_starting_words()
    return await coroutine_call.runner(body)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

    # uvicorn main:app --reload