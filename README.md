# Build Time Comparison

This project provides a script to compare build reports and identify differences in route sizes and first load JavaScript sizes between two builds.

## Files

- `script.py`: The main script that parses and compares the build reports.
- `old_report.txt`: The old build report.
- `new_report.txt`: The new build report.

## Requirements

- Python 3.9 or higher
- pandas
- tabulate

## Installation

1. Clone the repository.
2. Install the required Python packages:
   ```sh
   pip install pandas tabulate
   ```

## Usage

To compare two build reports, run the following command:

```sh
python [script.py] --old [old_report.txt] --new [new_report.txt]
```

## Example

```sh
python script.py --old old_report.txt --new new_report.txt
```

## Output

The script will output a table that shows the differences in route sizes and first load JavaScript sizes between the two builds.
