#!/usr/bin/python3
#
# compute the correct motor thrusts to generate
# the desired resultant on the ROV
#
# for theory and nomenclature, see 'docs/misc/dynamics/dynamics.pdf'

import numpy as np
import scipy.optimize as opt


# the ROV design paramters are described by the thruster configuration:
# position (r, theta, phi) and orientation (psi, alpha)
# all angles are in radians
class Thruster(object):
    def __init__(self, position, orientation):
        self.r, self.theta, self.phi = position
        self.psi, self.alpha = orientation


# filters a matrix for values greater in magnitude than the tolerance
# alternatively, sets values lesser in magnitude than the tolerance to zero
def zero(mat, tol=1e-10):
    return np.where(abs(mat) > tol, mat, 0)


# setup function computes the structure matrix B and its inverse
# it takes a list of Thruster objects
# this matrix should work at least in the coplanar case
# TODO: fix the matrix in the documentation
def setup(thrusters):
    B = np.array([[
        np.sin(t.psi) * np.cos(t.alpha),
        np.sin(t.psi) * np.sin(t.alpha),
        np.cos(t.psi),
        t.r * np.cos(t.psi) * np.sin(t.theta) * np.sin(t.phi),
        -t.r * np.cos(t.psi) * np.sin(t.theta) * np.cos(t.phi),
        t.r * np.sin(t.psi) * np.sin(t.theta) * np.sin(t.alpha-t.phi)]
    for t in thrusters]).transpose()
    return zero(B)


# solves for vector thrusts f
# arguments: resultant F, structure matrix B
# optional: tolerance for failure checking (default 0.0001)
# returns: vector f (for sign conventions, see documentation)
#          success (True if this is a solution, False if failed)
def solve(F, B, tol=0.0001):
    # this is equivalent to least squares regression to minimize the residual
    # |F - Bf|
    # we don't use the matrix inverse because not all B are nonsingular square
    solution = zero(opt.least_squares(
        lambda x: F - np.matmul(B, x), [0, 0, 0, 0, 0, 0]).x)

    # check to see if solution was a failure (Bf ~ F)
    if not np.count_nonzero(zero(np.matmul(B, solution) - F, tol=tol)):
        return solution, True
    else:
        return solution, False


# for feasibility testing, try the DART ADAM ROV values
DART_r = 1            # choose units so that r = 1
DART_theta = np.pi/2  # assume centroid coplanar with thrusters
DART_psi = 4*np.pi/9  # 80 deg = 4pi/9 rad
DART = zero(setup([
    Thruster((DART_r, DART_theta,   np.pi/4), (DART_psi, 3*np.pi/4)),
    Thruster((DART_r, DART_theta, 3*np.pi/4), (DART_psi,   np.pi/4)),
    Thruster((DART_r, DART_theta, 5*np.pi/4), (DART_psi, 7*np.pi/4)),
    Thruster((DART_r, DART_theta, 7*np.pi/4), (DART_psi, 5*np.pi/4)),
    Thruster((DART_r/np.sqrt(2), DART_theta,     0), (0, 0)),
    Thruster((DART_r/np.sqrt(2), DART_theta, np.pi), (0, 0))
]))

objective = np.array([0, 0, 0, 3, 0, 0])
solution, success = solve(objective, DART)

print('The structure matrix is:')
print(DART)
print()
print('The desired resultant is:')
print(objective)
print()
if success:
    print('The algorithm converged with solution:')
    print(solution)
else:
    print('The algorithm failed to converge to a solution.')
    print('Check that the objective is feasible with the given design.')
