if __name__ == '__main__':
    import os, sys
    currentdir = os.path.dirname(os.path.realpath(__file__))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

from helper.utils import Utils
from words_left.words_left_filter import WordsLeftFilter

class WordsLeftResults:
    def __init__(self, words_left_filter: WordsLeftFilter):
        self.words_left_filter = words_left_filter
        self.indexed_letters = self.words_left_filter.indexed_letters
        self.included_letters = self.words_left_filter.included_letters
        self.excluded_letters = self.words_left_filter.excluded_letters
        self.index_excludes_letters = self.words_left_filter.index_excludes_letters
        self.targets_left = self.targets_that_pass_filter()
        self.hard_mode_guesses_left = self.targets_that_pass_filter(hard_mode = True)

    def fails_indexed_letters(self, target: str) -> bool:
        for idx, letter in self.indexed_letters.items():
            if target[idx] != letter:
                return True


    def fails_included_letters(self, target: str) -> bool:
        target_w_uppers = Utils.make_second_appearance_of_letter_uppercase(target)
        for letter in self.included_letters: 
            if letter not in target_w_uppers:
                return True

    def fails_excluded_letters(self, target: str) -> bool:
        for letter in self.excluded_letters:
            if letter in target:
                return True

    def fails_index_excludes_letters(self, target: str) -> bool:
        for idx, failing_letters in self.index_excludes_letters.items():
            if target[idx] in failing_letters:
                return True

    def targets_that_pass_filter(self, targets: list[str] = None, hard_mode = False) -> list[str]:
        possible_answers = []
        if targets is None:
            targets = Utils.all_targets()
        if hard_mode:
            targets = Utils.all_playables()
        for target in targets:
            if self.indexed_letters and self.fails_indexed_letters(target):
                continue

            if self.included_letters and self.fails_included_letters(target):
                continue

            if self.excluded_letters and self.fails_excluded_letters(target):
                continue

            if self.index_excludes_letters and self.fails_index_excludes_letters(target):
                continue

            possible_answers.append(target)
        return possible_answers

if __name__ == '__main__':
    from game.wordle_game import WordleGame
    wgame = WordleGame('epoxy', ['oater', 'shuln'])
    wfilter = WordsLeftFilter(wgame)
    results = WordsLeftResults(wfilter)
    print(results.targets_left)
    # ['biome', 'dodge', 'movie', 'epoxy', 'voice', 'booze', 'diode', 'evoke', 'decoy', 'gecko']