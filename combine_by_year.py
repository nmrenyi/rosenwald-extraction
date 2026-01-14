#!/usr/bin/env python3
"""
Combine TSV files by year and add page column.
Input: rosenwald-extraction/YYYY-NNNN.tsv files
Output: combined-by-year/YYYY.tsv or YYYY.xlsx files with page column
"""

import os
import glob
from collections import defaultdict
import csv
import argparse

# Output directory constant
OUTPUT_DIR = 'combined-by-year'

def combine_tsvs_by_year(excel=False, single_file=False):
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Get all TSV files
    tsv_files = glob.glob('rosenwald-extraction/*.tsv')
    
    # Group files by year
    files_by_year = defaultdict(list)
    for filepath in tsv_files:
        filename = os.path.basename(filepath)
        year = filename.split('-')[0]
        page = filename.split('-')[1].replace('.tsv', '').lstrip('0') or '0'
        files_by_year[year].append((filepath, page))
    
    # Sort years
    years = sorted(files_by_year.keys())
    
    file_ext = 'xlsx' if excel else 'tsv'
    print(f"Found {len(tsv_files)} TSV files across {len(years)} years ({years[0]}-{years[-1]})")
    print(f"Output format: {file_ext.upper()}")
    print(f"Mode: {'Single file (all years)' if single_file else 'Separate files by year'}")
    
    # Import pandas if excel output requested
    if excel:
        try:
            import pandas as pd
        except ImportError:
            print("Error: pandas is required for Excel output. Install with: pip install pandas openpyxl")
            return
    
    if single_file:
        # Combine all years into one file
        output_file = f'{OUTPUT_DIR}/all_years.{file_ext}'
        print(f"\nCombining all years -> {output_file}")
        
        if excel:
            # Excel output - all years
            all_rows = []
            for year in years:
                files = sorted(files_by_year[year], key=lambda x: x[1])
                for filepath, page in files:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        reader = csv.DictReader(infile, delimiter='\t')
                        for row in reader:
                            row['year'] = year
                            row['page'] = page
                            all_rows.append(row)
            
            df = pd.DataFrame(all_rows)
            df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"  ✓ Wrote {len(all_rows)} rows to {output_file}")
        else:
            # TSV output - all years
            with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                writer = None
                first_file = True
                total_rows = 0
                
                for year in years:
                    files = sorted(files_by_year[year], key=lambda x: x[1])
                    for filepath, page in files:
                        with open(filepath, 'r', encoding='utf-8') as infile:
                            reader = csv.DictReader(infile, delimiter='\t')
                            
                            # Initialize writer with header including 'year' and 'page' columns
                            if first_file:
                                fieldnames = reader.fieldnames + ['year', 'page']
                                writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
                                writer.writeheader()
                                first_file = False
                            
                            # Write rows with year and page number
                            for row in reader:
                                row['year'] = year
                                row['page'] = page
                                writer.writerow(row)
                                total_rows += 1
                
                print(f"  ✓ Wrote {total_rows} rows to {output_file}")
    else:
        # Process each year separately
        for year in years:
            output_file = f'{OUTPUT_DIR}/{year}.{file_ext}'
            files = sorted(files_by_year[year], key=lambda x: x[1])  # Sort by page number
            
            print(f"\nProcessing {year}: {len(files)} files -> {output_file}")
            
            if excel:
                # Excel output using pandas
                all_rows = []
                for filepath, page in files:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        reader = csv.DictReader(infile, delimiter='\t')
                        for row in reader:
                            row['year'] = year
                            row['page'] = page
                            all_rows.append(row)
                
                df = pd.DataFrame(all_rows)
                df.to_excel(output_file, index=False, engine='openpyxl')
                print(f"  ✓ Wrote {len(all_rows)} rows to {output_file}")
            else:
                # TSV output (original code)
                with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                    writer = None
                    first_file = True
                    total_rows = 0
                    
                    for filepath, page in files:
                        with open(filepath, 'r', encoding='utf-8') as infile:
                            reader = csv.DictReader(infile, delimiter='\t')
                            
                            # Initialize writer with header including 'year' and 'page' columns
                            if first_file:
                                fieldnames = reader.fieldnames + ['year', 'page']
                                writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
                                writer.writeheader()
                                first_file = False
                            
                            # Write rows with year and page number
                            for row in reader:
                                row['year'] = year
                                row['page'] = page
                                writer.writerow(row)
                                total_rows += 1
                    
                    print(f"  ✓ Wrote {total_rows} rows to {output_file}")
    
    print(f"\n✓ All done! Combined files saved to '{OUTPUT_DIR}/' directory")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Combine Rosenwald TSV files by year with page numbers'
    )
    parser.add_argument(
        '--excel',
        action='store_true',
        help='Output as Excel (.xlsx) instead of TSV files'
    )
    parser.add_argument(
        '--single-file',
        action='store_true',
        help='Combine all years into a single file instead of separate files by year'
    )
    
    args = parser.parse_args()
    combine_tsvs_by_year(excel=args.excel, single_file=args.single_file)
