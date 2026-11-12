import sys
from pathlib import Path

# El código de la aplicación vive en src/ y se importa desde ahí.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
