"""一个无需第三方依赖的 Tkinter 矩阵计算器。"""

from fractions import Fraction
import tkinter as tk
from tkinter import messagebox, ttk


def parse_number(value: str) -> Fraction:
    """支持整数、分数（如 2/3）和有限小数（如 -1.25）。"""
    text = value.strip()
    if not text:
        raise ValueError("请输入所有矩阵元素")
    try:
        return Fraction(text)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"“{value}”不是有效的分数或小数") from exc


def matrix_text(matrix):
    if not matrix:
        return "[]"
    strings = [[str(x) for x in row] for row in matrix]
    widths = [max(len(row[c]) for row in strings) for c in range(len(strings[0]))]
    return "\n".join("[ " + "  ".join(v.rjust(widths[c]) for c, v in enumerate(row)) + " ]" for row in strings)


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def subtract(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def determinant_and_steps(matrix, include_steps=False):
    n = len(matrix)
    if n != len(matrix[0]):
        raise ValueError("行列式只适用于方阵")
    work = [row[:] for row in matrix]
    sign, det, steps = 1, Fraction(1), []
    for col in range(n):
        pivot = next((r for r in range(col, n) if work[r][col] != 0), None)
        if pivot is None:
            return Fraction(0), steps + ([f"第 {col + 1} 列无非零主元，因此 det = 0。"] if include_steps else [])
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            sign *= -1
            if include_steps: steps.append(f"交换第 {col + 1}、{pivot + 1} 行（行列式变号）：\n{matrix_text(work)}")
        p = work[col][col]
        det *= p
        for row in range(col + 1, n):
            if work[row][col] == 0: continue
            factor = work[row][col] / p
            work[row] = [work[row][j] - factor * work[col][j] for j in range(n)]
            if include_steps: steps.append(f"R{row + 1} ← R{row + 1} − ({factor})R{col + 1}\n{matrix_text(work)}")
    return sign * det, steps


def inverse_and_steps(matrix, include_steps=False):
    n = len(matrix)
    if n != len(matrix[0]):
        raise ValueError("逆矩阵只适用于方阵")
    aug = [row[:] + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    steps = []
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col] != 0), None)
        if pivot is None: raise ValueError("该矩阵不可逆（行列式为 0）")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
            if include_steps: steps.append(f"交换第 {col + 1}、{pivot + 1} 行：\n{matrix_text(aug)}")
        p = aug[col][col]
        if p != 1:
            aug[col] = [v / p for v in aug[col]]
            if include_steps: steps.append(f"R{col + 1} ← R{col + 1} / {p}\n{matrix_text(aug)}")
        for row in range(n):
            if row == col or aug[row][col] == 0: continue
            factor = aug[row][col]
            aug[row] = [aug[row][j] - factor * aug[col][j] for j in range(2 * n)]
            if include_steps: steps.append(f"R{row + 1} ← R{row + 1} − ({factor})R{col + 1}\n{matrix_text(aug)}")
    return [row[n:] for row in aug], steps


def matrix_power(matrix, exponent):
    """使用二进制快速幂计算非负整数次矩阵幂。"""
    n = len(matrix)
    result = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    base = [row[:] for row in matrix]
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent //= 2
    return result


class MatrixCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("矩阵计算器")
        self.minsize(900, 680)
        self.entries = {"A": [], "B": []}
        self.last_matrix = None
        self.size_vars = {name: (tk.IntVar(value=2), tk.IntVar(value=2)) for name in "AB"}
        self.show_steps = tk.BooleanVar(value=True)
        self.scalar = tk.StringVar(value="1")
        self.exponent = tk.StringVar(value="2")
        self._build()
        self.rebuild("A"); self.rebuild("B")

    def _build(self):
        top = ttk.Frame(self, padding=12); top.pack(fill="x")
        ttk.Label(top, text="输入支持：整数、分数（如 3/4）和小数（如 1.5）", font=("Arial", 12, "bold")).pack(anchor="w")
        grids = ttk.Frame(self, padding=(12, 0)); grids.pack(fill="x")
        for i, name in enumerate("AB"):
            box = ttk.LabelFrame(grids, text=f"矩阵 {name}", padding=8); box.grid(row=0, column=i, padx=(0, 12), sticky="nw")
            rows, cols = self.size_vars[name]
            controls = ttk.Frame(box); controls.pack(anchor="w")
            ttk.Label(controls, text="行").grid(row=0,column=0); ttk.Spinbox(controls, from_=1, to=8, textvariable=rows, width=4).grid(row=0,column=1)
            ttk.Label(controls, text="列").grid(row=0,column=2, padx=(8,0)); ttk.Spinbox(controls, from_=1, to=8, textvariable=cols, width=4).grid(row=0,column=3)
            ttk.Button(controls, text="更新尺寸", command=lambda n=name: self.rebuild(n)).grid(row=0,column=4, padx=8)
            frame = ttk.Frame(box); frame.pack(pady=(8,0)); setattr(self, f"grid_{name}", frame)
        options = ttk.Frame(self, padding=12); options.pack(fill="x")
        ttk.Checkbutton(options, text="显示计算过程", variable=self.show_steps).pack(side="left")
        ttk.Label(options, text="  标量（用于 A ÷ 标量）：").pack(side="left")
        ttk.Entry(options, textvariable=self.scalar, width=9).pack(side="left")
        ttk.Label(options, text="  指数 n（用于 Aⁿ）：").pack(side="left")
        ttk.Entry(options, textvariable=self.exponent, width=6).pack(side="left")
        buttons = ttk.Frame(self, padding=(12, 0)); buttons.pack(fill="x")
        for label, op in [("A + B", "add"), ("A − B", "sub"), ("A × B", "mul"), ("A ÷ B", "matdiv"), ("A ÷ 标量", "div"), ("Aⁿ", "power"), ("det(A)", "det"), ("A⁻¹", "inv")]:
            ttk.Button(buttons, text=label, command=lambda x=op: self.calculate(x)).pack(side="left", padx=(0,8), pady=4)
        output = ttk.LabelFrame(self, text="结果与过程", padding=8); output.pack(fill="both", expand=True, padx=12, pady=12)
        actions = ttk.Frame(output); actions.pack(fill="x", pady=(0, 6))
        ttk.Label(actions, text="复用结果：").pack(side="left")
        ttk.Button(actions, text="结果 → A", command=lambda: self.assign_result("A")).pack(side="left", padx=(0, 6))
        ttk.Button(actions, text="结果 → B", command=lambda: self.assign_result("B")).pack(side="left")
        self.result = tk.Text(output, wrap="word", font=("Menlo", 12)); self.result.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(output, command=self.result.yview); scroll.pack(side="right", fill="y"); self.result.configure(yscrollcommand=scroll.set)

    def rebuild(self, name):
        old = self.entries[name]
        values = [[e.get() for e in row] for row in old] if old else []
        for child in getattr(self, f"grid_{name}").winfo_children(): child.destroy()
        rows, cols = (var.get() for var in self.size_vars[name])
        self.entries[name] = []
        grid = getattr(self, f"grid_{name}")
        for r in range(rows):
            row = []
            for c in range(cols):
                e = ttk.Entry(grid, width=8); e.grid(row=r, column=c, padx=2, pady=2)
                e.insert(0, values[r][c] if r < len(values) and c < len(values[r]) else "0")
                row.append(e)
            self.entries[name].append(row)

    def read(self, name):
        return [[parse_number(entry.get()) for entry in row] for row in self.entries[name]]

    def assign_result(self, name):
        """将最近一次矩阵计算结果填入指定的操作数矩阵。"""
        if self.last_matrix is None:
            messagebox.showinfo("没有可复用的矩阵", "请先完成一次产生矩阵结果的计算。行列式是标量，不能直接赋给矩阵。")
            return
        rows, cols = len(self.last_matrix), len(self.last_matrix[0])
        self.size_vars[name][0].set(rows)
        self.size_vars[name][1].set(cols)
        self.rebuild(name)
        for r, row in enumerate(self.last_matrix):
            for c, value in enumerate(row):
                entry = self.entries[name][r][c]
                entry.delete(0, "end")
                entry.insert(0, str(value))
        self.result.insert("end", f"\n\n已将结果赋值给矩阵 {name}。")

    def calculate(self, operation):
        try:
            a, b, steps = self.read("A"), self.read("B"), []
            if operation in ("add", "sub"):
                if len(a) != len(b) or len(a[0]) != len(b[0]): raise ValueError("加减法要求两个矩阵尺寸相同")
                answer = add(a,b) if operation == "add" else subtract(a,b)
                title = "A + B" if operation == "add" else "A − B"
                if self.show_steps.get(): steps = [f"A =\n{matrix_text(a)}\n\nB =\n{matrix_text(b)}", "按相同位置的元素分别相加。" if operation == "add" else "按相同位置的元素分别相减。"]
            elif operation == "mul":
                if len(a[0]) != len(b): raise ValueError("乘法要求 A 的列数等于 B 的行数")
                answer, title = multiply(a,b), "A × B"
                if self.show_steps.get(): steps = [f"A =\n{matrix_text(a)}\n\nB =\n{matrix_text(b)}", "结果的第 i 行第 j 列 = A 的第 i 行与 B 的第 j 列的点积。"]
            elif operation == "matdiv":
                if len(b) != len(b[0]) or len(a[0]) != len(b): raise ValueError("A ÷ B 定义为 A × B⁻¹；B 必须为方阵且 A 的列数等于 B 的行数")
                inv_b, inv_steps = inverse_and_steps(b, self.show_steps.get())
                answer, title = multiply(a, inv_b), "A ÷ B = A × B⁻¹"
                if self.show_steps.get(): steps = [f"先求 B⁻¹，B =\n{matrix_text(b)}"] + inv_steps + [f"B⁻¹ =\n{matrix_text(inv_b)}", "再计算 A × B⁻¹。"]
            elif operation == "div":
                scalar = parse_number(self.scalar.get())
                if scalar == 0: raise ValueError("除数不能为 0")
                answer, title = [[v/scalar for v in row] for row in a], f"A ÷ {scalar}"
                if self.show_steps.get(): steps = [f"A 的每个元素都除以 {scalar}。"]
            elif operation == "power":
                if len(a) != len(a[0]): raise ValueError("矩阵乘方只适用于方阵")
                try:
                    exponent = int(self.exponent.get().strip())
                except ValueError as exc:
                    raise ValueError("指数 n 必须是整数") from exc
                base = a
                inverse_steps = []
                if exponent < 0:
                    base, inverse_steps = inverse_and_steps(a, self.show_steps.get())
                answer, title = matrix_power(base, abs(exponent)), f"A^{exponent}"
                if self.show_steps.get():
                    steps = ([f"A =\n{matrix_text(a)}"] + inverse_steps if exponent < 0 else [f"A =\n{matrix_text(a)}"])
                    if exponent == 0:
                        steps.append("任何方阵的 0 次幂都是同阶单位矩阵。")
                    elif exponent < 0:
                        steps.append(f"先求 A⁻¹，再计算 (A⁻¹)^{abs(exponent)}。")
                    else:
                        steps.append(f"将 A 连续相乘 {exponent} 次（程序使用快速幂计算）。")
            elif operation == "det":
                answer, steps = determinant_and_steps(a, self.show_steps.get()); title = "det(A)"
            else:
                answer, steps = inverse_and_steps(a, self.show_steps.get()); title = "A⁻¹"
            rendered = str(answer) if operation == "det" else matrix_text(answer)
            self.last_matrix = None if operation == "det" else [row[:] for row in answer]
            text = f"{title} =\n{rendered}"
            if self.show_steps.get() and steps: text += "\n\n计算过程：\n" + "\n\n".join(steps)
            self.result.delete("1.0", "end"); self.result.insert("1.0", text)
        except ValueError as exc:
            messagebox.showerror("无法计算", str(exc))


if __name__ == "__main__":
    MatrixCalculator().mainloop()
