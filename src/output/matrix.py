# noinspection PyUnresolvedReferences
import neopixel

from src.output.utils import Utils


class NeoMatrix:
    """
    Handels all the Conversion from Application to String
    The Application must be horizontal
    """
    matrix = []
    omatrix = []
    width = 0
    height = 0

    __pixels = object

    def __init__(self, width: int, height: int, pixels: neopixel.NeoPixel):
        self.width = width
        self.height = height

        self.__pixels = pixels
        self.utils = Utils()

        self.matrix = [[(0, 0, 0) for _ in range(height)] for _ in range(width)]
        self.omatrix = [[(0, 0, 0) for _ in range(height)] for _ in range(width)]

    def __getitem__(self, item):
        if len(item) != 2:
            raise ValueError('Index needs two values example: [1, 2]')
        return self.matrix[item[0]][item[1]]

    def __setitem__(self, key, value):
        if len(key) != 2:
            raise ValueError('Index needs two values example: [1, 2]')
        self.matrix[key[0]][key[1]] = value

    def submit_all(self):
        """
        Writes all the changes to tne Neopixel String
        """
        changes = self.utils.getChangedIndices(self.omatrix, self.matrix)

        self.omatrix = [row[:] for row in self.matrix]

        for i in range(len(changes)):
            pixelChange = (self.utils.getNumForCords(changes[i][0], changes[i][1], self.height))
            self.__pixels[pixelChange] = self.matrix[changes[i][0]][changes[i][1]]
        self.__pixels.write()
        
        print("neopixel submittttttttttttet")

    def fill_all(self, color: tuple):
        """
        Fills sets all the Pixels to the specified color
        :param color: needs to be a tripel with RGB values example: (255, 6, 187)
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] = color
        self.__pixels.fill(color)
        self.__pixels.write()

    def set_matrix(self, matrix):
        """
        Replace the matrix
        :param matrix: new 2dim tupel array must be same lengh as old one
        :return: true if lengh is right, false if not
        """
        if len(matrix) != len(self.matrix):
            print("matrix größe falsch")
            print("len1" + len(matrix))
            return False
        else:
            if len(matrix[0]) != len(self.matrix[0]):
                print("matrix größe falsch")
                print("len2" + len(matrix[0]))
                return False
            else:
                self.matrix = matrix
                print("matrix ERFOLG")
                return True
