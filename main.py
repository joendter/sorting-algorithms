from enum import Enum
import time
import pygame
import sys
import random


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


class Element(pygame.sprite.Sprite):
    def __init__(self, value, size: (int, int)):
        super(Element, self).__init__()
        width, height = size
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect()
        pygame.draw.rect(self.surf, (255, 255, 255), (0, 0, width, height),1)
        self.font = pygame.font.Font(None, int(size[1]*0.95))
        text = pygame.transform.rotate(self.font.render(str(value), False, (255, 255, 255)), -90)
        self.surf.blit(text, (int(width*0.05) + 1, int(height*0.05) + 1))


class Array:

    def __init__(self, debug: bool = True, **kwargs):
        """Currently just a mask for from file"""
        self.data = []
        self.mode = DataMode.INTEGER
        self.current_index: int = 0
        self.fromFile(**kwargs)
        self.length: int = len(self.data)
        self.debug: bool = debug
        self.t0: float = time.time()
        self.costs: {str: int} = {"move": 1,
                                  "swap": 1,
                                  "shuffle": 1,
                                  "compare": 1
                                  }

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

    def compare_current(self, idx: int):
        return self.compare(self.current_index, idx)

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
        return self.move_to(self.current_index + delta_index)

    def move_right(self) -> bool:
        self.debug_message("Moved right")
        return self.move(1)

    def move_left(self) -> bool:
        self.debug_message("Moved left")
        return self.move(-1)

    def move_to(self, index: int) -> bool:  # elementary
        if self.valid_index(index):
            self.current_index = index
            self.debug_message(f"New index {self.current_index}")
            return True
        return False

    def move_to_start(self) -> bool:
        return self.move_to(0)

    def debug_message(self, message):
        """A print that only gets executed in debug mode"""
        if self.debug:
            print(message)

    def start_timer(self):
        self.t0 = time.time()

    def read_timer(self) -> float:
        return time.time()-self.t0

    def sorted(self):
        """Returns if array is sorted"""
        self.debug_message("Checking if sorted")
        self.move_to_start()
        while self.current_index < self.length - 1:
            if self.compare_current_next():
                self.debug_message("Is sorted")
                return False
            self.move_right()
        self.debug_message("Is not sorted")
        return True

    def shuffle(self): # elementary
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
            time.sleep(1)

    def BogoSort(self):
        """https://en.wikipedia.org/wiki/Bogosort"""
        while not self.sorted():
            self.shuffle()

    def SelectionSort(self):
        """https://en.wikipedia.org/wiki/Selection_sort"""
        sorted_until = 0
        while not self.sorted():
            minimum_index = sorted_until
            self.move_to(sorted_until)
            while self.move_right():
                if not self.compare_current(minimum_index):
                    minimum_index = self.current_index
            self.swap(minimum_index, sorted_until)
            sorted_until += 1


a = Array(filepath="testdata1.txt")

a.SelectionSort()
print(a.data)


b = Array(False, filepath="testdata3.txt")
b.start_timer()
b.GnomeSort()
print(b.read_timer())
b.fromFile("testdata3.txt")
b.start_timer()
b.SelectionSort()
print(b.read_timer())


# screen =pygame.Surface(size)
tmpelement = Element(10, (20,20))
screen.blit(tmpelement.surf, (10,10))
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
