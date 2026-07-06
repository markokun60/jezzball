import pygame
from random import randint
from settings import *   
from themes import Theme
 
class Field:
    def __init__(self):
        self.set_cols_rows(COLS,ROWS)
        self.is_grid = True

    def set_cols_rows(self,cols:int,rows:int):
        self.rows = rows
        self.cols = cols
        self.cells = [[0 for y in range(rows)] for x in range(cols)]
        self.window_width = LEFT + self.cols * CELL_SIZE + RIGHT_EDGE
        self.window_height= TOP  + self.rows * CELL_SIZE + BOTTOM_EDGE

    def reset(self) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[col][row] = FREE

    def get_rect(self):
        return pygame.FRect(LEFT, TOP, self.cols * CELL_SIZE,self.rows * CELL_SIZE)
      
    def get_cell(self, position:tuple) -> tuple:
        (x,y) = position
        rect = self.get_rect()
        if x < rect.left or x > rect.right or y < rect.top or y > rect.bottom:return None

        col = int((x - rect.left) / CELL_SIZE)
        row = int((y - rect.top)  / CELL_SIZE)

        if row < 0 or row >= self.rows: return None
        return (col, row)   


    def get_cell_in_field(self, position:tuple) -> tuple:
        (x,y) = position

        rect = self.get_rect()
        if x < rect.left: 
            col = 0
        elif x >= rect.right: 
            col = self.cols -1
        else:
            col = int((x - rect.left) / CELL_SIZE)

        if y < rect.top: 
            row = 0
        elif y >= rect.bottom: 
            row = self.rows -1
        else:
            row = int((y - rect.left) / CELL_SIZE)

        return (col, row)    


    def mark_random(self,totals):
        i = 0
        while i < totals:
            r = randint(0,self.rows-1)
            c = randint(0,self.cols-1)
            if self.cells[c][r] == FREE: 
                self.cells[c][r] = MARKED
                i += 1

    def get_cell_rect(self, col:int, row:int) -> pygame.FRect:
        x = LEFT + col * CELL_SIZE
        y = TOP  + row * CELL_SIZE
        return pygame.FRect(x, y, CELL_SIZE, CELL_SIZE)

    def draw(self, screen:pygame.Surface) -> None: 
        clr_free = Theme.Current.closed_cell_color
        clr_bar = Theme.Current.open_cell_color        
        clr_brd  = Theme.Current.grid_color
        for row in range(self.rows):
            y = TOP  + row * CELL_SIZE
            for col in range(self.cols):
                x = LEFT + col * CELL_SIZE
                if self.cells[col][row] == FREE:
                    pygame.draw.rect(screen, clr_free, (x,y,CELL_SIZE,CELL_SIZE))
                    if self.is_grid:
                        pygame.draw.rect(screen, clr_brd, (x,y,CELL_SIZE,CELL_SIZE),1)
                elif self.cells[col][row] == BAR:                   
                    pygame.draw.rect(screen, clr_bar, (x,y,CELL_SIZE,CELL_SIZE))                       
                 

    def set_bar(self, rect:pygame.FRect,direction:str) -> None:
        if direction == HORIZONTAL:
            (col0,row) = self.get_cell_in_field((rect.left, rect.top))
            (col1,row) = self.get_cell_in_field((rect.right, rect.top))
            
            for col in range(col0, col1+1):
                self.cells[col][row] = BAR
        else:
            (col,row0) = self.get_cell_in_field((rect.left, rect.top))
            (col,row1) = self.get_cell_in_field((rect.left, rect.bottom))
            for row in range(row0, row1+1):
                self.cells[col][row] = BAR

    def change_marked_cells(self,old_value:int, new_value:int) ->  None: 
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[col][row] == old_value:
                    self.cells[col][row] = new_value

    def marked_cells(self, col0:int,row0:int) -> None:
        directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        for (r,c) in directions:
            row = row0 + r
            col = col0 + c   
            if 0 <= col < self.cols and 0 <= row < self.rows:
                if self.cells[col][row] == FREE:
                    self.cells[col][row] = MARKED
                    self.marked_cells(col,row)

    def count(self,value:int) -> int:
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[col][row] == value:
                    count += 1
        return count

    def print_cells(self) -> None:
        print('   ', end='')
        for col in range(self.cols):
            print(str(col+1), end=' ')
            if col < 10: print(' ', end='')
        print()
        #
        print('   ', end='')
        for col in range(self.cols):
            print('---', end='')
        print() 
        #
        for row in range(self.rows):
            print (str(row+1), end=' ')
            if row < 9: print(' ', end='')
            print('|', end=' ')
            for col in range(self.cols):
                print(self.cells[col][row], end='  ')
            print()                 
