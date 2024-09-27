# logica.py

import heapq
import random
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from json_utilidades import export_to_json  # Asegúrate de importar esta función

# Coordenadas de las calles, banquetas, cruces peatonales y edificios
calle_coords = [
    (6,0), (7,0), (6,2), (7,2), (6,3), (7,3), (6,4), (7,4), (6,5), (7,5), (6,6), (7,6),
    (6,7), (7,7), (6,8), (7,8), (6,9), (7,9), (6,10), (7,10), (6,11), (7,11), (6,12), (7,12),
    (6,14), (7,14), (5,4), (4,4), (2,4), (1,4), (0,4), (8,4), (9,4), (10,4), (12,4), (13,4), (14,4),
    (5,10), (4,10), (2,10), (1,10), (0,10), (8,10), (9,10), (10,10), (12,10), (13,10), (14,10)
]

cruce_peatonal_coords = [
    (6,1), (7,1), (3,4), (3,10), (6,13), (7,13), (11,10), (11,4),
]

banqueta_coords = [
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), 
    (0, 11), (0, 12), (0, 13), (0, 14), (1, 0), (1, 1), (1, 2), (1, 3), (1, 5), 
    (1, 6), (1, 7), (1, 8), (1, 9), (1, 11), (1, 12), (1, 13), (1, 14), (2, 0), 
    (2, 1), (2, 2), (2, 3), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 11), 
    (2, 12), (2, 13), (2, 14), (3, 0), (3, 1), (3, 2), (3, 3), (3, 5), (3, 6), 
    (3, 7), (3, 8), (3, 9), (3, 11), (3, 12), (3, 13), (3, 14), (4, 0), (4, 1), 
    (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 11), (4, 12), 
    (4, 13), (4, 14), (5, 0), (5, 1), (5, 2), (5, 3), (5, 5), (5, 6), (5, 7), 
    (5, 8), (5, 9), (5, 11), (5, 12), (5, 13), (5, 14), (8, 0), (8, 1), (8, 2), 
    (8, 3), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 11), (8, 12), (8, 13), 
    (8, 14), (9, 0), (9, 1), (9, 2), (9, 3), (9, 5), (9, 6), (9, 7), (9, 8), 
    (9, 9), (9, 11), (9, 12), (9, 13), (9, 14), (10, 0), (10, 1), (10, 2), 
    (10, 3), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 11), (10, 12), 
    (10, 13), (10, 14), (11, 0), (11, 1), (11, 2), (11, 3), (11, 5), (11, 6), 
    (11, 7), (11, 8), (11, 9), (11, 11), (11, 12), (11, 13), (11, 14), (12, 0), 
    (12, 1), (12, 2), (12, 3), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), 
    (12, 11), (12, 12), (12, 13), (12, 14), (13, 0), (13, 1), (13, 2), (13, 3), 
    (13, 5), (13, 6), (13, 7), (13, 8), (13, 9), (13, 11), (13, 12), (13, 13), 
    (13, 14), (14, 0), (14, 1), (14, 2), (14, 3), (14, 5), (14, 6), (14, 7), 
    (14, 8), (14, 9), (14, 11), (14, 12), (14, 13), (14, 14)
]

edificio_coords = [
    (8, 2), (9, 2), (10, 2), (1, 2), (2, 2), (1, 3), (2, 3), 
    (11, 7), (10, 7), (9, 7), (1, 12), (2, 12), (12, 12), (11, 12), 
    (10, 12), (9, 12), (12, 11), (11, 11), (10, 11), (9, 11)
]

obstaculo_permitido_coords = [
    (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (3, 0), (3, 1), (3, 2), 
    (13, 2), (12, 2), (11, 2), (13, 7), (12, 7), (0, 11), (1, 11), 
    (2, 11), (3, 11), (13, 13), (13, 12), (13, 11), (8, 13)
]

# Algoritmo A*
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def astar_search(start, goal, grid, model):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current, grid, model):
            if any(isinstance(agent, Peaton) for agent in model.grid.get_cell_list_contents([neighbor])):
                continue

            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

