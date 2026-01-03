# Lunar Base Simulation

**Lunar Base Simulation** is a Python-based software framework designed to model, visualize, and manage operations within a conceptual Lunar Base. The system integrates environment generation from structured data, real-time Pygame visualization, SQLite data persistence, and autonomous mobile robot agents.

The repository also includes a specialized module for **Fire Safety Simulation**, utilizing NEAT (NeuroEvolution) to train robots in fire detection and suppression tasks.

## 🚀 Key Features

* **Dynamic Environment Loading**: Automatically generates the lunar base layout (habitats, roads, control towers, etc.) by parsing `data/LunarBase.xlsx`.
* **Real-Time Visualization**: Renders the base and moving agents using **Pygame**, handling coordinate transformation from physical units to screen pixels.
* **Database Integration**: Stores simulation states, environment element properties, and robot tracking data into a local **SQLite** database (`lunar_base_sim.db`).
* **Mobile Robot Agents**: Simulates "Internal Robots" with configurable attributes, pathfinding capabilities, and task assignment logic.
* **Fire Propagation Experiment**: A dedicated module to simulate temperature maps, material ignition, fire spread, and robotic extinguishing behaviors.

## 📂 Project Structure

* **`main.py`**: The entry point for the simulation. It orchestrates loading the environment, initializing the database, and starting the visualization loop.
* **`environment/`**: Contains logic for parsing the Excel dataset and defining classes for base elements (e.g., `Superadobe`, `PressurizedModule`, `PavedRoad`).
* **`simulation_visualizer/`**: Handles the graphical interface and rendering logic using Pygame.
* **`sqlite_database/`**: Manages the database schema (`schema.py`) and handles reading/writing simulation data (`reader.py`, `writer.py`).
* **`mobileobjects/`**: Defines the behavior and configuration of mobile robots within the base.
* **`fire_simulation_experiment/`**: A standalone experiment for simulating fire dynamics, temperature grids, and autonomous fire-fighting agents.
* **`data/`**: Stores input data (Excel sheets) and output databases.

## 🛠️ Installation & Requirements

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/Sivaastro/lunar_base_simulation.git](https://github.com/Sivaastro/lunar_base_simulation.git)
    cd lunar_base_simulation
    ```

2.  **Install dependencies**:
    The project relies on several Python libraries including `numpy`, `pygame`, `pandas`, and `openpyxl`.
    ```bash
    pip install -r requirements.txt
    ```

    *Key dependencies include:*
    * `numpy`, `scipy`, `matplotlib` (Math & Plotting)
    * `pygame` (Visualization)
    * `pandas`, `openpyxl` (Data Loading)
    * `neat-python` (AI/Evolutionary Algorithms)

## 🎮 Usage

To run the main lunar base simulation:

```bash
python main.py