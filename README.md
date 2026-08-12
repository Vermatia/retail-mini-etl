# retail-mini-etl

A beginner-friendly Python ETL project for retail data processing.

## Project Structure

```
retail-mini-etl/
├── src/                 # Source code
│   └── etl.py          # Main ETL module
├── tests/              # Test files
│   └── test_etl.py     # Unit tests
├── data/
│   ├── raw/            # Raw input data
│   └── processed/      # Processed output data
├── db/                 # Database files
├── docs/               # Documentation
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Quick Start

### 1. Set up a virtual environment
```bash
python -m venv .venv
```

### 2. Activate the virtual environment
**On Windows (PowerShell):**
```bash
.\.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```bash
.venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the ETL script
```bash
python src/etl.py
```

### 5. Run tests
```bash
pytest tests/
```

To run tests with verbose output:
```bash
pytest tests/ -v
```

## Development

- Add your ETL logic in `src/etl.py`
- Write tests in `tests/test_etl.py`
- Place raw data files in `data/raw/`
- Processed data will be saved to `data/processed/`
- Database files will be stored in `db/`

## Dependencies

- **pandas**: Data manipulation and analysis
- **pytest**: Testing framework

To deactivate the virtual environment:
```bash
deactivate
```