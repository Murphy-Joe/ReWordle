import json

class Utils:

    @staticmethod
    def all_targets():
        with open('data/targets.json', 'r') as targets_json:
            targets = json.load(targets_json)
        return sorted(targets)

    @staticmethod
    def all_playables():
        with open('data/playable_words.json', 'r') as playables_json:
            return json.load(playables_json)

    @staticmethod
    def get_starting_words(cnt):
        with open('data/starting_words.json', 'r') as starters_json:
            starting_words = json.load(starters_json)
        starting_words_from_targets = [tup for tup in starting_words if tup[0] in Utils.all_targets()]
        starting_words_from_targets = [[word[0].upper(), word[1:]] for word in starting_words_from_targets]
        starting_words = [[word[0].upper(), word[1:]] for word in starting_words]
        return {
            "regular_mode": starting_words[:cnt],
            "hard_mode": starting_words[:cnt],
            "target_scores": starting_words_from_targets[:cnt]
        }
    
    @staticmethod
    def make_second_appearance_of_letter_uppercase(word: str) -> str:
        if len(word) == len(set(word)):
            return word
        word_builder = ''
        for ltr in word:
            if ltr not in word_builder:
                word_builder += ltr
            else:
                word_builder += ltr.upper()
        return word_builder

    @staticmethod
    def convert_uppercase_to_second_letter(results: dict[str, int]) -> dict[str, int]:
        formattedDict = {}
        for k in results.keys():
            if k.isupper():
                newKey = f"2nd-{k}"
                formattedDict[newKey] = results[k]
            else:
                formattedDict[k.upper()] = results[k]
        return formattedDict

    @staticmethod
    def sorted_algo_scores(results: list[tuple[str, int]]) -> list[tuple[str, int]]:
        return sorted(results, key=lambda tup: tup[1])

    @staticmethod
    def pick_best_guess(sorted_results: list[tuple[str, int]], targets_left) -> tuple[str, int]:
        best_score = sorted_results[0][1]
        top_item_or_items = [word_score for word_score in sorted_results if word_score[1] == best_score]

        if len(top_item_or_items) == 1:
            return top_item_or_items[0]
        elif not any(word in targets_left for word in top_item_or_items):
            return top_item_or_items[0]
        else:
            top_targets = [word for word in top_item_or_items if word in targets_left]
            return top_targets[0]

if __name__ == '__main__':
    import os, sys
    currentdir = os.path.dirname(os.path.realpath(__file__))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

    from middling.middling_letters import MiddlingLetters
    from middling.middling_words import MiddlingWords
    from game.wordle_game import WordleGame
    from words_left.words_left_filter import WordsLeftFilter
    from words_left.words_left_results import WordsLeftResults
    from algorithm.algo import Algo

    wgame = WordleGame('epoxy', ['oater', 'shuln'])
    wfilter = WordsLeftFilter(wgame)
    filter_results = WordsLeftResults(wfilter)
    middling_letters = MiddlingLetters(filter_results)
    middling_words = MiddlingWords(middling_letters)
    algo = Algo(middling_words)
    algo_results = algo.narrowing_scores()
    sorted_algo_results = Utils.sorted_algo_scores(algo_results)
    print(sorted_algo_results)
    #[('dicky', 1.0), ('biome', 1.1), ('midge', 1.2), ('gimpy', 1.2), ('gived', 1.2), ('bedim', 1.2), ('domic', 1.2), ('cebid', 1.2), ('viced', 1.2), ('micky', 1.2), ('kidge', 1.2), ('dicey', 1.2), ('midgy', 1.2), ('myoid', 1.2), ('zymic', 1.2), ('bovid', 1.2), ('diode', 1.3), ('deice', 1.3), ('ovoid', 1.3), ('picky', 1.4), ('kiddy', 1.4), ('dimbo', 1.4), ('gibed', 1.4), ('biddy', 1.4), ('kiddo', 1.4), ('combi', 1.4), ('dikey', 1.4), ('pigmy', 1.4), ('giddy', 1.4), ('voice', 1.5), ('medic', 1.6), ('middy', 1.6), ('ogmic', 1.6), ('biked', 1.6), ('demic', 1.6), ('cided', 1.6), ('diced', 1.6), ('miked', 1.6), ('diked', 1.7), ('dodge', 1.7), ('movie', 1.7), ('dived', 1.7), ('evoke', 1.7), ('imbed', 1.8), ('bided', 1.8), ('diddy', 1.8), ('booze', 1.9), ('decoy', 2.3), ('epoxy', 2.7), ('gecko', 2.9)]
    print(Utils.pick_best_guess(sorted_algo_results, algo.targets_left))
    #('dicky', 1.0)
