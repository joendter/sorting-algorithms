from enum import Enum
import time
import pygame
import random
import re
import os


pygame.init()

size = width, height = 256, 256
x_pos = 30
y_pos = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x_pos,y_pos)
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
    def __init__(self, value, size: (int, int), location: (int, int) = (0,0)):
        super(Element, self).__init__()
        self.value = value
        width, height = size
        self.size = size
        self.location = location
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect()
        pygame.draw.rect(self.surf, (255, 255, 255), (0, 0, width, height),1)
        font = pygame.font.Font(None, int(size[0]*0.95))
        text = pygame.transform.rotate(font.render(str(value), False, (255, 255, 255)), -90)
        self.surf.blit(text, (int(width*0.05) + 1, int(height*0.05) + 1))

    def move_to(self, location):
        self.location = location

    def move(self, dx = 0, dy = 0):
        self.move_to((self.location[0] + dx, self.location[1] + dy))


class Array:

    def __init__(self, debug: bool = True, animated: bool = True, **kwargs):
        """Currently just a mask for from file"""
        self.data = []
        self.debug: bool = debug
        self.mode = DataMode.INTEGER
        self.current_index: int = 0
        self.fromFile(**kwargs)
        self.length: int = len(self.data)

        self.t0: float = time.time()
        self.costs: {str: int} = {"move": 0.3,
                                  "swap": 0.5,
                                  "shuffle": 1,
                                  "compare": 0.3,
                                  "yeet":0.5
                                  }
        self.dimensions = (1024, 700)
        self.animated = animated
        if self.animated:
            self.initialise_pygame()


    def initialise_pygame(self):
        #self.window = Window(title="array", size=self.dimensions)
        #self.renderer = Renderer(self.window)
        self.screen = pygame.display.set_mode(self.dimensions)
        self.surface = self.screen#pygame.Surface(self.dimensions)
        self.pygame_objects = []
        object_size = (self.dimensions[0]//self.length, self.dimensions[1]//4)
        self.pointy_thingy = pygame.Surface((40,40), pygame.SRCALPHA)
        self.pointy_thingy.fill((255,255,255,0))
        points = [(0, 0), (20, 40), (40, 0)]
        pygame.draw.polygon(self.pointy_thingy, (255, 0, 0), points)
        for index in range(self.length):
            self.pygame_objects.append(Element(self.get_value(index), object_size, (index*(object_size[0]+1), self.dimensions[1]//3)))
        pygame.display.update()

    def update_screen(self):
        pygame.display.update()

    def draw_objects_on_surface(self):
        self.surface.fill((0, 0, 0))
        for obj in self.pygame_objects:
            self.surface.blit(obj.surf, obj.location)
        self.surface.blit(self.pointy_thingy, ((self.current_index + 0.5)*self.pygame_objects[0].size[0] - 20, 10))

    def draw_and_update(self):
        self.draw_objects_on_surface()
        self.update_screen()

    def fromFile(self, filepath: str, mode=FileMode.DECIMAL, sep: str = ",") -> bool:
        """ Function that loads an array from file;
            """

        if mode == FileMode.BINARY:
            # Import file as binary
            pass

        if mode == FileMode.DECIMAL:
            # Import file as list of decimal numbers
            with open(filepath, "r") as file:
                file_contents = file.read()
                if re.match(rf'^((\d)+{sep})*(\d)+$', file_contents):
                    self.data = list(map(int, file_contents.split(sep=sep)))
                    self.debug_message(self.data)
                    self.mode = DataMode.INTEGER
                    return True
                else:
                    print("invalid file data")
                    return False

        if mode == FileMode.STRING:
            # Import file as list of strings
            with open(filepath, "r") as file:
                file_contents = file.read()
                if re.match(rf'^([\da-zA-Z]+{sep})*[\da-zA-Z]+$', file_contents):
                    self.data = file.read().split(sep=sep)
                    self.mode = DataMode.STRING
                    return True
                else:
                    return False

    def valid_index(self, index: int) -> bool:
        return 0 <= index < self.length

    def get_value(self, index: int):
        return self.data[index]

    def get_current_value(self):
        return self.get_value(self.current_index)

    def compare(self, idx1: int, idx2: int):  # elementary
        result = compare_values(self.data[idx1], self.data[idx2], mode=self.mode)
        self.compare_animation(idx1, idx2, result)
        return result

    def compare_animation(self, idx1: int, idx2: int, result: bool) -> bool:
        if not self.animated:
            return False
        self.draw_objects_on_surface()
        dimensions = (self.pygame_objects[idx1].size[0], self.dimensions[1])
        tmp1 = pygame.Surface(dimensions)
        tmp1.fill((255*result, 255*(not result), 0))
        tmp1.set_alpha(40)
        tmp2 = pygame.Surface(dimensions)
        tmp2.fill((255*(not result), 255*result, 0))
        tmp2.set_alpha(40)
        self.surface.blit(tmp1, (self.pygame_objects[idx1].location[0], 0))
        self.surface.blit(tmp2, (self.pygame_objects[idx2].location[0], 0))
        #del tmp
        self.update_screen()
        time.sleep(self.costs["compare"])
        return True

    def compare_adjacent(self, idx: int):
        return self.compare(idx, idx+1)

    def compare_current_next(self):
        return self.compare_adjacent(self.current_index)

    def compare_current(self, idx: int):
        return self.compare(self.current_index, idx)

    def swap(self, idx1: int, idx2: int):  # elementary
        self.debug_message(f"Swapped index {idx1} with index {idx2}")
        if idx1 == idx2:
            return None
        temp = self.data[idx1]
        self.data[idx1] = self.data[idx2]
        self.data[idx2] = temp
        self.swap_animation(idx1, idx2)

    def swap_animation(self, idx1: int, idx2: int):
        if not self.animated:
            return False
        obj1 = self.pygame_objects[idx1]
        obj2 = self.pygame_objects[idx2]
        x1 = obj1.location[0]
        x2 = obj2.location[0]
        delta_x = -(obj1.location[0] - obj2.location[0])/32
        delta_y = (obj1.size[1] + 10)/16
        delta_t = self.costs["swap"]/64
        for i in range(16):  # rising
            obj1.move(dy=delta_y)
            obj2.move(dy=-delta_y)
            self.draw_and_update()
            time.sleep(delta_t)

        for i in range(32):  # x-movement
            obj1.move(dx=delta_x)
            obj2.move(dx=-delta_x)
            self.draw_and_update()
            time.sleep(delta_t)
        obj1.move(dx=x2-obj1.location[0])
        obj2.move(dx=x1-obj2.location[0])

        for i in range(16):  # falling
            obj1.move(dy=-delta_y)
            obj2.move(dy=delta_y)
            self.draw_and_update()
            time.sleep(delta_t)

        #tmp = copy.deepcopy(self.pygame_objects[idx1])
        self.pygame_objects[idx1] = obj2
        self.pygame_objects[idx2] = obj1

    def swap_adjacent(self, idx: int):
        self.swap(idx, idx + 1)

    def swap_current_next(self):
        self.swap_adjacent(self.current_index)

    def move(self, delta_index: int) -> bool:
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
        if self.animated:
            self.draw_and_update()
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
                self.debug_message("Is not sorted")
                return False
            self.move_right()
        self.debug_message("Is sorted")
        return True

    def random_index(self):
        return random.randint(0, self.length-1)

    def shuffle(self, depth: int = 10):  # elementary
        for i in range(depth):
            self.swap(self.random_index(), self.random_index())
        self.debug_message("Shuffled")

    def yeet(self, index):  # elementary; doesn't work nicely
        self.data.pop(index)
        if self.current_index >= index:
            self.current_index -= 1
        for i in range(32):
            self.pygame_objects[index].move(dy=self.dimensions[1]/100)
            self.draw_and_update()
            time.sleep(self.costs["yeet"]/32)
        self.pygame_objects.pop(index)
        self.length -= 1

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
        while sorted_until < self.length - 1:
            minimum_index = sorted_until
            self.move_to(sorted_until)
            while self.move_right():
                if not self.compare_current(minimum_index):
                    minimum_index = self.current_index
            self.swap(minimum_index, sorted_until)
            sorted_until += 1

    def StalinSort(self):
        self.move_to_start()
        while self.current_index < self.length - 1:
            if self.compare_current_next():
                self.yeet(self.current_index)
            self.move_right()



def example_sort(algorithm=0, datapath="testdata5.txt"):
    a = Array(filepath=datapath)
    if algorithm == 0:
        a.GnomeSort()
    if algorithm == 1:
        a.BubbleSort()
    if algorithm == 2:
        a.SelectionSort()
    if algorithm == 3:
        a.MiracleSort()
    if algorithm == 4:
        a.BogoSort()
    if algorithm == 5:
        a.StalinSort()


debugarray = Array(animated=False,filepath="testdata5.txt")


#
# t1 = threading.Thread(target=example_sort())
# t2 = threading.Thread(target=example_sort())
# t1.start()
# t2.start()
#
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
