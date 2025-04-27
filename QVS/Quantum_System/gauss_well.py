import sympy as sp
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.animation import FuncAnimation
from scipy.special import eval_hermite, factorial
from matplotlib.ticker import MaxNLocator

plt.rcParams['toolbar'] = 'none'
plt.rcParams['mathtext.fontset'] = 'cm'  # Usa la fuente Computer Modern para matemáticas
font_params = {"fontsize": 16, "fontweight": "bold", "fontstyle": "italic"}
#plt.rcParams['axes3d.mouserotationstyle'] = 'azel' 


def gauss_well(V0):
    def gaussian_potential(x, y, z, sigma=1.5, V0=V0):
        return V0*np.exp(-(x**2 + y**2) / (5 * sigma**2))

    x = np.linspace(-3.5, 3.5, 17)
    y = np.linspace(-3.5, 3.5, 17)

    X, Y = np.meshgrid(x, y)
    Z = gaussian_potential(X, Y, 0) 

    fig = plt.figure()
    ax = plt.axes(projection='3d',computed_zorder=False)
    ax.grid(False)

    ax.set_box_aspect([2.5, 2.5, 3])

    scatter = ax.scatter(0, 0, -5.5, color='#000000' , s=30, zorder=100)
    ax.text(0, 0, -5, r'$e^- \Rightarrow E_{n}$', fontsize=16, color='black', ha='center')

    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    ax.contour(X, Y, Z, zdir='z', offset=-21,  alpha=0.7, levels=10)
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('$V(x, y)$')
    ax.set_title(r"$e^{-} \, \mathrm{locked\ in\ potential} \, \left[ -\frac{\hbar^2}{2m} \nabla^2 - 20 e^{-\frac{x^2 + y^2}{2 (1.5)^2}} \right] |\psi\rangle = E_{n} |\psi\rangle$", fontsize=16, family="serif")
    ax.view_init(elev=25, azim=150)

    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.zaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))

    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    return fig


E = {'psi0': lambda a, b: 0.25*a**2 - 20.0*a*np.exp(-0.22*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22))/np.sqrt(1.0*a**2 + 0.22)

, 'psi1': lambda a, b: a**2*(0.75*a**4*np.sqrt(1.0*a**2 + 0.22)*np.exp(0.22*b**2) - 20.0*a**3*np.exp(0.0493827160493827*b**2/(1.0*a**2 + 0.22)) + 0.333333333333333*a**2*np.sqrt(1.0*a**2 + 0.22)*np.exp(0.22*b**2) - 1.97530864197531*a*b**2*np.exp(0.0493827160493827*b**2/(1.0*a**2 + 0.22)) - 4.44444444444444*a*np.exp(0.0493827160493827*b**2/(1.0*a**2 + 0.22)) + 0.037037037037037*np.sqrt(1.0*a**2 + 0.22)*np.exp(0.22*b**2))*np.exp(-0.22*b**2)/(np.sqrt(1.0*a**2 + 0.22)*(1.0*a**4 + 0.444444444444444*a**2 + 0.0493827160493827))

, 'psi2': lambda a, b: a*(-55358.4375*a**4*(1.0*a**2 + 0.22)**(19/2)*(b**4*(1.76208199114288e-6*a**2 + 3.91573775809528e-7) + 0.00010704648096193*b**2*(1.0*a**2 + 0.22)**2 + 0.000541922809869769*(1.0*a**2 + 0.22)**3)*np.exp(0.444444444444444*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) + 1822.5*a**2*(1.0*a**2 + 0.22)**(25/2)*(0.0109739368998628*a**2 + 0.00108384561973954*b**2 + 0.00243865264441396)*np.exp(0.444444444444444*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) + 1.25*a*(1.0*a**2 + 0.22)**15*np.exp(0.666666666666667*b**2) - 10.0*(1.0*a**2 + 0.22)**(29/2)*np.exp(b**2*(0.444444444444444 + 0.0493827160493827/(1.0*a**2 + 0.22))))*np.exp(-0.666666666666667*b**2)/(1.0*a**2 + 0.22)**15

