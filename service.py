from algo import Algo
from middling_letters import MiddlingLetters
from middling_words import MiddlingWords
from utils import Utils
from wordle_game import WordleGame
from words_left_filter import WordsLeftFilter
from words_left_results import WordsLeftResults

def create_words_left_results(guesses: list[str], target: str = None) -> WordsLeftResults:
    game = WordleGame(target, guesses)
    wfilter = WordsLeftFilter(game)
    return WordsLeftResults(wfilter)

def create_middling_letters(guesses: list[str], target: str = None) -> MiddlingLetters:
    words_left_results = create_words_left_results(guesses, target)
    return MiddlingLetters(words_left_results)

def create_middling_words(guesses: list[str], target: str = None) -> MiddlingWords:
    middling_letters = create_middling_letters(guesses, target)
    return MiddlingWords(middling_letters)

def create_algo(guesses: list[str], target: str = None) -> Algo:
    middling_words = create_middling_words(guesses, target)
    return Algo(middling_words)


def get_targets_left_for_api(guesses: list[str], target: str = None) -> list[str]:
    results = create_words_left_results(guesses, target)
    return results.targets_left

def get_middling_letters_for_api(guesses: list[str], target: str = None) -> dict[str, int]:
    middling_letters = create_middling_letters(guesses, target)
    return middling_letters.letters_for_api

def get_middling_words_for_api(guesses: list[str], target: str = None) -> list[str]:
    middling_words = create_middling_words(guesses, target)
    return middling_words.words_for_algo

def get_sorted_algo_results_for_api(guesses: list[str], target: str = None) -> list[tuple[str, int]]:
    algo = create_algo(guesses, target)
    return Utils.sorted_algo_scores(algo.narrowing_scores())

def get_best_guess_for_api(guesses: list[str], target: str = None) -> tuple[str, int]:
    algo = create_algo(guesses, target)
    sorted_algo_results = get_sorted_algo_results_for_api(guesses, target)
    return Utils.pick_best_guess(sorted_algo_results, algo.targets_left)
    
if __name__ == '__main__':
    print(get_targets_left_for_api(['oater', 'shuln'], 'epoxy'))
    # ['biome', 'dodge', 'movie', 'epoxy', 'voice', 'booze', 'diode', 'evoke', 'decoy', 'gecko']
    print(get_middling_letters_for_api(['oater', 'shuln'], 'epoxy'))
    # {'E': 100, 'O': 100, 'I': 40, 'D': 30, 'V': 30, 'C': 30, 'M': 20, 'B': 20, 'DD': 20, 'G': 20, 'Y': 20, 'K': 20, 'X': 10, 'P': 10, 'Z': 10, 'OO': 10, 'EE': 10}
    print(get_middling_words_for_api(['oater', 'shuln'], 'epoxy'))
    # ['evokE', 'gimpy', 'kidDy', 'cebid', 'viced', 'myoid', 'pigmy', 'ovOid', 'bovid', 'deicE', 'micky', 'imbed', 'ogmic', 'midgy', 'boOze', 'combi', 'diveD', 'cideD', 'miked', 'midge', 'dimbo', 'biome', 'midDy', 'dioDe', 'gecko', 'gived', 'diceD', 'epoxy', 'diDDy', 'zymic', 'bedim', 'voice', 'demic', 'gibed', 'picky', 'bideD', 'biked', 'domic', 'doDge', 'dicey', 'medic', 'dikeD', 'dikey', 'bidDy', 'kidDo', 'gidDy', 'movie', 'kidge', 'decoy', 'dicky']
    print(get_sorted_algo_results_for_api(['oater', 'shuln'], 'epoxy'))
    # [('dicky', 1.0), ('biome', 1.1), ('gimpy', 1.2), ('cebid', 1.2), ('viced', 1.2), ('myoid', 1.2), ('bovid', 1.2), ('micky', 1.2), ('midgy', 1.2), ('midge', 1.2), ('gived', 1.2), ('zymic', 1.2), ('bedim', 1.2), ('domic', 1.2), ('dicey', 1.2), ('kidge', 1.2), ('ovoid', 1.3), ('deice', 1.3), ('diode', 1.3), ('kiddy', 1.4), ('pigmy', 1.4), ('combi', 1.4), ('dimbo', 1.4), ('gibed', 1.4), ('picky', 1.4), ('dikey', 1.4), ('biddy', 1.4), ('kiddo', 1.4), ('giddy', 1.4), ('voice', 1.5), ('ogmic', 1.6), ('cided', 1.6), ('miked', 1.6), ('middy', 1.6), ('diced', 1.6), ('demic', 1.6), ('biked', 1.6), ('medic', 1.6), ('evoke', 1.7), ('dived', 1.7), ('dodge', 1.7), ('diked', 1.7), ('movie', 1.7), ('imbed', 1.8), ('diddy', 1.8), ('bided', 1.8), ('booze', 1.9), ('decoy', 2.3), ('epoxy', 2.7), ('gecko', 2.9)]
    print(get_best_guess_for_api(['oater', 'shuln'], 'epoxy'))
    # ('dicky', 1.0)

    print(get_targets_left_for_api(['oater', 'shuln']))
    print(get_middling_letters_for_api(['oater', 'shuln']))
    print(get_middling_words_for_api(['oater', 'shuln']))
    print(get_sorted_algo_results_for_api(['oater', 'shuln']))
    print(get_best_guess_for_api(['oater', 'shuln']))