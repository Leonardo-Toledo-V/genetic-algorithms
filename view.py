from tkinter import *
from tkinter import ttk
from logic import genetic_algorithm

class DataObject:
    def __init__(self, p_inicial, p_max, res, lim_inf, lim_sup, prob_ind, prob_gen, tipo_problema):
        self.p_inicial = p_inicial
        self.p_max = p_max
        self.res = res
        self.lim_inf = lim_inf
        self.lim_sup = lim_sup
        self.prob_ind = prob_ind
        self.prob_gen = prob_gen
        self.tipo_problema = tipo_problema


root = Tk()
root.title("Genetic algorithms")

def on_combobox_change(event):
    selected_value = combobox_var.get()
    print("Valor seleccionado en el Combobox:", selected_value)

    
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
for i in range(9):
    root.rowconfigure(i, weight=1)
    for j in range(3):
        mainframe.columnconfigure(j, weight=1) 




def save_data():
    p_inicial_value = p_inicial.get()
    p_max_value = p_max.get()
    res_value = res.get()
    lim_inf_value = lim_inf.get()
    lim_sup_value = lim_sup.get()
    prob_ind_value = prob_ind.get()
    prob_gen_value = prob_gen.get()
    tipo_problema_value = combobox_var.get()
    data = DataObject(p_inicial_value, p_max_value, res_value, lim_inf_value, lim_sup_value, prob_ind_value, prob_gen_value, tipo_problema_value)
    genetic_algorithm(data)        




p_inicial = StringVar()
ttk.Label(mainframe, text="Poblacion inicial:").grid(column=1, row=1, sticky=W)
ttk.Spinbox(mainframe, textvariable=p_inicial).grid(column=2, row=1, sticky=W)





p_max = StringVar()
ttk.Label(mainframe, text="Poblacion maxima:").grid(column=1, row=2, sticky=W)
ttk.Spinbox(mainframe, textvariable=p_max).grid(column=2, row=2, sticky=W)



res = StringVar()
ttk.Label(mainframe, text="Resolucion deseada:").grid(column=1, row=3, sticky=W)
ttk.Spinbox(mainframe, textvariable=res).grid(column=2, row=3, sticky=W)




lim_inf = StringVar()
ttk.Label(mainframe, text="Limite inferior:").grid(column=1, row=4, sticky=W)
ttk.Spinbox(mainframe, textvariable=lim_inf).grid(column=2, row=4, sticky=W)




lim_sup = StringVar()
ttk.Label(mainframe, text="Limite superior:").grid(column=1, row=5, sticky=W)
ttk.Spinbox(mainframe, textvariable=lim_sup).grid(column=2, row=5, sticky=W)





prob_ind = StringVar()
ttk.Label(mainframe, text="Probabilidad de muta del individuo:").grid(column=1, row=6, sticky=W)
ttk.Spinbox(mainframe, textvariable=prob_ind).grid(column=2, row=6, sticky=W)




prob_gen = StringVar()
ttk.Label(mainframe, text="Probabilidad de mutacion del gen:").grid(column=1, row=7, sticky=W)
ttk.Spinbox(mainframe, textvariable=prob_gen).grid(column=2, row=7, sticky=W)




# Definir el tipo de problema, si es de maximizacion o de minimizacion 
ttk.Label(mainframe, text="Tipo de problema:").grid(column=1, row=8, sticky=W)
combobox_var = StringVar(value="Minimizacion")
combobox=ttk.Combobox(mainframe, values=["Maximizacion","Minimizacion"],textvariable=combobox_var, state='readonly')
combobox.grid(column=2, row=8, sticky=W)
combobox.bind("<<ComboboxSelected>>", on_combobox_change)




ttk.Button(mainframe, text="Calculate", command=save_data).grid(column=3, row=9, sticky=W)


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=15, pady=5)



root.update()

window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = int((screen_width - window_width) / 2)
y_coordinate = int((screen_height - window_height) / 2)

root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

root.mainloop()
