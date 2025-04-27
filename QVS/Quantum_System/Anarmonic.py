import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator
import numpy as np
from scipy.special import eval_hermite, factorial
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import MaxNLocator

plt.rcParams['toolbar'] = 'none'
plt.rcParams['mathtext.fontset'] = 'cm'  # Usa la fuente Computer Modern para matemáticas
font_params = {"fontsize": 16, "fontweight": "bold", "fontstyle": "italic"}
#plt.rcParams['axes3d.mouserotationstyle'] = 'azel' 


def Anarmonic():   
    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)
    x, y = np.meshgrid(x, y)
    
    m, w, l = 1, 1, -0.1
    
    v = (1/2)*m*w*(x**2+y**2) + l*(x**4+y**4)
    
    fig = plt.figure()
    ax = plt.axes(projection='3d',computed_zorder=False)
    
    ax.plot_surface(x, y, v, cmap='viridis', alpha=0.8)
    ax.contour(x, y, v, zdir='z', offset=ax.get_zlim()[0], alpha=0.7)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('V(x, y)')
    ax.set_title(r"$e^{-}~~\mathrm{locked\ in\ potential}~~\left[ \frac{\hat{p}^2}{2m} + \frac{1}{2} m \omega^2 (\hat{x}^2 + \hat{y}^2) - 0.01 (\hat{x}^4 + \hat{y}^4) \right] |\psi\rangle = E_{n} |\psi\rangle$", fontsize=16)
    
    scatter = ax.scatter(0, 0, 0.9, color='#000000' , s=30, zorder=100)
    ax.text(0, 0, 1, r'$e^- \Rightarrow E_{n}$', fontsize=16, color='black', ha='center')
    

    ax.view_init(elev=20, azim=110)
    ax.set_box_aspect([6, 6, 2.5])
    ax.grid(False)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(2))
    ax.zaxis.set_major_locator(MultipleLocator(2))
    
    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    return fig


E = {'E0': lambda a, b: (-0.0075*a**4 - 0.03*a**2*b**2 + 0.25*a**2 - 0.01*b**4 + 0.5*b**2 + 0.25/a**2),
     'E1': lambda a, b: (-0.0375*a**4 - 0.09*a**2*b**2 + 0.75*a**2 - 0.01*b**4 + 0.5*b**2 + 0.75/a**2),
     'E2': lambda a, b: (-0.0975*a**4 - 0.15*a**2*b**2 + 1.25*a**2 - 6.93889390390723e-18*a*b**3/np.pi**0.5 - 0.01*b**4 + 0.5*b**2 + 1.25/a**2),
     'E3': lambda a, b: (-0.1875*a**4 - 0.21*a**2*b**2 + 1.75*a**2 - 0.01*b**4 + 0.5*b**2 + 1.75/a**2),
     'E4': lambda a, b: (-0.3075*a**4 - 0.27*a**2*b**2 + 2.25*a**2 - 0.01*b**4 + 0.5*b**2 + 2.25/a**2),
     'E5': lambda a, b: (-0.4575*a**4 + 4.44089209850063e-16*a**3*b/np.pi**0.5 - 0.329999999999999*a**2*b**2 + 2.75*a**2 + 1.11022302462516e-16*a*b**3/np.pi**0.5 - 0.01*b**4 + 0.5*b**2 + 2.75/a**2),
     'E6': lambda a, b: (-0.637500000000001*a**4 - 0.389999999999999*a**2*b**2 + 3.24999999999999*a**2 - 8.88178419700125e-16*a*b**3/np.pi**0.5 - 0.00999999999999993*b**4 + 0.499999999999996*b**2) + 3.25/a**2
     }

n = None

def function_2p(n_param):
    global n
    n = n_param
    
    a_values = np.linspace(0.7, 2, 40)
    b_values = np.linspace(-1, 1, 40)
    
    A, B = np.meshgrid(a_values, b_values)
    Z = E[f'E{n}'](A, B)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([4, 4, 2])

    ax.plot_surface(A, B, Z,cmap='viridis', edgecolor='none', rstride=2, cstride=2, alpha=0.7)
    ax.contour(A, B, Z, zdir='z', offset=ax.get_zlim()[0],  alpha=0.7)
    
    ax.view_init(elev=40, azim=150)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.zaxis.set_major_locator(MultipleLocator(0.9))

    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    
    ax.set_xlabel(r'$\alpha$', fontsize=16)
    ax.set_ylabel(r'$\beta$',  fontsize=16)
    ax.set_zlabel(r'$E(\alpha, \beta)$', fontsize=16)

    ax.grid(False)
    ax.set_title(r"$\mathrm{Average\ energy\ calculation}~~\langle E_{%d}(α, β) \rangle = \frac{\langle \Psi_{%d}(x) | \hat{H} | \Psi_{%d}(x) \rangle}{\langle \Psi_{%d}(x) | \Psi_{%d}(x) \rangle}$" % (n, n, n, n, n), fontsize=16)
    fig.text(0.5, 0.05, r"$\mathrm{Select\ a\ point\ \in ~~E(\alpha_{i}, \beta_{i})}$" , ha='center', fontsize=16, color="#4a6c65", family="serif")
    return a_values, b_values