, 'psi3': lambda a, b: a**2*(-1868347.265625*a**5*(1.0*a**2 + 0.22)**30*(1.71884236294992e-9*b**6 + b**4*(2.61049183873019e-7*a**2 + 5.80109297495597e-8) + 7.92936896014294e-6*b**2*(1.0*a**2 + 0.22)**2 + 2.67616202404824e-5*(1.0*a**2 + 0.22)**3)*np.exp(0.444444444444444*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) + 110716.875*a**3*(1.0*a**2 + 0.22)**31*(b**4*(1.76208199114288e-6*a**2 + 3.91573775809528e-7) + 0.00010704648096193*b**2*(1.0*a**2 + 0.22)**2 + 0.000541922809869769*(1.0*a**2 + 0.22)**3)*np.exp(0.444444444444444*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) - 2733.75*a*(1.0*a**2 + 0.22)**34*(0.0109739368998628*a**2 + 0.00108384561973954*b**2 + 0.00243865264441396)*np.exp(0.444444444444444*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) + 1.75*(1.0*a**2 + 0.22)**(73/2)*np.exp(0.666666666666667*b**2))*np.exp(-0.666666666666667*b**2)/(1.0*a**2 + 0.22)**(73/2)

, 'psi4': lambda a, b: a*(-66209556.225586*a**8*(1.0*a**2 + 0.22)**(127/2)*(1.19761699249673e-12*b**8 + b**6*(3.39524417372823e-10*a**2 + 7.5449870527294e-11) + 2.57826354442487e-8*b**4*(1.0*a**2 + 0.22)**2 + 5.22098367746037e-7*b**2*(1.0*a**2 + 0.22)**3 + 1.32156149335716e-6*(1.0*a**2 + 0.22)**4)*np.exp(0.888888888888889*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) + 5605041.796875*a**6*(1.0*a**2 + 0.22)**(131/2)*(1.71884236294992e-9*b**6 + b**4*(2.61049183873019e-7*a**2 + 5.80109297495597e-8) + 7.92936896014294e-6*b**2*(1.0*a**2 + 0.22)**2 + 2.67616202404824e-5*(1.0*a**2 + 0.22)**3)*np.exp(0.888888888888889*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) - 193754.53125*a**4*(1.0*a**2 + 0.22)**(133/2)*(b**4*(1.76208199114288e-6*a**2 + 3.91573775809528e-7) + 0.00010704648096193*b**2*(1.0*a**2 + 0.22)**2 + 0.000541922809869769*(1.0*a**2 + 0.22)**3)*np.exp(0.888888888888889*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) + 2733.75*a**2*(1.0*a**2 + 0.22)**(139/2)*(0.0109739368998628*a**2 + 0.00108384561973954*b**2 + 0.00243865264441396)*np.exp(0.888888888888889*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) + 2.25*a*(1.0*a**2 + 0.22)**72*np.exp(1.11111111111111*b**2) - 7.5*(1.0*a**2 + 0.22)**(143/2)*np.exp(b**2*(0.888888888888889 + 0.0493827160493827/(1.0*a**2 + 0.22))))*np.exp(-1.11111111111111*b**2)/(1.0*a**2 + 0.22)**72

, 'psi5': lambda a, b: a**2*(-2413338324.42261*a**9*(1.0*a**2 + 0.22)**112*(6.4901596572161e-16*b**10 + b**8*(2.95707899381909e-13*a**2 + 6.5712866529313e-14) + 4.19165947373855e-11*b**6*(1.0*a**2 + 0.22)**2 + 2.12202760858014e-9*b**4*(1.0*a**2 + 0.22)**3 + 3.22282943053109e-8*b**2*(1.0*a**2 + 0.22)**4 + 6.52622959682546e-8*(1.0*a**2 + 0.22)**5)*np.exp(0.888888888888889*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) + 264838224.902344*a**7*(1.0*a**2 + 0.22)**114*(1.19761699249673e-12*b**8 + b**6*(3.39524417372823e-10*a**2 + 7.5449870527294e-11) + 2.57826354442487e-8*b**4*(1.0*a**2 + 0.22)**2 + 5.22098367746037e-7*b**2*(1.0*a**2 + 0.22)**3 + 1.32156149335716e-6*(1.0*a**2 + 0.22)**4)*np.exp(0.888888888888889*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) - 12144257.2265625*a**5*(1.0*a**2 + 0.22)**116*(1.71884236294992e-9*b**6 + b**4*(2.61049183873019e-7*a**2 + 5.80109297495597e-8) + 7.92936896014294e-6*b**2*(1.0*a**2 + 0.22)**2 + 2.67616202404824e-5*(1.0*a**2 + 0.22)**3)*np.exp(0.888888888888889*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) + 276792.1875*a**3*(1.0*a**2 + 0.22)**117*(b**4*(1.76208199114288e-6*a**2 + 3.91573775809528e-7) + 0.00010704648096193*b**2*(1.0*a**2 + 0.22)**2 + 0.000541922809869769*(1.0*a**2 + 0.22)**3)*np.exp(0.888888888888889*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) - 3417.1875*a*(1.0*a**2 + 0.22)**120*(0.0109739368998628*a**2 + 0.00108384561973954*b**2 + 0.00243865264441396)*np.exp(0.888888888888889*b**2 + 0.0493827160493827*b**2/(1.0*a**2 + 0.22)) + 2.75*(1.0*a**2 + 0.22)**(245/2)*np.exp(1.11111111111111*b**2))*np.exp(-1.11111111111111*b**2)/(1.0*a**2 + 0.22)**(245/2)
}

