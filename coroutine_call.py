import asyncio
import time
import aiohttp

import service
from utils import Utils
from main import PostBody

async def runner(post_body: PostBody) -> list[tuple[str, int]]:
    async with aiohttp.ClientSession("https://v6xqpk.deta.dev") as session:
        guesses_to_run = service.get_middling_words_for_api(post_body.guesses, post_body.target)
        
        tasks = []
        for next_guess in guesses_to_run:
            task = asyncio.create_task(guess_score(post_body.guesses, session, next_guess))
            tasks.append(task)
        algo_results = await asyncio.gather(*tasks, return_exceptions=True)

        algo_results = Utils.sorted_algo_scores(algo_results)
        best_guess = Utils.pick_best_guess(algo_results, service.get_targets_left_for_api(post_body.guesses, post_body.target))
        algo_results.remove(best_guess)
        algo_results.insert(0, best_guess)
        return algo_results

async def guess_score(guess_list, session, next_guess):
    payload = {"guesses": guess_list, "next_guess": next_guess}
    async with session.post('/game', json=payload) as game_post:
        return await game_post.json()

if __name__ == "__main__":
    p_body = PostBody(
        guesses = ["oater", "shuln"],
        target = "epoxy"
    ) 

    start_time = time.time()
    results = asyncio.run(runner(p_body))
    duration = time.time() - start_time
    # avgNarrowingScore = sum([r["narrowing_scores"] for r in results]) / len(results)
    # print(f"\nheavy narrowing score loop took {avgNarrowingScore} seconds")
    print(results)

    print(f"\nCalled in {duration} seconds")