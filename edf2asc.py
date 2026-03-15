EyeLink EDF -> ASC batch converter (Python wrapper for edf2asc64.exe)

WHAT THIS SCRIPT DOES
---------------------
- Scans a folder for EyeLink .edf files
- For each .edf, converts it to .asc using SR Research's edf2asc64.exe
- Writes the .asc file into the same folder as the .edf file
- Skips conversion if the .asc already exists

WHY cwd MATTERS
---------------
edf2asc64.exe depends on DLLs (typically edfapi64.dll and zlibwapi.dll).
Windows will only find those DLLs if they are either:
- in the same folder as the EXE, OR
- in a folder on the system PATH, OR
- in the current working directory (cwd) when running the EXE.

So we run subprocess with:
    cwd = exe_folder
to make sure the EXE finds its DLLs.

FOLDER REQUIREMENTS
-------------------
Your converter folder must contain at least:
- edf2asc64.exe
- edfapi64.dll
- zlibwapi.dll

Example:
C:\\...\\EDF_Access_API\\Example\\
    edf2asc64.exe
    edfapi64.dll
    zlibwapi.dll
"""

from __future__ import annotations

import os
import subprocess
from typing import Optional, List


def convert_edf_folder(
    exe_folder: str,
    edf_folder: str,
    recursive: bool = False,
    overwrite: bool = False,
    verbose: bool = True,
) -> None:
    """
    Convert all EyeLink EDF files in `edf_folder` to ASC using edf2asc64.exe.

    Parameters
    ----------
    exe_folder : str
        Folder containing the converter binary and required DLLs:
            - edf2asc64.exe
            - edfapi64.dll
            - zlibwapi.dll
    edf_folder : str
        Folder containing .edf file(s) to convert.
    recursive : bool
        If True: search subfolders recursively for .edf files.
        If False: only convert EDFs directly inside `edf_folder`.
    overwrite : bool
        If True: reconvert even if .asc already exists.
        If False: skip if .asc exists.
    verbose : bool
        If True: print progress and converter output.

    Raises
    ------
    FileNotFoundError
        If the converter executable or EDF folder does not exist.
    RuntimeError
        If conversion fails for any file (non-zero return code) and no ASC is created.
    """

    # --- 1) Normalize paths (helps avoid issues with trailing slashes) ---
    exe_folder = os.path.abspath(exe_folder)
    edf_folder = os.path.abspath(edf_folder)

    # --- 2) Build absolute path to the EXE ---
    exe_path = os.path.join(exe_folder, "edf2asc64.exe")

    # --- 3) Validate basic requirements early (clear errors) ---
    if not os.path.isfile(exe_path):
        raise FileNotFoundError(f"Cannot find converter EXE: {exe_path}")

    if not os.path.isdir(edf_folder):
        raise FileNotFoundError(f"Cannot find EDF folder: {edf_folder}")

    # --- 4) Collect EDF files to convert ---
    edf_files: List[str] = []

    if recursive:
        # Walk through folder and all subfolders
        for root, _, files in os.walk(edf_folder):
            for f in files:
                if f.lower().endswith(".edf"):
                    edf_files.append(os.path.join(root, f))
    else:
        # Only list files in the top-level folder
        for f in os.listdir(edf_folder):
            if f.lower().endswith(".edf"):
                edf_files.append(os.path.join(edf_folder, f))

    if verbose:
        print(f"[INFO] Converter EXE: {exe_path}")
        print(f"[INFO] EDF folder:    {edf_folder}")
        print(f"[INFO] Recursive:     {recursive}")
        print(f"[INFO] Found {len(edf_files)} EDF file(s).")

    if not edf_files:
        # Nothing to do (not an error)
        if verbose:
            print("[INFO] No EDF files found. Exiting.")
        return

    # --- 5) Convert each EDF ---
    for edf_full in sorted(edf_files):
        base, _ = os.path.splitext(edf_full)
        asc_full = base + ".asc"

        # Skip if ASC exists and overwrite is False
        if (not overwrite) and os.path.isfile(asc_full):
            if verbose:
                print(f"[SKIP] ASC exists: {asc_full}")
            continue

        if verbose:
            print("\n----------------------------------------")
            print(f"[CONVERT] EDF: {edf_full}")
            print(f"[TARGET ] ASC: {asc_full}")

        # Run the converter.
        # IMPORTANT: cwd=exe_folder so edf2asc64.exe can find edfapi64.dll / zlibwapi.dll.
        res = subprocess.run(
            [exe_path, edf_full],
            cwd=exe_folder,
            capture_output=True,
            text=True,
        )

        # Print diagnostic output (if any)
        if verbose:
            print(f"[RESULT] returncode: {res.returncode}")
            if res.stdout.strip():
                print("[STDOUT]")
                print(res.stdout)
            if res.stderr.strip():
                print("[STDERR]")
                print(res.stderr)

        # Check if output exists
        if os.path.isfile(asc_full):
            if verbose:
                print(f"[OK] Created: {asc_full}")
            continue

        # If ASC not created, treat as failure
        raise RuntimeError(
            "Conversion failed (ASC not created).\n"
            f"EDF: {edf_full}\n"
            f"Return code: {res.returncode}\n"
            "Tip: Ensure edf2asc64.exe is in the same folder as edfapi64.dll and zlibwapi.dll, "
            "and that you are using matching 64-bit versions."
        )


# -------------------------
# USER SETTINGS (EDIT THESE)
# -------------------------
if __name__ == "__main__":
    # Folder that contains:
    #   edf2asc64.exe
    #   edfapi64.dll
    #   zlibwapi.dll
    EXE_FOLDER = r"C:\Users\user\Desktop"

    # Folder that contains the EDF file(s)
    EDF_FOLDER = r"C:\Users\user\Desktop"

    # Convert EDFs (set recursive=True if your EDFs are in subfolders too)
    convert_edf_folder(
        exe_folder=EXE_FOLDER,
        edf_folder=EDF_FOLDER,
        recursive=False,
        overwrite=False,
        verbose=True,
    )