import tkinter as tk
from gol import GOL
from brush import BaseBrush, GliderBrush, BlinkerBrush, PulsarBrush

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20

class GolGUI:
    def __init__(self, gol: GOL):
        self.game = gol
        self.root = tk.Tk()
        self.root.title("Game of Life")
        self.brush = BaseBrush()
        self.brushrepr = "Base"
        self.BaseBrush_Button = tk.Button(self.root,text="Base", command=lambda:self.setbrush("Base"))
        self.BaseBrush_Button.pack()
        self.GliderBrush_Button = tk.Button(self.root,text="Glider", command=lambda:self.setbrush("Glider"))
        self.GliderBrush_Button.pack()
        self.BlinkerBrush_Button = tk.Button(self.root,text="Blinker", command=lambda:self.setbrush("Blinker"))
        self.BlinkerBrush_Button.pack()
        self.PulsarBrush_Button = tk.Button(self.root,text="Pulsar", command=lambda:self.setbrush("Pulsar"))
        self.PulsarBrush_Button.pack()
        self.canvas = tk.Canvas(self.root, width=GRID_WIDTH*CELL_SIZE, height=GRID_HEIGHT*CELL_SIZE, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.draw_grid()
        self.start_button = tk.Button(self.root,text="Start", command=self.toggle_running)
        self.start_button.pack()
        self.step_button = tk.Button(self.root,text="Step", command=self.step)
        self.step_button.pack()
        self.info = tk.StringVar()
        self.info.set(f"Generation: 0 | Alive: 0 | Dead: {GRID_HEIGHT*GRID_WIDTH} | Brush: {self.brushrepr}")
        self.info_Label = tk.Label(self.root, textvariable=self.info)
        self.info_Label.pack()
        self.is_running = False
        self.root.mainloop()

    def toggle_running(self):
        self.is_running = not self.is_running
        self.start_button.config(text="Pause" if self.is_running else "Start")
        if self.is_running:
            self.run()

    def run(self):
        if self.is_running:
            self.step()
            self.root.after(300, self.run)

    def step(self):
        self.game.next_state()
        self.draw_grid()
        self.update_info()

    def toggle_cell(self,event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        self.brush.apply(gol,row,col)
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                colour = "black" if self.game.board[r][c] == 1 else "white"
                self.canvas.create_rectangle(
                    c*CELL_SIZE,
                    r*CELL_SIZE,
                    (c+1)*CELL_SIZE,
                    (r+1)*CELL_SIZE,
                    fill=colour,
                    outline="gray"
                )

    def setbrush(self, brushtype):
        if brushtype == "Base":
            self.brush = BaseBrush()
        elif brushtype == "Glider":
            self.brush = GliderBrush()
        elif brushtype == "Blinker":
            self.brush = BlinkerBrush()
        elif brushtype == "Pulsar":
            self.brush = PulsarBrush()

        self.brushrepr = brushtype

        self.update_info()

    def update_info(self):

        statistics = gol.get_statistics()
        self.info.set(f"Generation: {statistics["generation"]} | Alive: {statistics["alive"]} | Dead: {statistics["dead"]} | Brush: {self.brushrepr}")

if __name__ == "__main__":
    gol = GOL(GRID_WIDTH, GRID_HEIGHT)
    GolGUI(gol)