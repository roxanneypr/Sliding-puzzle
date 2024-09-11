'''
Roxanne Ysabel P. Resuello
WX2L
A python app that allows user to play an 8-puzzle game. This puzzle can also show the solution using BFS and DFS.

'''
from util import Node, StackFrontier, QueueFrontier
import pygame
import random
import tkinter as tk
from tkinter import filedialog
import time

# Read the initial puzzle from a file
def readFile():
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    f = open("puzzle.in", "r")
    numSequence = f.read().split('\n')
    i = 0

    for num in numSequence:
        for j in range(3):
            board[i][j] = int(numSequence[i][j])
        
        i+=1
    f.close()
    return board


# Function for initialing puzzle, if will not read from a file
def initializePuzzle():
    puzzle = [[0, 0, 0],
              [0, 0, 0], 
              [0, 0, 0]]
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(nums)
    i = 0

    for x in range(3):
        for y in range(3):
            puzzle[x][y] = nums[i]
            i += 1
    return puzzle

# Render tiles on screen
def renderImages(screen, puzzle, tiles):
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != 0:
                image = tiles[puzzle[i][j] - 1]
                screen.blit(image, (j*200+52, i*200+60))
    return

# Get index of clicked tile
def getTile(x,y):
    puzzleIndex = [0, 0]
    if x <= 252:
        puzzleIndex[0] = 0
    elif x <= 452:
        puzzleIndex[0] = 1
    else:
        puzzleIndex[0] = 2

    if y <= 260:
        puzzleIndex[1] = 0
    elif y <= 460:
        puzzleIndex[1] = 1
    else:
        puzzleIndex[1] = 2
    return puzzleIndex

# Get the index of zero. If not besid the clicked index, return an empty list
def getZero(index, board):
    # index = [x,y] clicked tile index
    i = index[0] - 1
    k = index[1] - 1
    for v in range(i, index[0] + 2):
        for s in range(k, index[1] + 2):
            if v >= 0 and v < 3 and s >= 0 and s < 3:
                if (v == index[0] + 1 and s == index[1]) or (v == index[0] - 1 and s == index[1]) or (v == index[0] and s == index[1] + 1) or (v == index[0] and s == index[1] - 1):
                    if board[v][s] == 0:
                        return [v, s]

    return []

# Check if puzzle is solvable
def checkSolvable(puzzle):
    inversion = 0
    numSequence = []

    for i in range(3):
        for j in range(3):
            numSequence.append(puzzle[i][j])
    for i in range(9):
        for j in range(i+1, 9):
            
            if numSequence[i] > numSequence[j] and numSequence[i] != 0 and numSequence[j] != 0:
                inversion += 1
    if inversion % 2 == 0:
        return True

    return False

# Check if puzzle is solved
def isDone(puzzle):
    counter = 0
    for i in range(3):
        for j in range(3):
            #print(f'{counter + 1} - {puzzle[i][j]}')
            if i == 2 and j == 2:
                return True
            if counter + 1 != puzzle[i][j]:
                return False
            counter += 1
    
    return True

# Function for BFS
def bfs(puzzle):
    start_time = time.time()
    puzzle = readFile()
    counter = 0
    frontier = QueueFrontier()
    explored = set()
    empty = zeroIndex(puzzle)
    start = Node(state=puzzle, parent=None, action=None, emptyTile=empty, g=None, h=None)
    frontier.add(start)
    
    while True:
        
        if frontier.empty():
            return None
        
        currentState = frontier.remove()
        #print(f'exploring current state {currentState.state}')
        explored.add(tuple(map(tuple, currentState.state)))
        counter+=1
        print(counter)

        if (isDone(currentState.state)):
            #print("DONE")
            end_time = time.time()
            print(end_time - start_time)
            return currentState
        else:
            temp = [list(row) for row in currentState.state]

            for action in (getActions(temp)):
                parentpuzzle = [list(row) for row in temp]
                result = getResult(parentpuzzle, action)
                #print(f'result: {result}')
                #print(f'current: {temp}')
                newNode = Node(state=[list(row) for row in result], parent=currentState, action=action, emptyTile=zeroIndex(result), g=None, h=None)
                #currentState.state = parentpuzzle
                if tuple(map(tuple, result)) not in explored:
                    
                    #currentState.state = parentpuzzle
                    #print(newNode.state)
                    frontier.add(newNode)

