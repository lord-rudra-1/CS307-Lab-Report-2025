import numpy as np
from PIL import Image
from functions.helpers import load_file, simulated_annealing, calculate_energy

# ------------------------ Parameters ------------------------
image_size = 512
initial_temp = 1000
decay_rate = 0.90
minimum_temp = 0.01
total_iterations = 10

# ------------------------ Load Input ------------------------
input_grid = load_file("lena.txt")

# Save initial image
Image.fromarray(input_grid.astype(np.uint8), mode='L').save('input_image.png')

# ------------------------ Simulated Annealing ------------------------
lowest_energy = float('inf')
best_solution_grid = None

for iteration in range(1, total_iterations + 1):
    # Run simulated annealing
    current_solution_grid = simulated_annealing(input_grid, initial_temp, decay_rate, minimum_temp)
    
    if current_solution_grid is None:
        continue

    # Calculate energy (cost) of current solution
    current_energy = calculate_energy(current_solution_grid)

    # Update best solution if energy is lower
    if current_energy < lowest_energy:
        lowest_energy = current_energy
        best_solution_grid = current_solution_grid.copy()
        input_grid = current_solution_grid.copy()
    
    print(f"Iteration {iteration}, Energy: {current_energy}")

    # Save intermediate output
    Image.fromarray(current_solution_grid.astype(np.uint8), mode='L').save(f'output_iteration_{iteration}.png')

# ------------------------ Save Final Output ------------------------
if best_solution_grid is not None:
    Image.fromarray(best_solution_grid.astype(np.uint8), mode='L').save('final_output.png')
