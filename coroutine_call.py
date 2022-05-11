import asyncio
import time
import aiohttp

import service

async def runner(guess_list: list[str]) -> list[tuple[str, int]]:
    async with aiohttp.ClientSession("https://1vv6d7.deta.dev") as session:
        guesses_to_run = service.get_middling_words_for_api(guess_list)
        
        tasks = []
        for next_guess in guesses_to_run:
            task = asyncio.create_task(guess_score(guess_list, session, next_guess))
            tasks.append(task)
        res = await asyncio.gather(*tasks, return_exceptions=True)

        res.sort(key=lambda tup: tup[1])
        best_guess = choose_best_guess(res, words_left)
        res.remove(best_guess)
        res.insert(0, best_guess)

        return res

async def guess_score(guess_list, session, next_guess):
    payload = {"guesses": guess_list, "next_guess": next_guess}
    async with session.post('/game', json=payload) as game_post:
        return await game_post.json()