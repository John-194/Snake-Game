class Snake:
    def __init__(self, land):
        self.coords = [[land.rows // 2 - 1, land.cols // 2 - 1]]  # queue
        self.currentMap = land
        self.headIndex = 0
        self.draw()
        self.lastMove = None

    def move(self, direction = " "):
        moveTo = self.coords[self.headIndex].copy()

        opposite = {"d":"a", "w": "s", "a":"d", "s":"w", None : None}
        if direction == " " or direction == opposite[self.lastMove]:
            direction = self.lastMove
        if direction == "w":  # new head coords move forward
            moveTo[0] -= 1
        elif direction == "s":
            moveTo[0] += 1
        elif direction == "d":
            moveTo[1] += 1
        elif direction == "a":
            moveTo[1] -= 1

        result = self.currentMap.getTerrain(moveTo)  # Gets future head position terrain
        if moveTo == self.coords[self.headIndex-1]:
            return True
        self.lastMove = direction
        if result != " ":  # Evaluates the terrain. Must be done before terrain changes
            if result == "F":
                self.currentMap.spawnFood()
            else:
                return False

        self.erase()
        if self.coords[self.headIndex] != self.coords[
            self.headIndex - 1]:  # if head has been duplicated: tail stays in place (head does not increment to the tail)
            self.headIndex += 1
            if self.headIndex == len(self.coords):
                self.headIndex = 0
        self.coords[self.headIndex] = moveTo  # Moves snake
        self.draw()
        if result == "F":  # Duplicates head if it has moved onto food
            self.snakeGrow()
        return True

    def snakeGrow(self):
        self.coords.insert(self.headIndex, self.coords[self.headIndex].copy())  # grow if eaten food
        self.headIndex += 1

    def erase(self, extra=()):
        self.currentMap.setTerrain(extra, " ")
        for coord in self.coords:
            self.currentMap.setTerrain(coord, " ")

    def draw(self):
        for coord in self.coords:
            self.currentMap.setTerrain(coord, "S")
        self.currentMap.setTerrain(self.coords[self.headIndex], "H")


class Map:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.terrain = [["O" if row == 0 or row == self.rows - 1 or col == 0 or col == self.cols - 1 else " " for col in
                         range(cols)] for row in range(rows)]
        self.food = self.spawnFood()

    def spawnFood(self):
        freeSpace = []
        for row in range(1, len(self.terrain) - 1):
            for col in range(1, len(self.terrain[0]) - 1):
                if self.terrain[row][col] == " ":
                    freeSpace.append([row, col])

        if len(freeSpace) == 0:
            return False

        self.food = random.choice(freeSpace)

        row, col = self.food[0], self.food[1]
        self.terrain[row][col] = "F"

    def setTerrain(self, coord, a):
        if len(coord) == 0: return
        self.terrain[coord[0]][coord[1]] = a

    def getTerrain(self, coord):
        return self.terrain[coord[0]][coord[1]]

    def drawMap(self):
        os.system('cls')
        for r, row in enumerate(self.terrain):
            print()
            for c, col in enumerate(row):
                print(col, end="  ")


def win(a):
    if not a:
        print("Lost the game")
    if a:
        print("Won the game")



import random

if __name__ == "__main__":
    import os

    land = Map(5, 5)
    snake = Snake(land)
    controls, i = ["w", "a", "s", "d", "e"], None
    while i != "e":
        land.drawMap()
        while i not in controls:
            i = input()
        snake.move(i)
        i = None
