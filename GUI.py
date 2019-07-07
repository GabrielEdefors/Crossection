from tkinter import Tk, Label, Button, W, E, N, Entry, OptionMenu, StringVar, LabelFrame, Canvas
from Moment_capacity import M_Rd

import pandas as pd
from draw_beam import Illustrator


class CreateGUI:

    def __init__(self, parent):
        self.parent = parent
        parent.title("Cross section 2000")
        parent.geometry('450x500')
        parent.resizable(False,False)

        # Add icon for the window
        parent.iconbitmap('icon_beam_2000.ico')

        # Add exit button
        self.exit = Button(parent, text="Exit", command=self.exit, width=20)
        self.exit.grid(row=4, column=1, padx=60, pady=10)

        # Input - Geometric input ======================================================================================

        # Create a lableframe to store the geometry entrys in
        self.geometryframe = LabelFrame(parent, text="Geometry", padx=10, pady=10)
        self.geometryframe.grid(row=0, column=0, columnspan=4, sticky=W+E)

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

        # Input - Reinforcement type ===================================================================================

        # Import reinforcement specs
        self.reinforcement_table = pd.read_excel('InputData.xlsx', 'Reinforcement')

        # Use the diamter as index
        self.reinforcement_table.set_index('Diameter', inplace=True)

        # Add a column with reinforcement name
        self.reinforcement_table['name'] = '\u03D5' + self.reinforcement_table.index.astype(str) + 'B500B'

        # Create drop down menu
        self.initial_value_reinforcement = StringVar(parent)
        self.initial_value_reinforcement.set(self.reinforcement_table.iloc[3, -1])

        self.popupMenu = OptionMenu(self.geometryframe, self.initial_value_reinforcement, *self.reinforcement_table.name)
        self.popupMenu.grid(row=3, column=0, columnspan=2)

        # Create canvas for drawing a beam illustration ================================================================

        self.canvas = Canvas(self.geometryframe, width=300, height=140)
        self.canvas.grid(row=0, column=2, columnspan=1, rowspan=4)

        # Call draw_beam to draw a cross section of a beam
        Illustrator(self.parent, self.canvas)

        # Labelframe for material properties ===========================================================================

        # Create a labelframe for material inputs
        self.materialframe = LabelFrame(parent, text="Material properties", padx=40, pady=10)
        self.materialframe.grid(row=2, column=0, columnspan=4, sticky=W + E)

        # Create a labeframe to store the partial coefficient entrys in
        self.partialframe = LabelFrame(self.materialframe, text="Partial coefficients" + " \u03B3")
        self.partialframe.grid(row=0, column=0, columnspan=1, rowspan=1)

        self.label_concrete = Label(self.partialframe, text="concrete")
        self.label_concrete.grid(row=0, sticky=E, pady=5)

        self.entry_concrete = Entry(self.partialframe,  width=8)
        self.entry_concrete.grid(row=0, column=1, pady=5, padx=20, sticky=W)

        self.label_steel = Label(self.partialframe, text="steel")
        self.label_steel.grid(row=1, sticky=E, pady=5)

        self.entry_steel = Entry(self.partialframe,  width=8)
        self.entry_steel.grid(row=1, column=1, pady=5, padx=20, sticky=W)

        # Input - Concrete type ========================================================================================

        # Create labelframe for concrete strength
        self.concreteframe = LabelFrame(self.materialframe, text="Concrete properties")
        self.concreteframe.grid(row=0, column=1, columnspan=1, rowspan=1, padx=30)

        self.label_steel = Label(self.concreteframe, text="Choose concrete strength")
        self.label_steel.grid(row=0, sticky=E, pady=5, padx=20)

        # Import concrete specs
        self.concrete_series = pd.read_excel('InputData.xlsx', 'Concrete')
        self.concrete_series['name'] = (self.concrete_series['Strength'] / 1e+6).astype(str) + ' MPa'

        # Create drop down menu
        self.initial_value_concrete = StringVar(parent)
        self.initial_value_concrete.set(self.concrete_series.iloc[0, -1])

        self.dropdownmenu_concrete = OptionMenu(self.concreteframe, self.initial_value_concrete, *self.concrete_series.name)
        self.dropdownmenu_concrete.grid(row=1, column=0)

        # Labelframe for analysis ======================================================================================

        self.analysisframe = LabelFrame(parent, text="Analysis", padx=40, pady=10)
        self.analysisframe.grid(row=3, column=0, columnspan=4, sticky=W + E)

        self.calculate = Button(self.analysisframe, text="Calculate", command=self.calculate_moment_capacity,  width=20)
        self.calculate.grid(row=3, column=1, pady=15, padx=15)

        # Adding entry to accomondate the answer
        self.answerentry = Entry(self.analysisframe, text='', borderwidth=3)
        self.answerentry.grid(row=3, column=2, sticky=W, pady=15, padx=35)


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

        # Display answer
        self.answerentry.insert(0, str(round(answer_MRd / 1e+3, 2)) + " kNm")


if __name__ == "__main__":
    parent = Tk()
    GUI_instance = CreateGUI(parent)
    parent.mainloop()




