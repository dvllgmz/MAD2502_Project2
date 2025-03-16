import numpy as np

def get_escape_time(c: complex, max_iterations: int) -> int | None:
    """
    Return number of iterations which pass before c escapes:
    c escapes for the first k for which |z_k| > 2

    :param c: complex number
    :param max_iterations: int
    :return: int or None
    """
    z = 0 #Iteration begins at z_0 = 0
    for k in range(max_iterations+1): #Runs loop from 0 to max_iterations (inclusive)
        z = z**2 + c
        if abs(z) > 2: #If value escapes
            return k
    return None #If value never escapes

def get_complex_grid(top_left: complex, bottom_right: complex, step: float) -> np.ndarray:
    """
    Return an array of evenly spaced complex numbers between top_left and bottom_right (exclusive)

    :param top_left: complex number
    :param bottom_right: complex number
    :param step: float
    :return: numpy array
    """
    #Setting bounds
    col_start = top_left.real #col = real numbers
    col_end = bottom_right.real
    row_start = top_left.imag #row = imaginary numbers
    row_end = bottom_right.imag

    real_range = np.arange(col_start, col_end, step) #range of real numbers
    imag_range = np.arange(row_start, row_end, -step) #range of imaginary numbers

    real_arr, imag_arr = np.meshgrid(real_range, imag_range) #creates grid with both real and imaginary
    return real_arr + 1j * imag_arr #Generated complex grid


def get_escape_time_color_arr(c_arr: np.ndarray, max_iterations: int) -> np.ndarray:
    """
    Takes input of array of c-values, returns array of same shape with color values in [0,1] according to escape time of each c-value

    :param c_arr: array of complex numbers
    :param max_iterations: int
    :return: numpy array
    """
    #make zero array and the other supporting arrays
    zeros = np.zeros_like(c_arr, dtype=complex)
    escape_times = np.full(c_arr.shape, max_iterations + 1, dtype=int)
    mask = np.ones(c_arr.shape, dtype=bool)

    for i in range(max_iterations + 1):
        zeros[mask] = zeros[mask] ** 2 + c_arr[mask]  #apply the mandelbrot iteration
        newly_escaped = mask & (np.abs(zeros) > 2 )  #find newly escaped points
        escape_times[newly_escaped] = i  #set escape times for new points
        mask[newly_escaped] = False  #get rid of the points

    #normalize
    colors = (max_iterations - escape_times + 1) / (max_iterations + 1)
    return colors.astype(float)


def get_julia_color_arr(grid: np.ndarray, c: complex, max_iterations: int) -> np.ndarray:
    """
    Collects escape data for filled in Julia set for given complex number c
    Converts grid to a color according to implementation of 'get_escape_time_color_arr'

    :param grid: complex grid
    :param c: complex number
    :param max_iterations: int
    :return: numpy array
    """

    z = np.copy(grid) #Grid for testing Julia set
    escape_times = np.full(grid.shape, max_iterations + 1, dtype=int)
    mask = np.ones(grid.shape, dtype=bool) #Tracks if points still in set

    for i in range(max_iterations + 1):
        z[mask] = z[mask] ** 2 + c #z = z^2 + c
        newly_escaped = mask & (np.abs(z) > 2) #checks final escapes
        escape_times[newly_escaped] = i #iteration count
        mask[newly_escaped] = False # remove points

    #normalize
    colors = (max_iterations - escape_times + 1) / (max_iterations + 1)
    return colors.astype(float)