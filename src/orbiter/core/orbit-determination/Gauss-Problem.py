import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial
from mpl_toolkits.mplot3d import Axes3D


class GaussProblem:

    def SolutionViaUniversalVariables(self, r1, r2, t1, t2, nu):
        """
        Solve the Gauss problem using universal variables.
        :param r1: Position vector at time t1
        :param r2: Position vector at time t2
        :param t1: Initial time
        :param t2: Final time
        :param nu: True anomaly
        :return: Orbital elements or state vectors
        """
        # Algorithm to solve the Gauss problem using universal variables

        # from r1 and r2 and the 'direction of motion' evaluate A 
        A = GaussProblem.getConstantA(r1, r2, nu)

        # Pick a trial value for z.  
        z = 0  # np.random.randint(1, np.pi**2)

        # Evaluate the functions S and C for Z
        S, C = GaussProblem.getS_and_C(z)

        # Evaluate the auxiliary variable y
        try:
            y = GaussProblem.getAuxiliaryVariable(r1, r2, A, z, S, C)
        except ValueError as e:
            print(e)
            return np.array([np.nan, np.nan, np.nan]), np.array([np.nan, np.nan, np.nan])

        # Determine the value of the universal variable x
        x = np.sqrt(y / C) if y > 0 else np.nan

        # Check the trial value of z by computing the time of flight
        t = GaussProblem.getTimeOfFlight(x, A, S, y) if y > 0 else np.nan

        # If the time of flight is not equal to the input time, adjust z and repeat
        max_iterations = 100
        iteration = 0
        while abs(t - (t2 - t1)) > 1e-6 and not np.isnan(t) and iteration < max_iterations:
            # Compute derivatives
            dS, dC = GaussProblem.getdS_anddC(z)
            dt_dz = GaussProblem.getTimeOfFlightDerivative(x, y, dS, S, dC, C, A)
            
            if abs(dt_dz) < 1e-12:  # Avoid division by very small numbers
                break
                
            # Adjust z based on the difference in time of flight
            z_new = z - (t - (t2 - t1)) / dt_dz
            
            # Update values
            z = z_new
            S, C = GaussProblem.getS_and_C(z)
            y = GaussProblem.getAuxiliaryVariable(r1, r2, A, z, S, C)
            x = np.sqrt(y / C) if y > 0 else np.nan
            t = GaussProblem.getTimeOfFlight(x, A, S, y) if y > 0 else np.nan
            
            iteration += 1

        # Once converged evaluate lagrange coefficients and compute velocity vectors
        f, g, g_dot = GaussProblem.lagrangeCoefficients(r1, r2, A, y, C) if y > 0 else (np.nan, np.nan, np.nan)
        v1, v2 = GaussProblem.getStateVectors(f, g, g_dot, r1, r2) if y > 0 else (np.array([np.nan, np.nan, np.nan]), np.array([np.nan, np.nan, np.nan]))

        return v1, v2

    @staticmethod
    def getTrueAnomaly(r1, r2):
        """
        Calculate the true anomaly from the position vectors.
        :param r1: Position vector at time t1
        :param r2: Position vector at time t2
        :return: True anomaly for Long and Short arcs
        """
        r1_norm = np.linalg.norm(r1)
        r2_norm = np.linalg.norm(r2)
        cos_nu = np.dot(r1, r2) / (r1_norm * r2_norm)
        
        # Clamp to valid range to avoid numerical errors
        cos_nu = np.clip(cos_nu, -1.0, 1.0)
        
        nu_short = np.arccos(cos_nu)
        nu_long = 2 * np.pi - nu_short

        print("True Anomaly Short:", nu_short)
        print("True Anomaly Long:", nu_long)

        return nu_short, nu_long
    
    @staticmethod
    def getConstantA(r1, r2, nu):
        """
        Calculate the constant A based on the true anomaly.
        :param r1: Position vector at time t1
        :param r2: Position vector at time t2
        :param nu: True anomaly
        :return: Constant A
        """
        r1_norm = np.linalg.norm(r1)
        r2_norm = np.linalg.norm(r2)
        
        # Your original formula was correct
        A = (np.sqrt(r1_norm * r2_norm) * np.sin(nu)) / np.sqrt(1 - np.cos(nu))
        
        print("Constant A:", A)
        return A

    @staticmethod
    def getS_and_C(z, terms=100):
        """
        Calculate the functions S and C for the given z using the truncated series.
        
        S = sum_{n=0}^∞ (-1)^n * z^n / (2n+3)!
        C = sum_{n=0}^∞ (-1)^n * z^n / (2n+2)!

        :param z: Universal variable (scalar or numpy array)
        :param terms: Number of terms to use in the approximation
        :return: Tuple (S, C)
        """
        n = np.arange(terms)
        signs = (-1) ** n
        z_powers = z ** n

        factorials_S = factorial(2 * n + 3, exact=False)
        factorials_C = factorial(2 * n + 2, exact=False)

        S = np.sum(signs * z_powers / factorials_S)
        C = np.sum(signs * z_powers / factorials_C)

        print("S:", S, "C:", C)
        return S, C
    
    @staticmethod
    def getAuxiliaryVariable(r1, r2, A, z, S, C):
        """
        Calculate the auxiliary variable y based on r1, r2, A, z, S, and C.
        :param r1: Position vector at time t1
        :param r2: Position vector at time t2
        :param A: Constant A
        :param z: Universal variable
        :param S: S value
        :param C: C value
        :return: Auxiliary variable y
        """
        r1_norm = np.linalg.norm(r1)
        r2_norm = np.linalg.norm(r2)
        
        # Fixed formula for y
        if C == 0:
            y = r1_norm + r2_norm
        else:
            y = r1_norm + r2_norm - (A * (1 - z * S) / np.sqrt(C))

        if y < 0:
            raise ValueError(f"Auxiliary variable y is negative: {y}. Check input parameters and equations.")

        print("Auxiliary Variable y:", y)
        return y
    
    @staticmethod
    def getTimeOfFlight(x, A, S, y, mu=1):
        """
        Calculate the time of flight based on x, A, S, and y.
        :param x: Universal variable
        :param A: Constant A
        :param S: S value
        :param y: Auxiliary variable
        :param mu: Gravitational parameter
        :return: Time of flight
        """
        t = (x**3 * S + A * np.sqrt(y)) / np.sqrt(mu)

        print("Time of Flight:", t)
        if np.isnan(t):
            raise ValueError("Time of flight calculation resulted in NaN. Check input parameters.")
        return t
    
    @staticmethod
    def getdS_anddC(z):
        """
        Calculate the derivatives of S and C with respect to z.
        :param z: Universal variable
        :return: Derivatives dS and dC
        """
        S, C = GaussProblem.getS_and_C(z)
        if z == 0:
            # Avoid division by zero for z = 0
            dS = -1/120  # Correct derivative at z=0
            dC = -1/24   # Correct derivative at z=0
        else:
            dS = (1 / (2*z)) * (C - 3 * S)
            dC = (1 / (2*z)) * (1 - z*S - 2*C)
        print("S:", S, "C:", C, "dS:", dS, "dC:", dC)
        return dS, dC

    @staticmethod
    def getTimeOfFlightDerivative(x, y, dS, S, dC, C, A, mu=1):
        """
        Calculate the derivative of the time of flight with respect to z.
        :param x: Universal variable
        :param y: Auxiliary variable
        :param dS: Derivative of S
        :param S: S value
        :param dC: Derivative of C
        :param C: C value
        :param A: Constant A
        :param mu: Gravitational parameter
        :return: Derivative of time of flight
        """
        print("x:",x)
        dT_dz = x**3 * (dS - (3 * S * dC / (2*C))) + (A / 8) * (((3 * S * np.sqrt(y)) / C) + A/x)
        print("dT/dz:", dT_dz)
        return dT_dz
    
    @staticmethod
    def lagrangeCoefficients(r1, r2, A, y, C, mu=1):
        """
        Calculate the Lagrange coefficients based on r1, r2, A, y, and mu.
        :param r1: Position vector at time t1
        :param r2: Position vector at time t2
        :param A: Constant A
        :param y: Auxiliary variable
        :param C: C value
        :param mu: Gravitational parameter
        :return: Lagrange coefficients f, g, and g_dot
        """
        r1_norm = np.linalg.norm(r1)
        r2_norm = np.linalg.norm(r2)
        
        f = 1 - (y / r1_norm)
        g = A * np.sqrt(y / mu)
        g_dot = 1 - (y / r2_norm)

        print("Lagrange Coefficients: f =", f, ", g =", g, ", g_dot =", g_dot)
        return f, g, g_dot
    
    @staticmethod
    def getStateVectors(f, g, g_dot, r1, r2):
        """
        Calculate the state vectors based on Lagrange coefficients and position vectors.
        :param f: Lagrange coefficient f
        :param g: Lagrange coefficient g
        :param g_dot: Lagrange coefficient g_dot
        :param r1: Position vector at time t1
        :param r2: Position vector at time t2
        :return: State vectors at time t1 and t2
        """
        v1 = (r2 - f * r1) / g
        v2 = (g_dot * r2 - r1) / g
        return v1, v2
        

def main():
    # Example usage
    r1 = np.array([.5, .6, .7])  # Position vector at time t1
    r2 = np.array([0, 1.0, 0])  # Position vector at time t2
    t1 = 0 # Initial time
    t2 = 0.9667  # Final time

    print("Magnitude at t1:", np.linalg.norm(r1))
    print("Magnitude at t2:", np.linalg.norm(r2))
    nu_short, nu_long = GaussProblem.getTrueAnomaly(r1, r2)

    gauss_problem = GaussProblem()

    # Determine which anomalies to solve for
    anomalies = []
    if nu_short >= 0:
        anomalies.append(("nu_short", nu_short))
    if nu_long >= 0:
        anomalies.append(("nu_long", nu_long))

    # Solve for each valid anomaly
    for label, nu in anomalies:
        print(f"\n--- Solving for {label} ---")
        v1, v2 = gauss_problem.SolutionViaUniversalVariables(r1, r2, t1, t2, nu)
        print(f"Velocity at t1 ({label}):", v1)
        print(f"Velocity at t2 ({label}):", v2)

if __name__ == "__main__":
    main()