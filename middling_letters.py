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

        sorted_freq_results = dict(sorted(freq_results.items(), key=lambda ltr_frq: ltr_frq[1], reverse=True))
        return Utils.convert_uppercase_to_double_letter(sorted_freq_results)

if __name__ == '__main__':
    from wordle_game import WordleGame
    from words_left_filter import WordsLeftFilter

    game = WordleGame('epoxy', ['oater', 'shuln'])
    filter = WordsLeftFilter(game)
    results = WordsLeftResults(filter)
    print(results.targets_left)
    middling_letters = MiddlingLetters(results)
    print(middling_letters.letters_for_algo)
    #{'i': 1.0, 'd': 2.0, 'v': 2.0, 'c': 2.0, 'm': 3.0, 'b': 3.0, 'D': 3.0, 'g': 3.0, 'y': 3.0, 'k': 3.0, 'p': 4.0, 'x': 4.0, 'O': 4.0, 'z': 4.0, 'E': 4.0, 'e': 5.0, 'o': 5.0}
    print(middling_letters.letters_for_api)
    #{'E': 100, 'O': 100, 'I': 40, 'D': 30, 'V': 30, 'C': 30, 'B': 20, 'M': 20, 'DD': 20, 'G': 20, 'Y': 20, 'K': 20, 'P': 10, 'X': 10, 'OO': 10, 'Z': 10, 'EE': 10}
    