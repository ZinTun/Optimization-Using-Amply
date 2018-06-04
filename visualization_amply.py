from tkinter import *
from tkinter import ttk
import pandas as pd

from amplpy import AMPL, Environment, DataFrame


import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
#import tkinter as Tk
import networkx as nx

def calculate(*args):
    try:
        ampl = AMPL(Environment('/Users/zintun/Downloads/amplide.macosx64')) ##path has to change accordingly
        ampl.setOption('solver', 'gurobi')

        ampl.read('Y3_Elementals.mod')
        ampl.readData('Y3_data.dat')

        day_val = int(day.get())
        print(day_val)

        T = ampl.getParameter('T')
        T.set(day_val)

        ampl.solve()

        v1 = ampl.getVariable('X').getValues()
            
        c = v1.toList()
        rows = [[int(column) for column in row] for row in c]

        org_mat = []
        dest_mat = []
        mod_mat = []
        value_mat = []
        for i in range(len(rows)):
            element = rows[i]
            origin = element[0]
            dest = element[1]
            mode = element[2]
            value = element[3]
            org_mat.append(origin)
            dest_mat.append(dest)
            mod_mat.append(mode)
            value_mat.append(value)

        N = ampl.getParameter('N').getValues()
        N1 = N.toList()
        N_rows = [[int(column) for column in row] for row in N1]
        count = 0
        exist = []
        while(count < len(N_rows)):
            if(N_rows[count][3] or N_rows[count+1][3] or N_rows[count+2][3] or N_rows[count+3][3]):
                exist.extend([1, 1, 1,1])
            else:
                exist.extend([0, 0, 0,0])
            count = count + 4

        
        cost = ampl.getObjective('Cost').value()

        drawGraph1(org_mat,dest_mat,mod_mat,value_mat,exist,cost)


    except ValueError:
        pass


def drawGraph1(org,des,mod,value,exist,cost):
    G1 = nx.DiGraph(directed=True)
    G = nx.Graph()

    for i in range(len(org)):
        origin = str(org[i])
        dest = str(des[i])
        weight = (value[i])
        mode = str(mod[i])
        exists = str(exist[i])
        
        G.add_edge(origin,dest,weight=int(weight),mode=int(mode),exists=int(exists)) 
        if weight:
            G1.add_edge(origin,dest,weight=int(weight),mode=int(mode),exists=int(exists)) 
             
       
    eno = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 0 and d['exists'] == 0]
    eexist = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 0 and d['exists'] == 1]

    e_air = [(u, v) for (u, v, d) in G1.edges(data=True) if d['weight'] == 1 and d['mode'] == 1 ]
    e_land = [(u, v) for (u, v, d) in G1.edges(data=True) if d['weight'] == 1 and d['mode'] == 2]
    e_train = [(u, v) for (u, v, d) in G1.edges(data=True) if d['weight'] == 1 and d['mode'] == 3]
    e_ship = [(u, v) for (u, v, d) in G1.edges(data=True) if d['weight'] == 1 and d['mode'] == 4]
    

    pos = nx.spring_layout(G)  # positions for all nodes
    pos1 = nx.spring_layout(G1)  # positions for all nodes


    for k,v in pos1.items():
        # Shift the x values of every node by 10 to the right
        v[0] = v[0] +3

    # # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_nodes(G1, pos1, node_size=700)

    # # edges
    
    nx.draw_networkx_edges(G, pos, edgelist=eexist,
                            width=2, alpha=0.5, edge_color='r', style='dashed')
    nx.draw_networkx_edges(G, pos, edgelist=eno,
                            width=0, alpha=0.5, edge_color='r', style='dashed')

    
    nx.draw_networkx_edges(G1, pos1, edgelist=e_air,
                            width=2)
    nx.draw_networkx_edges(G1, pos1, edgelist=e_land,
                            width=2, edge_color='r')
    nx.draw_networkx_edges(G1, pos1, edgelist=e_train,
                            width=2, edge_color='b')
    nx.draw_networkx_edges(G1, pos1, edgelist=e_ship,
                            width=2, edge_color='g')

    # # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    nx.draw_networkx_labels(G1, pos1, font_size=20, font_family='sans-serif')

    plt.text(1,-1.2,"air",color='black')
    plt.text(2,-1.2,"land",color='red')
    plt.text(3,-1.2,"train",color='blue')
    plt.text(4,-1.2,"ship",color='green')

    plt.axis('off')
    plt.title('Cost ={}'.format(cost))
    

    #plt.legend(['A simple line'])

    plt.show()

root = Tk()
root.title("Elementals!!!")

mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

orgin = StringVar()
dest = StringVar()
day = StringVar()
vol = StringVar()
v3 = StringVar()

origin_entry = ttk.Entry(mainframe, width=7, textvariable=orgin)
origin_entry.grid(column=2, row=1, sticky=(W, E))
origin_entry.insert(0, 'Singapore')

dest_entry = ttk.Entry(mainframe, width=7, textvariable=dest)
dest_entry.grid(column=2, row=2, sticky=(W, E))
dest_entry.insert(0, 'Shanghai')

day_entry = ttk.Entry(mainframe, width=7, textvariable=day)
day_entry.grid(column=2, row=3, sticky=(W, E))
day_entry.insert(0, '5000')

vol_entry = ttk.Entry(mainframe, width=7, textvariable=vol)
vol_entry.grid(column=2, row=4, sticky=(W, E))
vol_entry.insert(0, '1100')

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=4, sticky=W)

ttk.Label(mainframe, text="Origin:").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Destination:").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="Hours:").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="Volume:").grid(column=1, row=4, sticky=W)
ttk.Label(mainframe, textvariable=v3).grid(column=1, row=5, sticky=(W, E))


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

origin_entry.focus()
root.bind('<Return>', calculate)

root.mainloop()