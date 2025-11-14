import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox
import random

CELL_FONT = ("Consolas", 16)
PUZZLE_COLOR = "#1b1b1b"
USER_COLOR = "#1976d2"
BG_COLOR = "#f0f4f8"
BORDER_COLOR = "#9e9e9e"

class SudokuApp:
    def __init__(self, root, df):
        self.root = root
        self.df = df
        self.quiz_grid = None
        self.solution_grid = None
        self.entries = []

        self.root.title("🧩 Sudoku Game View")
        self.root.configure(bg=BG_COLOR)
        self.create_widgets()
        self.load_new_puzzle()

    def create_widgets(self):
        title = tk.Label(self.root, text="Sudoku Game Board",
                         font=("Arial", 22, "bold"), bg=BG_COLOR, fg=PUZZLE_COLOR)
        title.pack(pady=15)

        self.grid_frame = tk.Frame(self.root, bg=BORDER_COLOR, padx=4, pady=4)
        self.grid_frame.pack()

        # Create 9x9 Entry grid
        for i in range(9):
            row_entries = []
            for j in range(9):
                outer_frame = tk.Frame(self.grid_frame, bd=1)
                outer_frame.grid(row=i, column=j, padx=(2 if j % 3 == 0 else 1), pady=(2 if i % 3 == 0 else 1))

                e = tk.Entry(outer_frame, width=2, font=CELL_FONT,
                             justify="center", bd=0, relief="solid", bg="white")
                e.pack()
                row_entries.append(e)
            self.entries.append(row_entries)

        # Buttons
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="✔️ Check", font=("Arial", 12, "bold"),
                  command=self.check_solution, bg="#4caf50", fg="white", padx=10).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="💡 Show Solution", font=("Arial", 12, "bold"),
                  command=self.show_solution, bg="#2196f3", fg="white", padx=10).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="🔁 New Puzzle", font=("Arial", 12, "bold"),
                  command=self.load_new_puzzle, bg="#f57c00", fg="white", padx=10).grid(row=0, column=2, padx=5)

    def load_new_puzzle(self):
        self.clear_grid()
        idx = random.randint(0, len(self.df) - 1)
        self.quiz_grid = self.parse_grid(self.df.loc[idx, "quizzes"])
        self.solution_grid = self.parse_grid(self.df.loc[idx, "solutions"])

        for i in range(9):
            for j in range(9):
                val = self.quiz_grid[i][j]
                entry = self.entries[i][j]
                entry.config(state='normal', fg=PUZZLE_COLOR, bg="white")
                if val != 0:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(val))
                    entry.config(state='disabled', disabledforeground=PUZZLE_COLOR, disabledbackground="#e0e0e0")
                else:
                    entry.delete(0, tk.END)
                    entry.config(bg="#ffffff")

    def clear_grid(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].config(state='normal')
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(bg="white")

    def parse_grid(self, grid_str):
        return np.array([int(ch) for ch in grid_str]).reshape((9, 9))

    def check_solution(self):
        correct = True
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                if self.quiz_grid[i][j] == 0:
                    val = entry.get()
                    if not val.isdigit() or int(val) != self.solution_grid[i][j]:
                        correct = False
                        entry.config(fg="red", bg="#ffe6e6")
                    else:
                        entry.config(fg=USER_COLOR, bg="#e8f5e9")
        if correct:
            messagebox.showinfo("🎉 Correct!", "You solved the puzzle!")
        else:
            messagebox.showwarning("❌ Try Again", "There are incorrect entries.")

    def show_solution(self):
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.config(state='normal')
                entry.delete(0, tk.END)
                entry.insert(0, str(self.solution_grid[i][j]))
                entry.config(state='disabled', disabledforeground=USER_COLOR, disabledbackground="#d6f0ff")

# Load CSV
try:
    df = pd.read_csv("sudoku.csv")
except FileNotFoundError:
    messagebox.showerror("Missing File", "sudoku_dataset.csv not found in the folder.")
    exit()

# Run App
root = tk.Tk()
app = SudokuApp(root, df)
root.mainloop()
