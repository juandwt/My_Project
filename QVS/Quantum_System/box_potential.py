import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import MaxNLocator

plt.rcParams['toolbar'] = 'none'
plt.rcParams['mathtext.fontset'] = 'cm'  # Usa la fuente Computer Modern para matemáticas
font_params = {"fontsize": 16, "fontweight": "bold", "fontstyle": "italic"}
#plt.rcParams['axes3d.mouserotationstyle'] = 'azel' 


E = {'E1': lambda a, b:  (105.0*a**2 + 42.0*a*b + 5.9999999999997*b**2)/(21*a**2 + 9*a*b + b**2),
     'E2': lambda a, b:  (0.0249999999999999*a**2 + 0.00714285714285734*a*b + 0.000793650793649903*b**2)/(0.00119047619047619*a**2 + 0.000396825396825506*a*b + 3.60750360748341e-5*b**2),
     'E3': lambda a, b:  (0.00293944738389096*a**2 + 0.000646678424458536*a*b + 6.14611725708869e-5*b**2)/(5.87889476776904e-5*a**2 + 1.60333493673392e-5*a*b + 1.30185315394549e-6*b**2),
     'E4': lambda a, b:  (0.000333271329366003*a**2 + 5.49580627673407e-5*a*b + 4.48769980465613e-6*b**2)/(3.52295274183567e-6*a**2 + 7.69629676322658e-7*a*b + 5.41992732916441e-8*b**2),
     'E5': lambda a, b:  (3.87296969672768e-5*a**2 + 4.730018412058e-6*a*b + 3.25590882255256e-7*b**2)/(2.46239094281453e-7*a**2 + 4.26098338557335e-8*a*b + 2.51732590328402e-9*b**2),
     'E6': lambda a, b:  (4.65973975272149e-6*a**2 + 4.2800324973058e-7*a*b + 2.44310740526998e-8*b**2)/(1.9429461609044e-8*a**2 + 2.68855784857358e-9*a*b + 1.3041079327536e-10*b**2),
     }

def Box():
    fig = plt.figure()
    ax = plt.axes(projection='3d',computed_zorder=False)
    
    r = np.linspace(0, 1, 13)
    X, Y = np.meshgrid(r, r)
    
    Z_base = np.zeros_like(X)  
    Z_top = np.ones_like(X)    
    
    ax.plot_surface(0, X, Y, cmap='viridis' ,alpha=0.6)
    ax.plot_surface(1, X, Y, cmap='viridis',alpha=0.6)
    #ax.plot_surface(X, Y, Z_base, cmap='viridis', alpha=0.5)  # Base
    ax.plot_surface(X, 0 * Y, Y, cmap='viridis', alpha=0.6)   
    ax.plot_surface(X, Z_top, 1* Y, cmap='viridis', alpha=0.6)
    
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('V')
    
    scatter = ax.scatter(0.5, 0.5, 0.9, color='#000000' , s=30, zorder=100)
    ax.text(0.5, 0.5, 1,r'$e^- \Rightarrow E_{n}$', fontsize=16, color='black', ha='center')


    ax.set_title(r"$e^{-}~~\mathrm{locked\ in\ potential}~~\left[ \frac{\hat{p}^2}{2m} + 0 \hat{P}_{\mathrm{dentro}} + \infty \hat{P}_{\mathrm{fuera}} \right] |\psi\rangle = E_{n}|\psi\rangle$", fontsize=16)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)
    
    
    ax.set_box_aspect([3.5, 3.5, 2])
    ax.view_init(elev=10, azim=135)
    ax.grid(False)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
             
    ax.xaxis.set_major_locator(MultipleLocator(0.4))
    ax.yaxis.set_major_locator(MultipleLocator(0.4))
    ax.zaxis.set_major_locator(MultipleLocator(0.4))
             
    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    return fig

n = None

