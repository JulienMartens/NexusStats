import sys
import ctypes
from tkinter import *
from tkinter import filedialog
from Classes.Population import Population
from Classes.ComparatifPopulations import ComparatifPopulations

if 'win' in sys.platform:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
root = Tk()
root.withdraw()

population1= Population()
population2= Population()
emplacement1 = filedialog.askdirectory()
emplacement2 = filedialog.askdirectory()

population1.depuisDossier(emplacement1)
if emplacement2 !="":
    population2.depuisDossier(emplacement2)


comparaison = ComparatifPopulations(population1,population2)