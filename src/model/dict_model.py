from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from api.dict_api import DictApiManager

class DictModel:

    dict_api = DictApiManager()

    def get_word_info(self, word: str):
        api_response = DictModel.dict_api.request_json(word)

        # List of all possible parts of speech contexts
        pos_contexts = []

        for word_info in api_response:
            pos_contexts.append(self.process_word_info(word_info, word))

        # Always be a list with dicts containing all parts of speech contexts
        return list(filter(lambda pos_context: pos_context, pos_contexts))
    
    # Takes in raw JSON from API and splits into different word properties, returns dict
    def process_word_info(self, unprocessed_word: str, word_name: str):
        word_info = {}
        word_info["word_name"] = ''.join([letter for letter in unprocessed_word['meta']['id'] if letter.isalpha()])

        if self.is_valid_word(word_info, word_name):
            word_info["stem_set"] = set(map(lambda stem: stem.lower(), filter(lambda stem: len(stem.split(" ")) == 1, unprocessed_word["meta"]["stems"])))
            word_info["definitions"] = unprocessed_word["shortdef"] 
            word_info["part_of_speech"] = unprocessed_word["fl"]
            word_info["phonetics"] = list(filter(lambda info: info, [prs_info.get("mw", None) for prs_info in unprocessed_word["hwi"].get("prs", [])]))
                
             # Always be a dict with word property key pair values
            return word_info
    
    def is_valid_word(self, word_info: dict[str, str], word_name: str):
        return word_info["word_name"] == word_name