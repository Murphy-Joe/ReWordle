from middling_words import MiddlingWords
from wordle_game import WordleGame
from words_left_filter import WordsLeftFilter
from words_left_results import WordsLeftResults

class Algo:
    def __init__(self, middling_words: MiddlingWords):
        self.middling_words = middling_words
        self.words_for_algo = middling_words.words_for_algo
        self.targets_left = middling_words.targets_left
        self.game = middling_words.middling_letters.filter_results.words_left_filter.game
        self.algo_scores = self.narrowing_scores()

    def play_fake_guess(self, target: str, guess: str) -> int:
        new_game = WordleGame(target)
        new_filter = WordsLeftFilter(new_game)
        new_filter.add_guess(guess)
        new_results = WordsLeftResults(new_filter)
        return len(new_results.targets_that_pass_filter(self.targets_left))

    def narrowing_score_per_guess(self, guess_word: str) -> tuple[str, int]:
        guess_word = guess_word.lower()
        score = 0
        # start_time = time.time()
        for tgt in self.targets_left:
            if guess_word == tgt:
                continue
            else:
                score += self.play_fake_guess(tgt, guess_word)
        # end_time = time.time()
        # print(guess_word, end_time - start_time)
        return (guess_word, score/len(self.targets_left))

    def narrowing_scores(self) -> list[tuple[str, int]]:
        collect_guess_scores = []
        self.words_for_algo = [word.lower() for word in self.words_for_algo]
        for guess in self.words_for_algo:
            guess_score = self.narrowing_score_per_guess(guess)
            collect_guess_scores.append(guess_score)
        return collect_guess_scores

if __name__ == '__main__':
    from middling_letters import MiddlingLetters

    wgame = WordleGame('epoxy', ['oater', 'shuln'])
    wfilter = WordsLeftFilter(wgame)
    results = WordsLeftResults(wfilter)
    middling_letters = MiddlingLetters(results)
    middling_words = MiddlingWords(middling_letters)
    algo = Algo(middling_words)
    print(algo.narrowing_scores())
    #[('demic', 1.6), ('voice', 1.5), ('biome', 1.1), ('domic', 1.2), ('medic', 1.6), ('myoid', 1.2), ('biked', 1.6), ('bovid', 1.2), ('picky', 1.4), ('kidge', 1.2), ('diode', 1.3), ('micky', 1.2), ('gimpy', 1.2), ('gecko', 2.9), ('dimbo', 1.4), ('combi', 1.4), ('evoke', 1.7), ('deice', 1.3), ('giddy', 1.4), ('ovoid', 1.3), ('pigmy', 1.4), ('kiddy', 1.4), ('dicey', 1.2), ('miked', 1.6), ('diddy', 1.8), ('middy', 1.6), ('dikey', 1.4), ('gibed', 1.4), ('bedim', 1.2), ('cided', 1.6), ('dived', 1.7), ('epoxy', 2.7), ('ogmic', 1.6), ('cebid', 1.2), ('diced', 1.6), ('movie', 1.7), ('dicky', 1.0), ('biddy', 1.4), ('midge', 1.2), ('diked', 1.7), ('gived', 1.2), ('kiddo', 1.4), ('dodge', 1.7), ('imbed', 1.8), ('midgy', 1.2), ('zymic', 1.2), ('bided', 1.8), ('booze', 1.9), ('viced', 1.2), ('decoy', 2.3)]
