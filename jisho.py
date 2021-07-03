# -*- coding: utf-8 -*-
"""
Utils for parsing results from Jisho.
"""

import json
from typing import Any, Dict, Optional, Sequence
from urllib.parse import quote
from urllib.request import urlopen

from config import Config

JISHO_SEARCH = 'https://jisho.org/api/v1/search/words?keyword={0}'


class JishoError(Exception):
    pass


def fetch(search: str) -> Optional[Dict[str, Any]]:
    url = JISHO_SEARCH.format(quote(search.encode('utf8')))

    try:
        response = urlopen(url).read()
        data = json.loads(response)
    except IOError:
        raise JishoError

    try:
        return data['data'][0]
    except (IndexError, KeyError):
        raise JishoError


def create_note(data: Dict[str, Any], config: Config) -> Dict[str, str]:
    jp = data['japanese'][0]
    reading = try_get_data(jp, 'reading')
    senses = try_get_data(data, 'senses')
    word = reading if uses_kana(senses) else try_get_data(jp, 'word', 'reading')

    note = {
        'profile': config.profile,
        'type': config.note,
        'deck': config.deck,
    }

    try_set_key_val(note, 'tags', config.tags)
    try_set_key_val(note, config.reading_field, reading)
    try_set_key_val(note, config.meaning_field, get_meaning(senses))
    try_set_key_val(note, config.word_field, word)
    return note


def get_meaning(senses: Optional[Sequence[Dict[str, Sequence[str]]]]) -> Optional[str]:
    if not senses:
        return

    return f'''<dl>{''.join(
        f'<dt>{get_parts_of_speech(sense)}</dt>'
        f'<dd>{get_definition(sense)}</dd>'
        for sense in senses
    )}</dl>'''


def get_parts_of_speech(sense: Dict[str, Sequence[str]]) -> str:
    return ', '.join(sense['parts_of_speech'])


def get_definition(sense: Dict[str, Sequence[str]]) -> str:
    return '; '.join(sense['english_definitions'])


def uses_kana(senses: Sequence[Dict[str, Sequence[str]]]) -> bool:
    if not senses:
        return False
    return any('kana alone' in tag for tag in senses[0]['tags'])


def try_get_data(data: Dict[str, str], *keys: str) -> Optional[Any]:
    for key in keys:
        try:
            return data[key]
        except KeyError:
            pass


def try_set_key_val(note: Dict[str, str], key: str, value: Any):
    if not (key and value):
        return

    try:
        note[key] = value
    except KeyError:
        pass
