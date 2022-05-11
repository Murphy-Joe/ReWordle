from middling_words import MiddlingWords
from wordle_game import WordleGame
from words_left_filter import WordsLeftFilter
from words_left_results import WordsLeftResults

class Algo:
    def __init__(self, middling_words: MiddlingWords):
        self.words_for_algo = middling_words.words_for_algo
        self.targets_left = middling_words.targets_left
        self.game = middling_words.middling_letters.filter_results.words_left_filter.game

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
    # print(results.targets_left)
    middling_letters = MiddlingLetters(results)
    # print(middling_letters.letters_for_algo)
    middling_words = MiddlingWords(middling_letters)
    # print(middling_words.words_for_algo)
    algo = Algo(middling_words)
    print(algo.narrowing_scores())
