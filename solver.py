import sys
from enum import auto, Enum

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
                            and min(tp.supplies[y], tp.demands[i]) \
                                > min(tp.supplies[y], tp.demands[x])):
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
                            and min(tp.supplies[i], tp.demands[x]) \
                                > min(tp.supplies[y], tp.demands[x])):
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


class MODIMethodSolver(Solver):

    class DIRECTION(Enum):
        HORIZONTAL = auto()
        VERTICAL = auto()

    @classmethod
    def solve(cls, tp: TP) -> tuple[list[list[float]], float]:
        allocs, _ = VogelsApproximationMethodSolver.solve(tp)

        while True:
            cls._handle_degeneracy(tp, allocs)

            u, v = cls._calculate_u_v(tp, allocs)

            d, is_optimal, start = cls._calculate_opportunity_costs(tp, allocs, u, v)
            if is_optimal:
                return allocs, cls._calculate_total_cost(tp, allocs)

            loop = cls._create_loop([start], allocs, cls.DIRECTION.HORIZONTAL) \
                    or cls._create_loop([start], allocs, cls.DIRECTION.VERTICAL)

            cls._optimize(allocs, loop)

    @classmethod
    def _handle_degeneracy(cls, tp: TP, allocs: list[list[float]]):
        alloc_count = cls._get_alloc_count(allocs)
        height, width = len(tp.costs), len(tp.costs[0])

        while alloc_count < height+width-1:
            x, y = cls._get_min_cost_unalloc_pos(tp, allocs)
            allocs[y][x] = sys.float_info.min
            alloc_count += 1

    @classmethod
    def _get_alloc_count(cls, allocs: list[list[float]]) -> int:
        count = 0

        for row in allocs:
            for val in row:
                if val != 0:
                    count += 1

        return count

    @classmethod
    def _get_min_cost_unalloc_pos(
            cls,
            tp: TP,
            allocs: list[list[float]]
    ) -> tuple[int, int]:
        mx, my = 0, 0

        for y in range(len(tp.costs)):
            for x in range(len(tp.costs[0])):
                if allocs[y][x] == 0 and tp.costs[y][x] < tp.costs[my][mx]:
                    mx, my = x, y

        return mx, my

    @classmethod
    def _get_max_alloc_count_pos(
            cls,
            allocs: list[list[float]],
    ) -> tuple[int | None, int | None]:
        x, y = None, None
        max_allocs = 0

        for i, row in enumerate(allocs):
            count = sum([1 for v in row if v != 0])
            if count > max_allocs:
                y = i
                max_allocs = count

        for i in range(len(allocs[0])):
            col = [a[i] for a in allocs]
            count = sum([1 for v in col if v != 0])
            if count > max_allocs:
                y = None
                x = i
                max_allocs = count

        return x, y

    @classmethod
    def _calculate_u_v(
            cls,
            tp: TP,
            allocs: list[list[float]],
    ) -> tuple[list[float], list[float]]:
        u = [None for _ in range(len(allocs))]
        v = [None for _ in range(len(allocs[0]))]
        x, y = cls._get_max_alloc_count_pos(allocs)
        if x != None:
            v[x] = 0
        elif y != None:
            u[y] = 0

        while any(u is None for u in u) or any(v is None for v in v):
            for y in range(len(tp.costs)):
                for x in range(len(tp.costs[0])):
                    if allocs[y][x] == 0:
                        continue
                    if u[y] == None and v[x] != None:
                        u[y] = tp.costs[y][x] - v[x]
                    elif u[y] != None and v[x] == None:
                        v[x] = tp.costs[y][x] - u[y]

        return u, v

    @classmethod
    def _calculate_opportunity_costs(
            cls, tp: TP, allocs: list[list[float]],
            u: list[float], v: list[float],
    ) -> tuple[list[list[float]], bool, tuple[int, int]]:
        d = []
        start = None
        is_optimal = True

        for y in range(len(tp.costs)):
            d.append([])
            for x in range(len(tp.costs[y])):
                d[y].append(0)
                if allocs[y][x] == 0:
                    d[y][x] = tp.costs[y][x] - (u[y] + v[x])
                    if d[y][x] < 0:
                        is_optimal = False
                        if start == None or d[y][x] > start:
                            start = (x, y)

        return d, is_optimal, start

    @classmethod
    def _create_loop(
            cls, curr_path: list[tuple[int, int]], allocs: list[list[float]],
            direction: DIRECTION,
    ) -> list[tuple[int, int]] | None:
        candidates = []
        if direction == cls.DIRECTION.HORIZONTAL:
            y = curr_path[-1][1]
            if len(curr_path) >= 4 and y == curr_path[0][1]:
                return curr_path
            for x in range(len(allocs[y])):
                if allocs[y][x] != 0 and (x, y) not in curr_path:
                    candidates.append((x, y))
        elif direction == cls.DIRECTION.VERTICAL:
            x = curr_path[-1][0]
            if len(curr_path) >= 4 and x == curr_path[0][0]:
                return curr_path
            for y in range(len(allocs)):
                if allocs[y][x] != 0 and (x, y) not in curr_path:
                    candidates.append((x, y))
        else:
            assert False, "Unreachable"

        for x, y in candidates:
            new_dir = cls.DIRECTION.HORIZONTAL \
                    if direction == cls.DIRECTION.VERTICAL \
                    else cls.DIRECTION.VERTICAL
            path = cls._create_loop(curr_path + [(x, y)], allocs, new_dir)
            if path != None:
                return path

        return None

    @classmethod
    def _optimize(cls, allocs: list[list[float]], loop: list[tuple[int, int]]):
        mx, my = loop[1]

        for i in range(3, len(loop), 2):
            x, y = loop[i]
            if allocs[y][x] < allocs[my][mx]:
                mx, my = x, y

        ox, oy = loop[0]
        allocs[oy][ox] = allocs[my][mx]

        for i in range(2, len(loop), 2):
            x, y = loop[i]
            allocs[y][x] += allocs[oy][ox]

        for i in range(1, len(loop), 2):
            x, y = loop[i]
            allocs[y][x] -= allocs[oy][ox]

    @classmethod
    def _calculate_total_cost(cls, tp: TP, allocs: list[list[float]]) -> float:
        cost = 0

        for y in range(len(allocs)):
            for x in range(len(allocs[y])):
                cost += allocs[y][x]*tp.costs[y][x]

        return cost
