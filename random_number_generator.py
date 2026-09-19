import numpy as np
import scipy.integrate as integrate


class CustomRandomGenerator:

    def __init__(self, f, a, b, resolution=1000):
        """Pre-calculates the cumulative probability distribution once."""
        self.a = a
        self.b = b

        # 1. Create a fine grid of points between a and b
        self.x_grid = np.linspace(a, b, resolution)

        # 2. Evaluate the probability function f(x) at each point
        pdf = np.array([f(x) for x in self.x_grid])

        # 3. Calculate the Cumulative Distribution Function (CDF)
        # We use cumulative trapezoidal integration to find the running area under f(x)
        cdf = integrate.cumulative_trapezoid(pdf, self.x_grid, initial=0)

        # 4. Normalize the CDF so it ends exactly at 1.0 (valid probability)
        self.cdf = cdf / cdf[-1]

    def sample(self, size=1):
        """Generates random numbers instantly using the pre-calculated state."""
        # Generate uniform random numbers between 0 and 1
        u = np.random.uniform(0, 1, size)

        # Map the uniform numbers back to our x_grid using the CDF
        samples = np.interp(u, self.cdf, self.x_grid)

        # Return a single float if size is 1, otherwise return the array
        return samples[0] if size == 1 else samples


# 1. Define your probability function
def linear_ramp(x):
    return x

def quadratic_ramp(x):
    return x**2

def exponential_decay(x):
    return np.e**-x


# 2. Initialize the class (This does the heavy math setup)
linear_generator = CustomRandomGenerator(f=linear_ramp, a=0, b=5)
quadratic_generator = CustomRandomGenerator(f=quadratic_ramp, a=0.5, b=20)
exponential_decay_generator = CustomRandomGenerator(f=exponential_decay, a=0.5, b=20)



# 3. Generate a single random number
print(linear_generator.sample())
# Example output: 3.842

# 4. Generate 10,000 numbers instantly without recalculating the CDF
lot_of_samples = exponential_decay_generator.sample(size=1000)
print(lot_of_samples)
print("MAXIMUM = " + str(max(lot_of_samples)))
