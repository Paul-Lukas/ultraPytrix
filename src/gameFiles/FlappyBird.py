import random
import numpy as np

class FlappyBird():
    def __init__(self):
        # Array-dimension variables
        self.width = 15
        self.background_width = 30
        self.height = 30

        # Creating the arrays
        self.background = [[0 for j in range(self.height)] for i in range(self.background_width)]
        self.game = [[0 for j in range(self.height)] for i in range(self.width)]

        # Game-logic variables
        self.game_over = False
        self.level = 1
        self.pipe_number = 0
        self.pipe_x_pos = 0
        self.pipe_y_pos = 0

    def run(self):
        self.set_bird_pos(int(self.height/2))
        self.generate_clouds(True, 0)
        self.draw_pipe(8, 13, 2)
        self.show_array(1)
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

    # Depending on the Level changes obstacle type
    def manage_level(self):
        if (self.level % 2) != 0: # Even
            self.manage_pipe()
        else: # Odd
            if self.level == 2:
                self.manage_horizontal_pipe(False)
            else:
                self.manage_horizontal_pipe(True)

    # Draws a pipe with the given coordinates and gap
    def draw_pipe(self, x_pos, y_pos, gap):
        self.clear(1, 2)
        upper_y_pos = int(y_pos - gap)
        lower_y_pos = int(y_pos + gap)

        for i in range(self.height):
            if i < upper_y_pos:
                self.game[x_pos][i] = 2
            if i > lower_y_pos:
                self.game[x_pos][i] = 2
            if i == upper_y_pos or i == lower_y_pos:
                self.game[x_pos][i] = 2
                if i > 0:
                    self.game[x_pos - 1][i] = 2
                if i < (self.width - 1):
                    self.game[x_pos + 1][i] = 2

    # Moves the pipes and manages gap depending on level
    def manage_pipe(self):
        if self.pipe_number >= 5:
            self.pipe_number = 0
            self.level += 1
            return

        # New pipe
        if self.pipe_x_pos == 0:
            self.pipe_number += 1
            self.pipe_x_pos = (self.width - 1)
            self.pipe_y_pos = random.randint((self.get_gap(self.level) / 2) + 1, (self.height - 1) - ((self.get_gap(self.level) / 2) + 1))
            self.draw_pipe(self.pipe_x_pos, self.pipe_y_pos, self.get_gap(self.level))

        # Existing pipe
        if (self.pipe_x_pos <= (self.width - 1)) or (self.pipe_x_pos > 0):
            self.pipe_x_pos += -1
            self.draw_pipe(self.pipe_x_pos, self.pipe_y_pos, self.get_gap(self.level))

    # Draws a horizontal pipe with the given coordinates and gap
    def draw_horizontal_pipe(self, x_pos, y_pos, gap):
        # Move existing horizontal pipes
        for i in range(self.width):
            for j in range(self.height):
                if self.game[i][j] == 1:
                    continue
                if i != (self.width - 1) and self.game[i][j] == 2:
                    if self.game[i + 1][j] == 1:
                        self.game[i][j] = 0
                    else:
                        self.game[i][j] = self.game[i + 1][j]

    # Manages a horizontal pipe
    def manage_horizontal_pipe(self):
        pass

    def get_gap(self, level):
        gaps = {
            1: 12,
            2: 10,
            3: 8,
            4: 6,
            5: 4
        }
        return gaps.get(value, -1)


if __name__ == '__main__':
    fb = FlappyBird()
    fb.run()