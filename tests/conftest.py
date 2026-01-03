# tests/conftest.py
import sys
import os

# Get the absolute path to the 'src' directory
# This allows pytest to find 'core', 'screens', etc.
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_path)