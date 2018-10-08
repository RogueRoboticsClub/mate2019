#!/usr/bin/python3
#
# compute the correct motor thrusts to generate
# the desired resultant on the ROV
#
# for theory and nomenclature, see 'docs/misc/dynamics/dynamics.pdf'

import numpy as np
import sys


# the ROV design paramters are described by the thruster configuration:
# position (r, theta, phi) and orientation (psi, alpha)
# all angles are in radians
class Thruster(object):
    def __init__(self, position, orientation):
        self.r, self.theta, self.phi = position
        self.psi, self.alpha = orientation


# setup function computes the structure matrix B and its inverse
# it takes a list of Thruster objects; for us, length is always 6
def setup(thrusters):
    B = np.array([[
        np.sin(t.psi)*np.cos(t.alpha),
        np.sin(t.psi)*np.sin(t.alpha),
        np.cos(t.psi),
        t.r*np.cos(t.psi)*np.cos(t.theta) -
            t.r*np.sin(t.psi)*np.cos(t.alpha)*np.sin(t.theta)*np.sin(t.phi),
        t.r*np.sin(t.psi)*np.cos(t.alpha)*np.sin(t.theta)*np.cos(t.phi) -
            t.r*np.cos(t.psi)*np.cos(t.theta),
        -t.r*np.sin(t.psi)*np.sin(t.theta)*np.cos(t.alpha+t.phi)]
    for t in thrusters]).transpose()
    try:
        return B, np.linalg.inv(B)
    except np.linalg.linalg.LinAlgError:
        print('Error: structure matrix is singular (non-invertible)')
        sys.exit(1)


# solves for the necessary thrust vector f, given a desired resultant F
# and the inverse of the structure matrix
# resultant is a 6x1 vector; struct_inv is a 6x6 matrix
# the thrust vector f is a 6x1 vector
def solve(resultant, struct_inv):
    return np.matmul(struct_inv, resultant)


# for testing, we'll just use random values
# we don't have the ROV design yet, anyway
# TODO: update these values with the DART values to test feasibility
B, B_inv =  setup([
    Thruster((0.1, 1.5, 1.3), (1.2, 1.6)),
    Thruster((0.1, 2.2, 1.3), (2.8, 1.6)),
    Thruster((0.1, 2.7, 1.3), (2.9, 1.6)),
    Thruster((0.1, 2.8, 1.3), (3.0, 1.6)),
    Thruster((0.1, 3.4, 1.3), (3.6, 1.6)),
    Thruster((0.1, 5.5, 1.3), (4.8, 1.6))])
print(B)
print(B_inv)
print(solve([3, 3, 3, 0, 0, 0], B_inv))