n = None

def function_2p(n_param):
    global n
    n = n_param
    
    a_values = np.linspace(-0.5, 4, 50)
    b_values = np.linspace(-4, 4, 50)
    
    A, B = np.meshgrid(a_values, b_values)
    Z = E[f'psi{n}'](A, B)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([4, 4, 2])

    ax.plot_surface(A, B, Z,cmap='viridis', edgecolor='none', rstride=2, cstride=2, alpha=0.7)
    ax.contour(A, B, Z, zdir='z', offset=ax.get_zlim()[0],  alpha=0.7, levels=10)
    
    ax.view_init(elev=16, azim=120)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.zaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    
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
    E_func = E[f'psi{n}']

    # Minimización numerica
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
    
    # Validation
    import numpy as np
    from scipy.special import hermite, factorial
    
    s = 1.5
    
    def gauss_p(x):
        return -20 * np.exp(-x**2 / (2 * s**2))
    
    def phi_n(x, n, alpha, beta):
        normalization = 1 / np.sqrt(2**n * factorial(n))
        gaussian = np.exp(-0.5 * alpha**2 * (x - beta)**2)
        hermite_poly = hermite(n)(alpha * (x - beta))  # Usar polinomios de Hermite
        return normalization * (alpha / np.pi**0.25) * hermite_poly * gaussian
    
    alpha = theta_a
    beta  = theta_b
    E_w   = E_min
    
    x = np.linspace(-4, 4, 100)
    V = gauss_p(x)
    
    f = phi_n(x, 1, alpha, beta)
    d_f = np.gradient(f, x)  # Primera derivada
    d2_f = np.gradient(d_f, x)  # Segunda derivada
    
    A, B = np.meshgrid(a_values, b_values)
    Z = E_func(A, B)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(p_1, p_2, E_func(p_1,p_2), color="#e80000", s=10)
    
    ax.plot_surface(A, B, Z,cmap='viridis', edgecolor='none', rstride=2, cstride=2, alpha=0.7)
    ax.contour(A, B, Z, zdir='z', offset=ax.get_zlim()[0],  alpha=0.7, levels=10)
    ax.set_box_aspect([4, 4, 2])
    
    ax.view_init(elev=16, azim=120)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.zaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))

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

    title = ax.set_title(fr"$\hat{{H}}| \Psi_{{{n}}}\rangle= {round(E_func(p_1, p_2), 2)}|\Psi_{{{n}}}\rangle$" "\n"
                         ""  , fontsize=16, y=1.1)

    fig.text(0.5, 0.05, "The error" " " r"$J_{error} \rightarrow 0$" " " "when approaching the minimum", ha='center', fontsize=16, color="#4a6c65", family="serif")
    line,  = ax.plot([], [], [], label="Evolución de la línea", color="#000000")
    
    
    # Validation
    import numpy as np
    from scipy.special import hermite, factorial
    
    s = 1.5
    
    def gauss_p(x):
        return -20 * np.exp(-x**2 / (2 * s**2))
    
    def phi_n(x, n, alpha, beta):
        normalization = 1 / np.sqrt(2**n * factorial(n))
        gaussian = np.exp(-0.5 * alpha**2 * (x - beta)**2)
        hermite_poly = hermite(n)(alpha * (x - beta))  # Usar polinomios de Hermite
        return normalization * (alpha / np.pi**0.25) * hermite_poly * gaussian
    
    x = np.linspace(-4, 4, 100)
    V = gauss_p(x)
    
    f = phi_n(x, n, alpha, beta)
    d_f = np.gradient(f, x)  
    d2_f = np.gradient(d_f, x)
    
    
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
    #ani.save("min_gauss.mp4", writer="ffmpeg", fps=30)
    #plt.savefig("gauss_min.pdf", format="pdf", transparent=True, dpi=300)
    return fig, ani, theta_a, theta_b

