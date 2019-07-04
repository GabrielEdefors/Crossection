from tkinter import Tk, Label, Button, W, E, N, Entry, OptionMenu, StringVar, LabelFrame, Canvas
from Moment_capacity import M_Rd

import pandas as pd
from draw_beam import Illustrator


class CreateGUI:

    def __init__(self, parent):
        self.parent = parent
        parent.title("Cross section 2000")
        parent.geometry('500x500')

        self.exit = Button(parent, text="Exit", command=self.exit)
        self.exit.grid(row=7)

        self.calculate = Button(parent, text="Calculate", command=self.calculate_moment_capacity)
        self.calculate.grid(row=8)

        # Input - Geometric input ======================================================================================

        # Create a lableframe to store the geometry entrys in
        self.geometryframe = LabelFrame(parent, text="Geometry", padx=10, pady=5)
        self.geometryframe.grid(row=0, column=0, columnspan=5, rowspan=4)

        self.labeld = Label(self.geometryframe, text="d [m]")
        self.labeld.grid(row=0, column=0, sticky=E, padx=4)

        self.entryd = Entry(self.geometryframe, width=8)
        self.entryd.grid(row=0, column=1, padx=4, columnspan=1)

        self.labelb = Label(self.geometryframe, text="b [m]")
        self.labelb.grid(row=1, column=0, sticky=E, padx=4)

        self.entryb = Entry(self.geometryframe, width=8)
        self.entryb.grid(row=1, column=1, padx=4, columnspan=1)

        self.labeln = Label(self.geometryframe, text="No\u0332 bars")
        self.labeln.grid(row=2, column=0, padx=4, columnspan=1)

        self.entryn = Entry(self.geometryframe, width=8)
        self.entryn.grid(row=2, column=1, padx=4, columnspan=1)

        # Create canvas for drawing a beam illustration ================================================================

        self.canvas = Canvas(self.geometryframe, width=300, height=200)
        self.canvas.grid(row=0, column=2, columnspan=1, rowspan=12)

        # Call draw_beam to draw a cross section of a beam
        Illustrator(self.parent, self.canvas)

        # Input - Partial coefficients =================================================================================

        # Create a labeframe to store the partial coefficient entrys in
        self.partialframe = LabelFrame(parent, text="Partial coefficients" + " \u03B3")
        self.partialframe.grid(row=7, column=2, columnspan=4, rowspan=5)

        self.label_concrete = Label(self.partialframe, text="concrete")
        self.label_concrete.grid(row=0, sticky=E)

        self.entry_concrete = Entry(self.partialframe)
        self.entry_concrete.grid(row=0, column=1)

        self.label_steel = Label(self.partialframe, text="steel")
        self.label_steel.grid(row=1, sticky=E)

        self.entry_steel = Entry(self.partialframe)
        self.entry_steel.grid(row=1, column=1)

        # Input - Reinforcement type ===================================================================================

        # Import reinforcement specs
        self.reinforcement_table = pd.read_excel('InputData.xlsx', 'Reinforcement')

        # Use the diamter as index
        self.reinforcement_table.set_index('Diameter', inplace=True)

        # Add a column with reinforcement name
        self.reinforcement_table['name'] = '\u03D5' + self.reinforcement_table.index.astype(str) + 'B500B'


        # Create drop down menu
        self.initial_value_reinforcement = StringVar(parent)
        self.initial_value_reinforcement.set(self.reinforcement_table.iloc[3 ,-1])

        self.popupMenu = OptionMenu(parent, self.initial_value_reinforcement, * self.reinforcement_table.name)
        self.popupMenu.grid(row=6, column=1)

        # Input - Concrete type ========================================================================================

        # Import concrete specs
        self.concrete_series = pd.read_excel('InputData.xlsx', 'Concrete')
        self.concrete_series['name'] = (self.concrete_series['Strength'] / 1e+6).astype(str) + ' MPa'

        # Create drop down menu
        self.initial_value_concrete = StringVar(parent)
        self.initial_value_concrete.set(self.concrete_series.iloc[0, -1])

        self.dropdownmenu_concrete = OptionMenu(parent, self.initial_value_concrete, *self.concrete_series.name)
        self.dropdownmenu_concrete.grid(row=9, column=1)

    def exit(self):
        parent.destroy()

    def calculate_moment_capacity(self):

        # Retrieve values from GUI window
        d = float(self.entryd.get())
        b = float(self.entryb.get())
        n = float(self.entryn.get())
        partial_coefficient_concrete = float(self.entry_concrete.get())
        partial_coefficient_steel = float(self.entry_steel.get())
        reinforcement_type = self.initial_value_reinforcement.get()
        fck_name = self.initial_value_concrete.get()

        # Calculate reinforcement area
        Asi = self.reinforcement_table.loc[self.reinforcement_table['name'] == reinforcement_type, 'Area'].item()
        As = n * Asi

        # Retrieve value for steel stiffness
        Es = self.reinforcement_table.loc[self.reinforcement_table['name'] == reinforcement_type, 'Stiffness'].item()

        # Calculate design values based on partial coefficients
        fyk = self.reinforcement_table.loc[self.reinforcement_table['name'] == reinforcement_type, 'Strength'].item()
        fyd = partial_coefficient_steel * fyk

        fck = self.concrete_series.loc[self.concrete_series['name'] == fck_name, 'Strength'].item()

        fcd = partial_coefficient_concrete * fck

        answer_MRd = M_Rd(d, b, As, fcd, fyd, Es)

        print(answer_MRd)


if __name__ == "__main__":
    parent = Tk()
    GUI_instance = CreateGUI(parent)
    parent.mainloop()




