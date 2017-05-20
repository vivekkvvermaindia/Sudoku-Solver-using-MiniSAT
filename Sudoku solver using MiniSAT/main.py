import os
import sys
import string
import re
import Tkinter as tk
from constraint import Row, Column, smallbox, value, individual
from utils import convertBase9


#encodes input file into one string
def parseFile(filename):
  open_file = open(filename)
  content = open_file.readlines()
  encodedLine = ""
  for line in content:
    encodedLine += ''.join(line.split())
  return encodedLine

#-----genGrid(filename)-----#
#create a 2 by 2 array of the input puzzle
def genGrid(string):
  arr = [[0 for x in range(9)] for x in range(9)]
  for i in range(9):
    for j in range(9):
      arr[i][j] = string[ i * 9 + j ] 
  return arr


#-----MAIN-----#

line = parseFile(sys.argv[1])
grid = genGrid(line) #generate grid

#generate minimal clauses
clauses = 0
f = open('tempOutput.txt', 'w')
clauses += value(f, grid) #generate prefilled value from user input
clauses += individual(f, grid) #generate individual cells
clauses += Column(f, grid) #generate column constraints
clauses += Row(f, grid) #generate row constraints
clauses += smallbox(f, grid) #generate a list of boxes (3x3)
f.close()

f = open('tempOutput.txt','r')
temp = f.read()
f.close()

f = open('tempOutput.txt', 'w')
f.write("p cnf 729 " + str(clauses) + "\n")

f.write(temp)
f.close()

cmd = './minisat tempOutput.txt SATOutput.txt'
os.system(cmd)

# Decode output file
f = open('SATOutput.txt','r')
sat = f.readline().strip()

open_file = open("SolvedPuzzle.txt", 'w')
if(sat == 'SAT'):
  numbers = f.readline()
  asArr = numbers.split(' ')

  for i in range(len(asArr)):
    asArr[i] = int(asArr[i])

  for y in range(9):
    line = ''
    for x in range(9):
      for z in range(9):
        if(asArr[y*81 + 9*x + z] >= 0):
          line = line + str(z + 1) + ' '
          break
    #print(line + '\n')
    open_file.write(line + '\n')
else:
  print('\nProblem is unsatisfiable.')
  open_file.write("'\nProblem is unsatisfiable.'")
open_file.write('\n\n')
open_file.close()

#----GUI OUTPUT----#
f=open("SolvedPuzzle.txt")
class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, 9,9)
        t.pack(side="top", fill="x")

class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=9, columns=9):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
	    z=f.readline()
	    k=0
            for column in range(columns):
		a=z[k]
		#print a
                label = tk.Label(self, text = a, 
                                 borderwidth=0, width=5)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
		k=k+2
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()

