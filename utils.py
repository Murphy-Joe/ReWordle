import json

class Utils:

    @staticmethod
    def all_targets():
        with open('words/targets.json', 'r') as targets_json:
            return json.load(targets_json)

    @staticmethod
    def all_playables():
        with open('words/playable_words.json', 'r') as playables_json:
            return json.load(playables_json)
    
    @staticmethod
    def make_second_appearance_of_letter_uppercase(word: str) -> str:
        if len(word) == len(set(word)):
            return word
        word_builder = ''
        for ltr in word:
            if ltr not in word_builder:
                word_builder += ltr
            else:
                word_builder += ltr.upper()
        return word_builder

    @staticmethod
    def convert_uppercase_to_double_letter(self, results: dict[str, int]) -> dict[str, int]:
        formattedDict = {}
        for k in results.keys():
            if k.isupper():
                newKey = f"{k}{k}"
                formattedDict[newKey] = results[k]
            else:
                formattedDict[k.upper()] = results[k]
        return formattedDict