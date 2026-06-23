import numpy as np

def generate_data(n=100, x_min=0, x_max=10, noise=1.0):
    """Genere X et Y avec bruit aleatoire"""
    X = np.random.uniform(x_min, x_max, n)
    noise_arr = np.random.uniform(-noise, noise, n)
    Y = 2.5 * X + 5 + noise_arr
    return X, Y

def generate_multivar(n=100, ranges=None):
    """Genere plusieurs variables X1, X2, X3"""
    if ranges is None:
        ranges = [(-10, 10), (-5, 15), (0, 20)]
    data = {}
    for i, (mn, mx) in enumerate(ranges):
        data[f'X{i+1}'] = np.random.uniform(mn, mx, n)
    return data

def generate_time_series(n=200, x_min=-5, x_max=15):
    """Genere une serie temporelle aleatoire"""
    values = []
    v = np.random.uniform(x_min, x_max)
    for _ in range(n):
        v += np.random.uniform(-1, 1)
        v = np.clip(v, x_min, x_max)
        values.append(v)
    return np.array(values)
