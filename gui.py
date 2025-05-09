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
        self.root.geometry("450x520")
        self.brush = BaseBrush()
        self.brushrepr = "Base"

        self.root.columnconfigure((1,2), weight=1, uniform="a")
        self.root.columnconfigure((0,3), weight=1, uniform="a")
        #self.root.rowconfigure()

        self.BaseBrush_Button = tk.Button(self.root,text="Base", command=lambda:self.setbrush("Base"), width="5")
        self.BaseBrush_Button.grid(row=0, column=0, padx=5, pady=5, sticky="we")
        self.GliderBrush_Button = tk.Button(self.root,text="Glider", command=lambda:self.setbrush("Glider"), width="5")
        self.GliderBrush_Button.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        self.BlinkerBrush_Button = tk.Button(self.root,text="Blinker", command=lambda:self.setbrush("Blinker"), width="5")
        self.BlinkerBrush_Button.grid(row=0, column=2, padx=5, pady=5, sticky="we")
        self.PulsarBrush_Button = tk.Button(self.root,text="Pulsar", command=lambda:self.setbrush("Pulsar"), width="5")
        self.PulsarBrush_Button.grid(row=0, column=3, padx=5, pady=5, sticky="we")
        self.canvas = tk.Canvas(self.root, width=GRID_WIDTH*CELL_SIZE, height=GRID_HEIGHT*CELL_SIZE, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.draw_grid()
        self.start_button = tk.Button(self.root,text="Start", command=self.toggle_running, width="5")
        self.start_button.grid(row=2, column=1, padx=5, pady=5, sticky="we")
        self.step_button = tk.Button(self.root,text="Step", command=self.step, width="5")
        self.step_button.grid(row=2, column=2, padx=5, pady=5, sticky="we")
        self.info = tk.StringVar()
        self.info.set(f"Generation: 0 | Alive: 0 | Dead: {GRID_HEIGHT*GRID_WIDTH} | Brush: {self.brushrepr}")
        self.info_Label = tk.Label(self.root, textvariable=self.info)
        self.info_Label.grid(row=3, column=0, columnspan=4)
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