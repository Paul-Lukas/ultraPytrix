import random
import time

class FlappyBird():
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
        self.pipe_x_pos = 0
        self.pipe_y_pos = 0

    def run(self):
        self.set_bird_pos(int(self.height/2))
        self.generate_clouds(True, 0)
        self.show_array(self.background)
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
                        self.background[i][(position[i] + j) + offset] = 1

    # Moves the clouds from right to left at the rate of 1 pixel
    def move_clouds(self):
        for i in range(self.background_width - 1):  # Move every row
            for j in range(self.height):
                self.background[i][j] = self.background[(i+1)][j]
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
            #self.level_manager()
            #self.hit_detection()
            
            # Background:
            self.move_clouds()
            if self.check_clouds():
            	self.generate_clouds(False, 15)
            time.sleep(0.5)
            
            # Translation:
            self.output.set_matrix(self.translate_arrays())
            self.output.submit_all()
            

    # Depending on the Level changes obstacle type
    def manage_level(self):
        if (self.level % 2) != 0:  # Even
            self.manage_pipe()
        else:  # Odd
            self.manage_horizontal_pipe()

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
        # Done
        if self.pipe_number >= 5:
            self.pipe_number = 0
            self.pipe_x_pos = 0
            self.pipe_y_pos = 0
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

    # Move(s) existing horizontal pipe(s)
    def move_horizontal_pipes(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.game[i][j] == 1:
                    continue
                if i != (self.width - 1) and self.game[i][j] == 2:
                    if self.game[i + 1][j] == 1:
                        self.game[i][j] = 0
                    else:
                        self.game[i][j] = self.game[i + 1][j]
        self.pipe_x_pos += -1

    # Check if a horizontal pipe is comlplete (length = 3)
    def check_horizontal_pipe(self, x_pos, y_pos, gap):
        distance = int(gap / 2)
        for i in range(3):
            try:
                if (self.game[x_pos][y_pos + distance] == 2) and (self.game[x_pos][y_pos - distance] == 2):
                    continue
            except:
                return i-1
        return 2

    # Draws the beginning of a horizontal pipe with the given coordinates and gap
    def draw_horizontal_pipe(self, x_pos, y_pos, gap, first):
        distance = int(gap/2)
        self.game[x_pos][y_pos + distance]
        self.game[x_pos][y_pos - distance]
        if first:
            self.pipe_x_pos = x_pos
            self.pipe_y_pos = y_pos
            # gap = get_gap(self.level)

    # Manages a horizontal pipe
    def manage_horizontal_pipe(self):
        # Done
        if self.pipe_number >= 5:
            self.pipe_number = 0
            self.pipe_x_pos = 0
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
            # Pipe parts are missing
            if status == 1 or status == 0:
                self.move_horizontal_pipes()
                self.draw_horizontal_pipe(self.pipe_x_pos + 1, self.pipe_y_pos, self.get_gap(self.level))
            # Pipe is complete
            if status == 2:
                self.pipe_number += 1
                if self.pipe_number <= 4:
                    self.move_horizontal_pipes()
                    # New Pipe
                    self.pipe_x_pos = (self.width - 1)
                    direction = random.randint(1, 2)
                    if direction == 2:
                        direction = -1
                    self.pipe_y_pos += direction # move it down or upwards
                    self.draw_horizontal_pipe(self.pipe_x_pos, self.pipe_y_pos, self.get_gap(self.level))


    def get_gap(self, level):
        if level > 8:
            return 4
        fixed_level = level # TODO: Pray this works
        if (self.level % 2) != 0:
            fixed_level = level + 1

        gaps = {
            2: 12,
            4: 10,
            6: 8,
            8: 6
        }
        return gaps.get(fixed_level, -1)


if __name__ == '__main__':
    fb = FlappyBird()
    fb.run()
