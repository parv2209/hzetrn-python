"""Basic example of running HZETRN simulation and parsing output."""

import sys
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from hzetrn import HZETRNSimulator, parse_dose_output
from hzetrn.parser import get_dose_statistics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    """Run example HZETRN simulation."""
    # TODO: Update these paths for your system
    HZETRN_BIN = r"D:\New folder\hzetrn\hzetrn.exe"  # Windows path
    INPUT_FILE = r"D:\New folder\hzetrn\my_input.inp"
    OUTPUT_DIR = "./output"
    OUTPUT_FILE = "hzetrn_output.txt"  # Expected output filename from HZETRN

    try:
        # Initialize simulator
        print("[1/3] Initializing HZETRN simulator...")
        simulator = HZETRNSimulator(HZETRN_BIN, output_dir=OUTPUT_DIR)

        # Run simulation
        print("[2/3] Running HZETRN simulation...")
        output = simulator.run(INPUT_FILE)
        print("\nHZETRN Output:")
        print("-" * 60)
        print(output)
        print("-" * 60)

        # Parse results
        print("\n[3/3] Parsing dose output...")
        output_path = simulator.get_output_file(OUTPUT_FILE)
        dose_data = parse_dose_output(str(output_path))

        # Display results
        print(f"\n✓ Successfully parsed {len(dose_data['dose_rad'])} data points")
        print(f"\nDose Data Summary:")
        print(f"  Depths (g/cm²): {dose_data['depth_gcm2']}")
        print(f"  Doses (rad): {dose_data['dose_rad']}")
        print(f"  Dose Equivalent (rem): {dose_data['dose_eq_rem']}")

        # Calculate and display statistics
        stats = get_dose_statistics(dose_data)
        print(f"\nDose Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value:.4f}")

    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return 1
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        return 1
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {type(e).__name__}: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
