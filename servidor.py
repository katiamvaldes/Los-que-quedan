from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from logica import AvenidaModel, Peaton, Vehiculo, Semaforo, Obstaculo  # Importar las clases necesarias
from json_utilidades import export_to_json  # Importar la función de exportación

# Definir puntos de partida y destinos personalizados
custom_start_positions = [(0, 7), (3, 3)]
custom_destinations = [(11, 5), (11, 4)]
vehicle_start = (7, 0)
vehicle_end = (7, 14)

# Crear la función de representación de agentes
def agent_portrayal(agent):
    if isinstance(agent, Peaton):
        return {"Shape": "circle", "Color": "blue", "Filled": "true", "Layer": 1, "r": 0.8}
    elif isinstance(agent, Obstaculo):
        return {"Shape": "rect", "Color": "red", "Filled": "true", "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, Vehiculo):
        return {"Shape": "rect", "Color": "green", "Filled": "true", "Layer": 0, "w": 1, "h": 0.5}
    elif isinstance(agent, Semaforo):
        color = "green" if agent.estado == "verde" else "yellow" if agent.estado == "amarillo" else "red"
        return {"Shape": "rect", "Color": color, "Filled": "true", "Layer": 0, "w": 1, "h": 1}

# Configurar la grilla de visualización
grid = CanvasGrid(agent_portrayal, 15, 15, 500, 500)

# Crear el servidor para la visualización
server = ModularServer(
    AvenidaModel,
    [grid],
    "Simulación de Avenida con Vehículo y Semáforo",
    {"width": 15, "height": 15, "start_positions": custom_start_positions, "destinations": custom_destinations, "vehicle_start": vehicle_start, "vehicle_end": vehicle_end, "num_obstaculos": 3}
)

server.port = 8521  # Puerto del servidor

# Iniciar el servidor para lanzar la visualización en tiempo real
if __name__ == "__main__":
    server.launch()
