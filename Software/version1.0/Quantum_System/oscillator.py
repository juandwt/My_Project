import tkinter as tk
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator


colors = {"dark_green":"#4a6c65", "olive":"#7B904B", "black":"#000000",
          "green":"#488c2e", "purple":"#6a0606", "gray":"#b9b9b9", "blue":"#85fff8"}

psi_functions = {
    "psi1": lambda x, alpha: x * sp.exp(-alpha * x**2),
    "psi2": lambda x, alpha: 1 / (alpha * x**2 + 1)**2,
    "psi3": lambda x, alpha: 1 / (x**2 + alpha),
    "psi4": lambda x, alpha: 1 / (x**2 + alpha**2),
    "psi5": lambda x, alpha: 1 / (x**2 + alpha**2)**2,
    "psi6": lambda x, alpha: (x**2) / (x**2 + alpha)**2
    }


class QuantumOscillator:
    def __init__(self, Gui_instance):
        
        self.color = {"black": "#000000", "green": "#488c2e", "purple": "#6a0606", "gray": "#b9b9b9"}
        plt.rcParams["toolbar"] = "none"

        self.x, self.a, self.m, self.w, self.h = sp.symbols("x a m w h", real=True, positive=True)
        self.A = sp.symbols("A", real=True)  # Dejar A como un símbolo separado
        
        self.psi = None

        self.V = (1/2) * self.m * self.w**2 * self.x**2
        self.Gui_instance = Gui_instance
    
    def Psi(self, psi_key):
        self.psi = psi_functions[psi_key](self.x, self.a)
     
    def T(self, psi):
        T_hat = -(self.h**2) / (2 * self.m)
        return sp.integrate(psi * T_hat * sp.diff(psi, self.x, 2), (self.x, -sp.oo, sp.oo))

    def U(self, psi):
        return sp.integrate(psi * self.V * psi, (self.x, -sp.oo, sp.oo))

    def N(self, psi):
        return sp.integrate(psi * psi, (self.x, -sp.oo, sp.oo))

    def Normalize(self):
        cons = sp.solve(sp.Eq(sp.integrate(self.A * self.psi * self.A * self.psi, (self.x, -sp.oo, sp.oo)), 1), self.A)
        return cons[0]

    def calculate_energy(self):
        A_value = self.Normalize()
        psi_normalized = A_value * self.psi

        T_normalized = self.T(psi_normalized)
        U_normalized = self.U(psi_normalized)
        N_normalized = self.N(psi_normalized)

        E = T_normalized + U_normalized
        dE = sp.diff(E, self.a)

        return E, dE

    def plot_energy(self, E, dE):
        E_subs = E.subs({self.m: 1, self.w: 1, self.h: 1})
        dE_da = dE.subs({self.m: 1, self.w: 1, self.h: 1})
        dE_da = sp.lambdify(self.a, dE_da, 'numpy')

        E_plot = sp.lambdify(self.a, E_subs, 'numpy')

        a = np.linspace(0.1, 2, 100)
        Energy = E_plot(a)

        E_latex = sp.latex(E)

        # Minimizacion GD
         
        theta = float(self.Gui_instance.get_p1())
        mu    = float(self.Gui_instance.get_p2())

        lr    = float(self.Gui_instance.get_lr()) 
        iter  = int(self.Gui_instance.get_ep())
        
        Theta = []

        for i in range(iter):
            grad = dE_da(theta)
            theta -= lr * grad
            Theta.append(theta)
        
        Theta = np.array(Theta)
        colores = [(0.39, 0.02,  0.02, i) for i in np.linspace(0.2, 1, len(Theta))]    
        l_Theta = Theta[-1]

        w_val = 1
        m_val = 1
        x_val = np.linspace(-1, 1, 100)
        V_fun = lambda x: 0.5*m_val*w_val**2*x**2
        V_val = V_fun(x_val)
        
        x_sym = sp.Symbol("x")
        alpha_sym = sp.Symbol('alpha')
        alpha_value = theta
        
        sym_func  = self.psi.subs(self.a, alpha_value)
        func_numeric = sp.lambdify(x_sym, sym_func, 'numpy')
        
        x  = np.linspace(-10, 10, 100)
        y  = func_numeric(x) 
        Y  = y*y

        plt.subplot(2, 2, 1)
        plt.plot(x, y, color='#000000', label=r"$\psi_{t}$")
        plt.axhline(0, color='gray', linestyle='-', linewidth=1)
        plt.axvline(0, color='gray', linestyle='-', linewidth=1)
        plt.xlabel("x")
        plt.ylabel(r"$\psi_{t}$")
        plt.legend()
        
        plt.subplot(2, 2, 2)
        plt.plot(x, Y, color='gray', label=r"$|\psi_{t}|^{2}$")
        plt.fill(x, Y, color=colors["gray"])
        plt.axhline(0, color='gray', linestyle='-', linewidth=1)
        plt.axvline(0, color='gray', linestyle='-', linewidth=1)
        plt.xlabel("x")
        plt.ylabel(r"$|\psi_{t}|^{2}$")
        plt.legend()


        plt.subplot(2, 2, (3, 4))
        plt.plot(a, Energy, color=self.color["black"], label=f"E(a)=${E_latex}$")
        plt.scatter(l_Theta, E_plot(l_Theta), color=self.color["purple"], label=f"$E_{{min}}={E_plot(theta):.3f} \\hbar \\omega$", marker="*")
        plt.scatter(Theta, E_plot(Theta), color=colores, marker="*")
        plt.axvline(0, color=self.color["gray"])
        plt.axhline(0, color=self.color["gray"])
        plt.legend(loc="upper right", framealpha=1)
        plt.xlim(0.1, 2)
        plt.xlabel("x")
        plt.ylabel("E(a)")
    
        plt.tight_layout()
        #plt.subplots_adjust(wspace=0.3)
        #plt.subplots_adjust(hspace=0.4)

def OA(m=1, w=1, x_range=(-1, 1), y_range=(-1, 1), grid_points=40):

    def V_O(x):
        return 0.5 * m * w**2 * x**2

    x = np.linspace(x_range[0], x_range[1], grid_points)
    y = np.linspace(y_range[0], y_range[1], grid_points)

    X, Y = np.meshgrid(x, y)
    Z = V_O(X) + V_O(Y)

    #fig = plt.figure(figsize=(10, 7))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_wireframe(X, Y, Z, color="black", alpha=0.5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('V(x, y)')
    ax.set_title(r"$V(x, y) = \frac{1}{2}m\omega^{2}(x^{2}+y^{2})$")

    ax.view_init(elev=20, azim=135)
    ax.grid(False)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.zaxis.set_major_locator(MultipleLocator(1))

    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4       
 
