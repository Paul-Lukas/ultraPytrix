class Utils:
    @staticmethod
    def getChangedIndices(array1, array2) -> list:
        """
        generates a List of tuples with the Coordinates which have changed from array1 to array2
        @param array1: first array
        @param array2: second array
        @return: list with the Coordinates which have changed example [ (1, 2), (3, 4), (5, 6) ]
        """
        out = []
        for i in range(len(array1)):
            for j in range(len(array1[i])):
                if array1[i][j] != array2[i][j]:
                    out.append((i, j))
        return out

    @staticmethod
    def getNumForCords(x: int, y: int, yLen: int):
        """
        calculates the Number in the Pixel String from Coordinates
        @param x: x value
        @param y: y value
        @param yLen: lengh of y (height value)
        @return: number in Pixel String
        """
        if (x % 2) == 0:
            n = y + (x * yLen)
        else:
            n = (x * yLen) + (yLen - y - 1)
        return n
