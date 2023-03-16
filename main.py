from enum import Enum
import pygame
import sys
pygame.init()

size = width, height = 256, 256

screen = pygame.display.set_mode(size)


class FileMode(Enum):
    BINARY = "binary"
    DECIMAL = "decimal"
    STRING = "string"


class DataMode(Enum):
    INTEGER = "int"
    STRING = "str"
    FLOAT = "float"


def compare_values(value1, value2, mode) -> bool:
    """Compares value1 to value2 using a certain FileMode
        for integers it returns value1 > value2
        for strings it returns if value1 would be alphabetically in front of value2"""
    if mode == DataMode.INTEGER or mode == DataMode.FLOAT:
        return value1 > value2

    if mode == DataMode.STRING:
        return int(value1, 36) > int(value2, 36)


class Array:

    def __init__(self, **kwargs):
        """Currently just a mask for from file"""
        self.data = []
        self.mode = DataMode.INTEGER
        self.current_index: int = 0
        self.fromFile(**kwargs)
        self.length: int = len(self.data)


    def fromFile(self, filepath: str, mode=FileMode.DECIMAL, sep: str = ",") -> bool:
        """ Function that loads an array from file;
            """

        if mode == FileMode.BINARY:
            # Import file as binary
            pass

        if mode == FileMode.DECIMAL:
            # Import file as list of decimal numbers
            with open(filepath, "r") as file:
                self.data = list(map(int, file.read().split(sep=sep)))
                self.mode = DataMode.INTEGER
                return True

        if mode == FileMode.STRING:
            # Import file as list of strings
            with open(filepath, "r") as file:
                self.data = file.read().split(sep=sep)
                self.mode = DataMode.STRING
                return True

    def compare(self, idx1:int, idx2:int):
        return compare_values(self.data[idx1], self.data[idx2], mode=self.mode)

    def swap(self, idx1:int, idx2:int):
        temp = self.data[idx1]
        self.data[idx1] = self.data[idx2]
        self.data[idx2] = temp




a = Array(filepath="testdata1.txt")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            