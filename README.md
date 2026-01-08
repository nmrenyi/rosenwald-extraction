# Rosenwald Medical Directory Dataset

This repository contains structured tabular data extracted from the historical Rosenwald medical directories, spanning from 1887 to 1906. The dataset provides valuable insights into the French medical profession during the late 19th and early 20th centuries.

## Overview

The Rosenwald medical directories were comprehensive annual listings of medical practitioners in France, documenting physicians across Paris and the provinces. This dataset represents a machine-readable extraction of those historical records.

### Dataset Statistics

- **Total files**: 4,166 TSV files
- **Time period**: 1887-1906 (20 years)
- **Total entries**: ~381,000 lines (including headers)
- **Geographic coverage**: Paris and French provinces
- **Data format**: Tab-separated values (TSV)

## Data Structure

Each TSV file represents a single page from the original Rosenwald directories and follows this schema:

| Column | Description |
|--------|-------------|
| `nom` | Physician's surname/family name |
| `année` | Year of medical degree or qualification |
| `notes` | Professional notes, specialties, honors (e.g., ✶ for decorations, "mal. des yeux" for eye diseases, "dent." for dentist) |
| `adresse` | Practice address (street name and number) |
| `horaires` | Consultation hours (e.g., "Lun. Mer. Ven. 3 à 5" = Monday, Wednesday, Friday, 3-5pm) |
| `sexe` | Gender (when specified) |

### File Naming Convention

Files are named using the pattern: `YYYY-NNNN.tsv`
- `YYYY`: Publication year (1887-1906)
- `NNNN`: Page number (zero-padded, 4 digits)

Example: `1887-0022.tsv` represents page 22 from the 1887 directory.

## Sample Data

```tsv
nom	année	notes	adresse	horaires	sexe
Abadie	1870	✶, Mal. des yeux.	Volney 9	Lun. Mer. Ven. 3 à 5	
Adam	1875	dent.	pl. St-Michel 1		
Agard	1870		Bondy 28	1 à 3	
Anger (B.)	1865	✶, Ex-Int. des Hôp.	boul. Haussmann 33	3 à 6	
```

## Data Extraction

The data was extracted using a multi-stage pipeline combining OCR (Tesseract) and AI-powered text analysis (Gemini). The original source material consists of scanned pages from historical Rosenwald medical directories.

### Processing Pipeline

The `copy.sh` script demonstrates the data collection workflow:
```bash
# Copy extracted TSV files from the analysis directory
cp /path/to/analysed-tsv/*.tsv rosenwald-extraction/
```

## Usage Examples

### Loading the data in Python

```python
import pandas as pd
import glob

# Load a single file
df = pd.read_csv('rosenwald-extraction/1887-0022.tsv', sep='\t')

# Load all files from a specific year
files_1887 = glob.glob('rosenwald-extraction/1887-*.tsv')
df_1887 = pd.concat([pd.read_csv(f, sep='\t') for f in files_1887])

# Load entire dataset
all_files = glob.glob('rosenwald-extraction/*.tsv')
df_complete = pd.concat([pd.read_csv(f, sep='\t') for f in all_files])
```

### Basic analysis

```python
# Count physicians by year of qualification
print(df_complete['année'].value_counts().sort_index())

# Find specialists
specialists = df_complete[df_complete['notes'].notna()]

# Extract Paris addresses
paris = df_complete[df_complete['adresse'].notna()]
```

## Research Applications

This dataset can be used for:

- **Historical demographics**: Studying the growth and distribution of the medical profession in France
- **Medical specialization**: Tracking the emergence of medical specialties over time
- **Urban geography**: Mapping medical practices in Paris and provincial cities
- **Gender studies**: Analyzing women's entry into the medical profession
- **Social history**: Understanding professional honors, hospital affiliations, and consulting hours
- **Network analysis**: Identifying medical families and professional connections

## Data Quality Notes

- Some fields may be empty (especially `sexe` which was rarely documented)
- Addresses use historical street names and numbering systems
- Medical specialties are often abbreviated or in French
- Symbols like ✶ (star), ✢, and O indicate various honors and decorations
- OCR and extraction errors may be present despite multi-stage processing

<!-- ## Citation

If you use this dataset in your research, please cite:

```
Rosenwald Medical Directory Dataset (1887-1906)
Extracted from historical Rosenwald medical directories
Processed by: Ren Yi, 2025
``` -->

## Contact

For questions, feedback, or collaboration:

**Ren Yi**  
Email: [renyi1006@gmail.com](mailto:renyi1006@gmail.com)

## License

This dataset is derived from historical public domain documents. Please verify appropriate usage rights for your specific application.

## Acknowledgments

Data extracted using Tesseract OCR and Google Gemini AI from original Rosenwald directory scans.
## Related Resources

- [Extraction Pipeline](https://github.com/nmrenyi/extraire-tesseract-openai)
- [Original Rosenwald Guide publications (1887-1906)](https://gallica.bnf.fr/ark:/12148/cb344120051/date)