def get_neighbors(position, grid, model):
    neighbors = []
    x, y = position
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            if model.cell_tags[(nx, ny)] in ["banqueta", "cruce_peatonal"] and not any(isinstance(agent, Obstaculo) for agent in model.grid.get_cell_list_contents((nx, ny))):
                neighbors.append((nx, ny))
    return neighbors

# Definición de agentes
class Semaforo(Agent):
    def __init__(self, unique_id, model, posicion, tiempo_verde, tiempo_amarillo, tiempo_rojo):
        super().__init__(unique_id, model)
        self.posicion = posicion
        self.estado = "verde"
        self.tiempo_verde = tiempo_verde
        self.tiempo_amarillo = tiempo_amarillo
        self.tiempo_rojo = tiempo_rojo
        self.contador = 0

    def step(self):
        self.contador += 1
        if self.estado == "verde" and self.contador >= self.tiempo_verde:
            self.estado = "amarillo"
            self.contador = 0
        elif self.estado == "amarillo" and self.contador >= self.tiempo_amarillo:
            self.estado = "rojo"
            self.contador = 0
        elif self.estado == "rojo" and self.contador >= self.tiempo_rojo:
            self.estado = "verde"
            self.contador = 0

class Vehiculo(Agent):
    def __init__(self, unique_id, model, start_position, end_position):
        super().__init__(unique_id, model)
        self.start_position = start_position
        self.end_position = end_position
        self.path = self.calculate_path(start_position, end_position)
        self.has_arrived = False

    def calculate_path(self, start, end):
        path = []
        current_position = start
        x, y = current_position

        while current_position != end:
            if y < end[1]:
                y += 1
            elif y > end[1]:
                y -= 1
            current_position = (x, y)
            path.append(current_position)
        return path

    def step(self):
        if not self.has_arrived:
            if self.path:
                next_position = self.path[0]
                semaforo = next((agent for agent in self.model.grid.get_cell_list_contents([next_position]) if isinstance(agent, Semaforo)), None)
                if semaforo and semaforo.estado == "rojo":
                    return
                else:
                    self.path.pop(0)
                    self.model.grid.move_agent(self, next_position)
            if not self.path:
                self.has_arrived = True

class Peaton(Agent):
    def __init__(self, unique_id, model, start_position, destination):
        super().__init__(unique_id, model)
        self.start_position = start_position
        self.destination = destination
        self.path = astar_search(start_position, destination, self.model.grid_state, model)
        self.path_traveled = [start_position]
        self.waiting_time = 0

    def step(self):
        if self.path:
            next_position = self.path[0]
            if self.model.cell_tags[next_position] not in ["banqueta", "cruce_peatonal"]:
                return
            if any(isinstance(agent, Obstaculo) for agent in self.model.grid.get_cell_list_contents([next_position])):
                self.path = astar_search(self.pos, self.destination, self.model.grid_state, self.model)
                if self.path:
                    self.path.pop(0)
                return
            vehicle_detected = False
            for i in range(1, 4):
                directions = [(0, i), (i, 0), (-i, 0), (0, -i), (i, i), (-i, i), (i, -i), (-i, -i)]
                for dx, dy in directions:
                    future_position = (self.pos[0] + dx, self.pos[1] + dy)
                    if 0 <= future_position[0] < self.model.grid.width and 0 <= future_position[1] < self.model.grid.height:
                        if any(isinstance(agent, Vehiculo) and not agent.has_arrived for agent in self.model.grid.get_cell_list_contents([future_position])):
                            vehicle_detected = True
                            break
                if vehicle_detected:
                    break
            if vehicle_detected:
                self.waiting_time += 1
                if self.waiting_time > 5:
                    self.path.pop(0)
                    self.model.grid.move_agent(self, next_position)
                    self.model.grid_state[next_position[1]][next_position[0]] = 0.5
                    self.path_traveled.append(next_position)
                    self.waiting_time = 0
                return
            self.path.pop(0)
            self.model.grid.move_agent(self, next_position)
            self.model.grid_state[next_position[1]][next_position[0]] = 0.5
            self.path_traveled.append(next_position)

