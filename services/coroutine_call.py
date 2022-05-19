import aiohttp
import asyncio

if __name__ == '__main__':
    import os, sys
    currentdir = os.path.dirname(os.path.realpath(__file__))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

from services import service
from helper.utils import Utils

class PostBody():
    def __init__(self, guesses = None, target = None, next_guess = None):
        self.guesses: list[str] = guesses
        self.next_guess: str = next_guess
        self.target: str = target

async def runner(post_body: PostBody) -> list[tuple[str, int]]:
    async with aiohttp.ClientSession("https://1vv6d7.deta.dev") as session:
        guesses_to_run = service.get_middling_words_for_api(post_body.guesses, post_body.target)
        
        tasks = []
        for next_guess in guesses_to_run:
            task = asyncio.create_task(guess_score(post_body, session, next_guess.lower()))
            tasks.append(task)
        algo_results = await asyncio.gather(*tasks, return_exceptions=True)
        return packaged_algo_results(post_body, algo_results)

async def guess_score(post_body: PostBody, session, next_guess):
    payload = {"guesses": post_body.guesses, "next_guess": next_guess, "target": post_body.target}
    async with session.post('/singleguess', json=payload) as game_post:
        return await game_post.json()

def packaged_algo_results(post_body, algo_results):
    algo_results = Utils.sorted_algo_scores(algo_results)
    words_left_results_obj = service.create_words_left_results(post_body.guesses, post_body.target)
    best_guess = Utils.pick_best_guess(algo_results, words_left_results_obj.targets_left)
    algo_results.remove(best_guess)
    algo_results.insert(0, best_guess)

    hard_mode = [[result[0].upper(), result[1]] for result in algo_results if result[0] in words_left_results_obj.hard_mode_guesses_left]
    target_scores = [[result[0].upper(), result[1]] for result in algo_results if result[0] in words_left_results_obj.targets_left]
    return {
            "regular_mode": algo_results,
            "hard_mode": hard_mode,
            "target_scores": target_scores
        }

if __name__ == "__main__":
    
    import time

    p_body = PostBody(
        guesses = ["crane"],
        target = "epoxy")
    start_time = time.time()
    results = asyncio.run(runner(p_body))
    duration = time.time() - start_time
    print(results)

    print(f"\nCalled in {duration} seconds")