def function_2p(n_param):
    global n
    n = n_param
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([4, 4, 2])


    if   n == 1:
        a_values = np.linspace(0.3, 4.5, 40)
        b_values = np.linspace(1, 7, 40)
    
    elif n == 2:
        
        a_values = np.linspace(0.3, 3, 40)
        b_values = np.linspace(1, 7, 40)
    
    elif n == 3:
        
        a_values = np.linspace(0.1, 2, 40)
        b_values = np.linspace(1, 5, 40)
    
    elif n == 4:
        
        a_values = np.linspace(-0.006, 2, 40)
        b_values = np.linspace(1, 5, 40)
    
    elif n == 5:
        
        a_values = np.linspace(-0.006, 2, 40)
        b_values = np.linspace(1, 5, 40)


    elif n == 6:
        a_values = np.linspace(-0.006, 0.8, 30)
        b_values = np.linspace(0.9, 7, 30)
    else: 
        None

    A, B = np.meshgrid(a_values, b_values)
    Z = E[f'E{n}'](A, B)

    ax.plot_surface(A, B, Z,cmap='viridis', edgecolor='none', rstride=2, cstride=2, alpha=0.7)
    ax.contour(A, B, Z, zdir='z', offset=ax.get_zlim()[0],  alpha=0.7, levels=15)
    
    ax.view_init(elev=40, azim=150)
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
        if i%2 ==0 or i == iters -1:
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
    ax.contour(A, B, Z, zdir='z', offset=ax.get_zlim()[0],  alpha=0.7, levels=15)
    
    ax.set_box_aspect([4, 4, 2])
    
    ax.view_init(elev=16, azim=120)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.zaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))

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
    title = ax.set_title(fr"$H | \Psi_{{{n}}}\rangle= {round(E_func(p_1, p_2), 2)}|\Psi_{{{n}}}\rangle$", fontsize=16, y=1.1)
    line,  = ax.plot([], [], [], label="Evolución de la línea", color="#000000")
    fig.text(0.5, 0.05, "The error" " " r"$J_{error} \rightarrow 0$" " " "when approaching the minimum", ha='center', fontsize=16, color="#4a6c65", family="serif")
    # Validacion
    
    def phi_n(x, n, alpha, beta):
            if n == 1:
                return x * (1 - x) + beta * x**2 * (1 - x)**2 + alpha * x**2 * (1 - x)**3
        
            product_terms = np.ones_like(x)  # Inicializar con unos para evitar errores
            for k in range(1, n):
                product_terms *= (k/n - x)  # Multiplicación elemento a elemento
            
            return (x * (1 - x) * product_terms +  
                    beta * x**2 * (1 - x)**2 * product_terms + 
                    alpha * x**2 * (1 - x)**3 * product_terms)


    alpha = theta_a
    beta  = theta_b
    E_w   = E_min
    
    x = np.linspace(0, 1, 100)
    V = 1
    
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
    
    #ani.save("min_slab.mp4", writer="ffmpeg", fps=30)
    #plt.savefig("min_slab.pdf", format="pdf", transparent=True, dpi=300)
    return fig, ani, theta_a, theta_b

def wave_function(n, alpha, beta):
    def phi_n(x, n, alpha, beta):
            if n == 1:
                return x * (1 - x) + beta * x**2 * (1 - x)**2 + alpha * x**2 * (1 - x)**3

            product_terms = np.ones_like(x)  # Inicializar con unos para evitar errores
            for k in range(1, n):
                product_terms *= (k/n - x)  # Multiplicación elemento a elemento
            
            return (x * (1 - x) * product_terms +  
                    beta * x**2 * (1 - x)**2 * product_terms + 
                    alpha * x**2 * (1 - x)**3 * product_terms)
      
    x = np.linspace(0, 1, 70)
    y = np.linspace(0, 1, 70)
    
    X, Y = np.meshgrid(x, y)
    phi_x = phi_n(x, n, alpha, beta)
    phi_y = phi_n(x, n, alpha, beta)
    
    phi_c = np.outer(phi_x, phi_y)
    phi_d = np.abs(phi_c)**2
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, phi_c, cmap='viridis', edgecolor='none', alpha=0.7, rstride=2, cstride=2)
  

    fig.colorbar(surf, ax=ax, shrink=0.5, pad=0.1,  aspect=30)  # Barra de color
    ax.contour(X, Y, phi_c, zdir='z', offset=ax.get_zlim()[0],  alpha=0.5, levels=10)
    ax.contour(X, Y, phi_c, zdir='x', offset=ax.get_ylim()[-1], alpha=0.5, levels=5, colors="gray")
    ax.contour(X, Y, phi_c, zdir='y', offset=ax.get_ylim()[0],  alpha=0.5, levels=5, colors="gray")
    
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
    
    ax.grid(False)

    ax.zaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    
    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    
    #plt.savefig("wave_slab.pdf")
    #plt.savefig("wave_slab.pdf", format="pdf", transparent=True, dpi=300)
    plt.tight_layout()


def density(n, alpha, beta):
 
    def phi_n(x, n, alpha, beta):
            if n == 1:
                return x * (1 - x) + beta * x**2 * (1 - x)**2 + alpha * x**2 * (1 - x)**3
        
            product_terms = np.ones_like(x) 
            for k in range(1, n):
                product_terms *= (k/n - x)  
            
            return (x * (1 - x) * product_terms +  
                    beta * x**2 * (1 - x)**2 * product_terms + 
                    alpha * x**2 * (1 - x)**3 * product_terms)
 
    x = np.linspace(0, 1, 40)
    y = np.linspace(0, 1, 40)
    
    X, Y = np.meshgrid(x, y)
    
    phi_x = phi_n(x, n, alpha, beta)
    phi_y = phi_n(x, n, alpha, beta)
    
    phi_c = np.outer(phi_x, phi_y)
    phi_d = np.abs(phi_c)**2

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, phi_d, cmap='viridis', edgecolor='none', alpha=0.7, rstride=2, cstride=2)
    
    ax.contour(X, Y, phi_d, zdir='z', offset=ax.get_zlim()[0],  alpha=0.7, levels=15)
    ax.contour(X, Y, phi_d, zdir='x', offset=X.max(),           alpha=0.7, levels=5, colors="gray")
    ax.contour(X, Y, phi_d, zdir='y', offset=ax.get_zlim()[0],  alpha=0.7, levels=5, colors="gray")
    
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
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))

    ax.grid(False)

    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    
    plt.tight_layout()