# Function for DFS
def dfs(puzzle):
    start_time = time.time()
    puzzle = readFile()
    counter = 0
    frontier = StackFrontier()
    explored = set()
    empty = zeroIndex(puzzle)
    start = Node(state=puzzle, parent=None, action=None, emptyTile=empty, g=None, h=None )
    frontier.add(start)
    n = 0
    while True:
    
        if frontier.empty():
            return None
        
        currentState = frontier.remove()
        explored.add(tuple(map(tuple, currentState.state)))
        #print(f'exploring current state {currentState.state}')
        
        counter+=1
        print(counter)

        if (isDone(currentState.state)):
            #print("DONE")
            end_time = time.time()
            print(end_time - start_time)
            return currentState
        else:
            
            temp = [list(row) for row in currentState.state]

            for action in (getActions(temp)):
                parentpuzzle = [list(row) for row in temp]
                result = getResult(parentpuzzle, action)
                #print(f'result: {result}')
                #print(f'current: {temp}')
                newNode = Node(state=[list(row) for row in result], parent=currentState, action=action, emptyTile=zeroIndex(result), g=None, h=None)
                #currentState.state = parentpuzzle
                if tuple(map(tuple, result)) not in explored:
                    frontier.add(newNode)
            
            #frontier.removeMinF()
        #n += 1
    

    #print(explored)
        
# Get index of zero tile
def zeroIndex(puzzle):
    index = []
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == 0:
                 index = [i, j]
    return index

# Get actions available for the puzzle
def getActions(puzzle):
    actions = []
   
    index = zeroIndex(puzzle)
    x = index[0]
    y = index[1]
    if x - 1 >= 0:
        actions.append([x-1, y, 'U'])
    if y + 1 <= 2:
        actions.append([x, y+1, 'R'])
    if x + 1 <= 2:
        actions.append([x+1, y, 'D'])
    if y - 1 >= 0:
        actions.append([x, y-1, 'L'])
    #print(actions)
    return actions

# Get the resulting puzzle given the initial puzzle and the action to be applied
def getResult(puzzle, action):

    if len(action) == 3:
        movement = action[2]
        x = action[0]
        y = action[1]
    else:
        zero = zeroIndex(puzzle)
        #print(f'{x} - {y}')
        movement = action

        if action == 'U':
            x = zero[0] - 1
            y = zero[1]
        elif action == 'R':
            x = zero[0]
            y = zero[1] + 1
        elif action == 'D':
            x = zero[0] + 1
            y = zero[1]
        else:
            x = zero[0]
            y = zero[1] - 1

    temp = puzzle[x][y]

    #print(f'\npuzzle in result: {puzzle}')
    #print(f'action in result: {movement}')

    if movement == 'U':
        puzzle[x+1][y] = temp
        puzzle[x][y] = 0
        #print(f'Switched with upper tile {puzzle}')
    elif movement == 'R':
        puzzle[x][y-1] = temp
        puzzle[x][y] = 0
        #print(f"Switched with right tile {puzzle}")
    elif movement == 'D':
        puzzle[x-1][y] = temp
        puzzle[x][y] = 0
        #print(f"Switched with down tile {puzzle}")
    else:
        puzzle[x][y+1] = temp
        puzzle[x][y] = 0
        #print(f"Switched with left tile {puzzle}")
    return puzzle

# Get the path cost
def pathcost():
    cost = 0
    try:
        f = open("puzzle.out", "r")
        path = f.read()
        #print(path)
        cost += len(path)
        return cost
    except:
        print("File doesn't exist.")

    return None

# Write path to a file
def writePath(node):
    f = open("puzzle.out", "w+")
    path = []
    explored = []
    pathInFile = ''
    while node.parent is not None:
        path.append(node.action)
        explored.append(node.state)
        node = node.parent

    path.reverse()
    explored.reverse()

    for action in path:
        f.write(f'{action[2]}')
        pathInFile += action[2]
    #print(f'path: {path}')
    #print(f'puzzles: {explored}')
    f.close()

    return pathInFile

