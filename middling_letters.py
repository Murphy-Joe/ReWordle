from utils import Utils
from words_left_results import WordsLeftResults

class MiddlingLetters:
    def __init__(self, filter_results: WordsLeftResults):
        self.filter_results = filter_results
        self.targets_left = filter_results.targets_left
        self.letters_for_algo = self.letters_sorted_by_middleness_for_algo()
        self.letters_for_api = self.letters_sorted_by_middleness_for_api()

    def letter_frequency(self) -> dict[str, int]:
        freq_results = {}
        target_list = [Utils.make_second_appearance_of_letter_uppercase(word) for word in self.targets_left]
        for word in target_list:
            for ltr in set(word):
                freq_results.setdefault(ltr, 0)
                freq_results[ltr] += 1
        return freq_results

    def letters_sorted_by_middleness_for_algo(self) -> dict[str, int]:
        freq_results: dict[str, int] = self.letter_frequency()

        for ltr, freq in freq_results.items():
            freq_results[ltr] = abs(freq - len(self.targets_left)/2)

        return dict(sorted(freq_results.items(), key=lambda ltr_frq: ltr_frq[1]))

    def letters_sorted_by_middleness_for_api(self) -> dict[str, int]:
        freq_results = self.letter_frequency()

        for ltr, freq in freq_results.items():
            freq_results[ltr] = round(freq/len(self.targets_left)*100)

        return dict(sorted(freq_results.items(), key=lambda ltr_frq: ltr_frq[1], reverse=True))

if __name__ == '__main__':
    from wordle_game import WordleGame
    from words_left_filter import WordsLeftFilter

    game = WordleGame('epoxy', ['oater', 'shuln'])
    filter = WordsLeftFilter(game)
    results = WordsLeftResults(filter)
    print(results.targets_left)
    middling_letters = MiddlingLetters(results)
    print(middling_letters.letters_for_algo)
    print(middling_letters.letters_for_api)
    