import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
import traceback

# First, let's try to manually execute the module code
script_dir = os.path.dirname(os.path.abspath(__file__))
eq_file = os.path.join(script_dir, 'src/pfr_model/reactor/pfr_model_equation.py')

print(f"Reading {eq_file}...")
with open(eq_file, 'r') as f:
    source = f.read()

print("Attempting to execute the source code...")
namespace = {'__name__': '__main__', '__file__': eq_file}
try:
    # First test importing the dependencies
    print("\nTesting import of pfr_model.kinetics.arrhenius...")
    from pfr_model.kinetics.arrhenius import rate_constant
    print("  Success! rate_constant imported")
    
    print("\nTesting import of pfr_model.config.parameters...")
    from pfr_model.config.parameters import *
    print("  Success! All parameters imported")
    
    print("\nNow executing the module code...")
    exec(source, namespace)
    print("Execution successful!")
    print("Namespace keys:", [k for k in namespace.keys() if not k.startswith('_')])
    print("Has pfr_odes?", 'pfr_odes' in namespace)
except Exception as e:
    print("Error during execution:")
    traceback.print_exc()
