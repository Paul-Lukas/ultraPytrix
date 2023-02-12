import random
import numpy as np

class FlappyBird():
    def __init__(self):
        self.width = 15
        self.background_width = 30
        self.height = 30
        self.game_over = False
        self.level = 1
        self.background = [[0 for j in range(self.height)] for i in range(self.background_width)]
        self.game = [[0 for j in range(self.height)] for i in range(self.width)]

    def run(self):
        self.set_bird_pos(int(self.height/2))
        self.generate_clouds(True, 0)
        self.show_array(2)
        #self.clock()

    # Deletes the old and sets the new player y-position
    def set_bird_pos(self, y_pos):
        if y_pos != self.get_bird_pos():
            self.clear(1, 1)
            self.game[1][y_pos] = 1

    # Returns players y-position
    def get_bird_pos(self):
        for i in range(self.height):
            if self.game[1][i] == 1:
                return i

    # Deletes one or multiple given values from a chosen array
    def clear(self, array, *value_type):
        for i in range(self.width):
            for j in range(self.height):
                if (array == 1) and (self.game[i][j] in value_type):
                    self.game[i][j] = 0
                elif (array == 2) and (self.background[i][j] in value_type):
                    self.background[i][j] = 0

    # Prints an array
    def show_array(self, array):
        if array == 1:
            print(np.matrix(self.game))
        else:
            print(np.matrix(self.background))

    # Checks if the not visible side of background[][] has no clouds in it
    def check_clouds(self):
        empty = True
        for i in range(self.width):
            for j in range(self.height):
                if self.background[(i + self.width)][j] == 1:
                    empty = False
        return empty

    # Generates cloud paterns for background[][]
    def generate_clouds(self, startup, offset):
        if startup:
            self.generate_clouds(False, 0)
            self.generate_clouds(False, self.width)

        else:
            chance = [random.randint(0, 1) for i in range(self.height)]
            position = [random.randint(0, (self.width - 1)) for j in range(self.height)]
            length = [random.randint(1, 4) for k in range(self.height)]
            for i in range(self.height):
                if chance[i] == 0:
                    continue

                for j in range(length[i]):
                    if (position[i] + j) < self.width:
                        self.background[i][(position[i] + j) + offset] = 1

    # Moves the clouds from right to left at the rate of 1 pixel
    def move_clouds(self):
        for i in range((self.background_width-1)):
            for j in range(self.height):
                self.background[i][j] = self.game[(i+1)][j]
        for k in range(self.height):
            self.background[self.background_width][k] = 0

    # Translates the values inside game[][] to match together[][]
    def translate_array_values(self, value):
        values = {
            1: 2,  # Player
            2: 3  # Pipe
        }
        return values.get(value, -1)

    # Translates the values inside together[][] to rgb-color values
    def translate_color_values(self, value):
        colors = {
            0: (0, 188, 255),  # Background: Light Blue
            1: (255, 255, 255),  # Clouds: White
            2: (255, 0, 0),  # Player: Red
            3: (0, 255, 34)  # Pipe: Green
        }
        return colors.get(value, -1)

    # Puts game[][] and background[][] together and creates an array filled with rgb-color values
    def translate_arrays(self):
        together = [[0 for j in range(self.height)] for i in range(self.width)]
        for i in range(self.width):
            for j in range(self.height):
                together[i][j] = self.background[i][j]
                if self.game[i][j] != 0:
                    together[i][j] = self.translate_array_values(self.game[i][j])

        final = [[(0, 0, 0) for j in range(self.height)] for i in range(self.background_width)]
        for i in range(self.width):
            for j in range(self.height):
                final[i][j] = self.translate_color_values(together[i][j])
        return final

    # Checks if nothing is between new and old position before movement
    def move_detection(self, old_y_pos, new_y_pos):
        if old_y_pos == new_y_pos:
            return False

        if new_y_pos < old_y_pos:
            raange = range(old_y_pos, new_y_pos - 1, -1)
        else:
            raange = range(old_y_pos, new_y_pos + 1)

        for i in raange:
            if i == 0:
                continue

            if self.game[1][old_y_pos + i] != 0:
                return True
        return False

    # Checks if the bird would hit something in the next move
    def hit_detection(self):
        if self.game[2][self.get_bird_pos()] != 0:
            return True
        return False

    # Game-Loop
    def clock(self):
        while not self.game_over:
            self.level_manager()
            self.hit_detection()

    # TODO: Should decide whether pipes or other things are spawned
    def level_manager(self):
        # Idea 4 pipes = 1 level
        # Horizontal pipe = 1 level
        # after level 3 horizontal pipes should change over time
        # difficulty = gap and speed(?)
        if self.level == 1:  # 4 pipes
            pass
        if self.level == 2:  # Horizontal pipe
            pass
        if self.level >= 3:  # odd = changing horizontal pipe | even = 4 pipes
            pass



if __name__ == '__main__':
    fb = FlappyBird()
    fb.run()