class Obstaculo(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

# Definición del modelo
class AvenidaModel(Model):
    def __init__(self, width, height, start_positions, destinations, vehicle_start, vehicle_end, num_obstaculos):
        super().__init__()
        self.num_agents = len(start_positions)
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.grid_state = [[0 for _ in range(width)] for _ in range(height)]
        self.destinations = destinations
        self.cell_tags = {}
        self.datacollector = DataCollector({"Peatones": lambda m: m.schedule.get_agent_count()})
        self.definir_etiquetas_de_celdas()
        self.obstaculo_permitido_coords = obstaculo_permitido_coords.copy()
        
        for i in range(num_obstaculos):
            if self.obstaculo_permitido_coords:
                coord = random.choice(self.obstaculo_permitido_coords)
                self.obstaculo_permitido_coords.remove(coord)
                obstaculo = Obstaculo(i + 2000, self)
                self.grid.place_agent(obstaculo, coord)
                self.schedule.add(obstaculo)
                self.grid_state[coord[1]][coord[0]] = 0.9
        
        for i in range(self.num_agents):
            start_position = start_positions[i]
            destination = destinations[i]
            peaton = Peaton(i, self, start_position, destination)
            if self.grid.is_cell_empty(start_position):
                self.grid.place_agent(peaton, start_position)
                self.schedule.add(peaton)
                self.grid_state[start_position[1]][start_position[0]] = 0.5
        
        vehiculo = Vehiculo(9999, self, vehicle_start, vehicle_end)
        self.grid.place_agent(vehiculo, vehicle_start)
        self.schedule.add(vehiculo)
        
        semaforo = Semaforo(10000, self, (7, 7), 5, 1, 3)
        self.grid.place_agent(semaforo, semaforo.posicion)
        self.schedule.add(semaforo)
        
        self.datacollector.collect(self)

    def definir_etiquetas_de_celdas(self):
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                self.cell_tags[(x, y)] = "calle"

        for coord in banqueta_coords:
            self.cell_tags[coord] = "banqueta"
        
        for coord in cruce_peatonal_coords:
            self.cell_tags[coord] = "cruce_peatonal"

        for coord in edificio_coords:
            self.cell_tags[coord] = "edificio"

    def model_to_json(self):
        data = {
            "peatones": [
                {
                    "id": agent.unique_id,
                    "pos": {"x": agent.pos[0], "y": agent.pos[1]},
                    "ruta_completa": [{"position": {"x": pos[0], "y": pos[1]}} for pos in agent.path_traveled]
                } for agent in self.schedule.agents if isinstance(agent, Peaton)
            ],
            "vehiculos": [
                {
                    "id": agent.unique_id,
                    "pos": {"x": agent.pos[0], "y": agent.pos[1]},
                    "ruta_completa": [{"position": {"x": pos[0], "y": pos[1]}} for pos in agent.path]
                } for agent in self.schedule.agents if isinstance(agent, Vehiculo)
            ],
            "semaforos": [
                {
                    "id": agent.unique_id,
                    "pos": {"x": agent.pos[0], "y": agent.pos[1]},
                    "estado": agent.estado,
                    "historial_estados": [
                        {"estado": "verde", "duracion": agent.tiempo_verde},
                        {"estado": "amarillo", "duracion": agent.tiempo_amarillo},
                        {"estado": "rojo", "duracion": agent.tiempo_rojo}
                    ]
                } for agent in self.schedule.agents if isinstance(agent, Semaforo)
            ],
            "obstaculos": [
                {
                    "id": agent.unique_id,
                    "pos": {"x": agent.pos[0], "y": agent.pos[1]}
                } for agent in self.schedule.agents if isinstance(agent, Obstaculo)
            ]
        }
        return data

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        
        # Exportar los datos en cada ciclo de la simulación
        data = self.model_to_json()
        export_to_json(data, 'output.json')  # Exportar datos en cada paso

        # Verificar si todos los peatones han llegado a su destino
        all_arrived = True
        for peaton in self.schedule.agents:
            if isinstance(peaton, Peaton):
                if peaton.pos != peaton.destination:
                    all_arrived = False
                    break

        if all_arrived:
            self.running = False
            print("Todos los peatones han llegado a su destino.")
            # Exportar datos finales al completar la simulación
            data = self.model_to_json()
            export_to_json(data, 'output.json')  # Exportar los datos finales
