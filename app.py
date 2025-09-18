from flask import Flask, render_template, request
import pandas as pd
import glob
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # Get container volume from input
        container_liters = float(request.form["container_volume"])
        container_ml = container_liters * 1000

        # Read all CSV files in CSV_set
        csv_files = glob.glob(os.path.join("CSV_set", "frame_000.csv"))
        particles_count = []

        for file in csv_files:
            df = pd.read_csv(file)
            particles_count.append(len(df))

        # Calculate average number of particles
        avg_particles = sum(particles_count) / len(particles_count)

        # MP in sample
        mp_in_ml_sample = avg_particles
        particle_volume_ml = 0.01  # actual volume of 1 particle
        mp_in_ml_sample = avg_particles * particle_volume_ml
        percentage_sample = (mp_in_ml_sample / 250) * 100
        percentage_container = (mp_in_ml_sample / container_ml) * 100

        # Prepare results
        result = {
            "avg_particles": f"{avg_particles:.2f}",
            "percentage_sample": f"{percentage_sample:.4f}%",
            "mp_in_ml_sample": f"{mp_in_ml_sample:.2f} ml",
            "container_volume": f"{container_ml} ml",
            "percentage_container": f"{percentage_container:.6f}%"
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
