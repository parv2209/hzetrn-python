"""Output parsing module for HZETRN simulation results.

Provides utilities to parse HZETRN output files and extract dose data.
"""

import logging
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


def parse_dose_output(output_file: str) -> Dict[str, List[float]]:
    """Parse HZETRN dose output file.
    
    Extracts depth, dose, and dose equivalent data from HZETRN output.
    Skips comment lines (starting with # or !) and handles parsing errors gracefully.
    
    Args:
        output_file: Path to HZETRN output file.
        
    Returns:
        dict: Dictionary with keys:
            - 'depth_gcm2': Depth values in g/cm²
            - 'dose_rad': Dose in rad
            - 'dose_eq_rem': Dose equivalent in rem
            
    Raises:
        FileNotFoundError: If output file does not exist.
        ValueError: If file format is invalid or no valid data found.
        
    Example:
        >>> data = parse_dose_output('hzetrn_output.txt')
        >>> print(f"Max dose: {max(data['dose_rad'])} rad")
    """
    output_path = Path(output_file)

    if not output_path.is_file():
        raise FileNotFoundError(f"Output file not found: {output_path}")

    data = {"depth_gcm2": [], "dose_rad": [], "dose_eq_rem": []}
    error_count = 0
    valid_lines = 0

    try:
        with open(output_path, "r") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith(("#", "!")):
                    continue

                try:
                    parts = line.split()
                    if len(parts) < 3:
                        error_count += 1
                        continue

                    depth = float(parts[0])
                    dose = float(parts[1])
                    dose_eq = float(parts[2])

                    data["depth_gcm2"].append(depth)
                    data["dose_rad"].append(dose)
                    data["dose_eq_rem"].append(dose_eq)
                    valid_lines += 1

                except (ValueError, IndexError) as e:
                    error_count += 1
                    logger.debug(f"Skipped line {line_num}: {line[:50]}... (Error: {e})")
                    continue

    except IOError as e:
        raise IOError(f"Error reading output file: {e}")

    if valid_lines == 0:
        raise ValueError(
            f"No valid data found in output file. "
            f"Skipped {error_count} lines. "
            f"Check file format: expected [depth, dose, dose_eq] per line."
        )

    logger.info(
        f"Successfully parsed {valid_lines} data points from {output_path}. "
        f"({error_count} lines skipped)"
    )
    return data


def get_dose_statistics(data: Dict[str, List[float]]) -> Dict[str, float]:
    """Calculate statistics from parsed dose data.
    
    Args:
        data: Dictionary from parse_dose_output().
        
    Returns:
        dict: Statistics including min, max, mean, and range values.
        
    Example:
        >>> stats = get_dose_statistics(data)
        >>> print(f"Peak dose: {stats['max_dose_rad']} rad")
    """
    if not data["dose_rad"]:
        raise ValueError("No dose data available for statistics.")

    dose_values = data["dose_rad"]
    dose_eq_values = data["dose_eq_rem"]

    return {
        "max_dose_rad": max(dose_values),
        "min_dose_rad": min(dose_values),
        "mean_dose_rad": sum(dose_values) / len(dose_values),
        "max_dose_eq_rem": max(dose_eq_values),
        "min_dose_eq_rem": min(dose_eq_values),
        "mean_dose_eq_rem": sum(dose_eq_values) / len(dose_eq_values),
        "num_data_points": len(dose_values),
    }
