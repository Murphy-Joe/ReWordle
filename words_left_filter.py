from wordle_game import WordleGame

class WordsLeftFilter:
    def __init__(self, game: WordleGame):
        self.game = game
        self.indexed_letters: dict[int, str] = {}
        self.included_letters: list[str] = []
        self.index_excludes_letters: dict[int, set[str]] = {}
        self.excluded_letters: set[str] = set()
        self.init_filter()

    def append_to_included_letters(self, letter: str, guess: str) -> None:
        times_letter_guessed = guess.count(letter)
        times_letter_appears_in_target = self.game.target.count(letter)
        for i in range(times_letter_guessed):
            self.included_letters.append(letter)

    def add_guess(self, guess):
        for i, letter in enumerate(guess):
            if self.game.target[i] == letter:
                self.indexed_letters[i] = letter
                self.included_letters.append(letter)
                # self.append_to_included_letters(letter, guess)
            elif letter in self.game.target:
                self.index_excludes_letters.setdefault(i, set())
                self.index_excludes_letters[i].add(letter)
                guess = guess.replace(letter, '', 1)
                self.included_letters.append(letter)
            else:
                self.excluded_letters.add(letter)

    def init_filter(self) -> None:
        for guess in self.game.guesses:
            self.add_guess(guess)

    

if __name__ == '__main__':
    game = WordleGame('canny', ['crane', 'shame', 'china'])
    filter = WordsLeftFilter(game)
    print(filter.__dict__)
    # 'indexed_letters': {0: 'c', 3: 'n'}, 
    # 'included_letters': ['c', 'a', 'n'], 
    # 'index_excludes_letters': {2: {'a'}, 4: {'a'}}, 
    # 'excluded_letters': {'m', 'r', 'e', 's', 'i', 'h'}

    filter.add_guess('nnafy')
    print(filter.__dict__)
    # 'indexed_letters': {0: 'c', 3: 'n', 4: 'y'}, 
    # 'included_letters': ['c', 'a', 'n', 'n', 'y'],
    # 'index_excludes_letters': {2: {'a'}, 4: {'a'}, 0: {'n'}, 1: {'n'}}, 
    # 'excluded_letters': {'m', 'r', 'e', 's', 'f', 'i', 'h'}}