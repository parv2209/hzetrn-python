# HZETRN Python Interface

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready Python wrapper for **NASA's HZETRN2020** space radiation transport code. Simplifies galactic cosmic ray (GCR) shielding analysis and space radiation dose simulations on Windows and Unix systems.

## 🚀 Features

- **Easy-to-use API** — Run HZETRN simulations with just a few lines of Python
- **Robust error handling** — Comprehensive validation and informative error messages
- **Output parsing** — Automatically extract dose, depth, and dose-equivalent data
- **Statistics module** — Calculate min, max, mean dose values
- **Logging support** — Track execution and debug issues
- **Cross-platform** — Works on Windows, Linux, and macOS

## 📋 Requirements

- **Python 3.8+**
- **NASA HZETRN2020** executable (Windows: `hzetrn.exe`, Unix: `hzetrn`)
  - Download from: [NASA HZETRN2020](https://www.nasa.gov/)

## 🔧 Installation

1. Clone this repository:
```bash
git clone https://github.com/parv2209/hzetrn-python.git
cd hzetrn-python
```

2. Set your HZETRN binary path in your code or environment.

## 📖 Quick Start

### Basic Example

```python
from hzetrn import HZETRNSimulator, parse_dose_output
from hzetrn.parser import get_dose_statistics

# Initialize simulator
simulator = HZETRNSimulator(r"path/to/hzetrn.exe", output_dir="./output")

# Run simulation
output = simulator.run("my_input.inp")

# Parse results
dose_data = parse_dose_output("./output/hzetrn_output.txt")

# Get statistics
stats = get_dose_statistics(dose_data)
print(f"Maximum dose: {stats['max_dose_rad']} rad")
print(f"Mean dose equivalent: {stats['mean_dose_eq_rem']} rem")
```

### Full Example

See `examples/example_basic.py` for a complete working example.

## 📚 API Documentation

### `HZETRNSimulator`

```python
HZETRNSimulator(hzetrn_bin: str, output_dir: str = "./output")
```

**Methods:**
- `run(input_file: str, timeout: Optional[int] = None) -> str`
  - Execute HZETRN simulation
  - Returns standard output from HZETRN
  - Raises: `FileNotFoundError`, `RuntimeError`

- `get_output_file(filename: str) -> Path`
  - Get path to output file in output directory

### `parse_dose_output`

```python
parse_dose_output(output_file: str) -> Dict[str, List[float]]
```

Parse HZETRN output file and extract dose data.

**Returns:**
```python
{
    'depth_gcm2': [list of depths in g/cm²],
    'dose_rad': [list of doses in rad],
    'dose_eq_rem': [list of dose equivalents in rem]
}
```

### `get_dose_statistics`

```python
get_dose_statistics(data: Dict[str, List[float]]) -> Dict[str, float]
```

Calculate statistics from dose data.

**Returns:**
```python
{
    'max_dose_rad': float,
    'min_dose_rad': float,
    'mean_dose_rad': float,
    'max_dose_eq_rem': float,
    'min_dose_eq_rem': float,
    'mean_dose_eq_rem': float,
    'num_data_points': int
}
```

## 🛠️ Configuration

### HZETRN Binary Path

Update the path to your HZETRN executable:

**Windows:**
```python
HZETRN_BIN = r"D:\path\to\hzetrn.exe"
```

**Linux/macOS:**
```python
HZETRN_BIN = "/path/to/hzetrn"
```

### Logging

Enable detailed logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

## ⚠️ Error Handling

```python
from hzetrn import HZETRNSimulator

try:
    simulator = HZETRNSimulator("hzetrn.exe")
    output = simulator.run("input.inp", timeout=300)
except FileNotFoundError as e:
    print(f"File not found: {e}")
except RuntimeError as e:
    print(f"Simulation failed: {e}")
except subprocess.TimeoutExpired:
    print("Simulation timed out")
```

## 📊 Understanding the Output

**Depth (g/cm²):** Shielding depth in grams per square centimeter  
**Dose (rad):** Absorbed radiation dose  
**Dose Equivalent (rem):** Biological effect-adjusted dose  

## 🔬 Physics Background

HZETRN is used to:
- Model galactic cosmic ray (GCR) transport through materials
- Calculate radiation shielding effectiveness
- Assess space radiation risks for astronauts and spacecraft
- Evaluate radiation damage to electronics

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact & References

- **HZETRN Documentation:** NASA SHIELDING (SHIELDOSE, DELTA86-H, HZETRN)
- **Related Research:** Galactic cosmic ray transport and shielding analysis

## ⭐ Citation

If you use this wrapper in research, please cite:
```
HZETRN Python Interface (2026)
Python wrapper for NASA HZETRN2020 space radiation transport code
https://github.com/parv2209/hzetrn-python
```
