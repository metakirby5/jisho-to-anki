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

        def get_field(name: str):
            return 'fld' + fields[name]

        self.meaning_field: str = get_field('meaning')
        self.reading_field: str = get_field('reading')
        self.word_field: str = get_field('word')
