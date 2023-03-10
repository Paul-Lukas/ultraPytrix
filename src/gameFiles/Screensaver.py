import random

class Screensaver:
    def __init__(self, base, output):
        self.output = output
        self.base = base
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
        self.pipe_x_pos = -1
        self.pipe_y_pos = 0

    def run(self):
        self.set_bird_pos(int(self.height / 2))
        self.generate_clouds(True, 0)
        self.clock()

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

    # Should always place the bird in the correct position
    def move_bird_automatically(self):
        if self.pipe_x_pos == 2:
            self.set_bird_pos(self.pipe_y_pos)
            return

        bird_position = self.get_bird_pos()
        drop = 1
        if ((self.pipe_x_pos - 1) <= 5) & (abs(bird_position - self.pipe_y_pos) > 8):
            drop = 2

        if bird_position == self.pipe_y_pos:
            return
        if bird_position > self.pipe_y_pos:
            self.set_bird_pos(bird_position - drop)
        else:
            self.set_bird_pos(bird_position + drop)

    # Deletes one or multiple given values from a chosen array
    def clear(self, array, *value_type):
        for i in range(self.width):
            for j in range(self.height):
                if (array == 1) and (self.game[i][j] in value_type):
                    self.game[i][j] = 0
                elif (array == 2) and (self.background[i][j] in value_type):
                    self.background[i][j] = 0

    # Prints a given array
    def show_array(self, array):
        for i in range(len(array[0])):
            print("\n")
            for j in range(len(array)):
                print(array[j][i], end=' ')

    # Checks if the not visible side of background[][] has no clouds in it
    def check_clouds(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.background[(i + self.width)][j] == 1:
                    return False
        return True

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
                        self.background[(position[i] + j) + offset][i] = 1

    # Moves the clouds from right to left at the rate of 1 pixel
    def move_clouds(self):
        for i in range(self.background_width - 1):  # Move every row
            for j in range(self.height):
                self.background[i][j] = self.background[(i + 1)][j]
        for k in range(self.height):  # Delete the last row
            self.background[(self.background_width - 1)][k] = 0

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

    # Flips the array
    def debug_mirror_array(self, array):
        new_array = []
        for i in range(len(array)):
            new_array.append(array[i][::-1])
        return new_array

    # Rotates the array counterclockwise 90 degrees
    def debug_rotate_array(self, array, amount):
        new_array = [[array[j][i] for j in range(len(array))] for i in range(len(array[0]) - 1, -1, -1)]
        if amount > 0:
            return self.debug_rotate_array(new_array, amount - 1)
        else:
            return new_array

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
            # Game:
            self.move_bird_automatically()

            if (self.level % 2) != 0:
                self.level += 1
            self.manage_level()

            # Background:
            self.move_clouds()
            if self.check_clouds():
                self.generate_clouds(False, 15)

            # Translation:
            self.output.set_matrix(self.translate_arrays())
            self.output.submit_all()
        print("-- Flappy-Bird Ending --")

    # Depending on the Level changes obstacle type
    def manage_level(self):
        if (self.level % 2) != 0:  # Even
            self.manage_pipe()
        else:  # Odd
            self.manage_horizontal_pipe()

    # Draws a pipe with the given coordinates and gap
    def draw_pipe(self, x_pos, y_pos, gap):
        self.clear(1, 2)
        upper_y_pos = int(y_pos - ((gap / 2) + 1))
        lower_y_pos = int(y_pos + ((gap / 2) + 1))

        for i in range(self.height):
            if i == upper_y_pos or i == lower_y_pos:
                if 0 <= x_pos <= (self.width - 1):  # Middle piece
                    self.game[x_pos][i] = 2
                if 0 <= (x_pos - 1) < self.width:  # Left piece
                    self.game[x_pos - 1][i] = 2
                if (self.width - 1) >= (x_pos + 1) >= 0:  # Right piece
                    self.game[x_pos + 1][i] = 2

            if x_pos == -1 or x_pos == self.width:
                continue

            if ((i >= 0) and (i < upper_y_pos)) or ((i <= (self.height - 1)) and (i > lower_y_pos)):
                self.game[x_pos][i] = 2

    # Moves the pipes and manages gap depending on level
    def manage_pipe(self):
        # Done
        if self.pipe_number >= 5:
            self.pipe_number = 0
            self.pipe_x_pos = 0  # 0 needed for manage_horizontal_pipe
            self.pipe_y_pos = 0
            self.level += 1
            return

        # New pipe
        if self.pipe_x_pos == -1:
            self.pipe_number += 1
            self.pipe_x_pos = self.width
            self.pipe_y_pos = random.randint((self.get_gap(self.level) / 2) + 1,
                                             (self.height - 1) - ((self.get_gap(self.level) / 2) + 1))
            self.draw_pipe(self.pipe_x_pos, self.pipe_y_pos, self.get_gap(self.level))

        # Existing pipe
        if (self.pipe_x_pos <= self.width) or (self.pipe_x_pos >= 0):
            self.pipe_x_pos += -1
            self.draw_pipe(self.pipe_x_pos, self.pipe_y_pos, self.get_gap(self.level))

    # Move(s) existing horizontal pipe(s)
    def move_horizontal_pipes(self):
        for i in range(self.width - 1):
            for j in range(self.height):
                if self.game[i][j] == 1:
                    continue
                if self.game[i + 1][j] == 1:
                    self.game[i][j] = 0
                    continue
                self.game[i][j] = self.game[i + 1][j]
        for k in range(self.height):
            self.game[self.width - 1][k] = 0

    # Check if a horizontal pipe is comlplete (length = 3)
    def check_horizontal_pipe(self, x_pos, y_pos, gap):
        upper_y_pos = int(y_pos - ((gap / 2) + 1))
        lower_y_pos = int(y_pos + ((gap / 2) + 1))
        length = 0

        for i in range(3):
            if (x_pos + i) > (self.width - 1):
                break
            if (self.game[x_pos + i][upper_y_pos] == 2) and (self.game[x_pos + i][lower_y_pos] == 2):
                length += 1

        return length

    # Draws the beginning of a horizontal pipe with the given coordinates and gap
    def draw_horizontal_pipe(self, x_pos, y_pos, gap):
        upper_y_pos = int(y_pos - ((gap / 2) + 1))
        lower_y_pos = int(y_pos + ((gap / 2) + 1))

        if 0 <= x_pos <= (self.width - 1):
            self.game[x_pos][upper_y_pos] = 2
            self.game[x_pos][lower_y_pos] = 2

    # Manages a horizontal pipe
    def manage_horizontal_pipe(self):
        # Done
        if self.pipe_number >= 5:
            self.pipe_number = 0
            self.pipe_x_pos = -1  # -1 needed for manage_pipe
            self.pipe_y_pos = 0
            self.level += 1
            return

        # New pipe
        if self.pipe_x_pos == 0:
            self.pipe_x_pos = (self.width - 1)
            self.pipe_y_pos = random.randint((self.get_gap(self.level) / 2) + 1,
                                             (self.height - 1) - ((self.get_gap(self.level) / 2) + 1))
            self.draw_horizontal_pipe(self.pipe_x_pos, self.pipe_y_pos, self.get_gap(self.level))

        # Existing pipe(s)
        if (self.pipe_x_pos <= (self.width - 1)) or (self.pipe_x_pos > 0):
            status = self.check_horizontal_pipe(self.pipe_x_pos, self.pipe_y_pos, self.get_gap(self.level))
            print("Status:" + str(status))
            # Pipe parts are missing
            if status == 1 or status == 2:
                self.move_horizontal_pipes()
                self.pipe_x_pos += - 1
                self.draw_horizontal_pipe((self.width - 1), self.pipe_y_pos, self.get_gap(self.level))
            # Pipe is complete
            if status == 3:
                self.pipe_number += 1
                if self.pipe_number <= 4:
                    self.move_horizontal_pipes()
                    # New Pipe
                    self.pipe_x_pos = (self.width - 1)
                    direction = random.randint(1, 3)
                    # 1: Upwards; 2: Downwards; 3: No change
                    if direction == 2:
                        direction = -1
                    if direction == 3:
                        direction = 0

                    # Out of bounds:
                    if 0 <= (self.pipe_y_pos + direction) <= (self.height - 1):
                        self.pipe_y_pos += direction  # move it down or upwards
                    else:
                        self.pipe_y_pos += (direction * -1)
                    self.draw_horizontal_pipe((self.width - 1), self.pipe_y_pos, self.get_gap(self.level))

    def get_gap(self, level):
        if level > 8:
            return 4
        fixed_level = level
        if (self.level % 2) != 0:
            fixed_level = level + 1

        gaps = {
            2: 12,
            4: 10,
            6: 8,
            8: 6
        }
        return gaps.get(fixed_level, -1)
