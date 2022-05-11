from utils import Utils
from wordle_game import WordleGame

class WordsLeftFilter:
    def __init__(self, game: WordleGame):
        self.game = game
        self.indexed_letters: dict[int, str] = {}
        self.included_letters: set[str] = set()
        self.index_excludes_letters: dict[int, set[str]] = {}
        self.excluded_letters: set[str] = set()
        self.init_filter()

    def add_guess(self, guess):
        self.handle_included_letters_w_upper(guess)

        for i, letter in enumerate(guess):
            if self.game.target[i] == letter:
                self.indexed_letters[i] = letter
                self.included_letters.add(letter)
            elif letter in self.game.target:
                self.index_excludes_letters.setdefault(i, set())
                self.index_excludes_letters[i].add(letter)
            else:
                self.excluded_letters.add(letter)

    def handle_included_letters_w_upper(self, guess):
        target_w_uppers = Utils.make_second_appearance_of_letter_uppercase(self.game.target)
        guess_w_uppers = Utils.make_second_appearance_of_letter_uppercase(guess)

        for letter in guess_w_uppers:
            if letter in target_w_uppers: 
                self.included_letters.add(letter)

    def init_filter(self) -> None:
        for guess in self.game.guesses:
            self.add_guess(guess)

    

if __name__ == '__main__':
    wgame = WordleGame('canny', ['crane', 'shame', 'china'])
    wfilter = WordsLeftFilter(wgame)
    print(wfilter.__dict__)
    # 'indexed_letters': {0: 'c', 3: 'n'}, 
    # 'included_letters': {'a', 'c', 'n'}, 
    # 'index_excludes_letters': {2: {'a'}, 4: {'a'}}, 
    # 'excluded_letters': {'s', 'r', 'i', 'm', 'e', 'h'}}

    wfilter.add_guess('nnafy')
    print(wfilter.__dict__)
    # 'indexed_letters': {0: 'c', 3: 'n', 4: 'y'}, 
    # 'included_letters': {'a', 'c', 'y', 'N', 'n'}, 
    # 'index_excludes_letters': {2: {'a'}, 4: {'a'}, 0: {'n'}, 1: {'n'}}, 
    # 'excluded_letters': {'f', 's', 'r', 'i', 'm', 'e', 'h'}}