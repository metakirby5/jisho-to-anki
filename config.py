# -*- coding: utf-8 -*-
"""
Configuration values.
"""
import json


class Config:
    def __init__(self, fp):
        config = json.load(fp)
        self.profile: str = config['profile']
        self.note: str = config['note']
        self.deck: str = config['deck']
        self.tags: str = config['tags']

        fields = config['fields']
        self.lookup_field: str = fields['lookup']
        self.meaning_field: str = fields['meaning']
        self.reading_field: str = fields['reading']
        self.word_field: str = fields['word']