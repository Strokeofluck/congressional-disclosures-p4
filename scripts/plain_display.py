"""Text fallback for running the notebook's computations outside Jupyter."""
def display(value): print(value)
def Code(value,language=None): return value
def HTML(value): return value
def SVG(value): return value
