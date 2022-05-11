import asyncio
import time
import aiohttp

import service
from utils import Utils

async def runner(guess_list: list[str]) -> list[tuple[str, int]]:
    async with aiohttp.ClientSession("http://0.0.0.0:8000") as session:
        guesses_to_run = service.get_middling_words_for_api(guess_list)
        
        tasks = []
        for next_guess in guesses_to_run:
            task = asyncio.create_task(guess_score(guess_list, session, next_guess))
            tasks.append(task)
        res = await asyncio.gather(*tasks, return_exceptions=True)

        res = Utils.sorted_algo_scores(res)
        best_guess = Utils.pick_best_guess(res, service.get_targets_left_for_api(guess_list))
        res.remove(best_guess)
        res.insert(0, best_guess)
        return res

async def guess_score(guess_list, session, next_guess):
    payload = {"guesses": guess_list, "next_guess": next_guess}
    async with session.post('/game', json=payload) as game_post:
        return await game_post.json()

if __name__ == "__main__":
    guesses = ["basks"]

    start_time = time.time()
    results = asyncio.run(runner(guesses))
    duration = time.time() - start_time
    # avgNarrowingScore = sum([r["narrowing_scores"] for r in results]) / len(results)
    # print(f"\nheavy narrowing score loop took {avgNarrowingScore} seconds")
    print(results)

    print(f"\nCalled in {duration} seconds")