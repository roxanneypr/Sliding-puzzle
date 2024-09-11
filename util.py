'''
Roxanne Ysabel P. Resuello
WX2L
A python app that allows user to play an 8-puzzle game. This puzzle can also show the solution using BFS and DFS.

'''





'''
- Author: Harvard 
- Date: September 17 2023
- Title of program/source code: CS50 AI Degrees
- Code version
- Type: source code
- Web address: 
'''

class Node():
    def __init__(self, state, parent, action, emptyTile, g, h):
        self.state = state
        self.parent = parent
        self.action = action
        self.tile = emptyTile
        self.g = g
        self.h = h
        
    def f(self):
        return self.g + self.h
    

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
    
    def removeMinF(self):
        
        if self.empty():
            raise Exception("empty frontier")
        else:
            for i in range(1, len(self.frontier)):

                key_item = self.frontier[i]
                j = i - 1

                while j >= 0 and self.frontier[j].f() > key_item.f():
                    # Shift the value one position to the left
                    # and reposition j to point to the next element
                    # (from right to left)
                    self.frontier[j + 1] = self.frontier[j]
                    j -= 1
                self.frontier[j + 1] = key_item


            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            #print(node.state)
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
