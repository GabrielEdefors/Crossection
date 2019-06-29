import math


def M_Rd(d, b, As, fcd, fyd, Es):

    """

    Function for calculating ultimate limit state moment capacity of beams
    Applicable for beams with only bottom reinforcement

    Args:
        d: Effective height of the cross section
        b: Sectional width
        As: Total reinforcement area
        fcd: Design compressive strength of the concrete

    """

    # Parameters
    alpha = 0.81
    beta = 0.416
    epsilon_cu = 3.5e-3

    # Assume that the reinforcement and the concrete is yielding at ULS
    sigmas_1 = fyd
    epsilon_1 = epsilon_cu

    # Call calculate_x to calculate x for current assumption
    x1 = calculate_x(As, sigmas_1, b, fcd, alpha)

    # Check if the reinforcement is yielding
    sigmas = Es * (d - x1) / x1 * epsilon_1

    if sigmas >= fyd:

        # Assumption ok, calculate moment capacity
        M_Rd = calculate_MRd(sigmas, b, fcd, alpha, x1, beta, d)

    else:

        # *** Assumption not ok, assume linear regime of reinforcement *** #

        # sigma_2 = lambda x: Es * (d - x) / x * epsilon_cu

        # The coefficients to this equation are
        a = alpha * fcd * epsilon_cu
        b = Es * epsilon_cu * As
        c = - b * d

        # Call solve_x to calculate x
        x2 = solve_x(a, b, c, d)

        # Call calculate_MRd to calculate the moment capacity
        M_Rd = calculate_MRd(sigmas, b, fcd, alpha, x2, beta, d)

    return M_Rd

def calculate_x(As, sigmas, b, fcd, alpha):

    """Function for calculating the height x of the compressive zone"""
    x = As * sigmas / (b * fcd * alpha)
    return x

def calculate_MRd(sigmas, b, fcd, alpha, x, beta, d):

    """Function for calculating the moment capacity"""
    M_Rd = alpha * fcd * b * x * (d - beta*x)
    return M_Rd

def solve_x(a, b, c, d):

    """Function finding admissible root to the quadratic equation defined by coefficients a, b, c"""
    d = b ** 2 - 4 * a * c  # discriminant

    if d < 0:
        print("This equation has no real solution")

    elif d == 0:
        x = (-b + math.sqrt(b ** 2 - 4 * a * c)) / 2 * a
        return x

    else:
        x1 = (-b + math.sqrt((b ** 2) - (4 * (a * c)))) / (2 * a)
        x2 = (-b - math.sqrt((b ** 2) - (4 * (a * c)))) / (2 * a)

        for x in [x1, x2]:
            if 0 < x < d:
                return x

