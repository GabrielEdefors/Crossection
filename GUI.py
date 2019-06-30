from tkinter import Tk, Label, Button, W, E, N, Entry, OptionMenu, StringVar
from Moment_capacity import M_Rd
import pandas as pd


class CreateGUI:

    def __init__(self, parent):
        self.parent = parent
        parent.title("Cross section 2000")
        parent.geometry('500x500')

        self.exit = Button(parent, text="Exit", command=self.exit)
        self.exit.grid(row=7)

        self.calculate = Button(parent, text="Calculate", command=self.calculate_moment_capacity)
        self.calculate.grid(row=8)

        # Input - Effective height =====================================================================================
        self.labeld = Label(parent, text="d [m]")
        self.labeld.grid(row=1, sticky=E)

        self.entryd = Entry(parent)
        self.entryd.grid(row=1, column=1)

        # Input - Cross sectional width ================================================================================
        self.labelb = Label(parent, text="b [m]")
        self.labelb.grid(row=2, sticky=E)

        self.entryb = Entry(parent)
        self.entryb.grid(row=2, column=1)

        # Input - Design compressive strength ==========================================================================
        self.labelfcd = Label(parent, text="fcd [MPa]")
        self.labelfcd.grid(row=3, sticky=E)

        self.entryfcd = Entry(parent)
        self.entryfcd.grid(row=3, column=1)

        # Input - Reinforcement type ===================================================================================

        # Import reinforcement specs
        self.reinforcement_table = pd.read_excel('InputData.xlsx', 'Reinforcement')

        # Use the diamter as index
        self.reinforcement_table.set_index('Diameter', inplace=True)

        # Add a column with reinforcement name
        self.reinforcement_table['name'] = '\u03D5' + self.reinforcement_table.index.astype(str) + 'B500B'

        # Create label
        self.labeln = Label(parent, text="Number of bars ")
        self.labeln.grid(row=5, sticky=E)

        # Create drop down menu
        self.entryn = Entry(parent)
        self.entryn.grid(row=5, column=1)

        self.initial_value = StringVar(parent)
        self.initial_value.set(self.reinforcement_table.iloc[3 ,-1])

        self.popupMenu = OptionMenu(parent, self.initial_value, * self.reinforcement_table.name)
        self.popupMenu.grid(row=6, column=1)

    def exit(self):
        parent.destroy()

    def calculate_moment_capacity(self):

        d = self.entryd.get()
        b = self.entryb.get()
        fcd = self.entryfcd.get()
        n = self.entryn.get()
        reinforcment_type = self.initial_value.get()

        # Calculate reinforce ment area
        reinforcement_index = reinforcement_type
        As = n * self.reinforcement_table.loc[reinforcement_type, 'Area']

        print(As)




        #M_Rd(d, b, As, fcd, fyd, Es)


if __name__ == "__main__":
    parent = Tk()
    GUI_instance = CreateGUI(parent)
    parent.mainloop()




