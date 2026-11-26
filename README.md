# Smart City Traffic & Accident Data Analysis

## Project objective

Analyze traffic and road accident data to identify accident-prone locations, understand traffic patterns, examine accident trends, and develop evidence-based road safety recommendations.

This repository is a project scaffold. It contains no datasets or analysis results yet.

## Tools

- **Python:** pandas, NumPy, SciPy, scikit-learn, Matplotlib, Seaborn, Plotly, and Jupyter
- **Excel:** initial inspection and spreadsheet-based data review
- **SQL:** database creation, data import, and analysis queries
- **Power BI:** interactive dashboards and presentation

Install the Python dependencies from this directory:

```bash
python -m pip install -r requirements.txt
```

Launch Jupyter from this directory:

```bash
jupyter notebook
```

The Python script entry point is `Python/main.py`. The starter notebook is `Python/01_Data_Exploration/01_data_exploration.ipynb`.

## Workflow

1. Download relevant traffic and accident datasets from Kaggle or other documented sources.
2. Keep original downloads unchanged in `Dataset/Raw/`; record source details and licenses in `Dataset/External_Sources/`.
3. Inspect and profile data in `Python/01_Data_Exploration/` and, where useful, `Excel/Raw_Data/`.
4. Perform cleaning in `Python/02_Data_Cleaning/` and save separate cleaned outputs under `Dataset/Processed/` or `Excel/Cleaned_Data/`. Never overwrite the raw source files.
5. Conduct exploratory, statistical, location, time, and hotspot analyses in the corresponding `Python/` folders. Store SQL scripts in the appropriate `SQL/` folders.
6. Build visualizations and a Power BI dashboard, then prepare reports and road safety recommendations.

## Folder guide and deliverables

- `Dataset/`: source data, processed data, and external-source records
- `Excel/`: raw and cleaned spreadsheet work
- `SQL/`: database setup, import scripts, and analysis queries
- `Python/`: modular exploration, cleaning, analysis, and notebook workflows
- `PowerBI/`: dashboard files and screenshots
- `Reports/`: accident trend, location analysis, and safety recommendation reports
- `Kaggle_Code/`: project-related Kaggle notebooks or scripts
- `Visualizations/`: exported charts and figures
- `Documentation/`: methodology, data dictionary, and supporting notes

Expected project deliverables include documented and reproducible analysis, charts/maps of trends and accident hotspots, an interactive dashboard, and data-backed road safety recommendations. These will be added after the datasets are selected and analyzed; no findings are assumed in advance.

## Data handling

Keep downloaded originals in `Dataset/Raw/` and do not edit them in place. Put transformed files in `Dataset/Processed/` or `Excel/Cleaned_Data/`. Raw datasets are excluded from Git by `.gitignore`; commit source links, licenses, and documentation rather than redistributing data unless the dataset license permits it.
