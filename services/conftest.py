import os, sys, pathlib

# Ensure repository root is in sys.path so "import services.agent_core..." works reliably
ROOT = pathlib.Path(__file__).resolve().parents[1]
ROOT_STR = str(ROOT)
if ROOT_STR not in sys.path:
    sys.path.insert(0, ROOT_STR)
