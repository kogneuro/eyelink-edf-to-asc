# EyeLink EDF → ASC Converter (Python)

This project converts **EyeLink `.edf`** files into **`.asc`** using SR Research’s **`edf2asc64.exe`** via a Python wrapper.  
It’s intended for **batch conversion** (no drag & drop). If you have the **`edf2asc64.exe`** app but have an issue to run it; try this!

---

## What it does

For each `.edf` file in a target folder, the script:

1. checks whether a matching `.asc` already exists  
2. if not, runs `edf2asc64.exe` to convert  
3. writes the `.asc` file into the **same folder** as the `.edf`

---

## Requirements (very important)

### Converter folder must include these files (same folder)

- `edf2asc64.exe`
- `edfapi64.dll`
- `zlibwapi.dll`

Example:

C:\Users\user\Desktop\EyeLink\EDF_Access_API\Example
edf2asc64.exe
edfapi64.dll
zlibwapi.dll


If these DLLs are missing or not found, `edf2asc64.exe` may crash silently and produce no output.

---

## EDF folder structure

Example:


C:\Users\user\Desktop\\EyeLink\example_edf.edf


After conversion:


C:\Users\user\Desktop\\EyeLink\example_edf.asc


---

## How to run

### Run from VS Code

1. Open `edf_to_asc_converter.py`
2. Edit the settings at the bottom:
   - `EXE_FOLDER`
   - `EDF_FOLDER`
3. Run the file (Run ▶ / Debug)

### Option B: Run from terminal


python edf2asc.py


---

## Settings you can change

Inside the script call:

- `recursive=False`  
  - `False`: only convert EDF files directly in `EDF_FOLDER`  
  - `True`: convert EDF files in all subfolders too

- `overwrite=False`  
  - `False`: skip if `.asc` already exists  
  - `True`: reconvert and overwrite

- `verbose=True`  
  - prints detailed progress and converter return codes

---
