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

        # Define canvas grid
        self.delta_x = self.width / 8
        delta_y = self.height / 7

        # Define beam dimensions
        self.beamwidth = 6 * self.delta_x
        self.beamheight = 4 * delta_y

        # Define the corners of the beam
        self.x1 = self.delta_x
        self.y1 = delta_y + self.beamheight
        self.x2 = self.width - self.delta_x
        self.y2 = delta_y + self.beamheight
        self.x3 = self.width - self.delta_x
        self.y3 = delta_y
        self.x4 = self.delta_x
        self.y4 = delta_y

        # x4,y4 ---------------------- x3,y3
        #   |                           |
        #   |                           |
        #   |                           |
        # x1,y1 ---------------------- x2,y2

        # Define margins for rulers
        self.margin_ruler = self.beamheight / 8
        self.ruler_end_length = self.margin_ruler

        # Define cover thickness
        self.c = self.margin_ruler

        self.draw_beam()
        self.draw_rulers()
        self.add_reinforcment()

    def draw_beam(self):

        # Draw the beam
        self.canvas.create_rectangle(self.x4, self.y4, self.x2, self.y2, outline="#000000")

    def draw_rulers(self):

        # Draw the wisth ruler
        self.canvas.create_line(self.x1, self.y1 + self.margin_ruler, self.x2, self.y2 + self.margin_ruler, fill="#000000")
        self.canvas.create_line(self.x1, self.y1 + self.ruler_end_length / 2,self.x1, self.y1 + 3 * self.ruler_end_length / 2, fill="#000000")
        self.canvas.create_line(self.x2, self.y2 + self.ruler_end_length / 2, self.x2, self.y2 + 3 * self.ruler_end_length / 2, fill="#000000")

        # Add width text
        self.canvas.create_text(self.width / 2, self.y1 + 2 * self.margin_ruler, text="b")

        # Draw the ruler for the inner lever arm
        self.canvas.create_line(self.x1 - self.margin_ruler, self.y4, self.x1 -self.margin_ruler, self.y1 - self.c, fill="#000000")
        self.canvas.create_line(self.x1 - 3 * self.ruler_end_length / 2, self.y4, self.x1 - self.ruler_end_length / 2,  self.y4, fill="#000000")
        self.canvas.create_line(self.x1 - 3 * self.ruler_end_length / 2, self.y1 - self.c, self.x1 - self.ruler_end_length / 2, self.y1 - self.c, fill="#000000")

        # Add height text
        self.canvas.create_text(self.x1 - 2 * self.margin_ruler,  self.y4 + self.beamheight / 2 - self.c / 2, text="d")

    def add_reinforcment(self):

        # Parameters
        y_bars = self.y1 - self.c
        diameter = 6
        n_bars = 5

        for i in range(1, n_bars + 1):
            x = self.x1 + self.delta_x * i
            self.canvas.create_oval(x, y_bars, x + diameter, y_bars + diameter, fill="#000000")






