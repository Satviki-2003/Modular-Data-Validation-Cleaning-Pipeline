# Modular Data Validation & Cleaning Pipeline

A robust, metadata-driven Python framework designed to transform "dirty" raw data into production-ready datasets. This project moves away from static cleaning scripts by using a **JSON-driven architecture** to handle imputation, business rule validation, and outlier detection dynamically.

## 🚀 Key Features

* **JSON Configuration:** All cleaning rules are defined in a central `config.json`, making the pipeline dataset-agnostic.
* **Four-Stage Processing:**
    1.  **Ingestion:** Safe file loading with extension validation (CSV/Excel).
    2.  **Imputation:** Statistical null-filling strategies (Mean, Median, Mode, or Constant).
    3.  **Validation:** Regex-based "Sieve" logic to enforce business rules (e.g., phone formats, status codes).
    4.  **Outlier Engineering:** IQR-based (Interquartile Range) detection with "Cap" or "Drop" strategies.
* **Quarantine Layer:** Instead of deleting invalid records, the system isolates them into a `quarantine.csv` for audit and manual review.
* **Dynamic Reporting:** Automatically generates a text-based Executive Summary with data health metrics.

## 📂 Project Structure

```text
├── data/
│   ├── input/       # Raw, uncleaned datasets
│   ├── output/      # Final cleaned CSVs & Health Reports
│   └── quarantine/  # Isolated invalid records
├── src/             # Source code modules
│   ├── reader.py          # Data ingestion logic
│   ├── validator.py       # Imputation & Regex validation
│   ├── outlier_engine.py  # IQR outlier handling
│   └── reporter.py        # Automated report generation
├── config.json      # The "Brain" - Define your rules here
└── main.py          # Entry point
```

## 🛠️ Installation & Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment:
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate it (Windows)
   venv\Scripts\activate
   
   # Activate it (Mac/Linux)
   source venv/bin/activate

   # Install required libraries
   pip install -r requirements.txt
   ```

3. **Configure your rules** in `config.json`:
   ```json
   "Salary": {
       "nulls": "mean",
       "outliers": "cap"
   },
   "Phone": {
       "rule": "^[0-9]{10}$",
       "nulls": "Unknown"
   }
   ```

4. **Run the pipeline**:
   ```bash
   python main.py
   ```

## 📊 Sample Pipeline Report
After execution, the system generates a `report.txt`:
```text
=== DATA PIPELINE EXECUTIVE SUMMARY ===
Total Records Input:   1020
Cleaned Records:       927
Quarantined Records:   93
Pipeline Success Rate: 90.88%

=== DYNAMIC COLUMN SUMMARY ===
[SALARY]
  - Average: 85240.15
  - Median:  84100.00
...
```

## 🧠 Technical Highlights
* **OOP Design:** Built using Object-Oriented principles for high maintainability and scalability.
* **Data Integrity:** Implements a "Fill-then-Validate" strategy to ensure formatting checks don't fail on missing data.
* **Vectorized Operations:** Leverages Pandas and NumPy for high-performance data manipulation.