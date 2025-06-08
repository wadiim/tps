class TP:

    def __init__(
            self,
            costs: list[list[float]],
            supplies: list[float],
            demands: list[float],
    ):
        self.costs = costs
        self.supplies = supplies
        self.demands = demands

    def __str__(self) -> str:
        ret = ""
        widths = self._calc_col_widths()

        for i, row in enumerate(self.costs):
            for j, v in enumerate(row):
                real_len, frac_len = self._calc_num_widths(v)
                ret += " " + (" "*(widths[j][0] - real_len)) \
                        + f"{v:.{widths[j][1]}f}"
            real_len, frac_len = self._calc_num_widths(self.supplies[i])
            ret += " | " + (" "*(widths[-1][0] - real_len)) \
                    + f"{self.supplies[i]:.{widths[-1][1]}f}\n"

        total_width = 1
        for w in widths[:-1]:
            total_width += w[0] + w[1] + (1 if w[1] > 0 else 0) + 1
        ret += "-"*total_width + "+"
        last_width = widths[-1][0] + widths[-1][1] \
                + (1 if widths[-1][1] > 0 else 0) + 1
        ret += "-"*last_width + "\n"

        for i, d in enumerate(self.demands):
            real_len, frac_len = self._calc_num_widths(d)
            ret += " " + (" "*(widths[i][0] - real_len)) \
                    + f"{d:.{widths[i][1]}f}"
        ret += " |"

        return ret

    def balance(self) -> None:
        total_supply = sum(self.supplies)
        total_demand = sum(self.demands)

        if total_supply > total_demand:
            for i in range(len(self.costs)):
                self.costs[i].append(0)
            self.demands.append(total_supply - total_demand)
        elif total_supply < total_demand:
            self.costs.append([0 for _ in range(len(self.costs[0]))])
            self.supplies.append(total_demand - total_supply)

    def _calc_num_widths(self, num: float) -> tuple[int, int]:
        num_str_parts = str(num).split('.')
        real_len = len(num_str_parts[0])
        frac_len = len(num_str_parts[1]) if len(num_str_parts) > 1 else 0

        return (real_len, frac_len)

    def _calc_col_widths(self) -> list[int]:
        widths = []

        if len(self.costs) > 0 and len(self.costs[0]) == 0:
            return [(0, 0)]

        matrix = []
        for i, row in enumerate(self.costs):
            matrix.append(row + [self.supplies[i]])
        matrix.append(self.demands + [0])

        for row in matrix:
            for i, val in enumerate(row):
                real_len, frac_len = self._calc_num_widths(val)
                while len(widths) <= i:
                    widths.append((real_len, frac_len))
                if real_len > widths[i][0]:
                    widths[i] = (real_len, widths[i][1])
                if frac_len > widths[i][1]:
                    widths[i] = (widths[i][0], frac_len)

        return widths