# implements a* function
def aStar(puzzle):
    start_time = time.time()
    puzzle = readFile()
    openList = StackFrontier()
    closed_set = set()
    g=0
    h=hfunc(puzzle)
    
    
    empty = zeroIndex(puzzle)
    start = Node(state=puzzle, parent=None, action=None, emptyTile=empty, g=0, h=h)
    openList.add(start)
    counter=0

    while openList:
        if openList.empty():
            return None
        
        bestNode = openList.removeMinF()
        
        counter+=1
        #print(f'exploring current state {bestNode.state}')
        #print(counter)
        if isDone(bestNode.state):
            #path = writePath(bestNode)
            end_time = time.time()
            print(end_time - start_time)
            return bestNode
        else:
            closed_set.add(tuple(map(tuple, bestNode.state)))

            temp = [list(row) for row in bestNode.state]

            for action in (getActions(temp)):
                
                parentpuzzle = [list(row) for row in temp]
                xstate = getResult(parentpuzzle, action)
                
                x = Node(state=[list(row) for row in xstate], parent=bestNode, action=action, emptyTile=zeroIndex(xstate), g = bestNode.g + 1, h=hfunc(xstate))
                #x = getResult(bestNode.state, action)
                duplicate = openList.contains_state(x)
                #if (not openList.contains_state(x) or x not in closedList) or (openList.contains_state(x) and x.g < duplicate.g):
                    #x.parent = bestNode
                if tuple(map(tuple, xstate)) not in closed_set:
                    #print(f'IN: {xstate} - h: {hfunc(xstate)} - g{bestNode.g + 1}')
                    openList.add(x)


'''
- Author: Saturn Cloud 
- Date: July 18 2023
- Title of program/source code: Solving The 8 Puzzle With A* Algorithm
- Code version
- Type: source code
- Web address: https://saturncloud.io/blog/solving-the-8-puzzle-with-a-algorithm/
'''
#heuristic function
def hfunc(puzzle):
    hscore = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != 0:
                row = (puzzle[i][j] - 1) // 3
                col = (puzzle[i][j] - 1) % 3
                hscore += abs(row - i) + abs(col - j)
    return hscore

#Function for reading/uploading new file
def read_file():
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    root = tk.Tk()
    root.withdraw()

    path = str(filedialog.askopenfilename())

    if path:
        try:
            f = open(path, "r")
            numSequence = f.read().split('\n')
            i = 0

            for num in numSequence:
                for j in range(3):
                    board[i][j] = int(numSequence[i][j])
                
                i+=1
            f.close()
        except:
            print("Input file Error")
            root.destroy()
            return None
    else:
        root.destroy()
        return None
    
    root.destroy()
    return board

#Changes puzzle.in to the newly upload file
def changeInputFile(puzzle):
    f = open("puzzle.in", "w+")
    numSequence = ''

    for row in puzzle:
        for j in row:
            numSequence += str(j)

    counter = 0
    print(numSequence)
    for i in range(3):
        for j in range(3):
            f.write(f'{numSequence[counter]}')
            counter+=1
        if counter != 9:
            f.write('\n')
    f.close()
    return