def minimizacion(a_values, b_values, l_r, e_p, p_1, p_2):
    E_func = E[f'E{n}']

    def numerical_derivate(func, a, b, h=1e-5):   
        partial_a = (func(a + h, b) - func(a - h, b)) / (2 * h)
        partial_b = (func(a, b + h) - func(a, b - h)) / (2 * h)
        return partial_a, partial_b
    
    theta_a = p_1
    theta_b = p_2
    lr      = l_r
    iters   = e_p
    
    last_thetas_a = []
    last_thetas_b = []
     
    for i in range(iters):
        dE_da, dE_db = numerical_derivate(E_func, theta_a, theta_b)
        theta_a     -= lr * dE_da 
        theta_b     -= lr * dE_db
        if i%2 ==0 or i == iters - 1:
            last_thetas_a.append(theta_a)
            last_thetas_b.append(theta_b)
    
    
    E_min = E_func(theta_a, theta_b)
    
    #points 
    
    E_x = []
    E_y = []
    E_z = []
    
    for a, b in zip(last_thetas_a, last_thetas_b):
        E_x.append(a)
        E_y.append(b)
        E_z.append(E_func(a, b))
    
    A, B = np.meshgrid(a_values, b_values)
    Z = E_func(A, B)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(p_1, p_2, E_func(p_1,p_2), color="#e80000", s=10)
    
    ax.plot_surface(A, B, Z,cmap='viridis', edgecolor='none', rstride=2, cstride=2, alpha=0.7)
    
    ax.contour(A, B, Z, zdir='z', offset=ax.get_zlim()[0],  alpha=0.7)
    
    ax.set_box_aspect([4, 4, 2])
    
    ax.view_init(elev=16, azim=120)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.zaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))

    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    
    ax.set_xlabel(r'$\alpha$', fontsize=16)
    ax.set_ylabel(r'$\beta$',  fontsize=16)
    ax.set_zlabel(r'$E(\alpha, \beta)$', fontsize=16)
    #Validation
 
    def phi_n(x, n, alpha, beta):
        normalization = 1 / np.sqrt(2**n * factorial(n))
        gaussian = np.exp(-0.5 * ((x - beta) / alpha)**2)
        hermite_poly = eval_hermite(n, alpha * (x - beta) / alpha)
        return normalization * (alpha / np.pi**0.25) * hermite_poly * gaussian
    
    alpha = theta_a
    beta  = theta_b
    E_w     = E_min
    
    x = np.linspace(-4, 4, 100)
    V = -0.5 * x**2
    
    f = phi_n(x, n, alpha, beta)
    d_f = np.gradient(f, x)  # Primera derivada
    d2_f = np.gradient(d_f, x)
    
    ax.grid(False)
    title = ax.set_title(fr"$H | \Psi_{{{n}}}\rangle= {round(E_func(p_1, p_2), 2)}|\Psi_{{{n}}}\rangle$", fontsize=16, y=1.1)
    fig.text(0.5, 0.05, "The error" " " r"$J_{error} \rightarrow 0$" " " "when approaching the minimum", ha='center', fontsize=16, color="#4a6c65", family="serif")
    line,  = ax.plot([], [], [], label="Evolución de la línea", color="#000000")
    
    def init():
        line.set_data([], [])
        line.set_3d_properties([])
        return line,title
    
    def update(frame):
        line.set_data(E_x[:frame], E_y[:frame])
        line.set_3d_properties(E_z[:frame])
        title.set_text(fr"$\hat{{H}} | \Psi_{{{n}}} \rangle = {round(E_z[frame - 1], 2)} |\Psi_{{{n}}} \rangle, \quad J_{{error}} = \frac{{1}}{{N}} \sum_{{i=1}}^{{N}} \left| \hat{{H}} |\Psi_{{{n}}} \rangle - E_{{{n}}} |\Psi_{{{n}}} \rangle \right|^2 = {np.round(np.mean(np.abs(-0.5 * d2_f + V * f  -  round(E_z[frame - 1], 2) * f)), 3)},  \quad \mathrm{{Step}} = {2 * frame}$")
        return line, title
    
    ani = FuncAnimation(fig, update, frames=len(E_x), init_func=init, blit=False, interval=50, repeat=False)
    #plt.show()
    #ani.save("min_Ah.mp4", writer="ffmpeg", fps=30)

    #plt.savefig("min_Ah.pdf", format="pdf", transparent=True, dpi=300)
    return fig, ani, theta_a, theta_b

