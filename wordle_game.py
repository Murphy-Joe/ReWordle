from datetime import date
from utils import Utils

class WordleGame:
    def __init__(self, target: str = None, guesses: list[str] = None):
        self.target = target if target else self.get_todays_target()
        self.guesses: list[str] = guesses if guesses else []
        
    # These 2 methods may go away if wordle is no longer choosing targets based on date
    def days_since_21Jun19th(self) -> int:
        return (date.today() - date(year=2021, month=6, day=19)).days

    def get_todays_target(self) -> str:
        targets_list = Utils.all_targets()
        return targets_list[self.days_since_21Jun19th()]


if __name__ == '__main__':
    game = WordleGame('')
    
    print(game.days_since_21Jun19th())
    print(game.get_todays_target())
    print(Utils.all_targets().index(game.get_todays_target()))