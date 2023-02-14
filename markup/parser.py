from pathlib import Path
from lark import Lark

grammar = open(Path(__file__).parent.joinpath('grammar.lark'))

parser = Lark(grammar)
