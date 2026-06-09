"""Core HZETRN simulation module.

Provides the main HZETRNSimulator class for running HZETRN2020 simulations
and managing input/output files.
"""

import subprocess
import os
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class HZETRNSimulator:
    """Interface for NASA HZETRN2020 space radiation transport code.
    
    This class handles the execution of HZETRN simulations, manages input/output
    files, and provides error handling for galactic cosmic ray (GCR) dose calculations.
    
    Attributes:
        hzetrn_bin (Path): Path to the HZETRN executable.
        output_dir (Path): Directory for output files.
    """

    def __init__(
        self,
        hzetrn_bin: str,
        output_dir: str = "./output",
    ):
        """Initialize HZETRN simulator.
        
        Args:
            hzetrn_bin: Path to HZETRN executable (e.g., 'hzetrn.exe' on Windows).
            output_dir: Directory to store output files. Defaults to './output'.
            
        Raises:
            FileNotFoundError: If HZETRN executable not found at specified path.
        """
        self.hzetrn_bin = Path(hzetrn_bin)
        self.output_dir = Path(output_dir)

        if not self.hzetrn_bin.is_file():
            raise FileNotFoundError(
                f"HZETRN binary not found at: {self.hzetrn_bin}\n"
                f"Please set the correct path to the HZETRN2020 executable."
            )

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"HZETRN initialized. Binary: {self.hzetrn_bin}")
        logger.info(f"Output directory: {self.output_dir}")

    def run(
        self,
        input_file: str,
        timeout: Optional[int] = None,
    ) -> str:
        """Run HZETRN simulation with input file.
        
        Args:
            input_file: Path to HZETRN input file (.inp format).
            timeout: Process timeout in seconds. None = no timeout.
            
        Returns:
            str: HZETRN standard output.
            
        Raises:
            FileNotFoundError: If input file does not exist.
            RuntimeError: If HZETRN execution fails.
            subprocess.TimeoutExpired: If process exceeds timeout.
            
        Example:
            >>> simulator = HZETRNSimulator('hzetrn.exe')
            >>> output = simulator.run('my_input.inp')
            >>> print(output)
        """
        input_path = Path(input_file)

        if not input_path.is_file():
            raise FileNotFoundError(
                f"Input file not found: {input_path}\n"
                f"Please verify the input file exists and path is correct."
            )

        logger.info(f"Running HZETRN with input: {input_path}")

        try:
            result = subprocess.run(
                [str(self.hzetrn_bin), str(input_path)],
                capture_output=True,
                text=True,
                cwd=str(self.output_dir),
                timeout=timeout,
            )

            if result.returncode != 0:
                error_msg = (
                    f"HZETRN execution failed with return code {result.returncode}\n"
                    f"Error: {result.stderr}"
                )
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            logger.info("HZETRN simulation completed successfully.")
            return result.stdout

        except subprocess.TimeoutExpired:
            logger.error(f"HZETRN execution timed out after {timeout} seconds.")
            raise

    def get_output_file(self, filename: str) -> Path:
        """Get path to output file in output directory.
        
        Args:
            filename: Name of the output file.
            
        Returns:
            Path: Full path to the output file.
        """
        return self.output_dir / filename
