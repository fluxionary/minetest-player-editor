#!/usr/bin/env python3
""""""
import argparse
import pathlib
import sqlite3


def main(args):
    name = args.player_name
    pos = args.position
    with sqlite3.connect(str(args.player_file)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE player
               SET posX = ?
                 , posY = ?
                 , posZ = ?
             WHERE name = ?
        ''', (pos.x, pos.y, pos.z, name))
        print(f'{cursor.rowcount} rows updated')


class Coords:
    def __init__(self, coords_as_str):
        coords = tuple(map(int, map(str.strip, coords_as_str.strip().split(','))))
        if len(coords) != 3:
            raise ValueError(f'"{coords_as_str}" is not in the format "X,Y,Z"')

        if not all(-30912 <= coord <= 30927 for coord in coords):
            raise ValueError(f'"{coords_as_str}" is outside the map boundaries')

        self.x, self.y, self.z = coords

    def __repr__(self):
        return f'{self.x},{self.y},{self.z}'


def parse_args(argv=None, namespace=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('player_file', type=pathlib.Path,
                        help='location of the players.sqlite file')
    parser.add_argument('player_name', type=str,
                        help='name of the player (case sensitive)')
    parser.add_argument('--position', '-p', type=str, default=Coords('0,0,0'), metavar='X,Y,Z',
                        help='position (default: %(default)s)')
    return parser.parse_args(argv, namespace)


if __name__ == '__main__':
    main(parse_args())
