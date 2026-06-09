"""HZETRN Python Interface - Space Radiation Transport Simulation

A Python wrapper for NASA's HZETRN2020 code to simulate galactic cosmic ray (GCR)
shielding and space radiation dose calculations.
"""

from .core import HZETRNSimulator
from .parser import parse_dose_output

__version__ = "1.0.0"
__author__ = "Space Radiation Research"
__all__ = ["HZETRNSimulator", "parse_dose_output"]
