import pandas as pd

# ------------------------
# User-defined parameters
# ------------------------
sample_volume_ml = 250             # sample size taken for analysis
particle_volume_ml = 0.001         # assumed volume of one MP in ml (adjust with calibration)

# ------------------------
# Load CSV (initial scattered state)
# ------------------------
df = pd.read_csv("CSV_set/frame_140.csv")

# ------------------------
# 1. Number of particles in the sample (frame)
# ------------------------
num_particles = len(df)

# ------------------------
# 2 & 3. Volume and percentage of MPs in sample
# ------------------------
mp_total_volume_ml = num_particles * particle_volume_ml
mp_percentage_sample = (mp_total_volume_ml / sample_volume_ml) * 100

# ------------------------
# 4. Input container size
# ------------------------
container_volume_l = float(input("Enter the total container size (in Litres): "))
container_volume_ml = container_volume_l * 1000

# ------------------------
# 5. Scale MP percentage to container
# ------------------------
# MPs per ml in sample
mp_per_ml = num_particles / sample_volume_ml

# Estimate MPs in container
estimated_total_mps = mp_per_ml * container_volume_ml

# MP volume in container
estimated_mp_volume_container = estimated_total_mps * particle_volume_ml

# MP % in container
mp_percentage_container = (estimated_mp_volume_container / container_volume_ml) * 100

# ------------------------
# Results
# ------------------------
print("\n--- Results for Sample ---")
print(f"Number of microplastic particles detected: {num_particles}")
print(f"Estimated MP Volume in {sample_volume_ml} ml: {mp_total_volume_ml:.4f} ml")
print(f"Estimated MP % in sample: {mp_percentage_sample:.4f}%")

print(f"\n--- Scaled Results for {container_volume_l} L Container ---")
print(f"Estimated Total MPs: {int(estimated_total_mps)}")
print(f"Estimated MP Volume in Container: {estimated_mp_volume_container:.4f} ml")
print(f"Estimated MP % in container: {mp_percentage_container:.4f}%")
