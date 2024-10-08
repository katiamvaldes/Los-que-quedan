# Los-que-quedan
This project addresses the lack of optimization in the urban design of Cuauhtémoc-San Nicolás Avenue, where elements such as poles and vehicles parked on the sidewalks hinder pedestrian mobility and generate risks. Through multi-agent simulations, the aim is to identify solutions such as the elimination of obstacles or the widening of sidewalks, to improve pedestrian flow and safety. The objective is to create a more accessible and safe environment that promotes sustainable urban development in this key area of ​​Monterrey.


![Captura de Pantalla 2024-09-30 a la(s) 10 41 24 a m](https://github.com/user-attachments/assets/bb8012c6-d73c-460b-a926-c4d0dd7d1792)


![Captura de Pantalla 2024-09-30 a la(s) 10 41 44 a m](https://github.com/user-attachments/assets/a23ca8e8-ece9-4a76-bfe7-b4696b3b885e)


Python logic: This part of the project is responsible for defining how agents behave within the simulation. Behavior algorithms (e.g. how pedestrians and vehicles move), interactions between agents (such as obstacle detection or reaction to traffic lights), and the overall state of the simulation are implemented.

Python server: It acts as the core for simulation data visualization and export. This server is responsible for two key functions: Real-time visualization using MESA and JSON file generation.

It serves as the bridge between simulation in Python and 3D modeling in Unity. The JSON format is ideal for storing and transporting structured data representing the state of agents in the simulation.

Unity reads the JSON files generated by the server and models the simulation in a 3D environment, visualizing the agents and their behavior
