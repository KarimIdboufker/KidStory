import sys
import os
from pathlib import Path

# Add the parent directory to PYTHONPATH so tests can import from models
sys.path.append(str(Path(__file__).parent.parent)) 