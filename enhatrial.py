import numpy as np
import matplotlib.pyplot as p
from matplotlib.animation import FuncAnimation

#Conditions to input
print("Input the parameters for the Vibrating String (Fundamental Mode)")
l = float(input("Enter the length of the string (l, m) //e.g., 2.0: "))
a = float(input("Enter the maximum amplitude (a, m) //e.g., 0.1: "))
c = float(input("Enter the wave speed (c, m/s) //e.g., 50.0: "))
xp= float(input("Enter the specific position to track (x_p, m) [0 < point_to_track < length_of_string]: "))

if not (0 < xp < l):
    print(f"Error: The tracking point x_p={xp} must be strictly between 0 and l={l}. Setting point to track = length/2.")
    xp= l / 2


period = 2 * l / c#period of refernce
print(f"\n*FYI: One full period of oscillation is T = {period:.4f} seconds.")
ts = float(input("Enter the total simulation time (s) //e.g., 2.0: "))
if ts < period:
    print(f"Warning: Simulation time is less than one period ({period:.4f} s).")
print("\nGenerating animation...")


nx = 200  #a random possible number chosen as number of spacial points
x = np.linspace(0, l, nx) # Position vector

nt = 100  #number of time steps for the animation
tv= np.linspace(0, ts, nt) # Time vector


def displacement(x, t, l, a, c):
    spatial_part = a * np.sin(np.pi * x / l)
    time_part = np.cos(np.pi * c * t / l)
    return spatial_part * time_part

#Animation
fig, ax = p.subplots(figsize=(10, 5))
line, = ax.plot(x, displacement(x, 0, l, a, c), 'b-', linewidth=3, label='String Shape')
# Marker for the specific point to track
point_marker, = ax.plot(xp, displacement(xp, 0, l, a, c), 'ro', markersize=8, label=f'Tracked Point at $x={xp:.2f}$')

ax.set_xlim(0, l)
ax.set_ylim(-a * 1.5, a * 1.5)
ax.set_xlabel('Position x (m)')
ax.set_ylabel('Displacement y (m)')
ax.set_title('Vibrating String Animation')
ax.grid()
ax.axhline(0, color='k', linestyle=':', linewidth=1)
time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12)
ax.legend(loc='upper right')

#updating animation:
def update(frame):
    t = tv[frame]
    y_current = displacement(x, t, l, a, c)
    yp= displacement(xp, t, l, a, c)
    
    line.set_ydata(y_current)
    point_marker.set_data([xp], [yp]) 
    time_text.set_text(f'Time: t = {t:.3f} s')
    
    return line, point_marker, time_text


interval_ms = ts* 1000 / nt 
ani = FuncAnimation(fig, update, frames=nt, interval=interval_ms, blit=True)
p.show()


#Second Plot (Displacement vs time for the point we are tracking):

#calculating the displacement history for the tracked point x_point
y_history = displacement(xp, tv, l, a, c)

p.figure(figsize=(10, 5))
p.plot(tv, y_history, 'g-', linewidth=2)
# Highlight the maximum and minimum displacements
amplitude_at_x = a * np.sin(np.pi * xp / l)
p.axhline(amplitude_at_x, color='r', linestyle='--', label='Max Amplitude')
p.axhline(-amplitude_at_x, color='r', linestyle='--')

p.title(f'Displacement Over Time for Point $x = {xp:.2f}$ m')
p.xlabel(f'Time t (s) (Period T = {period:.3f} s)')
p.ylabel('Displacement y (m)')
p.grid()
p.legend()
p.show()