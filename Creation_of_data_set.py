import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import pandas as pd

# ------------------------
# Parameters
# ------------------------
n_particles = 10
L = 10
timesteps = 200
dt = 0.02
k = 2 * np.pi / (L/2)
force_strength = 2.0
damping = 0.98
repulsion_strength = 0.05
min_dist = 0.2

# Save directories
save_dir = "Data_set"
csv_dir = "CSV_set"
os.makedirs(save_dir, exist_ok=True)
os.makedirs(csv_dir, exist_ok=True)

# Initial positions
x = np.random.rand(n_particles) * L
y = np.random.rand(n_particles) * L

# Initial velocities
vx = np.random.randn(n_particles) * 0.1
vy = np.random.randn(n_particles) * 0.1

# Acoustic force model
def acoustic_force(px, py):
    fx = -force_strength * np.sin(k * px)
    fy = -force_strength * np.sin(k * py)
    return fx, fy

# Repulsion force
def repulsion(px, py):
    fx = np.zeros_like(px)
    fy = np.zeros_like(py)
    for i in range(len(px)):
        dx = px[i] - px
        dy = py[i] - py
        dist2 = dx**2 + dy**2 + 1e-6
        mask = dist2 < (min_dist**2)
        dx = dx[mask]
        dy = dy[mask]
        dist2 = dist2[mask]
        if len(dist2) > 0:
            fx[i] += np.sum(repulsion_strength * dx / dist2)
            fy[i] += np.sum(repulsion_strength * dy / dist2)
    return fx, fy

# ------------------------
# Visualization
# ------------------------
fig, ax = plt.subplots(figsize=(6, 6))
scat = ax.scatter(x, y, s=10, c="dodgerblue", alpha=0.7, edgecolor="k")

ax.set_xlim(0, L)
ax.set_ylim(0, L)
ax.set_title("Acousto-Clustering of Microplastics", fontsize=14)

def update(frame):
    global x, y, vx, vy
    fx, fy = acoustic_force(x, y)
    rx, ry = repulsion(x, y)
    fx += rx
    fy += ry

    vx = damping * (vx + fx * dt)
    vy = damping * (vy + fy * dt)

    x += vx * dt
    y += vy * dt
    x = np.clip(x, 0, L)
    y = np.clip(y, 0, L)

    scat.set_offsets(np.c_[x, y])

    # ------------------------
    # Save as PNG
    fname = os.path.join(save_dir, f"frame_{frame:03d}.png")
    plt.savefig(fname, dpi=100)

    # ------------------------
    # Save coordinates as CSV
    df = pd.DataFrame({"x": x, "y": y})
    csv_name = os.path.join(csv_dir, f"frame_{frame:03d}.csv")
    df.to_csv(csv_name, index=False)

    return scat,

ani = FuncAnimation(fig, update, frames=timesteps, interval=120, blit=False)
plt.show()
