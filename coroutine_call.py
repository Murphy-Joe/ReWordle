import aiohttp
import asyncio

import service
from utils import Utils

class PostBody():
    def __init__(self, guesses = None, target = None, next_guess = None):
        self.guesses: list[str] = guesses
        self.next_guess: str = next_guess
        self.target: str = target

async def runner(post_body: PostBody) -> list[tuple[str, int]]:
    async with aiohttp.ClientSession("https://v6xqpk.deta.dev") as session:
        guesses_to_run = service.get_middling_words_for_api(post_body.guesses, post_body.target)
        
        tasks = []
        for next_guess in guesses_to_run:
            task = asyncio.create_task(guess_score(post_body, session, next_guess.lower()))
            tasks.append(task)
        algo_results = await asyncio.gather(*tasks, return_exceptions=True)

        return sorted_algo_results(post_body, algo_results)

def sorted_algo_results(post_body, algo_results):
    algo_results = Utils.sorted_algo_scores(algo_results)
    targets_left = service.get_targets_left_for_api(post_body.guesses, post_body.target)
    best_guess = Utils.pick_best_guess(algo_results, targets_left)
    algo_results.remove(best_guess)
    algo_results.insert(0, best_guess)
    return algo_results

async def guess_score(post_body: PostBody, session, next_guess):
    payload = {"guesses": post_body.guesses, "next_guess": next_guess, "target": post_body.target}
    async with session.post('/game', json=payload) as game_post:
        return await game_post.json()

if __name__ == "__main__":
    
    import time

    p_body = PostBody(
        guesses = ["oater", "clons", "biome"],
        target = "epoxy")
    start_time = time.time()
    results = asyncio.run(runner(p_body))
    duration = time.time() - start_time
    print(results)

    print(f"\nCalled in {duration} seconds")