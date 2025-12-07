# Cloth Simulation

<p align="center">
  <b> English </b> &nbsp;|&nbsp; <a href="./README.vi.md"> Tiếng Việt </a>
</p>

This project implements a physics-based simulation of a grid (cloth/mesh) using a **Mass-Spring System** and **Verlet Integration**. The simulation models the physical behavior of deformable materials by treating them as a network of mass points connected by virtual springs.

## 1. Theoretical Basis: Mass-Spring System

The core model represents the object as a grid of discrete **mass points** connected by weightless springs. To simulate realistic behavior, the grid topology utilizes three specific types of springs:

### Grid Topology

1. **Structural Springs:**
    
    - Connect adjacent nodes (horizontally and vertically).
        
    - **Function:** Handle the primary tension and compression forces.
        
2. **Shear Springs:**
    
    - Connect nodes diagonally.
        
    - **Function:** Prevent the grid from shearing or becoming distorted (skewed).
        
3. **Bend Springs:**
    
    - Connect nodes separated by one intermediate node (skipping a point).
        
    - **Function:** Provide stiffness and prevent the material from folding onto itself too easily.
        

### Hooke's Law (Elastic Force)

The force exerted between two points, $P_1$ and $P_2$, is calculated using Hooke's Law:

$$\vec{F}_s = k \cdot (|\vec{L}| - R) \cdot \frac{\vec{L}}{|\vec{L}|}$$

**Where:**

- $k$: Stiffness coefficient.
    
- $\vec{L} = P_2 - P_1$: Vector pointing from $P_1$ to $P_2$.
    
- $|\vec{L}|$: Current distance between points.
    
- $R$: Rest length of the spring.
    
- $\frac{\vec{L}}{|\vec{L}|}$: Unit vector representing the direction of the force.
    

---

## 2. Verlet Integration

This simulation uses **Verlet Integration** rather than Euler Integration for updating particle positions.

### Why Verlet?

- **Euler Integration** ($v = v + a \cdot dt; p = p + v \cdot dt$): Often unstable for physics simulations. It introduces energy drift, causing the system to gain energy over time (the mesh may "explode" if $dt$ is too large).
    
- **Verlet Integration:** Calculates the new position based on the current position and the _previous_ position. It is symplectic (conserves energy better), stable, and handles velocity implicitly without needing to store a specific velocity variable.
    

### Position Update Formula

$$\vec{x}_{new} = 2\vec{x}_{curr} - \vec{x}_{prev} + \vec{a} \cdot \Delta t^2$$

- Where acceleration $\vec{a} = \frac{\vec{F}}{m}$.
    

---

## 3. Simulation Loop

The simulation is updated every frame using the following pipeline:

### Step 1: Accumulate Forces

1. Reset forces on all nodes to zero.
    
2. **Apply Gravity:** $\vec{F} \mathrel{+}= m \cdot \vec{g}$.
    
3. **Apply Spring Forces:** Iterate through all springs (Structural, Shear, Bend), calculate forces using Hooke's Law, and apply them to the connected nodes.
    
    - _Note:_ Air resistance (Damping) is often added here to prevent the system from oscillating indefinitely.
        

### Step 2: Integrate (Verlet)

For every mass point, update its position using the Verlet formula derived from the accumulated forces and the previous position.

### Step 3: Constraint Solving

Constraints are applied immediately after integration to ensure stability:

1. **Pinning:** Hard-lock specific points (e.g., to hang a cloth) so they do not move.
    
2. **Collision Handling:** Detect if points penetrate the ground or obstacles and project them back to the surface.
    
3. **Stick Constraints (Optional/Advanced):** Instead of relying solely on soft spring forces, rigid distance constraints can be enforced (often using relaxation iterations) to prevent the fabric from looking like "super-elastic" rubber.

## 🛠 Installation & Run

### Requirements

* Git
* Python 3.8-3.12

### Clone the Repository

```bash
git clone https://github.com/lmToT27/Cloth-Simulation.git
cd Cloth-Simulation
```

### Set up virtual environment and install libraries (Windows & Linux)

#### Windows (PowerShell / CMD)

```bash
python -m venv venv
venv\Scripts\activate
pip install numpy numba pygame
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy numba pygame
```

## Run the program

```bash
python Main.py
```