def wave_function(n, alpha, beta):
    
    def phi_n(x, n, alpha, beta):
        normalization = 1 / np.sqrt(2**n * factorial(n))
        gaussian = np.exp(-0.5 * alpha**2 * (x - beta)**2)
        hermite_poly = eval_hermite(n, alpha * (x - beta))
        return normalization * (alpha / np.pi**0.25) * hermite_poly * gaussian
    
    x = np.linspace(-4, 4, 60)
    y = np.linspace(-4, 4, 60)
    
    X, Y = np.meshgrid(x, y)

    phi_x = phi_n(x, n, alpha, beta)
    phi_y = phi_n(x, n, alpha, beta)
    
    phi_c = np.outer(phi_x, phi_y)
    
    phi_d = np.abs(phi_c)**2
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, phi_c, cmap='viridis', edgecolor='none', alpha=0.7)
    
    ax.contour(X, Y, phi_c, zdir='z', offset=ax.get_zlim()[0],  alpha=0.7, levels=10)
    ax.contour(X, Y, phi_c, zdir='y', offset=ax.get_ylim()[0],  alpha=0.7, levels=10, colors="gray")
    ax.contour(X, Y, phi_c, zdir='x', offset=ax.get_xlim()[1],  alpha=0.7, levels=10, colors="gray")
    
    fig.colorbar(surf, ax=ax, shrink=0.5, pad=0.1,  aspect=30)  # Barra de color
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(r"$\Psi_{%d}(x, y; \alpha={%.2f}, \beta={%.2e})$" % (n, alpha, beta), fontsize=16)
    fig.text(0.5, 0.05, r"$\Psi(x, y; \alpha, \beta)$" " " "electron wave function inside the potential" , ha='center', fontsize=16, color="#4a6c65", family="serif")
    
    ax.set_box_aspect([4, 4, 3])
    ax.view_init(elev=16, azim=120)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.zaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))

    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.grid(False)
    
    #plt.savefig("wave_gauss.pdf")
    #plt.savefig("gauss_den.pdf", format="pdf", transparent=True, dpi=300)
    plt.tight_layout()


def density(n, alpha, beta):
    
    def phi_n(x, n, alpha, beta):
        normalization = 1 / np.sqrt(2**n * factorial(n))
        gaussian = np.exp(-0.5 * alpha**2 * (x - beta)**2)
        hermite_poly = eval_hermite(n, alpha * (x - beta))
        return normalization * (alpha / np.pi**0.25) * hermite_poly * gaussian
    
    x = np.linspace(-3, 3, 60)
    y = np.linspace(-3, 3, 60)
    
    X, Y = np.meshgrid(x, y)
    
    phi_x = phi_n(x, n, alpha, beta)
    phi_y = phi_n(x, n, alpha, beta)
    
    phi_c = np.outer(phi_x, phi_y)
    phi_d = np.abs(phi_c)**2

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, phi_d, cmap='viridis', edgecolor='none', alpha=0.7)
    ax.contour(X, Y, phi_d, zdir='z', offset=ax.get_zlim()[0],  alpha=0.7, levels=10)
    ax.contour(X, Y, phi_d, zdir='y', offset=ax.get_ylim()[0],  alpha=0.7, levels=10, colors="gray")
    ax.contour(X, Y, phi_d, zdir='x', offset=ax.get_xlim()[1],  alpha=0.7, levels=10, colors="gray")
    
    #ax.plot_surface(A, B, Z,cmap='viridis', edgecolor='none', rstride=2, cstride=2, alpha=0.7)
    fig.colorbar(surf, ax=ax, shrink=0.5, pad=0.1,  aspect=30)  # Barra de color
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(r"$P(x, y) = |\langle x, y | \Psi_{%d}(\alpha={%.2f}, \beta={%.2e}) \rangle|^{2}$" % (n, alpha, beta), fontsize=16)
    fig.text(0.5, 0.05, r"$P(x, y)$" " " "Describes the most probable regions for finding the electron" , ha='center', fontsize=15, color="#4a6c65", family="serif")
    
    ax.set_box_aspect([4, 4, 3])
    ax.view_init(elev=16, azim=120)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.zaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))

    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.grid(False)
    
    plt.tight_layout()

