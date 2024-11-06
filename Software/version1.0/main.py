import tkinter as tk
from tkinter import ttk
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Quantum_System.oscillator import QuantumOscillator, psi_functions
from Quantum_System.H import Hydrogen


colors = {"dark_green":"#4a6c65", "olive":"#7B904B", "black":"#000000",
          "green":"#488c2e", "purple":"#6a0606", "gray":"#b9b9b9", "white": "#ffffff"}

# Gui 

class Gui:
    def __init__(self, window):
        self.window = window
        self.right_half = tk.Frame(self.window, bg="#FFFFFF")
        self.right_half.pack(side=tk.RIGHT, fill="both", expand=1)
        self.left_half = tk.Frame(self.window, bg=colors["dark_green"])
        self.left_half.pack(side=tk.LEFT, fill="both", expand=1)
        self.text_label = tk.Label(self.left_half, text="", bg="#4a6c65", fg="white", width=30)
        self.text_label.place(relx=0.5, rely=0.5, anchor="center")
        self.canvas = None
        self.create_widgets()   

        self.window_counter = 0 
        self.window.bind("<Configure>", self.resize_frames)

        self.style = ttk.Style()
        self.style.configure("TNotebook", background="#FFFFFF", borderwidth=1,
                             highlightthickness=0, relief="flat")  # Configura el fondo del Notebook
        self.style.configure("TNotebook.Tab", background="#FFFFFF", foreground="#000000", padding=[10, 5])
        self.style.map("TNotebook.Tab",
               background=[("selected", "#FFFFFF")],  # Color de la pestaña seleccionada
               foreground=[("selected", "#000000")])  # Color del texto de la pestaña seleccionada
        
        # Configura el color de fondo y del texto de las pestañas
         
        self.window.bind("<Configure>", self.resize_frames)
    

        self.notebook = ttk.Notebook(self.right_half)
        self.notebook.pack(fill="both", expand=1)
        self.open_new_tab()
        
        new = tk.Button(self.left_half, text="New", fg="#FFFFFF", command=self.open_new_tab)
        new.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        new.place(relx=0.5, rely=0.1, anchor="center")
        
        self.selected_system = None


    def open_new_tab(self):    
        self.window_counter += 1
        new_tab = tk.Frame(self.notebook, bg="#FFFFFF")  # Usa el notebook como contenedor
        self.notebook.add(new_tab, text=f"Ventana {self.window_counter}")
        #label = tk.Label(new_tab, text="Esta es una nueva pestaña vacía", bg="#FFFFFF", fg="#000000")
        #label.pack(pady=40)
        self.notebook.select(new_tab)
    
    def create_widgets(self):
        btn_exit = tk.Button(self.left_half, text="Exit", fg="#FFFFFF", command=self.exit)
        btn_exit.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_exit.place(relx=0.25, rely=0.7, anchor="center")

        approach = tk.Button(self.left_half, text="Approach", fg="#FFFFFF", command=self.Approach)
        approach.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")  
        approach.place(relx=0.5, rely=0.7, anchor="center")

        btn_graph = tk.Button(self.left_half, text="3D", fg="#FFFFFF", command=None)
        btn_graph.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_graph.place(relx=0.75, rely=0.7, anchor="center")

        btn_clear = tk.Button(self.left_half, text="Clear", fg="#FFFFFF", command=self.clean)
        btn_clear.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_clear.place(relx=0.25, rely=0.8, anchor="center")

        btn_about = tk.Button(self.left_half, text="About", fg="#FFFFFF", command=self.Algorithm)
        btn_about.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_about.place(relx=0.5, rely=0.8, anchor="center")

        btn_graph_3D = tk.Button(self.left_half, text="LOGO", fg="#FFFFFF", command=self.logo)
        btn_graph_3D.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_graph_3D.place(relx=0.75, rely=0.8, anchor="center")
    

        density = tk.Button(self.left_half, text=r"Density", fg="#FFFFFF", command=None)
        density.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        density.place(relx=0.5, rely=0.9, anchor="center")
         
        
        # start points
        self.p1 = tk.Entry(self.left_half, width=6, bg="#4a6c65", fg="white", bd=1, relief="flat",
                           highlightbackground="white", highlightcolor="white")
        self.p1.place(relx=0.75, rely=0.4, anchor="center")
        p1 = tk.Label(self.left_half, text="P1", fg="white")
        p1.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        p1.place(relx=0.6, rely=0.4, anchor="center")
        

        
        self.p2 = tk.Entry(self.left_half, width=6, bg="#4a6c65", fg="white", bd=1, relief="flat",
                           highlightbackground="white", highlightcolor="white")
        self.p2.place(relx=0.75, rely=0.5, anchor="center")
        p2 = tk.Label(self.left_half, text="P2", fg="white")
        p2.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        p2.place(relx=0.6, rely=0.5, anchor="center")
        
        self.E = tk.Entry(self.left_half, width=6, bg="#4a6c65", fg="white", bd=1, relief="flat",
                          highlightbackground="white", highlightcolor="white")
        self.E.place(relx=0.75, rely=0.6, anchor="center")
        E = tk.Label(self.left_half, text="E", fg="white")
        E.place(relx=0.6, rely=0.6, anchor="center")
        E.config(bg="#4a6c65", borderwidth=0, fg="white")


        # learning rate 
        self.lr = tk.Entry(self.left_half, width=6, bg="#4a6c65",fg="white", bd=1, relief="flat",
                      highlightbackground="white", highlightcolor="white")
        self.lr.place(relx=0.38, rely=0.4, anchor="center")


        lr_label = tk.Label(self.left_half, text="Lr", fg="white")
        lr_label.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        lr_label.place(relx=0.23, rely=0.4, anchor="center")
        
        #Epochs
        self.epochs = tk.Entry(self.left_half, width=6, bg="#4a6c65",fg="white", bd=1, relief="flat",
                      highlightbackground="white", highlightcolor="white")
        self.epochs.place(relx=0.38, rely=0.5, anchor="center")

        ep_label = tk.Label(self.left_half, text="Ep", fg="white")
        ep_label.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        ep_label.place(relx=0.23, rely=0.5, anchor="center")
        
        
        Labs = tk.Button(self.left_half, text=r"Labs", fg="#FFFFFF", command=None)
        Labs.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        Labs.place(relx=0.75, rely=0.9, anchor="center")
         
        menu_labs  = tk.Menubutton(self.left_half, text="Labs", relief=tk.FLAT, 
                                   bg=colors["dark_green"], fg=colors["white"], bd=0)
        
        menu_labs.menu = tk.Menu(menu_labs, tearoff=0, 
                                bg="white", fg="black", 
                                activebackground=colors["dark_green"], 
                                activeforeground="white", relief=tk.FLAT, bd=0)
      
        menu_labs["menu"] = menu_labs.menu
        menu_labs.place(relx=0.75, rely=0.9,anchor="center")

        menu_labs.menu.add_command(label="Hydrogen Atom", command=self.labs)
        menu_labs.menu.add_command(label="Yukawa", command=None)
        menu_labs.menu.add_command(label="Quantum Oscillator", command=None)


        menu_boton = tk.Menubutton(self.left_half, text="Quamtum System", relief=tk.FLAT,
                                bg=colors["dark_green"], fg="white", bd=0)

        menu_boton.menu = tk.Menu(menu_boton, tearoff=0, 
                                bg="white", fg="black", 
                                activebackground=colors["dark_green"], 
                                activeforeground="white", relief=tk.FLAT, bd=0)
        menu_boton["menu"] = menu_boton.menu
        

        menu_boton.menu.add_command(label="Quamtum oscillator", command=self.update_psi_trial_oscillator)
        menu_boton.menu.add_command(label="Hydrogen Atom", command=self.update_Hydrogen)

        #menu_boton.menu.add_command(label="Particle in box", command=self.update_psi_trial_particleinbox)
        #menu_boton.menu.add_command(label="Double well", command=self.update_Double_well)
        #menu_boton.menu.add_command(label="Anaharmonic oscillator", command=self.update_Anarmonic)
        #menu_boton.menu.add_command(label="Yukawa", command=self.update_yukawa)
        #menu_boton.menu.add_command(label="Lennard-Jhones", command=self.update_LJ)
        #menu_boton.menu.add_command(label="Histograma", command=self.histograma)

        menu_boton.place(relx=0.36, rely=0.2, anchor="center")

        self.psi_trial = tk.Menubutton(self.left_half, text=r"Ψ Trial", relief=tk.FLAT, 
                                  bg=colors["dark_green"], fg="white", bd=0)

        self.psi_trial.menu = tk.Menu(self.psi_trial, tearoff=0, 
                                bg="white", fg="black", 
                                activebackground=colors["dark_green"], 
                                activeforeground="white", relief=tk.FLAT, bd=0)
        
        self.psi_trial["menu"] = self.psi_trial.menu
        self.psi_trial.place(relx=0.75, rely=0.2, anchor="center")
    
    # ========
    # The Logo 
    # ========

    def logo(self):
        
        current_tab = self.notebook.nametowidget(self.notebook.select())
        
        import matplotlib.image as mpimg
        import os
        
        self.clean()

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        ruta = os.path.abspath('logo.jpg')
        imagen = mpimg.imread(ruta)
        
        plt.axis("off")
        plt.imshow(imagen)

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
    
    # ====================== 
    # The Quamtum oscillator 
    # ======================
    
    def update_psi_trial_oscillator(self):
       
        from Quantum_System.oscillator import OA

        current_tab     = self.notebook.nametowidget(self.notebook.select())
        self.selected_system = "Quantum oscillator"  
        
        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ₁(x) = x * e^(-α * x²)", command=lambda: Q_O.Psi("psi1"))
        self.psi_trial.menu.add_command(label="ψ₂(x) = 1 / (α * x² + 1)²", command=lambda: Q_O.Psi("psi2"))
        self.psi_trial.menu.add_command(label="ψ₃(x) = 1 / (x² + α)", command=lambda: Q_O.Psi("psi3"))
        self.psi_trial.menu.add_command(label="ψ₄(x) = 1 / (x² + α²)", command=lambda: Q_O.Psi("psi4"))
        self.psi_trial.menu.add_command(label="ψ₅(x) = 1 / (x² + α²)²", command=lambda: Q_O.Psi("psi5"))
        self.psi_trial.menu.add_command(label="ψ₆(x) = (x²) / (x² + α)²", command=lambda: Q_O.Psi("psi6"))
        
        #self.clean()
        OA()
    
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
    
        
    
    # ============  
    # The Hydrogem
    # ============  

    
    
    def update_Hydrogen(self):
        
        from Quantum_System.H import H
        current_tab     = self.notebook.nametowidget(self.notebook.select())
        self.selected_system = "Hydrogen Atom"  

        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ(x) = α * e^(-β*r)")
        self.psi_trial.menu.add_command(label="ψ(x) = 11")
        
        #self.clean()
        H()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

    def Approach(self):

        current_tab = self.notebook.nametowidget(self.notebook.select())
 
        if self.selected_system == "Quantum oscillator":
            print(self.selected_system)
            E_1, dE_1 = Q_O.calculate_energy()
            Q_O.plot_energy(E_1, dE_1)
            self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
        elif self.selected_system == "Hydrogen Atom":
            print(self.selected_system)
            E = H_A.Variation()
            self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)


    # ===========================================
    # The riseze of the windows and more settings 
    # ===========================================

    def resize_frames(self, event):
        global_width = self.window.winfo_width()
        new_global_width = global_width // 3
        self.left_half.configure(width=new_global_width)
        self.right_half.configure(width=2*new_global_width)

    def exit(self):
        self.window.quit()
    
    def get_p1(self):
        return self.p1.get()
    
    def get_p2(self):
        return self.p2.get()

    def get_lr(self):
        return self.lr.get()

    def get_ep(self):
        return self.epochs.get()

    def Algorithm(self):
        
        from Quantum_System.Algorithm import Algorithm
        
        current_tab = self.notebook.nametowidget(self.notebook.select())
        self.psi_trial.menu.delete(0, tk.END)
        self.clean()
        Algorithm()

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
     
    
    def clean(self):
         if self.canvas:
             self.canvas.get_tk_widget().pack_forget()
             plt.clf()  # Clear the current figure
             self.canvas = None
    
    def labs(self):
        from H.D_A_H import GUI
        app = GUI()
        
    
       
if __name__ == "__main__":

    window = tk.Tk()
    window.config(bg="#FFFFFF")
    window.minsize(1000, 500)
    #window.maxsize(1000, 500)
    app = Gui(window=window)
    Q_O = QuantumOscillator(app)
    H_A = Hydrogen(app)
    window.mainloop()

