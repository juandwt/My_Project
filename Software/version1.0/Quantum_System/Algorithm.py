import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

colors = {"dark_green":"#4a6c65", "olive":"#7B904B", "black":"#000000",
          "green":"#488c2e", "purple":"#6a0606", "gray":"#b9b9b9"}

#self.clean()
 
def Algorithm():       
    plt.rcParams["toolbar"] = "none"
    fig, ax = plt.subplots(nrows=1, ncols=1)
    plt.axis("off")
    #plt.rcParams["text.usetex"] = True  # Habilitar LaTeX
    
    plt.rcParams['mathtext.fontset'] = 'cm'  # Usa la fuente Computer Modern para matemáticas
    
    font_params = {"fontsize": 16, "fontweight": "bold", "fontstyle": "italic"}
    
    an0 = ax.annotate(r"$\{V(\vec{r}),~ \psi_{test}\}$", xy=(0.15, 0.71), xycoords="axes fraction",
                      va="center", ha="center", 
                      bbox=dict(boxstyle="square", fc="w", linestyle="-"),
                      arrowprops=dict(arrowstyle="->"),
                      xytext=(0.15, 0.85), **font_params)
    
    
    an1 = ax.annotate(r"$E[\psi_{test}] = \frac{< \psi_{test} | \hat{H} | \psi_{test} >}{< \psi_{test} | \psi_{test} >} \geq E_0$",
                      xy=(0.15, 0.5), xycoords="data",
                      va="center", ha="center",
                      bbox=dict(boxstyle="square", fc="w", linestyle="-"),
                      arrowprops=dict(arrowstyle="->"),
                      xytext=(0.15, 0.65), **font_params)
    
    an2 = ax.annotate(r"$E(\theta^{(t)}, \mu^{(t)})$", 
                      xy=(0.49, 0.2), xycoords="data",
                      va="center", ha="center",
                      bbox=dict(boxstyle="square", fc=colors["dark_green"], 
                                edgecolor=colors["dark_green"], alpha=0.5),
                      arrowprops=dict(arrowstyle="->", connectionstyle="angle, angleA=90, angleB=180, rad=0"),
                      xytext=(0.15, 0.45), **font_params)
    
    
    an3 = ax.annotate(r"$\theta^{(t+1)} = \theta^{(t)} - \eta_{\theta}\nabla_{\theta} E(\theta, \mu)$" "\n" r"$\mu^{(t+1)} = \mu^{(t)} - \eta_{\mu}\nabla_{\mu} E(\theta, \mu)$",
                      xy=(0.75, 0.41), xycoords="data",
                      va="center", ha="center",
                      bbox=dict(boxstyle="square", fc="w"),
                      arrowprops=dict(arrowstyle="->", connectionstyle="angle, angleA=90, angleB=180, rad=0"),
                      xytext=(0.75, 0.2), **font_params)
    
    an4 = ax.annotate(r"$\eta_{\theta}, Iter$", xy=(0.37, 0.2), xycoords="data",
                      va="center", ha="center", 
                      bbox=dict(boxstyle="square", fc="w", linestyle="--"),
                      arrowprops=dict(arrowstyle="->"),
                      xytext=(0.37, 0.35), **font_params)
    
    an5 = ax.annotate(r"$E_{0}$", xy=(0.75, 0.61), xycoords="data",
                      va="center", ha="center", 
                      bbox=dict(boxstyle="square", fc=colors["dark_green"], alpha=0.5),
                      arrowprops=dict(arrowstyle="->"),
                      xytext=(0.75, 0.45), **font_params)
    
    an5 = ax.annotate(r"$H_{0}\psi_{test} - E_{0}\Psi_{test}=0$", xy=(0.75, 0.65), xycoords="data",
              va="center", ha="center", 
              bbox=dict(boxstyle="square", fc="w"),
              arrowprops=dict(arrowstyle="->"),
              xytext=(0.75, 0.65), **font_params)
    
    

    plt.rcParams["text.usetex"] = False

    
