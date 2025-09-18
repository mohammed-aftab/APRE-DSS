import numpy as np
import matplotlib.pyplot as plt

# ------------------------
# Parameters
# ------------------------
n_particles = 80
L = 10

# Generate clustered positions (near node centers)
centers = [(3, 3), (7, 3), (5, 7)]  # cluster centers
x, y = [], []
for cx, cy in centers:
    x.extend(cx + 0.3 * np.random.randn(n_particles // len(centers)))
    y.extend(cy + 0.3 * np.random.randn(n_particles // len(centers)))

x = np.array(x)
y = np.array(y)

# ------------------------
# Visualization
# ------------------------
fig, ax = plt.subplots(figsize=(6, 6))
scat = ax.scatter(x, y, s=80, c="skyblue", alpha=0.7, edgecolor="k")

ax.set_xlim(0, L)
ax.set_ylim(0, L)
ax.set_facecolor("white")
ax.set_title("Before Nile Red Staining (No UV)", fontsize=14)

# ------------------------
# Event Handler for Click
# ------------------------
stained = [False]  # state tracker

def on_click(event):
    if not stained[0]:
        scat.set_color("red")
        scat.set_alpha(0.9)
        ax.set_facecolor("black")
        ax.set_title("After Nile Red Staining (Fluorescence under UV)", fontsize=14)
        stained[0] = True
    else:
        scat.set_color("skyblue")
        scat.set_alpha(0.7)
        ax.set_facecolor("white")
        ax.set_title("Before Nile Red Staining (No UV)", fontsize=14)
        stained[0] = False
    fig.canvas.draw()

# Connect click event
fig.canvas.mpl_connect("button_press_event", on_click)

plt.show()
