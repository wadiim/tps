from tp import TP


class Solver():

    @classmethod
    def solve(cls, tp: TP) -> tuple[list[list[float]], float]:
        pass


class NorthWestCellMethodSolver(Solver):

    @classmethod
    def solve(cls, tp: TP) -> tuple[list[list[float]], float]:
        obj_val = 0
        solution = [
                [0 for _ in range(len(tp.costs[0]))]
                    for _ in range(len(tp.costs))
        ]
        x, y = 0, 0

        while x < len(tp.demands) and y < len(tp.supplies):
            solution[y][x] = min(tp.supplies[y], tp.demands[x])
            tp.supplies[y] -= solution[y][x]
            tp.demands[x] -= solution[y][x]
            obj_val += tp.costs[y][x]*solution[y][x]

            if tp.supplies[y] == 0 and tp.demands[x] == 0:
                x, y = x+1, y+1
            elif tp.supplies[y] == 0:
                y = y+1
            elif tp.demands[x] == 0:
                x = x+1

        return solution, obj_val


class RowMinimaMethodSolver(Solver):

    @classmethod
    def solve(cls, tp: TP) -> tuple[list[list[float]], float]:
        obj_val = 0
        solution = [
                [0 for _ in range(len(tp.costs[0]))]
                    for _ in range(len(tp.costs))
        ]

        x, y = 0, 0
        while True:
            if tp.supplies[y] == 0:
                y += 1
                if y >= len(tp.supplies):
                    break

            x = 0
            for i, cost in enumerate(tp.costs[y]):
                if tp.demands[i] == 0: continue
                if tp.demands[x] == 0 or cost < tp.costs[y][x] \
                        or (cost == tp.costs[y][x] \
                            and min(tp.supplies[y], tp.demands[x]) \
                                > min(tp.supplies[y], tp.demands[i])):
                    x = i

            solution[y][x] = min(tp.supplies[y], tp.demands[x])
            tp.supplies[y] -= solution[y][x]
            tp.demands[x] -= solution[y][x]
            obj_val += tp.costs[y][x]*solution[y][x]

        return solution, obj_val


class ColMinimaMethodSolver(Solver):

    @classmethod
    def solve(cls, tp: TP) -> tuple[list[list[float]], float]:
        obj_val = 0
        solution = [
                [0 for _ in range(len(tp.costs[0]))]
                    for _ in range(len(tp.costs))
        ]

        x, y = 0, 0
        while True:
            if tp.demands[x] == 0:
                x += 1
                if x >= len(tp.demands):
                    break

            y = 0
            col = [tp.costs[i][x] for i in range(len(tp.costs))]
            for i, cost in enumerate(col):
                if tp.supplies[i] == 0: continue
                if tp.supplies[y] == 0 or cost < tp.costs[y][x] \
                        or (cost == tp.costs[y][x] \
                            and min(tp.supplies[y], tp.demands[x]) \
                                > min(tp.supplies[y], tp.demands[i])):
                    y = i

            solution[y][x] = min(tp.supplies[y], tp.demands[x])
            tp.supplies[y] -= solution[y][x]
            tp.demands[x] -= solution[y][x]
            obj_val += tp.costs[y][x]*solution[y][x]

        return solution, obj_val


class VogelsApproximationMethodSolver(Solver):

    @classmethod
    def solve(cls, tp: TP) -> tuple[list[list[float]], float]:
        obj_val = 0
        solution = [
                [0 for _ in range(len(tp.costs[0]))]
                    for _ in range(len(tp.costs))
        ]

        x, y = 0, 0
        row_penalties = [0 for _ in range(len(tp.supplies))]
        col_penalties = [0 for _ in range(len(tp.demands))]

        while not cls._is_solved(tp):
            for i, row in enumerate(tp.costs):
                rm1, rm2 = cls._find_two_smallest(row)
                row_penalties[i] = abs(rm1 - rm2)
            for j in range(len(tp.costs[0])):
                col = [tp.costs[i][j] for i in range(len(tp.costs))]
                cm1, cm2 = cls._find_two_smallest(col)
                col_penalties[j] = abs(cm1 - cm2)

            max_row_penalty = -1
            for i, penalty in enumerate(row_penalties):
                if tp.supplies[i] == 0: continue
                if tp.supplies[y] == 0 or penalty > max_row_penalty:
                    max_row_penalty = penalty
                    y = i

            max_col_penalty = -1
            for i, penalty in enumerate(col_penalties):
                if tp.demands[i] == 0: continue
                if tp.demands[x] == 0 or penalty > max_col_penalty:
                    max_col_penalty = penalty
                    x = i

            if max_row_penalty > max_col_penalty:
                x = 0
                for i in range(len(tp.costs[y])):
                    if tp.demands[i] == 0: continue
                    if tp.demands[x] == 0 or tp.costs[y][i] < tp.costs[y][x]:
                        x = i
            elif max_row_penalty < max_col_penalty:
                y = 0
                for i in range(len(tp.costs)):
                    if tp.supplies[i] == 0: continue
                    if tp.supplies[y] == 0 or tp.costs[i][x] < tp.costs[y][x]:
                        y = i
            else:
                rx, ry = 0, y
                for i in range(len(tp.costs[y])):
                    if tp.demands[i] == 0: continue
                    if tp.demands[rx] == 0 or tp.costs[y][i] < tp.costs[y][rx]:
                        rx = i

                cx, cy = x, 0
                for i in range(len(tp.costs)):
                    if tp.supplies[i] == 0: continue
                    if tp.supplies[cy] == 0 or tp.costs[i][x] < tp.costs[cy][x]:
                        cy = i

                if min(tp.supplies[ry], tp.demands[rx]) \
                        > min(tp.supplies[cy], tp.demands[cy]):
                    x, y = rx, ry
                else:
                    x, y = cx, cy

            solution[y][x] = min(tp.supplies[y], tp.demands[x])
            tp.supplies[y] -= solution[y][x]
            tp.demands[x] -= solution[y][x]
            obj_val += tp.costs[y][x]*solution[y][x]

        return solution, obj_val

    @classmethod
    def _is_solved(cls, tp: TP) -> bool:
        for supply in tp.supplies:
            if supply != 0:
                return False

        for demand in tp.demands:
            if demand != 0:
                return False

        return True

    @classmethod
    def _find_two_smallest(cls, l: list[float]) -> tuple[float, float]:
        min1, min2 = l[0], l[1]
        if min1 > min2:
            min1, min2 = min2, min1

        for i in range(2, len(l)):
            if l[i] < min1:
                min1, min2 = l[i], min1
            elif l[i] < min2:
                min2 = l[i]

        return min1, min2
