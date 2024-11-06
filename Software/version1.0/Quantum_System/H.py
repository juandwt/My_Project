import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator
import numpy as np
import sympy as sp

psi = {"psi1": lambda r, alpha: sp.exp(-alpha*r)}


class Hydrogen:
    def __init__(self, Gui_instance):
        
        self.Gui_instance = Gui_instance

    def Variation(self):
        r, c, m, h, Z, e, k = sp.symbols("r c m h Z e k", real=True, positive=True)

        m = 9.10938356e-31      
        h = 1.0545718e-34        
        Z = 1                   
        e = 1.602176634e-19     
        k = 8.9875517873681764e9 

        V = -Z * e**2 * k / r

        psi1 = psi["psi1"](r, c)

        E_V = sp.integrate(psi1 * psi1 * V * 4 * sp.pi * r**2, (r, 0, sp.oo))
        E_T = sp.integrate((-h**2 / (2 * m)) * 4 * sp.pi * psi1 * sp.diff(psi1 * r**2, r, 2), (r, 0, sp.oo))
        N_D = sp.integrate(psi1 * psi1 * 4 * sp.pi * r**2, (r, 0, sp.oo))

        E = sp.simplify((-E_T + E_V) / N_D)
        E_grad = sp.diff(E, c, 1)

        sol_c = sp.solve(E_grad, c)
        sol = sol_c[0].evalf()

        E_grad = sp.lambdify(c, E_grad, 'numpy')
        E = sp.lambdify(c, E)

        theta = float(self.Gui_instance.get_p1())
        lr    = float(self.Gui_instance.get_lr())

        Theta = []
        iter  = int(self.Gui_instance.get_ep())

        for i in range(iter):
            grad = E_grad(theta)
            theta -= lr * grad
            Theta.append(theta)

        Theta = np.array(Theta)

        c_vals = np.linspace(-1e20, 1e20, 100)
        Energy_vals = E(c_vals) * 6.242e18
        Energy_Theta = E(Theta) * 6.242e18

        fig = plt.figure()
        

        E_min = E(Theta[-1]) * 6.242e18

        colors = ['#FF0000', '#00FFFF', '#0000FF', '#800080', '#FF00FF']
        l = []
        L = [656.3, 486.1, 434, 410.2]

        def Waveleght(E_min, n):
            E = abs(-(E_min) / (2**2) + (E_min / (n**2)))
            wl = ((4.135e-15 * 3e8) / E) * 1e9
            return round(wl, 1)

        n_values = [3, 4, 5, 6]

        for n in n_values:
            waveleght = Waveleght(E_min, n)
            l.append(waveleght)

        fig, (ax1, ax2) = plt.subplots(2, 1)

        for waveleght_t in L:
            ax1.axvline(x=waveleght_t, color="#a2a2a2")

        for waveleght, color in zip(l, colors):
            ax1.axvline(x=waveleght, color=color)

        ax1.set_facecolor('#000000')
        ax1.yaxis.set_visible(False)
         
        ax2.plot(c_vals, Energy_vals, color="#000000", label="Energía (MeV)")
        ax2.scatter(Theta, Energy_Theta)
        #plt.tight_layout()
        plt.subplots_adjust(hspace=0.5)








def H():   
    e = 1.602e-19          
    epsilon_0 = 8.854e-12  
    
    def potential(x, y, z):
        r = np.sqrt(x**2 + y**2 + z**2)
        return -e**2 / (4 * np.pi * epsilon_0 * r)
    
    x = np.linspace(-1, 1, 50)
    y = np.linspace(-1, 1, 50)
    X, Y = np.meshgrid(x, y)
    
    z_val = 0
    Z = np.full_like(X, z_val)
    
    V = potential(X, Y, Z)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_wireframe(X, Y, V, color="black", alpha=0.5)
    ax.contour(X, Y, V, zdir='z', levels=30, offset=ax.get_zlim()[0], colors="black", alpha=0.7)
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('$V(x, y)$')
    ax.set_title(r"$V(x, y) = -\frac{e^2}{4 \pi \epsilon_0 \sqrt{x^2 + y^2}}$")
    
    ax.view_init(elev=25, azim=135)
    ax.grid(False)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.yaxis.set_major_locator(MultipleLocator(4))
    ax.zaxis.set_major_locator(MultipleLocator(4))
    
    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4


