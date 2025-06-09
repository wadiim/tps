import tkinter as tk
from tkinter import font

from tp import TP
from solver import *
from method import Method


class GUI(tk.Frame):

    MIN_SUPPLY_COUNT = 2
    MIN_DEMAND_COUNT = 2
    MAX_SUPPLY_COUNT = 8
    MAX_DEMAND_COUNT = 8

    ENTRY_WIDTH = 5

    METHODS = [m.name for m in Method]

    BASE_PADDING = 4
    BASE_FRAME_PADDING = 32

    def __init__(self, master):
        super().__init__(master)

        self.solution_cells = []
        self.demand_labels = []
        self.demand_entries = []
        self.supply_labels = []
        self.supply_entries = []
        self.cost_entries = []

        self.pack(expand=True)

        self.font = font.Font(self, size=16)
        
        self.method_frame = tk.Frame(master=self)
        self.method_frame.grid(
                row=0, column=0,
                padx=self.BASE_FRAME_PADDING,
                pady=self.BASE_FRAME_PADDING,
        )

        self.method = tk.StringVar(master)
        self.method.set(self.METHODS[0])
        self.method_label = tk.Label(
                self.method_frame, text="Method:", font=self.font,
        )
        self.method_label.grid(
                row=0, column=0, padx=self.BASE_PADDING,
        )
        self.method_menu = tk.OptionMenu(
                self.method_frame, self.method, *self.METHODS,
        )
        self.method_menu.grid(row=0, column=1)

        self.problem_solution_frame = tk.Frame(master=self)
        self.problem_solution_frame.grid(row=1, column=0)

        self.solution_frame = tk.Frame(self.problem_solution_frame)
        self.solution_frame.grid(
                row=0, column=1,
                padx=0.5*self.BASE_FRAME_PADDING,
                pady=self.BASE_FRAME_PADDING,
        )

        self.solution_frame_label = tk.Label(
                self.solution_frame, text="Solution", font=self.font,
                width=13, anchor="w",
        )
        self.solution_frame_label.grid(row=0, column=0)

        self.solution_frame_body = tk.Frame(self.solution_frame)
        self.solution_frame_body.grid(row=1, column=0)

        self.solution_demand_labels = []
        self.solution_supply_labels = []
        for i in range(self.MIN_SUPPLY_COUNT):
            self._increment_solution_rows()

            demand_label = tk.Label(
                    self.solution_frame_body, text=f"D{i+1}", font=self.font,
            )
            demand_label.grid(
                    row=0, column=i+1,
                    padx=self.BASE_PADDING, pady=self.BASE_PADDING,
            )
            self.solution_demand_labels.append(demand_label)

        self.total_cost_label = tk.Label(
                self.solution_frame_body, text="Cost:", font=self.font,
        )
        self.total_cost_label.grid(
                row=self.MAX_SUPPLY_COUNT+1, column=1,
                padx=self.BASE_PADDING, pady=self.BASE_PADDING,
        )

        self.total_cost_val_label = tk.Label(
                self.solution_frame_body, font=self.font,
        )
        self.total_cost_val_label.grid(
                row=self.MAX_SUPPLY_COUNT+1, column=2,
                padx=self.BASE_PADDING, pady=self.BASE_PADDING,
        )

        # For alignment purposes only.
        tk.Label(self.solution_frame_body, font=self.font).grid(
                row=self.MAX_SUPPLY_COUNT+2, column=1,
                padx=self.BASE_PADDING, pady=self.BASE_PADDING,
        )
        tk.Label(
                self.solution_frame_body, font=self.font, width=12,
        ).grid(
                row=1, column=self.MAX_DEMAND_COUNT+1,
                padx=self.BASE_PADDING, pady=self.BASE_PADDING,
        )

        self.problem_frame = tk.Frame(self.problem_solution_frame)
        self.problem_frame.grid(
                row=0, column=0,
                padx=0.5*self.BASE_FRAME_PADDING,
                pady=self.BASE_FRAME_PADDING,
        )

        self.problem_frame_label = tk.Label(
                self.problem_frame, text="Problem", font=self.font,
                width=12, anchor="w",
        )
        self.problem_frame_label.grid(row=0, column=0)

        self.problem_frame_body = tk.Frame(self.problem_frame)
        self.problem_frame_body.grid(row=1, column=0)

        for i in range(self.MIN_SUPPLY_COUNT):
            demand_label = tk.Label(
                    self.problem_frame_body, text=f"D{i+1}", font=self.font,
            )
            demand_label.grid(
                    row=0, column=i+1,
                    padx=self.BASE_PADDING, pady=self.BASE_PADDING,
            )
            self.demand_labels.append(demand_label)

            demand_entry = tk.Entry(
                    self.problem_frame_body,
                    width=self.ENTRY_WIDTH,
                    font=self.font,
            )
            demand_entry.grid(
                    row=self.MAX_SUPPLY_COUNT+1, column=i+1,
                    padx=self.BASE_PADDING, pady=self.BASE_PADDING,
            )
            self.demand_entries.append(demand_entry)

        self.demand_row_label = tk.Label(
                self.problem_frame_body, text="Demand", font=self.font,
        )
        self.demand_row_label.grid(
                row=self.MAX_SUPPLY_COUNT+1, column=0,
                padx=self.BASE_PADDING, pady=self.BASE_PADDING,
        )

        for i in range(self.MIN_SUPPLY_COUNT):
            self._increment_supply_count()

        self.supply_col_label = tk.Label(
                self.problem_frame_body, text="Supply", font=self.font,
        )
        self.supply_col_label.grid(
                row=0, column=self.MAX_DEMAND_COUNT+1,
        )

        self.demand_count_pm_frame = tk.Frame(self.problem_frame_body)
        self.demand_count_pm_frame.grid(
                row=1, column=self.MAX_DEMAND_COUNT+2,
                padx=self.BASE_PADDING, pady=self.BASE_PADDING,
        )

        demand_count_minus_button = tk.Button(
                self.demand_count_pm_frame, text="-",
        )
        demand_count_minus_button.bind(
                '<Button-1>', self._decrement_demand_count,
        )
        master.bind('<Control-h>', self._decrement_demand_count)
        demand_count_minus_button.pack(side="left")

        demand_count_plus_button = tk.Button(
                self.demand_count_pm_frame, text="+",
        )
        demand_count_plus_button.bind(
                '<Button-1>', self._increment_demand_count,
        )
        master.bind('<Control-l>', self._increment_demand_count)
        demand_count_plus_button.pack(side="right")

        self.supply_count_pm_frame = tk.Frame(self.problem_frame_body)
        self.supply_count_pm_frame.grid(
                row=self.MAX_SUPPLY_COUNT+2, column=1,
                padx=self.BASE_PADDING, pady=self.BASE_PADDING,
        )

        supply_count_minus_button = tk.Button(
                self.supply_count_pm_frame, text="-",
        )
        supply_count_minus_button.bind(
                '<Button-1>', self._decrement_supply_count,
        )
        master.bind('<Control-k>', self._decrement_supply_count)
        supply_count_minus_button.pack(side="left")

        supply_count_plus_button = tk.Button(
                self.supply_count_pm_frame, text="+",
        )
        supply_count_plus_button.bind(
                '<Button-1>', self._increment_supply_count,
        )
        master.bind('<Control-j>', self._increment_supply_count)
        supply_count_plus_button.pack(side="right")

        self.solve_frame = tk.Frame(master=self)
        self.solve_frame.grid(
                row=2, column=0,
                padx=self.BASE_FRAME_PADDING,
                pady=self.BASE_FRAME_PADDING,
        )

        self.solve_button = tk.Button(
                self.solve_frame, text="Solve", font=self.font,
        )
        self.solve_button.bind('<Button-1>', self._solve)
        self.solve_button.pack()

    def _solve(self, _=None):
        costs = self._get_costs()
        supplies = self._get_supplies()
        demands = self._get_demands()

        tp = TP(costs, supplies, demands)
        cost_rows, cost_cols = len(tp.costs), len(tp.costs[0])
        tp.balance()

        if len(tp.costs) > cost_rows:
            self._increment_supply_count()
            for cost in self.cost_entries[-1]:
                cost.insert(0, "0")
            self.supply_entries[-1].insert(0, tp.supplies[-1])
        elif len(tp.costs[0]) > cost_cols:
            self._increment_demand_count()
            for cost_row in self.cost_entries:
                cost_row[-1].insert(0, "0")
            self.demand_entries[-1].insert(0, tp.demands[-1])

        method = Method.NorthWestCornelCell
        for m in Method:
            if self.method.get() == m.name:
                method = m
                break

        solver = None
        match method:
            case Method.NorthWestCornelCell:
                solver = NorthWestCellMethodSolver
            case Method.RowMinima:
                solver = RowMinimaMethodSolver
            case Method.ColMinima:
                solver = ColMinimaMethodSolver
            case Method.VogelsApproximation:
                solver = VogelsApproximationMethodSolver

        solution, total_cost = solver.solve(tp)

        for y in range(len(solution)):
            for x in range(len(solution[y])):
                self.solution_cells[y][x].delete(0, tk.END)
                self.solution_cells[y][x].insert(0, solution[y][x])

        self.total_cost_val_label.config(text=total_cost)

    def _get_costs(self):
        ret = []

        for cost_row in self.cost_entries:
            new_row = []
            for cost in cost_row:
                c = cost.get()
                if c == "": c = 0
                new_row.append(float(c))
            ret.append(new_row)

        return ret

    def _get_supplies(self):
        ret = []

        for supply in self.supply_entries:
            s = supply.get()
            if s == "": s = 0
            ret.append(float(s))

        return ret

    def _get_demands(self):
        ret = []

        for demand in self.demand_entries:
            d = demand.get()
            if d == "": d = 0
            ret.append(float(d))

        return ret

    def _increment_supply_count(self, _=None):
        if len(self.cost_entries) >= self.MAX_SUPPLY_COUNT:
            return

        demand_count = self.MIN_DEMAND_COUNT
        if len(self.cost_entries) > 0:
            demand_count = len(self.cost_entries[-1])

        self.cost_entries.append([])

        supply_label = tk.Label(
                self.problem_frame_body,
                text=f"S{len(self.cost_entries)}",
                font=self.font,
                anchor="e",
                width=6,
        )
        supply_label.grid(
                row=len(self.cost_entries), column=0,
                padx=self.BASE_PADDING, pady=self.BASE_PADDING,
        )
        self.supply_labels.append(supply_label)

        for i in range(demand_count):
            cost_entry = tk.Entry(
                    self.problem_frame_body,
                    width=self.ENTRY_WIDTH,
                    font=self.font,
            )
            cost_entry.grid(
                    row=len(self.cost_entries),
                    column=len(self.cost_entries[-1])+1,
                    padx=self.BASE_PADDING, pady=self.BASE_PADDING,
            )
            self.cost_entries[-1].append(cost_entry)

        supply_entry = tk.Entry(
                self.problem_frame_body,
                width=self.ENTRY_WIDTH,
                font=self.font,
        )
        supply_entry.grid(
                row=len(self.cost_entries),
                column=self.MAX_DEMAND_COUNT+1,
                padx=self.BASE_PADDING, pady=self.BASE_PADDING,
        )
        self.supply_entries.append(supply_entry)

        self._increment_solution_rows()

    def _decrement_supply_count(self, _=None):
        if len(self.cost_entries) <= self.MIN_SUPPLY_COUNT:
            return

        for entry in self.cost_entries[-1]:
            entry.grid_forget()
        self.cost_entries.pop()

        self.supply_labels.pop().grid_forget()
        self.supply_entries.pop().grid_forget()
        self._decrement_solution_rows()

    def _increment_demand_count(self, _=None):
        if len(self.cost_entries) == 0 \
                or len(self.cost_entries[-1]) >= self.MAX_DEMAND_COUNT:
            return

        for i, row in enumerate(self.cost_entries):
            cost_entry = tk.Entry(
                    self.problem_frame_body,
                    width=self.ENTRY_WIDTH,
                    font=self.font,
            )
            cost_entry.grid(
                    row=i+1,
                    column=len(self.cost_entries[i])+1,
                    padx=self.BASE_PADDING, pady=self.BASE_PADDING,
            )
            row.append(cost_entry)

        demand_label = tk.Label(
                self.problem_frame_body,
                text=f"D{len(self.cost_entries[i])}",
                font=self.font,
        )
        demand_label.grid(
                row=0, column=len(self.cost_entries[i]),
                padx=self.BASE_PADDING, pady=self.BASE_PADDING,
        )
        self.demand_labels.append(demand_label)

        demand_entry = tk.Entry(
                self.problem_frame_body,
                width=self.ENTRY_WIDTH,
                font=self.font,
        )
        demand_entry.grid(
                row=self.MAX_SUPPLY_COUNT+1,
                column=len(self.cost_entries[i]),
                padx=self.BASE_PADDING, pady=self.BASE_PADDING,
        )
        self.demand_entries.append(demand_entry)
        self._increment_solution_cols()

    def _decrement_demand_count(self, _=None):
        if len(self.cost_entries) == 0 \
                or len(self.cost_entries[-1]) <= self.MIN_DEMAND_COUNT:
            return

        for row in self.cost_entries:
            row.pop().grid_forget()

        self.demand_labels.pop().grid_forget()
        self.demand_entries.pop().grid_forget()
        self._decrement_solution_cols()

    def _decrement_solution_rows(self, _=None):
        for entry in self.solution_cells[-1]:
            entry.grid_forget()
        self.solution_cells.pop()
        self.solution_supply_labels.pop().grid_forget()

    def _increment_solution_rows(self, _=None):
        if len(self.cost_entries) == 0:
            return

        self.solution_cells.append([])

        supply_label = tk.Label(
                self.solution_frame_body,
                text=f"S{len(self.solution_cells)}",
                font=self.font,
                anchor="e",
                width=6,
        )
        supply_label.grid(
                row=len(self.solution_cells), column=0,
                padx=3*self.BASE_PADDING, pady=self.BASE_PADDING,
        )
        self.solution_supply_labels.append(supply_label)

        for i in range(len(self.cost_entries[-1])):
            cell = tk.Entry(
                    self.solution_frame_body,
                    width=self.ENTRY_WIDTH,
                    font=self.font,
            )
            cell.grid(
                    row=len(self.cost_entries),
                    column=i+1,
                    padx=self.BASE_PADDING, pady=self.BASE_PADDING,
            )
            self.solution_cells[-1].append(cell)

    def _increment_solution_cols(self, _=None):
        for i, row in enumerate(self.solution_cells):
            cell = tk.Entry(
                    self.solution_frame_body,
                    width=self.ENTRY_WIDTH,
                    font=self.font,
            )
            cell.grid(
                    row=i+1,
                    column=len(self.solution_cells[i])+1,
                    padx=self.BASE_PADDING, pady=self.BASE_PADDING,
            )
            row.append(cell)

        demand_label = tk.Label(
                self.solution_frame_body,
                text=f"D{len(self.solution_cells[i])}",
                font=self.font,
        )
        demand_label.grid(
                row=0, column=len(self.solution_cells[i]),
                padx=self.BASE_PADDING, pady=self.BASE_PADDING,
        )
        self.solution_demand_labels.append(demand_label)

    def _decrement_solution_cols(self, _=None):
        for row in self.solution_cells:
            row.pop().grid_forget()

        self.solution_demand_labels.pop().grid_forget()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("TPS")
    gui = GUI(root)
    root.mainloop()
