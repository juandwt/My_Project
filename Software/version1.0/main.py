import tkinter as tk
from tkinter import ttk

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
colors = {"green_1": "#4a6c65", "black":"#000000", "white": "#ffffff"}

# =============
#  Gui's class 
# =============      

class Gui:
    def __init__(self, window):
        self.window = window
        self.window.title(" ")
        
        self.right_half = tk.Frame(self.window, bg="#FFFFFF")
        self.right_half.pack(side=tk.RIGHT, fill="both", expand=1)
        
        self.left_half = tk.Frame(self.window, bg=colors["green_1"])
        self.left_half.pack(side=tk.LEFT, fill="both", expand=1)
        
        self.text_label = tk.Label(self.left_half, text="", bg=colors['green_1'], fg="white", width=30)
        self.text_label.place(relx=0.5, rely=0.5, anchor="center")

        self.canvas = None
        self.selected_system = None

        self.a = None
        self.b = None
        self.S = None

        self.window_counter = 0
        self.max_windows = 6

        
        self.style = ttk.Style()
        self.style.configure("TNotebook", background="#FFFFFF", borderwidth=1, highlightthickness=0, relief="flat")
        self.style.configure("TNotebook.Tab", background="#FFFFFF", foreground="#000000", padding=[10, 5])
        self.style.map("TNotebook.Tab", background=[("selected", "#FFFFFF")], foreground=[("selected", "#000000")])

        self.notebook = ttk.Notebook(self.right_half)
        self.notebook.pack(fill="both", expand=1)
        
        self.window_names = ["Hamiltonian", "Energy", "Minimization", "Wave function", "Density", "Algorithm"]
        
        self.tabs = {}
        self.canvas_dict = {}

        for title in self.window_names:
            self.tabs[title] = tk.Frame(self.notebook, bg=colors['white'])
            self.notebook.add(self.tabs[title], text=title)
            self.canvas_dict[title] = None

        self.window.bind("<Configure>", self.resize_frames)

        self.create_widgets()

        
    def create_widgets(self):

        self.Energy_l = tk.Entry(self.left_half, width=6, bg=colors['green_1'], fg="white", bd=1, relief="flat",
                                 highlightbackground="white", highlightcolor="white")
        self.Energy_l.place(relx=0.75, rely=0.2, anchor="center")
        Energy_l = tk.Label(self.left_half, text="Eₙ", fg="white")
        Energy_l.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        Energy_l.place(relx=0.6, rely=0.2, anchor="center")


        Energy_label = tk.Button(self.left_half, text="E (α, β)", fg="#FFFFFF", command=self.Energy)
        Energy_label.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")  
        Energy_label.place(relx=0.25, rely=0.7, anchor="center")


        approach = tk.Button(self.left_half, text="Approach", fg="#FFFFFF", command=self.approach)
        approach.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")  
        approach.place(relx=0.5, rely=0.7, anchor="center")

        wave_f = tk.Button(self.left_half, text=r"Wave function", fg="#FFFFFF", command=self.wave_funtion)
        wave_f.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        wave_f.place(relx=0.8, rely=0.7, anchor="center")

        density = tk.Button(self.left_half, text=r"Density Pt", fg="#FFFFFF", command=self.density)
        density.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        density.place(relx=0.25, rely=0.8, anchor="center")

        btn_clear = tk.Button(self.left_half, text="Clear", fg="#FFFFFF", command=self.clean)
        btn_clear.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        btn_clear.place(relx=0.25, rely=0.9, anchor="center")

        btn_about = tk.Button(self.left_half, text="Algorithm", fg="#FFFFFF", command=self.Algorithm)
        btn_about.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        btn_about.place(relx=0.5, rely=0.8, anchor="center")

        btn_exit = tk.Button(self.left_half, text="Exit", fg="#FFFFFF", command=self.exit)
        btn_exit.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        btn_exit.place(relx=0.77, rely=0.8, anchor="center")


        btn_graph_3D = tk.Button(self.left_half, text="About", fg="#FFFFFF", command=self.logo)
        btn_graph_3D.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        btn_graph_3D.place(relx=0.5, rely=0.9, anchor="center")

        
        # start points
        self.p1 = tk.Entry(self.left_half, width=6, bg=colors['green_1'], fg="white", bd=1, relief="flat",
                           highlightbackground="white", highlightcolor="white")
        self.p1.place(relx=0.75, rely=0.4, anchor="center")

        p1 = tk.Label(self.left_half, text="α ", fg="white")
        p1.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        p1.place(relx=0.6, rely=0.4, anchor="center")


        self.p2 = tk.Entry(self.left_half, width=6, bg=colors['green_1'], fg="white", bd=1, relief="flat",
                           highlightbackground="white", highlightcolor="white")
        self.p2.place(relx=0.75, rely=0.5, anchor="center")
        p2 = tk.Label(self.left_half, text="β", fg="white")
        p2.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        p2.place(relx=0.6, rely=0.5, anchor="center")

        # learning rate 

        self.lr = tk.Entry(self.left_half, width=6, bg=colors['green_1'],fg="white", bd=1, relief="flat",
                           highlightbackground="white", highlightcolor="white")
        self.lr.place(relx=0.38, rely=0.4, anchor="center")


        lr_label = tk.Label(self.left_half, text="Lr", fg="white")
        lr_label.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        lr_label.place(relx=0.23, rely=0.4, anchor="center")
        

        self.epochs_var = tk.StringVar()
        self.epochs_var.trace_add("write", lambda *args: self.limit(*args))

        #Epochs
        self.epochs = tk.Entry(self.left_half, width=6, bg=colors['green_1'],fg="white", bd=1, relief="flat",
                               highlightbackground="white", highlightcolor="white", textvariable=None)
        self.epochs.place(relx=0.38, rely=0.5, anchor="center")

        ep_label = tk.Label(self.left_half, text="Ep", fg="white")
        ep_label.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        ep_label.place(relx=0.23, rely=0.5, anchor="center")


        menu_boton = tk.Menubutton(self.left_half, text="Quantum System", relief=tk.FLAT,
                                   bg=colors["green_1"], fg="white", bd=0)

        menu_boton.menu = tk.Menu(menu_boton, tearoff=0, 
                                  bg="white", fg="black", 
                                  activebackground=colors["green_1"], 
                                  activeforeground="white", relief=tk.FLAT, bd=0)
        menu_boton["menu"] = menu_boton.menu


        menu_boton.menu.add_command(label="Quantum Slab",          command=self.select_system_box) 
        menu_boton.menu.add_command(label="Anharmonic Oscillator", command=self.select_system_ao)
        menu_boton.menu.add_command(label="Gaussian Well",         command=self.select_system_gauss)         

        menu_boton.place(relx=0.36, rely=0.2, anchor="center")
    
    def limit(self, *args):
        value = self.epochs_var.get()
        if value.isdigit():
            if int(value)>100:
                self.epochs_var.set("1000")
        else:
            self.epochs_var.set("")
    

    def select_system_box(self):

        self.S = 0
        from Quantum_System.box_potential import Box

        current_tab  = self.notebook.nametowidget(self.notebook.select())

        for name, frame in self.tabs.items():
            if frame == current_tab:
                tab_name = name 
                break

        self.clean(tab_name)
        fig  = Box()

        self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=current_tab)
        self.canvas_dict[tab_name].draw()
        self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)


    def select_system_gauss(self):
        self.S = 2
        from Quantum_System.gauss_well import gauss_well
        current_tab     = self.notebook.nametowidget(self.notebook.select())

        for name, frame in self.tabs.items():
            if frame == current_tab:
                tab_name = name 
                break


        self.clean(tab_name)
        fig = gauss_well(-20)

        self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=current_tab)
        self.canvas_dict[tab_name].draw()
        self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)


    def select_system_ao(self):
        self.S = 1
        from Quantum_System.Anarmonic import Anarmonic 
        current_tab = self.notebook.nametowidget(self.notebook.select())

        for name, frame in self.tabs.items():
            if frame == current_tab:
                tab_name = name 
                break

        self.clean(tab_name)
        fig = Anarmonic()

        self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=current_tab)
        self.canvas_dict[tab_name].draw()
        self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill='both', expand=1)


    def logo(self):

        current_tab = self.notebook.nametowidget(self.notebook.select())

        import matplotlib.image as mpimg
        import os

        for name, frame in self.tabs.items():
            if frame == current_tab:
                tab_name = name 
                break

        self.clean(tab_name)

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        ruta = os.path.abspath('logo1.jpg')
        imagen = mpimg.imread(ruta)

        fig, ax = plt.subplots()

        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        ax.axis("off")
        ax.imshow(imagen)

        self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=current_tab)
        self.canvas_dict[tab_name].draw()
        self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

    # ===================
    #   Energy's Graph
    # ===================

    def Energy(self):

        current_tab = self.notebook.nametowidget(self.notebook.select())

        for name, frame in self.tabs.items():
            if frame == current_tab:
                tab_name = name 
                break

        print(self.S)

        if self.S==0:
            from Quantum_System.box_potential import function_2p

            self.clean(tab_name)
            function_2p(int(self.Energy_l.get()))

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        elif self.S==2:
            from Quantum_System.gauss_well import function_2p

            self.clean(tab_name)
            function_2p(int(self.Energy_l.get()))

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        elif self.S==1:
            from Quantum_System.Anarmonic import function_2p

            self.clean(tab_name)
            function_2p(int(self.Energy_l.get()))

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        else:
            None

    # ===================
    #   Energy's Approach
    # ===================


    def approach(self):

        current_tab = self.notebook.nametowidget(self.notebook.select())

        for name, frame in self.tabs.items():
            if frame == current_tab:
                tab_name = name 
                break


        if self.S == 0:
            from Quantum_System.box_potential import function_2p, minimizacion

            self.clean(tab_name)

            fig, ani, self.a, self.b = minimizacion(*function_2p(int(self.Energy_l.get())), 
                                                    float(self.lr.get()), int(self.epochs.get()), float(self.p1.get()), float(self.p2.get()))

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=current_tab)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)


        elif self.S ==2:

            from Quantum_System.gauss_well import function_2p, minimizacion
            self.clean(tab_name)

            fig, ani, self.a, self.b = minimizacion(*function_2p(int(self.Energy_l.get())), 
                                                    float(self.lr.get()), int(self.epochs.get()), float(self.p1.get()), float(self.p2.get()))

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=current_tab)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        elif self.S ==1:

            from Quantum_System.Anarmonic import function_2p, minimizacion
            self.clean(tab_name)

            fig, ani, self.a, self.b = minimizacion(*function_2p(int(self.Energy_l.get())), 
                                                    float(self.lr.get()), int(self.epochs.get()), float(self.p1.get()), float(self.p2.get()))

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=current_tab)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        else:
            None


    # ===================
    #    Wave Function
    # ===================


    def wave_funtion(self):

        current_tab = self.notebook.nametowidget(self.notebook.select())

        for name, frame in self.tabs.items():
            if frame == current_tab:
                tab_name = name 
                break

        if self.S ==0:
            from Quantum_System.box_potential import wave_function

            self.clean(tab_name)

            wave_function(int(self.Energy_l.get()), self.a, self.b)

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        elif self.S ==2:
            from Quantum_System.gauss_well import wave_function

            self.clean(tab_name)

            wave_function(int(self.Energy_l.get()), self.a, self.b)

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        elif self.S ==1:

            from Quantum_System.Anarmonic import wave_function

            self.clean(tab_name)

            wave_function(int(self.Energy_l.get()), self.a, self.b)

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        else:
            None

    def density(self):

        current_tab = self.notebook.nametowidget(self.notebook.select())

        for name, frame in self.tabs.items():
            if frame == current_tab:
                tab_name = name 
                break

        if self.S ==0:
            from Quantum_System.box_potential import density 

            self.clean(tab_name)

            density(int(self.Energy_l.get()), self.a, self.b)

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        elif self.S ==2:
            from Quantum_System.gauss_well import density 
            self.clean(tab_name)
            
            density(int(self.Energy_l.get()), self.a, self.b)
            
            self.canvas_dict[tab_name] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
        

        elif self.S ==1:
            
            from Quantum_System.Anarmonic import density 
            self.clean(tab_name)
            
            density(int(self.Energy_l.get()), self.a, self.b)
            
            self.canvas_dict[tab_name] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        else:
            None
    
    # ===========================================
    # The riseze of the windows and more settings 
    # ===========================================

    def resize_frames(self, event):
        
        global_width = self.window.winfo_width()
        new_global_width = global_width // 2.7

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
        
        #from Quantum_System.Algorithm.Algorithm import Algorithm
        current_tab = self.notebook.nametowidget(self.notebook.select())
        
        for name, frame in self.tabs.items():
            if frame == current_tab:
                tab_name = name 
                break

        self.clean(tab_name)
        #fig = Algorithm()
        #fig = manual()

        import matplotlib.image as mpimg
        import os
        
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        if   self.S == 0:
            ruta = os.path.abspath('algorithm.jpg')
        elif self.S == 1:
            ruta = os.path.abspath('algorithm1.jpg')
        elif self.S == 2:
            ruta = os.path.abspath('algorithm2.jpg')
        else:
            None

        imagen = mpimg.imread(ruta)
        
        fig, ax = plt.subplots()
        
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        ax.axis("off")
        ax.imshow(imagen)

        self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=current_tab)
        self.canvas_dict[tab_name].draw()
        self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
     

    def clean_(self, tab_name):
        if self.canvas_dict.get(tab_name):
            self.canvas_dict[tab_name].get_tk_widget().destroy()
            self.canvas_dict[tab_name] = None
    
    def clean(self, tab_name=None):
 
        if tab_name is None:
            current_tab = self.notebook.select()  
            tab_name = self.notebook.tab(current_tab, "text")  

        if tab_name in self.canvas_dict and self.canvas_dict[tab_name]:
            self.canvas_dict[tab_name].get_tk_widget().destroy()
            self.canvas_dict[tab_name] = None


if __name__ == "__main__":

    window = tk.Tk()
    window.config(bg="#FFFFFF")
    window.minsize(1150, 550) # 1100 550
    window.maxsize(1150, 550)
    app = Gui(window=window)
    #app.Algorithm()
    window.mainloop()
