#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A simple web server which redirects to generate an Anki entry on iOS.
"""

import argparse
import os
import sys
from urllib.parse import urlencode, quote

import argcomplete
import bottle
import termcolor

import jisho
from config import Config

HERE = os.path.abspath(os.path.dirname(__file__))
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = '8080'
DEFAULT_CONFIG_FILE = os.path.join(HERE, 'config.json')

STATIC_ROOT = os.path.join(HERE, 'static')
ANKI_URL = 'anki://x-callback-url/addnote?'
CHROME_URL = 'googlechrome://'
bottle.TEMPLATE_PATH = [os.path.join(HERE, 'views')]


def fail_with(msg):
    print(termcolor.colored(msg, 'red'))
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--host',
        help=f"""
        The server host.
        Default: {DEFAULT_HOST}
        """,
        default=DEFAULT_HOST)

    parser.add_argument(
        '--port', '-p',
        help=f"""
        The server port.
        Default: {DEFAULT_PORT}
        """,
        default=DEFAULT_PORT)

    parser.add_argument(
        'config_file',
        help=f"""
        The config file to use.
        Default: {DEFAULT_CONFIG_FILE}
        """,
        nargs='?',
        default=DEFAULT_CONFIG_FILE)

    argcomplete.autocomplete(parser)
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        with open(args.config_file) as f:
            config = Config(f)
    except FileNotFoundError:
        fail_with(f'Config file "{args.config_file}" not found.')

    @bottle.get(f'/static/<filepath:path>')
    def static_route(filepath):
        return bottle.static_file(filepath, root=STATIC_ROOT)

    @bottle.get('/')
    @bottle.view('index')
    def index_route():
        return {'config': config}

    @bottle.get('/search/<query>')
    def search(query: str):
        try:
            data = jisho.fetch(query)
        except jisho.JishoError:
            return {}

        note = jisho.create_note(data, config)
        note['x-success'] = CHROME_URL
        url = ANKI_URL + urlencode(note, quote_via=quote)
        return {'url': url, 'note': note}

    bottle.run(host=args.host, port=args.port)


if __name__ == '__main__':
    main()
