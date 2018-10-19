#!/usr/bin/python3
#
# compute the correct motor thrusts to generate
# a desired resultant on the ROV
#
# for theory and nomenclature, see 'docs/misc/dynamics/dynamics.pdf'

# should we replace numpy with our own solving routines?
import numpy as np



# the ROV design paramters are described by the thruster configuration:
# position (r, theta, phi) and orientation (psi, alpha)
# all angles are in radians
class Thruster(object):
    def __init__(self, position, orientation):
        self.r, self.theta, self.phi = position
        self.psi, self.alpha = orientation



# this is the primary interface for solving 3D ROV thrust problems
# a usage example can be seen by running this file
class Solver(object):
    # compute the structure matrix from a list of Thruster objects
    def setup(self, thruster_list):
        self.thrusters = thruster_list
        self.structure_matrix = self.__zero(np.array([[
            np.sin(t.psi) * np.cos(t.alpha),
            np.sin(t.psi) * np.sin(t.alpha),
            np.cos(t.psi),
            t.r*np.sin(t.theta)*np.sin(t.phi)*np.cos(t.psi) -
                t.r*np.cos(t.theta)*np.sin(t.psi)*np.sin(t.alpha),
            t.r*np.cos(t.theta)*np.sin(t.psi)*np.cos(t.alpha) -
                t.r*np.sin(t.theta)*np.cos(t.phi)*np.cos(t.psi),
            t.r*np.sin(t.theta)*np.sin(t.psi)*np.sin(t.alpha - t.phi)]
        for t in self.thrusters]).transpose())


    # solve for the thrusts needed to achieve the given resultant
    # optional: tolerance for failure checking (default 0.0001)
    # returns:  vector of thrusts (for sign conventions, see documentation)
    #           success (True if this is a solution, False if failed)
    def solve(self, resultant, tol=0.0001):
        # equivalent to a least squares regression to minimize residual norm
        solution = self.__zero(
            np.linalg.lstsq(self.structure_matrix, resultant, rcond=-1)[0])

        # check to see if solution was a success (Bf ~ F)
        if not np.count_nonzero(self.__zero(
            np.matmul(self.structure_matrix, solution) - resultant, tol=tol)):
            return solution, True
        else:
            return solution, False


    # private ultility function
    # zeros values in a matrix that are lesser in magnitude than tolerance
    def __zero(self, mat, tol=1e-10):
        return np.where(abs(mat) > tol, mat, 0)



# handy usage example: run this file with the interpreter
if __name__ == '__main__':
    # for feasibility testing, we will try the DART ADAM ROV values
    DART_r = 0.5          # estimate r = 0.5 m
    DART_theta = np.pi/2  # unspecified, so assume everything is coplanar
    DART_psi = 4*np.pi/9  # 80 deg = 4pi/9 rad

    # setup the solver
    ThrustSolver = Solver()
    ThrustSolver.setup([
        Thruster((DART_r, DART_theta,   np.pi/4), (DART_psi, 3*np.pi/4)),
        Thruster((DART_r, DART_theta, 3*np.pi/4), (DART_psi,   np.pi/4)),
        Thruster((DART_r, DART_theta, 5*np.pi/4), (DART_psi, 7*np.pi/4)),
        Thruster((DART_r, DART_theta, 7*np.pi/4), (DART_psi, 5*np.pi/4)),
        Thruster((DART_r/np.sqrt(2), DART_theta,     0), (0, 0)),
        Thruster((DART_r/np.sqrt(2), DART_theta, np.pi), (0, 0))
    ])

    # now let's assume we want 1 N in the x-direction on the ROV
    # we represent this as [fx, fy, fz, tx, ty, tz]
    # for a force f along an axis and a torque t about an axis
    objective = [1, 0, 0, 0, 0, 0]
    thrusts, success = ThrustSolver.solve(objective)

    # display results
    print('The desired resultant is:')
    print(objective)
    print()
    if success:
        print('The algorithm converged with solution:')
        print(thrusts)
    else:
        print('The algorithm failed to find a solution. Best attempt:')
        print('  ', solution)
        print('This yields a resultant of:')
        print('  ', zero(np.matmul(DART, solution), tol=1e-8))
        print('Check that the objective is feasible with this design.')
