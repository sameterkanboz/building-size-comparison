import re
import pandas as pd
from tabulate import tabulate
import argparse


def parse_report(report):
    routes = []
    pattern = r"(●|○|ƒ)\s+(/\S+)\s+(\d+(?:\.\d+)?)\s+kB\s+(\d+(?:\.\d+)?)\s+kB"

    for line in report.splitlines():
        match = re.search(pattern, line)
        if match:
            route_type, route, size, first_load_js = match.groups()
            routes.append({
                "Route": route,
                "Size (kB)": float(size),
                "First Load JS (kB)": float(first_load_js)
            })

    return pd.DataFrame(routes)


def compare_builds(old_report, new_report):
    old_df = parse_report(old_report)
    new_df = parse_report(new_report)
    
    # Print columns of both DataFrames for debugging
    print("Old DataFrame columns:", old_df.columns)
    print("New DataFrame columns:", new_df.columns)
    
    merged_df = pd.merge(old_df, new_df, on="Route", suffixes=("_old", "_new"))
    
    # Print columns of merged DataFrame for debugging
    print("Merged DataFrame columns:", merged_df.columns)
    
    # Ensure the columns exist before performing the operation
    if "Size (kB)_old" in merged_df.columns and "Size (kB)_new" in merged_df.columns:
        merged_df["Size Diff (kB)"] = merged_df["Size (kB)_old"] - merged_df["Size (kB)_new"]
    else:
        print("Required columns are missing in the merged DataFrame.")
    
    return merged_df


def main():
    parser = argparse.ArgumentParser(description="Compare build reports.")
    parser.add_argument("--old", required=True, help="Path to the old report file.")
    parser.add_argument("--new", required=True, help="Path to the new report file.")
    args = parser.parse_args()
    
    with open(args.old, 'r') as f:
        old_report = f.read()
    with open(args.new, 'r') as f:
        new_report = f.read()
    
    df = compare_builds(old_report, new_report)
    print(df)


if __name__ == "__main__":
    main()