#minimizacion(*function_2p(0), 0.01, 100, 0.7, 0.5)

def wave_function(n, alpha, beta):
    
    def phi_n(x, n, alpha, beta):
        normalization = 1 / np.sqrt(2**n * factorial(n))
        gaussian = np.exp(-0.5 * ((x - beta) / alpha)**2)
        hermite_poly = eval_hermite(n, alpha * (x - beta) / alpha)
        return normalization * (alpha / np.pi**0.25) * hermite_poly * gaussian

    x = np.linspace(-5, 5, 70)
    y = np.linspace(-5, 5, 70)
    
    X, Y = np.meshgrid(x, y)
    phi_x = phi_n(x, n, alpha, beta)
    phi_y = phi_n(x, n, alpha, beta)
    
    phi_c = np.outer(phi_x, phi_y)
    phi_d = np.abs(phi_c)**2
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, phi_c, cmap='viridis', edgecolor='none', alpha=0.7, rstride=2, cstride=2)
    ax.contour(X, Y, phi_c, zdir='z', offset=ax.get_zlim()[0],  alpha=0.7, levels=15)
    ax.contour(X, Y, phi_c, zdir='y', offset=ax.get_ylim()[0],  alpha=0.7, levels=5, colors="gray")
    ax.contour(X, Y, phi_c, zdir='x', offset=ax.get_xlim()[1],  alpha=0.7, levels=5, colors="gray")
    
    fig.colorbar(surf, ax=ax, shrink=0.5, pad=0.1,  aspect=30)  # Barra de color
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(r"$\Psi_{%d}(x, y; \alpha={%.2f}, \beta={%.2e})$" % (n, alpha, beta), fontsize=16)
    fig.text(0.5, 0.05, r"$\Psi(x, y; \alpha, \beta)$" " " "electron wave function inside the potential" , ha='center', fontsize=16, color="#4a6c65", family="serif")
    
    ax.set_box_aspect([4, 4, 2])
    ax.view_init(elev=16, azim=120)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.zaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))


    #ax.xaxis.set_major_locator(MultipleLocator(4))
    #ax.yaxis.set_major_locator(MultipleLocator(4))
    #ax.zaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.grid(False)
    #plt.savefig("wave_Ah.pdf", format="pdf", transparent=True, dpi=300)
    #plt.savefig("wave_Ah.pdf")
    plt.tight_layout()

def density(n, alpha, beta):

    def phi_n(x, n, alpha, beta):
           normalization = 1 / np.sqrt(2**n * factorial(n))
           gaussian = np.exp(-0.5 * ((x - beta) / alpha)**2)
           hermite_poly = eval_hermite(n, alpha * (x - beta) / alpha)
           return normalization * (alpha / np.pi**0.25) * hermite_poly * gaussian


    x = np.linspace(-3, 3, 40)
    y = np.linspace(-3, 3, 40)
    
    X, Y = np.meshgrid(x, y)
    
    phi_x = phi_n(x, n, alpha, beta)
    phi_y = phi_n(x, n, alpha, beta)
    
    phi_c = np.outer(phi_x, phi_y)
    phi_d = np.abs(phi_c)**2

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, phi_d, cmap='viridis', edgecolor='none', alpha=0.7, rstride=2, cstride=2)
    
    ax.contour(X, Y, phi_d, zdir='z', offset=ax.get_zlim()[0],  alpha=0.7, levels=15)
    ax.contour(X, Y, phi_d, zdir='y', offset=ax.get_ylim()[0],  alpha=0.7, levels=5, colors="gray")
    ax.contour(X, Y, phi_d, zdir='x', offset=ax.get_xlim()[1],  alpha=0.7, levels=5, colors="gray")
    
    #ax.plot_surface(A, B, Z,cmap='viridis', edgecolor='none', rstride=2, cstride=2, alpha=0.7)
    fig.colorbar(surf, ax=ax, shrink=0.5, pad=0.1,  aspect=30)  # Barra de color
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(r"$P(x, y) = |\langle x, y | \Psi_{%d}(\alpha={%.2f}, \beta={%.2e}) \rangle|^{2}$" % (n, alpha, beta), fontsize=16)
    fig.text(0.5, 0.05, r"$P(x, y)$" " " "Describes the most probable regions for finding the electron" , ha='center', fontsize=15, color="#4a6c65", family="serif")
    
    ax.set_box_aspect([4, 4, 2])
    ax.view_init(elev=16, azim=120)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.zaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))

    #ax.xaxis.set_major_locator(MultipleLocator(4))
    #ax.yaxis.set_major_locator(MultipleLocator(4))
    #ax.zaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4

    ax.grid(False)
    
    plt.tight_layout()
