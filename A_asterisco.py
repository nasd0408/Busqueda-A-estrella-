
"""
Para utilizar este script se recomienda instalar las dependencias usando Dependencias.py 
Se recomienda correr en PowerShell 

Script por: Nicolás Sira

Inteligencia artificia: INF10IA33

Docente: María Auxiliadora Pérez
"""


import curses
from heapq import heappush, heappop
import math
import networkx as nx
import matplotlib.pyplot as plt


#Introducimos el grafo suministrado en formato de diccionario de diccionarios 
graph = {
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Zerind": {"Oradea": 71, "Arad": 75},
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Rimnicu_Vilcea": 146, "Pitesti": 138},
    "Sibiu": {"Oradea": 151, "Arad": 140, "Rimnicu_Vilcea": 80, "Fagaras": 99},
    "Rimnicu_Vilcea": {"Sibiu": 80, "Craiova": 146, "Pitesti": 97},
    "Pitesti": {"Craiova": 138, "Rimnicu_Vilcea": 97, "Bucharest": 101},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Urziceni": {"Bucharest": 85, "Vaslui": 142, "Hirsova": 98},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Eforie": {"Hirsova":86},
    "Giurgiu":{"Bucharest":90},
    "Neamt":{"Iasi":87},
}
#Hacemos un array con los nombres de los nodos
#Para el menu de seleccion 
nodes =list(graph.keys())


#Funcion A* 
def A_star(graph, start, goal):
    frontier = [(0, start)]  # Lista de prioridad con costo y nodo
    path = {start: None}  # guarda el camino desde el inicio hasta cada nodo
    cost = {start: 0}  # guarda el costo de llegar desde el inicio hasta cada nodo

    while frontier:
        current_cost, current_node = heappop(frontier)

        if current_node == goal:
            break

        for next_node, edge_cost in graph[current_node].items():
            new_cost = cost[current_node] + edge_cost
            if next_node not in cost or new_cost < cost[next_node]:
                cost[next_node] = new_cost
                priority = new_cost
                heappush(frontier, (priority, next_node))
                path[next_node] = current_node

    return path, cost

#funcion para imprimir el camino 
def format_path(path, goal):
    node = goal
    formatted_path = [node]
    while path[node] is not None:
        formatted_path.append(path[node])
        node = path[node]
    return formatted_path[::-1]

#menu de eleccion de nodos 
def choice(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    options = nodes
    current_choice = 0
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        for index, option in enumerate(options):
            x = width//2 - len(option)//2
            y = height//2 - len(options)//2 + index
            if index == current_choice:
                stdscr.addstr(y, x, option, curses.color_pair(1))
            else:
                stdscr.addstr(y, x, option, curses.color_pair(2))
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and current_choice > 0:
            current_choice -= 1
        elif key == curses.KEY_DOWN and current_choice < len(options)-1:
            current_choice += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            selected_option = options[current_choice]
            break
    stdscr.clear()
    stdscr.addstr(0,0, f"Seleccionaste: {selected_option}")
    stdscr.refresh()
    stdscr.getch()
    curses.endwin()
    return(selected_option)
   
#Mostramos el grafo usando  networkX y Matplotlib 
def graficar(graph):
    G = nx.Graph(graph)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, edge_color='black', width=2)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='Arial')
    plt.show()
#Ejecucion de programa

#Se muestra el grafo
graficar(graph)

#Seleccion de inicio y meta
start = curses.wrapper(choice)
goal = curses.wrapper(choice)

#Ejecucion de la busqueda
path, cost = A_star(graph, start, goal)

#Formato e impresion de la respuesta
formatted_path = format_path(path, goal)
print("Camino desde {} hasta {}: {}".format(start, goal, " -> ".join(formatted_path)))
print("Costo desde {} hasta {}: {}".format(start, goal, cost[goal]))


