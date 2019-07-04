from tkinter import Canvas

class Illustrator:

    def __init__(self, parent, canvas_object):
        self.parent = parent
        self.canvas = canvas_object
        self.c = 10

        # Parametrize the width and height of the canvas
        self.parent.update_idletasks()
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()

        self.draw_beam()
        self.draw_rulers()
        self.add_reinforcment()

    def draw_beam(self):

        # Create frame for the canvas
        self.canvas.create_rectangle(5, 5, self.width-5, self.height-5, outline="#000000")

        # Draw the beam
        self.canvas.create_rectangle(self.width/4, self.height/3, 3*self.width/4, 2*self.height/3, outline="#000000")

    def draw_rulers(self):

        # Draw the wisth ruler
        self.canvas.create_line(self.width/4, 2*self.height/3+10, 3*self.width/4, 2*self.height/3+10, fill="#000000")
        self.canvas.create_line(self.width/4, 2*self.height/3+7,self.width/4 ,2*self.height/3+14, fill="#000000")
        self.canvas.create_line(3*self.width/4, 2 * self.height/3+7, 3*self.width/4, 2*self.height/3+14, fill="#000000")

        # Add width text
        self.canvas.create_text(self.width/2,  2*self.height/3+18, text="b")

        # Draw the ruler for the inner lever arm
        self.canvas.create_line(self.width/4 - 10, self.height/3, self.width/4 - 10, 2*self.height/3 - self.c + 2.5, fill="#000000")
        self.canvas.create_line(self.width/4 - 14, self.height/3, self.width/4 - 6,  self.height/3, fill="#000000")
        self.canvas.create_line(self.width / 4 - 14, 2*self.height/3 - self.c + 2.5, self.width / 4 - 6,
                                2*self.height/3 - self.c + 2.5, fill="#000000")

        # Add height text
        self.canvas.create_text(self.width/4 - 18,  self.height/2, text="d")

    def add_reinforcment(self):

        # Parameters
        y_bars =   2 * self.height/3 - self.c
        diamter = 5

        # Divide the beam into five section
        delta_x = self.width / 2 / 5
        x0 = self.width/4

        for i in range(1, 5):
            x = x0 + delta_x*i
            self.canvas.create_oval(x, y_bars, x + diamter, y_bars + diamter, fill="#000000")






