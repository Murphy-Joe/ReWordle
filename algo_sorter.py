from algo import Algo


class AlgoSorter:
    def __init__(self, algo_results: Algo):
        self.algo = algo_results
        self.targets_left = algo_results.targets_left
        self.sorted_algo_results: list[tuple[str, int]] = self.sorted_algo_scores()
        self.best_guess: tuple[str, int] = self.pick_best_guess()

    def sorted_algo_scores(self) -> list[tuple[str, int]]:
        return sorted(self.algo.algo_scores, key=lambda tup: tup[1])

    def pick_best_guess(self) -> tuple[str, int]:
        best_score = self.sorted_algo_results[0][1]
        top_item_or_items = [word_score for word_score in self.sorted_algo_results if word_score[1] == best_score]

        if len(top_item_or_items) == 1:
            return top_item_or_items[0]
        elif not any(word in self.targets_left for word in top_item_or_items):
            return top_item_or_items[0]
        else:
            top_targets = [
                word for word in top_item_or_items if word in self.targets_left]
            return top_targets[0]

if __name__ == '__main__':
    from middling_letters import MiddlingLetters
    from middling_words import MiddlingWords
    from wordle_game import WordleGame
    from words_left_filter import WordsLeftFilter
    from words_left_results import WordsLeftResults

    wgame = WordleGame('epoxy', ['oater', 'shuln'])
    wfilter = WordsLeftFilter(wgame)
    results = WordsLeftResults(wfilter)
    middling_letters = MiddlingLetters(results)
    middling_words = MiddlingWords(middling_letters)
    algo = Algo(middling_words)
    algo_sorter = AlgoSorter(algo)
    print(algo_sorter.sorted_algo_results) 
    #[('dicky', 1.0), ('biome', 1.1), ('midge', 1.2), ('gimpy', 1.2), ('gived', 1.2), ('bedim', 1.2), ('domic', 1.2), ('cebid', 1.2), ('viced', 1.2), ('micky', 1.2), ('kidge', 1.2), ('dicey', 1.2), ('midgy', 1.2), ('myoid', 1.2), ('zymic', 1.2), ('bovid', 1.2), ('diode', 1.3), ('deice', 1.3), ('ovoid', 1.3), ('picky', 1.4), ('kiddy', 1.4), ('dimbo', 1.4), ('gibed', 1.4), ('biddy', 1.4), ('kiddo', 1.4), ('combi', 1.4), ('dikey', 1.4), ('pigmy', 1.4), ('giddy', 1.4), ('voice', 1.5), ('medic', 1.6), ('middy', 1.6), ('ogmic', 1.6), ('biked', 1.6), ('demic', 1.6), ('cided', 1.6), ('diced', 1.6), ('miked', 1.6), ('diked', 1.7), ('dodge', 1.7), ('movie', 1.7), ('dived', 1.7), ('evoke', 1.7), ('imbed', 1.8), ('bided', 1.8), ('diddy', 1.8), ('booze', 1.9), ('decoy', 2.3), ('epoxy', 2.7), ('gecko', 2.9)]
    print(algo_sorter.best_guess)
    #('dicky', 1.0)
