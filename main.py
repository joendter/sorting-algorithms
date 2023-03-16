from enum import Enum
from time import sleep
#import pygame
import sys
#pygame.init()
import random

size = width, height = 256, 256

#screen = pygame.display.set_mode(size)


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
        self.debug = True


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

    def valid_index(self, index: int) -> bool:
        return 0 <= index < self.length

    def compare(self, idx1: int, idx2: int):
        return compare_values(self.data[idx1], self.data[idx2], mode=self.mode)

    def compare_adjacent(self, idx: int):
        return self.compare(idx, idx+1)

    def compare_current_next(self):
        return self.compare_adjacent(self.current_index)

    def swap(self, idx1: int, idx2: int):  # elementary
        temp = self.data[idx1]
        self.data[idx1] = self.data[idx2]
        self.data[idx2] = temp
        self.debug_message(f"Swapped index {idx1} with index {idx2}")

    def swap_adjacent(self, idx: int):
        self.swap(idx, idx + 1)

    def swap_current_next(self):
        self.swap_adjacent(self.current_index)

    def move(self, delta_index: int) -> bool:  # elementary
        if self.valid_index(self.current_index + delta_index):
            self.current_index += delta_index
            self.debug_message(f"New index {self.current_index}")
            return True
        return False

    def move_right(self):
        self.debug_message("Moved right")
        return self.move(1)

    def move_left(self):
        self.debug_message("Moved left")
        return self.move(-1)

    def move_to_start(self):
        return self.move(-self.current_index)

    def debug_message(self, message):
        """A print that only gets executed in debug mode"""
        if self.debug:
            print(message)

    def sorted(self):
        """Returns if array is sorted"""
        while self.current_index < self.length - 1:
            if self.compare_current_next():
                return False
            self.move_right()
        return True

    def shuffle(self):
        random.shuffle(self.data)
        self.debug_message("Shuffled")

    def GnomeSort(self):
        """https://en.wikipedia.org/wiki/Gnome_sort"""
        self.move_to_start()
        while self.current_index < self.length-1:
            if self.compare_current_next():
                self.swap_current_next()
                self.move_left()
            else:
                self.move_right()

    def BubbleSort(self):
        """https://en.wikipedia.org/wiki/Bubble_sort"""
        swapped = True
        while swapped:
            swapped = False
            self.move_to_start()
            while self.current_index < self.length - 1:
                if self.compare_current_next():
                    self.swap_current_next()
                    swapped = True
                self.move_right()

    def MiracleSort(self):
        """https://en.wikipedia.org/wiki/Bogosort#Related_algorithms"""
        while not self.sorted():
            sleep(1)

    def BogoSort(self):
        """https://en.wikipedia.org/wiki/Bogosort"""
        while not self.sorted():
            self.shuffle()


a = Array(filepath="testdata1.txt")

a.BogoSort()
print(a.data)
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#