# check kernel
try:
    shell = get_ipython().__class__.__name__
    print(shell)
except NameError:
    print("Not in IPython/Jupyter")