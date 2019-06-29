from tkinter import Tk, Label, Button, W, E, N, Entry, OptionMenu, StringVar
from Moment_capacity import M_Rd


class CreateGUI:

    def __init__(self, parent):
        self.parent = parent
        parent.title("Cross section 2000")
        parent.geometry('500x500')

        self.exit = Button(parent, text="Exit", command=self.exit)
        self.exit.grid(row=7)

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

        # Input - Steel stiffness ======================================================================================
        self.labelEs = Label(parent, text="Es [GPa]")
        self.labelEs.grid(row=4, sticky=E)

        self.entryEs = Entry(parent)
        self.entryEs.grid(row=4, column=1)

        # Input - Reinforcement type ===================================================================================
        self.labeln = Label(parent, text="Number of bars ")
        self.labeln.grid(row=5, sticky=E)

        self.entryn = Entry(parent)
        self.entryn.grid(row=5, column=1)

        list_rebars = ['\u03D5' + '16B500B' ]

        initial_value = StringVar(parent)
        initial_value.set(list_rebars[0])


        self.popupMenu = OptionMenu(parent, initial_value, list_rebars)
        self.popupMenu.grid(row=6, column=1)



    def exit(self):
        parent.destroy()

    def calculate_moment_capacity(self):

        d = self.entryd.get()
        # M_Rd(d, b, As, fcd, fyd, Es)



parent = Tk()
GUI_instance = CreateGUI(parent)
parent.mainloop()

