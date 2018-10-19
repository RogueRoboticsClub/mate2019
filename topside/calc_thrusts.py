#!/usr/bin/python3
#
# compute the correct motor thrusts to generate
# a desired resultant on the ROV
#
# for theory and nomenclature, see 'docs/misc/dynamics/dynamics.pdf'

import numpy as np


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


# setup function computes the structure matrix B
# it takes a list of Thruster objects
def setup(thrusters):
    B = np.array([[
        np.sin(t.psi) * np.cos(t.alpha),
        np.sin(t.psi) * np.sin(t.alpha),
        np.cos(t.psi),
        t.r*np.sin(t.theta)*np.sin(t.phi)*np.cos(t.psi) -
            t.r*np.cos(t.theta)*np.sin(t.psi)*np.sin(t.alpha),
        t.r*np.cos(t.theta)*np.sin(t.psi)*np.cos(t.alpha) -
            t.r*np.sin(t.theta)*np.cos(t.phi)*np.cos(t.psi),
        t.r*np.sin(t.theta)*np.sin(t.psi)*np.sin(t.alpha - t.phi)]
    for t in thrusters]).transpose()
    return zero(B)


# solves for vector thrusts f
# arguments: resultant F, structure matrix B
# optional: tolerance for failure checking (default 0.0001)
# returns: vector f (for sign conventions, see documentation)
#          success (True if this is a solution, False if failed)
def solve(F, B, tol=0.0001):
    # equivalent to a least squares regression to minimize the residual norm
    # we don't use the matrix inverse because not all B are invertible
    solution = zero(np.linalg.lstsq(B, F, rcond=-1)[0])

    # check to see if solution was a success (Bf ~ F)
    if not np.count_nonzero(zero(np.matmul(B, solution) - F, tol=tol)):
        return solution, True
    else:
        return solution, False


# for feasibility testing, try the DART ADAM ROV values
DART_r = 1            # choose units so that r = 1
DART_theta = np.pi/2  # documentation does not specify theta
DART_psi = 4*np.pi/9  # 80 deg = 4pi/9 rad
DART = zero(setup([
    Thruster((DART_r, DART_theta,   np.pi/4), (DART_psi, 3*np.pi/4)),
    Thruster((DART_r, DART_theta, 3*np.pi/4), (DART_psi,   np.pi/4)),
    Thruster((DART_r, DART_theta, 5*np.pi/4), (DART_psi, 7*np.pi/4)),
    Thruster((DART_r, DART_theta, 7*np.pi/4), (DART_psi, 5*np.pi/4)),
    Thruster((DART_r/np.sqrt(2), DART_theta,     0), (0, 0)),
    Thruster((DART_r/np.sqrt(2), DART_theta, np.pi), (0, 0))
]))

# TODO: investigate failures at [0,1,0,0,0,0] and [0,0,0,1,0,0]
# TODO: investigate if this actually works
objective = np.array([0, 0, 0, 0, 0, 1])
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
    print('The algorithm failed to converge to a solution. Best attempt:')
    print('  ', solution)
    print('This yields a resultant of:')
    print('  ', zero(np.matmul(DART, solution), tol=1e-8))
    print('Check that the objective is feasible with the given design.')
