from util import utils
from speech_converter import speech_to_text
from grammar_rater import rate_spelling
from grammar_rater import rate_unnecessary_fillers
from grammar_rater import rate_grammar
import time
import asyncio
import json
from json import JSONEncoder


filename = "speech.txt"


class SpeechRater:
    def __init__(self, fluencyRating, spellingRating, fillerRating, grammarRating, totalRating):

        self.fluencyRating = fluencyRating
        self.spellingRating = spellingRating
        self.fillerRating = fillerRating
        self.grammarRating = grammarRating
        self.totalRating = totalRating

    def get_fluencyRating(self):
        return self.fluencyRating


class SpeechRaterEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def rate(file):

    if speech_to_text(file):
        data = utils.read_file(filename)
        words_count = utils.total_words(data)

        fluency_rating = utils.rate_speech_on_fluency(words_count)

        spelling_rating = rate_spelling(data, words_count)

        filler_rating = rate_unnecessary_fillers(data)

        grammar_rating = rate_grammar(data)

        total_rating = fluency_rating + spelling_rating + filler_rating + grammar_rating

        rating = SpeechRater(fluency_rating, spelling_rating,
                             filler_rating, grammar_rating, total_rating)

        return json.dumps(rating, cls=SpeechRaterEncoder)
