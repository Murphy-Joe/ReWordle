from utils import Utils
from middling_letters import MiddlingLetters

class MiddlingWords:
    def __init__(self, middling_letters: MiddlingLetters):
        self.middling_letters = middling_letters
        self.targets_left = middling_letters.targets_left
        self.letters_for_algo = middling_letters.letters_for_algo
        self.words_for_algo = self.words_for_brute_force()

    def words_sorted_by_middleness_w_upper(self, available_words: list[str]) -> list[tuple[str, int]]:
        available_words = [Utils.make_second_appearance_of_letter_uppercase(word) for word in available_words]
        word_scores = {}
        for word in available_words:
            word_scores.setdefault(word, 0)
            for ltr in word:
                try:
                    word_scores[word] += self.letters_for_algo[ltr]
                except KeyError:  # ltr not in any self.targets_left
                    word_scores[word] += len(self.targets_left)

        return sorted(word_scores.items(), key=lambda w_s: w_s[1])

    def words_for_brute_force(self) -> list[str]:
        playable_guesses_w_upper = self.words_sorted_by_middleness_w_upper(Utils.all_playables())
        guesses_w_upper_from_targets = self.words_sorted_by_middleness_w_upper(self.targets_left)

        best_playable_guesses_w_upper = [tup[0] for tup in playable_guesses_w_upper[:40]]
        best_guesses_w_upper_from_targets = [tup[0] for tup in guesses_w_upper_from_targets[:10]]

        return list(set(best_playable_guesses_w_upper + best_guesses_w_upper_from_targets))

if __name__ == '__main__':
    from wordle_game import WordleGame
    from words_left_filter import WordsLeftFilter
    from words_left_results import WordsLeftResults

    game = WordleGame('epoxy', ['oater', 'shuln'])
    filter = WordsLeftFilter(game)
    results = WordsLeftResults(filter)
    print(results.targets_left)
    middling_letters = MiddlingLetters(results)
    print(middling_letters.letters_for_algo)
    middling_words = MiddlingWords(middling_letters)
    print(middling_words.words_for_algo)

    