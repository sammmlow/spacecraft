# -*- coding: utf-8 -*-
"""

Created on Thu Jun 15 22:33:46 2023
Example Python script on how you can use the Spacecraft module.
For the attention of Eng Kee, Matthew, and Andrew

"""

# First, the most important object you ever want to import is the "spacecraft"
from source import spacecraft

# We can import some common math libraries too.
import numpy as np
from numpy.linalg import norm

# There are two ways we can define a spacecraft: either by defining it by the
# osculating Keplerian orbital elements, or by the inertial frame coordinates.
# In this library, the J2000 coordinate frame is used. Try it below!

# Init Method 1: [a, e, i, w, O, M]  where angles are in degrees
sc_elements = [7000.0, 0.002, 97.597, 45.0, -45.0, 60.0]
mySpacecraft_1 = spacecraft.Spacecraft( elements = sc_elements )

# Init Method 2: [px, py, pz, vx, vy, vz] where units are in km
sc_states = [-1927.231, 665.509, 6689.186, -4.973, 5.341, -1.950]
mySpacecraft_2 = spacecraft.Spacecraft( states = sc_states )

# Try printing out the states of the spacecraft.

# Printing the spacecraft tells you its name. Uncomment below to print.

# print(mySpacecraft_1)
# print(mySpacecraft_2)

# Printing the full state of the spacecraft is more useful. Uncomment below.

# mySpacecraft_1.status()
# mySpacecraft_2.status()

# We can then set some of the spacecraft parameters such as its mass, drag
# area, drag coefficient, and toggle what kind of forces we have online.

mySpacecraft_1.mass = 15.0 # kg
mySpacecraft_1.Cd = 2.34   # no units
mySpacecraft_1.area = 1.1  # m^2

# Let's toggle drag and J2 online for Spacecraft 2.

mySpacecraft_2.forces['j2']   = True # Enable J2 effects
mySpacecraft_2.forces['drag'] = True # Enable drag effects

# Next, we can try propagating analytically using pure Keplerian motion.
# Note that when you do pure Keplerian propagation, the above J2 and drag
# doesn't actually get effected. Propagate for 10000 seconds.

mySpacecraft_1.propagate_orbit( 10000 )

# Now, let's do a NUMERICAL propagation on Spacecraft 2, where the J2 and 
# drag effects are taken into account on top of the Keplerian forces. 
# Set the RK4 time step and the total propagation time.

mySpacecraft_2.propagate_perturbed( t=10000, step=60 )

# Try printing out the states of the spacecraft. Observe the very minor
# differences that J2 and drag have on their orbits. Uncomment below.

mySpacecraft_1.status()
mySpacecraft_2.status()

# Currently, SRP + Moon + Sun hasn't been implemented in my library yet.
# However, continuous low-thrust maneuvers are. You can set the frame of
# the maneuvers. Typically maneuvers are performed in the RTN frame (by
# default in this library too) but you can change to ECI if you want.
# You can print out the force frame to check just in case.

# Note that only the `propagate_perturbed` method will take maneuvers, and
# all other forms of perturbations, into account. Uncomment below if you wish.

# mySpacecraft_2.set_force_frame('ECI')
# print(mySpacecraft_2.force_frame)

# mySpacecraft_2.set_force_frame('RTN')
# print(mySpacecraft_2.force_frame)

# You MUST enable maneuvers in order to apply them.
mySpacecraft_2.forces['maneuvers'] = True

# Set the continuous thrust here. Warning: units in km!
mySpacecraft_2.set_thruster_acceleration([0.00000, 0.00001, 0.00000])

# Let's print out the initial distance. Uncomment below

# print('Initial distance from Earth Center = ', norm([ mySpacecraft_2.px,
#                                                       mySpacecraft_2.py,
#                                                       mySpacecraft_2.pz ]))

# Now propagate the spacecraft and observe it getting further from Earth.
mySpacecraft_2.propagate_perturbed( t=10000, step=60 )

# print('Final distance from Earth Center = ', norm([ mySpacecraft_2.px,
#                                                     mySpacecraft_2.py,
#                                                     mySpacecraft_2.pz ]))

# On a final note, the spacecraft object was designed to update the
# absolute states and elements whenever the user changes its coordinates
# explicity. For example, consider printing the spacecraft states before
# and after I change the orbital elements.

# print("States before: ", mySpacecraft_2.states)

# Perturb the semi-major axis for some reason.
mySpacecraft_2.a += 10

# print("States after: ", mySpacecraft_2.states)

# There are other features in the spacecraft library that pertain to formation
# flying and relative orbital elements tracking which you can explore in the
# original "spacecraft.py" class if you are interested, such as tagging
# chief-to-deputy relationships. Feel free to also develop new tools on it =)