def main():
    
    # Initialize screen
    pygame.font.init()
    pygame.init()
    pygame.display.set_caption("Sliding Puzzle")
    screen = pygame.display.set_mode((700, 800))
    #BFSbutton = pygame.Rect(70, 700, 100, 30)
    #DFSbutton = pygame.Rect(70, 740, 100, 30)
    #nextbutton = pygame.Rect(190, 700, 60, 60)

    # Initialize variables
    bg = pygame.image.load('images/background.png')
    solvableText = pygame.image.load('images/solvable.png')
    notsolvableText = pygame.image.load('images/notsolvable.png')
    play = pygame.image.load('images/play.png')
    bfsButton = pygame.image.load('images/bfs.png')
    dfsButton = pygame.image.load('images/dfs.png')
    astarButton = pygame.image.load('images/a*.png')
    uploadButton = pygame.image.load('images/upload.png')
    winText = pygame.image.load('images/win.png')
    pathCostSolved = pygame.image.load('images/pathcost.png')
    ONE = pygame.image.load('images/1.png')
    TWO = pygame.image.load('images/2.png')
    THREE = pygame.image.load('images/3.png')
    FOUR = pygame.image.load('images/4.png')
    FIVE = pygame.image.load('images/5.png')
    SIX = pygame.image.load('images/6.png')
    SEVEN = pygame.image.load('images/7.png')
    EIGHT = pygame.image.load('images/8.png')

    TILES = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT]

    #puzzle = [[2,3,0], [1,5,6], [4,7,8]]
    #puzzle = initializePuzzle()
    puzzle = readFile()
    running = True
    solvable = checkSolvable(puzzle)
    done = False
    pathFound = False
    moveCounter = 0


    
    #aStar(puzzle)

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check if there is mouse click and if not yet solved
            if event.type == pygame.MOUSEBUTTONDOWN and done == False:
                y, x = pygame.mouse.get_pos()
                #print(f'{x} - {y}')
                if solvable and y >= 60 and y<=160 and x>= 690 and x<=730:
                    puzzle = readFile()
                    solvedNode = bfs(puzzle)
                    
                    if solvedNode is not None:
                        path = writePath(solvedNode)
                        cost = pathcost()
                        pathFound = True

                        if pathcost is not None:
                            print(f'Cost: {cost}')

                    else:
                        print("No solution")
                
                # next button
                if pathFound and y >= 300 and y<=380 and x>= 690 and x<=770:
                    #print(moveCounter)
                    if moveCounter < cost:
                        puzzle = getResult(puzzle, path[moveCounter])
                        moveCounter += 1
                        
                
                if solvable and y >= 60 and y<=160 and x>= 730 and x<=770:
                    print("DFS")
                    puzzle = readFile()
                    solvedNode = dfs(puzzle)

                    if solvedNode is not None:
                        path = writePath(solvedNode)
                        cost = pathcost()
                        pathFound = True

                        if pathcost is not None:
                            print(f'Cost: {cost}')

                    else:
                        print("No solution")

                if solvable and y >= 180 and y<=280 and x>= 690 and x<=730:
                    print("astar")
                    puzzle = readFile()
                    solvedNode = aStar(puzzle)

                    if solvedNode is not None:
                        path = writePath(solvedNode)
                        cost = pathcost()
                        pathFound = True

                        if pathcost is not None:
                            print(f'Cost: {cost}')

                    else:
                        print("No solution")
                
                if y >= 180 and y<=280 and x>= 730 and x<=770:
                    temp = read_file()
                    if temp:
                        puzzle = temp
                        changeInputFile(puzzle)

                # Check if mouse click is within the tiles
                if x >= 52 and x <= 652 and y >= 60 and y <= 660 and not pathFound:

                    # Get tile's index and zero's index
                    tileIndex = getTile(x, y)
                    zeroIndex = getZero(tileIndex, puzzle)

                    # If zero is beside the clicked tile, swith the clicked index and 0
                    if zeroIndex:
                        temp = puzzle[tileIndex[0]][tileIndex[1]]
                        puzzle[zeroIndex[0]][zeroIndex[1]] = temp
                        puzzle[tileIndex[0]][tileIndex[1]] = 0

                    # Check if puzzle is done
                    if isDone(puzzle):
                        done = True


        # Display background and render tiles
        screen.blit(bg, (0, 0))
        renderImages(screen, puzzle, TILES)
        
        #pygame.draw.rect(screen, (255,255,255), BFSbutton)
        #pygame.draw.rect(screen, (255,255,255), DFSbutton)
        #pygame.draw.rect(screen, (255,255,255), nextbutton)
        screen.blit(play, (300, 690))
        screen.blit(bfsButton, (60, 690))
        screen.blit(dfsButton, (60, 730))
        screen.blit(astarButton, (180, 690))
        screen.blit(uploadButton, (180, 730))

        # Display if puzzle is solvable or not 
        if solvable:
            screen.blit(solvableText,(430, 645))
        else:
            screen.blit(notsolvableText,(430, 645))

        # If puzzle is solved, display wining text
        if done:
            pygame.event.set_blocked(pygame.MOUSEMOTION)
            screen.blit(winText,(150, 250))

        if pathFound:
            my_font = pygame.font.SysFont('Comic Sans MS', 20)
            pathText = my_font.render(f'path : {path}', False, (255, 255, 255))
            screen.blit(pathText, (65,8))

        # Display path cost
        if pathFound and moveCounter == cost:
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            costText = my_font.render(f'{cost}', False, (255, 255, 255))
            pygame.event.set_blocked(pygame.MOUSEMOTION)
            screen.blit(pathCostSolved,(150, 250))
            screen.blit(costText, (405,395))
        
        pygame.display.update()


if __name__ == '__main__':
    main()
