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
        self.window.title("QVS")
        
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
        self.style.map("TNotebook.Tab", background=[("selected", "#cfdeda")], foreground=[("selected", "#000000")])

        self.notebook = ttk.Notebook(self.right_half)
        self.notebook.pack(fill="both", expand=1)
        
        self.window_names = ["Hamiltonian", "Energy", "Optimization", "Wave function", "Probability density", "Algorithm", "Manual"]
        
        self.tabs = {}
        self.canvas_dict = {}
        
        # ===========
        # Manual load
        # ===========

        self.manual_pages = []
        self.page_index = 0

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

        self.Energy_label = tk.Button(self.left_half, text="E (α, β)", fg="#FFFFFF", command=self.Energy, state="disable")
        self.Energy_label.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")  
        self.Energy_label.place(relx=0.25, rely=0.7, anchor="center")

        self.approach = tk.Button(self.left_half, text="Optimization", fg="#FFFFFF", command=self.approach, state="disable")
        self.approach.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")  
        self.approach.place(relx=0.52, rely=0.7, anchor="center")

        self.wave_f = tk.Button(self.left_half, text=r"Ψ(x,y)", fg="#FFFFFF", command=self.wave_funtion, state="disable")
        self.wave_f.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        self.wave_f.place(relx=0.8, rely=0.7, anchor="center")

        self.density = tk.Button(self.left_half, text=r"|Ψ(x, y)|²", fg="#FFFFFF", command=self.density, state="disable")
        self.density.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        self.density.place(relx=0.25, rely=0.8, anchor="center")

        self.btn_clear = tk.Button(self.left_half, text="Clear", fg="#FFFFFF", command=self.clean, state="disable")
        self.btn_clear.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        self.btn_clear.place(relx=0.25, rely=0.9, anchor="center")

        self.btn_about = tk.Button(self.left_half, text="Algorithm", fg="#FFFFFF", command=self.Algorithm, state="disable")
        self.btn_about.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        self.btn_about.place(relx=0.52, rely=0.8, anchor="center")

        self.btn_exit = tk.Button(self.left_half, text="Exit", fg="#FFFFFF", command=self.exit)
        self.btn_exit.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        self.btn_exit.place(relx=0.51, rely=0.9, anchor="center")

        self.manual = tk.Button(self.left_half, text="Manual", fg="#FFFFFF", command=self.Manual, state="normal")
        self.manual.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        self.manual.place(relx=0.79, rely=0.9, anchor="center")

        self.next_page = tk.Button(self.left_half, text="〉 ", fg="#FFFFFF", command=self.next_page, state="disable")
        self.next_page.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        self.next_page.place(relx=0.87, rely=0.95, anchor="center")
        
        self.previous_page = tk.Button(self.left_half, text="〈", fg="#FFFFFF", command=self.previous_page, state="disable")
        self.previous_page.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        self.previous_page.place(relx=0.72, rely=0.95, anchor="center")

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

        self.lr = tk.Entry(self.left_half, width=6, bg=colors['green_1'],fg="white", bd=1, relief="flat",
                           highlightbackground="white", highlightcolor="white")
        self.lr.place(relx=0.38, rely=0.4, anchor="center")

        lr_label = tk.Label(self.left_half, text="Step size", fg="white")
        lr_label.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        lr_label.place(relx=0.18, rely=0.4, anchor="center")
        
        self.epochs_var = tk.StringVar()
        self.epochs_var.trace_add("write", lambda *args: self.limit(*args))

        self.epochs = tk.Entry(self.left_half, width=6, bg=colors['green_1'],fg="white", bd=1, relief="flat",
                               highlightbackground="white", highlightcolor="white", textvariable=None)
        self.epochs.place(relx=0.38, rely=0.5, anchor="center")

        ep_label = tk.Label(self.left_half, text="Steps", fg="white")
        ep_label.config(bg=colors['green_1'], borderwidth=0, highlightthickness=0, relief="flat")
        ep_label.place(relx=0.15, rely=0.5, anchor="center")

        menu_boton = tk.Menubutton(self.left_half, text="Quantum System ▼", relief=tk.FLAT,
                                   bg=colors["green_1"], fg="white", bd=0)

        menu_boton.menu = tk.Menu(menu_boton, tearoff=0, 
                                  bg="white", fg="black", 
                                  activebackground=colors["green_1"], 
                                  activeforeground="white", relief=tk.FLAT, bd=0)
        menu_boton["menu"] = menu_boton.menu

        menu_boton.menu.add_command(label="Quantum Slab",          command=self.select_system_box) 
        menu_boton.menu.add_command(label="Anharmonic Oscillator", command=self.select_system_ao)
        menu_boton.menu.add_command(label="Gaussian Well",         command=self.select_system_gauss)         

        menu_boton.place(relx=0.29, rely=0.2, anchor="center")

        self.current_system = tk.Label(self.left_half, text="Current System", bg=colors["green_1"], fg=colors["white"],
                                       font=("Helvetica", 12, "bold"))
        self.current_system.place(relx=0.5, rely=0.1, anchor="center")
    
    
    # ==========
    #   Manual 
    # ==========

    def Manual(self):

        self.next_page.config(state="normal")
        self.previous_page.config(state="normal")

        tab_name = self.notebook.nametowidget(".!frame.!notebook.!frame7")

        import matplotlib.image as mpimg
        import os

        self.clean(tab_name)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        self.manual_pages = [
                os.path.abspath("Images/welcome.jpg"), 
                os.path.abspath("Images/manual_p1.png"), 
                os.path.abspath("Images/manual_p2.png"),
                os.path.abspath("Images/manual_p3.png"),
                os.path.abspath("Images/manual_p4.png"),
                os.path.abspath("Images/manual_p5.png")
                ]

        imagen = mpimg.imread(self.manual_pages[self.page_index])
        fig, ax = plt.subplots()

        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        ax.axis("off")
        ax.imshow(imagen)

        self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=tab_name)
        self.canvas_dict[tab_name].draw()
        self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
        self.notebook.select(self.tabs["Manual"])
    
    def next_page(self):
        if self.page_index ==5:
            self.page_index = 5 
        else:
            self.page_index +=1
            self.Manual()

    def previous_page(self):
        if self.page_index ==0:
            self.page_index =0
        else:
            self.page_index -=1 
            self.Manual()

    def select_system_box(self):
        
        self.Energy_label.config(state="normal")
        self.manual.config(state="normal")
        self.current_system.config(text="Quantum Slab")

        self.approach.config(state="disable")
        self.wave_f.config(state="disable")
        self.density.config(state="disable")
        self.btn_about.config(state="disable")
        self.btn_clear.config(state="normal")


        tab_name = self.notebook.nametowidget(".!frame.!notebook.!frame")
        self.Energy_label.config(state="normal")
        self.S = 0
        from Quantum_System.box_potential import Box

        self.clean(tab_name)
        fig  = Box()
        self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=tab_name)
        self.canvas_dict[tab_name].draw()
        self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
        self.notebook.select(self.tabs["Hamiltonian"])

    def select_system_gauss(self):

        self.Energy_label.config(state="normal")
        self.current_system.config(text="Gauss Well")

        self.approach.config(state="disable")
        self.wave_f.config(state="disable")
        self.density.config(state="disable")
        self.btn_about.config(state="disable")
        self.btn_clear.config(state="normal")

        self.S = 2

        from Quantum_System.gauss_well import gauss_well
        tab_name = self.notebook.nametowidget(".!frame.!notebook.!frame")

        self.clean(tab_name)
        fig = gauss_well(-20)

        self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=tab_name)
        self.canvas_dict[tab_name].draw()
        self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
        self.notebook.select(self.tabs["Hamiltonian"])

    def select_system_ao(self):
  
        self.Energy_label.config(state="normal")
        self.current_system.config(text="Anharmonic Oscillator")

        self.approach.config(state="disable")
        self.wave_f.config(state="disable")
        self.density.config(state="disable")
        self.btn_about.config(state="disable")
        self.btn_clear.config(state="normal")

        tab_name = self.notebook.nametowidget(".!frame.!notebook.!frame")
        self.Energy_label.config(state="normal")
        self.S = 1
        from Quantum_System.Anarmonic import Anarmonic 
        
        self.clean(tab_name)
        fig = Anarmonic()

        self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=tab_name)
        self.canvas_dict[tab_name].draw()
        self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill='both', expand=1)
        self.notebook.select(self.tabs["Hamiltonian"])

    def logo(self):

        tab_name = self.notebook.nametowidget(".!frame.!notebook.!frame")

        import matplotlib.image as mpimg
        import os

        self.clean(tab_name)

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        ruta = os.path.abspath('Images/welcome.jpg')
        imagen = mpimg.imread(ruta)

        fig, ax = plt.subplots()

        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        ax.axis("off")
        ax.imshow(imagen)

        self.canvas_dict[tab_name] = FigureCanvasTkAgg(fig, master=tab_name)
        self.canvas_dict[tab_name].draw()
        self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

    # ===================
    #   Energy's Graph
    # ===================

    def Energy(self):

        self.approach.config(state="normal")
        tab_name = self.notebook.nametowidget(".!frame.!notebook.!frame2")

        if self.S==0:
            from Quantum_System.box_potential import function_2p

            self.clean(tab_name)
            function_2p(int(self.Energy_l.get()))

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(plt.gcf(), master=tab_name)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        elif self.S==2:
            from Quantum_System.gauss_well import function_2p

            self.clean(tab_name)
            function_2p(int(self.Energy_l.get()))

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(plt.gcf(), master=tab_name)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        elif self.S==1:
            from Quantum_System.Anarmonic import function_2p

            self.clean(tab_name)
            function_2p(int(self.Energy_l.get()))

            self.canvas_dict[tab_name] = FigureCanvasTkAgg(plt.gcf(), master=tab_name)
            self.canvas_dict[tab_name].draw()
            self.canvas_dict[tab_name].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        else:
            None

        self.notebook.select(self.tabs["Energy"])

    # ===================
    #   Energy's Approach
    # ===================


    def approach(self):
        self.wave_f.config(state="normal")
        current_tab = self.notebook.nametowidget(".!frame.!notebook.!frame3")

        if self.S == 0:
            from Quantum_System.box_potential import function_2p, minimizacion

            self.clean(current_tab)

            fig, ani, self.a, self.b = minimizacion(*function_2p(int(self.Energy_l.get())), 
                                                    float(self.lr.get()), int(self.epochs.get()), float(self.p1.get()), float(self.p2.get()))

            self.canvas_dict[current_tab] = FigureCanvasTkAgg(fig, master=current_tab)
            self.canvas_dict[current_tab].draw()
            self.canvas_dict[current_tab].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)


        elif self.S ==2:

            from Quantum_System.gauss_well import function_2p, minimizacion
            self.clean(current_tab)

            fig, ani, self.a, self.b = minimizacion(*function_2p(int(self.Energy_l.get())), 
                                                    float(self.lr.get()), int(self.epochs.get()), float(self.p1.get()), float(self.p2.get()))

            self.canvas_dict[current_tab] = FigureCanvasTkAgg(fig, master=current_tab)
            self.canvas_dict[current_tab].draw()
            self.canvas_dict[current_tab].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        elif self.S ==1:

            from Quantum_System.Anarmonic import function_2p, minimizacion
            self.clean(current_tab)

            fig, ani, self.a, self.b = minimizacion(*function_2p(int(self.Energy_l.get())), 
                                                    float(self.lr.get()), int(self.epochs.get()), float(self.p1.get()), float(self.p2.get()))
            self.canvas_dict[current_tab] = FigureCanvasTkAgg(fig, master=current_tab)
            self.canvas_dict[current_tab].draw()
            self.canvas_dict[current_tab].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
            
        else:
            None

        self.notebook.select(self.tabs["Optimization"])

    # ===================
    #    Wave Function
    # ===================

    def wave_funtion(self):
        self.density.config(state="normal")
        current_tab = self.notebook.nametowidget(".!frame.!notebook.!frame4")

        if self.S ==0:
            from Quantum_System.box_potential import wave_function

            self.clean(current_tab)

            wave_function(int(self.Energy_l.get()), self.a, self.b)

            self.canvas_dict[current_tab] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[current_tab].draw()
            self.canvas_dict[current_tab].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        elif self.S ==2:
            from Quantum_System.gauss_well import wave_function
            from Quantum_System.gauss_well import gauss_well

            self.clean(current_tab)

            wave_function(int(self.Energy_l.get()), self.a, self.b)

            self.canvas_dict[current_tab] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[current_tab].draw()
            self.canvas_dict[current_tab].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        elif self.S ==1:

            from Quantum_System.Anarmonic import wave_function

            self.clean(current_tab)

            wave_function(int(self.Energy_l.get()), self.a, self.b)

            self.canvas_dict[current_tab] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[current_tab].draw()
            self.canvas_dict[current_tab].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        else:
            None

        self.notebook.select(self.tabs["Wave function"])

    def density(self):
        self.btn_about.config(state="normal")
        current_tab = self.notebook.nametowidget(".!frame.!notebook.!frame5")

        if self.S ==0:
            from Quantum_System.box_potential import density 

            self.clean(current_tab)

            density(int(self.Energy_l.get()), self.a, self.b)

            self.canvas_dict[current_tab] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[current_tab].draw()
            self.canvas_dict[current_tab].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        elif self.S ==2:
            from Quantum_System.gauss_well import density 
            self.clean(current_tab)
            
            density(int(self.Energy_l.get()), self.a, self.b)
            
            self.canvas_dict[current_tab] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[current_tab].draw()
            self.canvas_dict[current_tab].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
        

        elif self.S ==1:
            
            from Quantum_System.Anarmonic import density 
            self.clean(current_tab)
            
            density(int(self.Energy_l.get()), self.a, self.b)
            
            self.canvas_dict[current_tab] = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
            self.canvas_dict[current_tab].draw()
            self.canvas_dict[current_tab].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

        else:
            None

        self.notebook.select(self.tabs["Probability density"])
    
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
        current_tab = self.notebook.nametowidget(".!frame.!notebook.!frame6")
        
        self.clean(current_tab)

        import matplotlib.image as mpimg
        import os
        
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        if   self.S == 0:
            ruta = os.path.abspath('Images/algorithm.jpg')
        elif self.S == 1:
            ruta = os.path.abspath('Images/algorithm1.jpg')
        elif self.S == 2:
            ruta = os.path.abspath('Images/algorithm2.jpg')
        else:
            None

        imagen = mpimg.imread(ruta)
        fig, ax = plt.subplots()
        
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        ax.axis("off")
        ax.imshow(imagen)

        self.canvas_dict[current_tab] = FigureCanvasTkAgg(fig, master=current_tab)
        self.canvas_dict[current_tab].draw()
        self.canvas_dict[current_tab].get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
        self.notebook.select(self.tabs["Algorithm"])
     
    def clean(self, tab_name=None):

        if tab_name is None:
            tab_name = self.notebook.nametowidget(self.notebook.select())

            if tab_name in self.canvas_dict and self.canvas_dict[tab_name]:
                self.canvas_dict[tab_name].get_tk_widget().destroy()
                self.canvas_dict[tab_name] = None

        if tab_name in self.canvas_dict and self.canvas_dict[tab_name]:
            self.canvas_dict[tab_name].get_tk_widget().destroy()
            self.canvas_dict[tab_name] = None
    
if __name__ == "__main__":
    window = tk.Tk()
    window.config(bg="#FFFFFF")
    window.minsize(1150, 550) 
    window.maxsize(1150, 550)
    app = Gui(window=window)
    window.after(1, app.logo)
    window.mainloop()
