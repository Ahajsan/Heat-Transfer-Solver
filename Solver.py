import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt


class HeatTransferApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Heat Transfer Solver")
        self.root.geometry("600x300")
        tk.Label(self.root, text="Heat Transfer FEM Solver", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text="Enter number of elements below (n>2):").pack()
        self.entry = tk.Entry(self.root, justify="center")
        self.entry.pack(pady=5)
        tk.Button(self.root, text="Solve", command=self.solve).pack(pady=20)
        self.root.mainloop()

    def solve(self):
        try:
            n = int(self.entry.get())
            if n <= 2:
                raise ValueError("Number of elements must be greater than 2.")
            x, y = compute_solution(n)
            plot_solution(x, y, n)
        except Exception as e:
            messagebox.showerror("Error", str(e))


def thermal_conductivity(x):
    if 0 <= x <= 1:
        return 1
    elif 1 < x <= 2:
        return 2 * x
    return 0


def basis_function(i, x, h):
    xi = h * i
    if x < xi - h or x > xi + h:
        return 0
    elif xi - h <= x < xi:
        return (x - (xi - h)) / h
    elif xi <= x <= xi + h:
        return ((xi + h) - x) / h
    return 0


def basis_derivative(i, x, h):
    xi = h * i
    if xi - h <= x < xi:
        return 1 / h
    elif xi <= x <= xi + h:
        return -1 / h
    return 0


def stiffness_matrix_element(i, j, h):
    def integrand_low(x):
        return basis_derivative(i, x, h) * basis_derivative(j, x, h)

    def integrand_high(x):
        return 2 * x * basis_derivative(i, x, h) * basis_derivative(j, x, h)
    k1 = integrate.quad(integrand_low, max(0, (i - 1) * h), min(1, (i + 1) * h))[0]
    k2 = integrate.quad(integrand_high, max(1, (i - 1) * h), min(2, (i + 1) * h))[0]
    boundary_term = -basis_function(j, 0, h) * basis_function(i, 0, h)
    return k1 + k2 + boundary_term


def load_vector_element(i, h):
    def source_term(x):
        return 100 * x * basis_function(i, x, h)
    return integrate.quad(source_term, max(0, (i - 1) * h), min(2, (i + 1) * h))[0] - 20 * basis_function(i, 0, h)


def assemble_system(n):
    h = 2 / n
    A = np.zeros((n, n))
    b = np.zeros(n)

    for i in range(n):
        for j in range(max(0, i - 1), min(n, i + 2)):
            A[i, j] = stiffness_matrix_element(i, j, h)
        b[i] = load_vector_element(i, h)

    return A, b


def compute_solution(n):
    A, b = assemble_system(n)
    h = 2 / n
    x = np.linspace(0, 2, n + 1)
    y = np.linalg.solve(A, b)
    y = np.append(y, 0)
    return x, y


def plot_solution(x, y, n):
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, 'r-', label="Temperature Distribution")
    plt.title(f"Heat Transfer Solution (n={n})")
    plt.xlabel("x")
    plt.ylabel("Temperature")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    HeatTransferApp()