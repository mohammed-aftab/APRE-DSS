import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ------------------------
# Parameters
# ------------------------
n_particles = 120
L = 10
timesteps = 200
dt = 0.02
k = 2 * np.pi / (L / 2)
force_strength = 2.0
damping = 0.9
repulsion_strength = 0.05
min_dist = 0.2

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
        dist2 = dx ** 2 + dy ** 2 + 1e-6
        mask = dist2 < (min_dist ** 2)
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
plt.style.use("dark_background")  # dark theme for UV-like effect
fig, ax = plt.subplots(figsize=(6, 6))
colors = plt.cm.plasma(np.linspace(0, 1, n_particles))  # color map

scat = ax.scatter(x, y, s=60, c=colors, alpha=0.8, edgecolor="white", linewidth=0.5)

ax.set_xlim(0, L)
ax.set_ylim(0, L)
title = ax.set_title("Acousto-Clustering of Microplastics", fontsize=14, color="cyan")


# Update function
def update(frame):
    global x, y, vx, vy

    # Forces
    fx, fy = acoustic_force(x, y)
    rx, ry = repulsion(x, y)
    fx += rx
    fy += ry

    # Motion
    vx = damping * (vx + fx * dt)
    vy = damping * (vy + fy * dt)
    x += vx * dt
    y += vy * dt
    x = np.clip(x, 0, L)
    y = np.clip(y, 0, L)

    # Distance to center (for coloring effect)
    dist_to_center = np.sqrt((x - L / 2) ** 2 + (y - L / 2) ** 2)
    normalized = (dist_to_center - dist_to_center.min()) / (np.ptp(dist_to_center) + 1e-6)
    new_colors = plt.cm.plasma(1 - normalized)  # closer → warmer

    scat.set_offsets(np.c_[x, y])
    scat.set_facecolor(new_colors)

    # Dynamic title
    title.set_text(f"Acousto-Clustering of Microplastics\nFrame {frame + 1}/{timesteps}")

    return scat, title


ani = FuncAnimation(fig, update, frames=timesteps, interval=80, blit=False)

# To save HD video or gif
# ani.save("clustering.mp4", writer="ffmpeg", dpi=200)
# ani.save("clustering.gif", writer="pillow", fps=15)

plt.show()
