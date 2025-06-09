# IRLS Signal Recovery System

This project demonstrates how to recover sparse signals sent from an Arduino (via Modbus) to LabVIEW, using IRLS (Iteratively Reweighted Least Squares) in Python.

## Structure

- `irls.py`: Main Python script with IRLS algorithm and modulation matrix generator.
- `theory.md`: Description of compressed sensing and IRLS.
- `formulas.md`: Key formulas.
- `system.md`: System architecture and LabVIEW integration.

## How to Use

1. Generate a measurement matrix `A` using a known pseudo-random sequence and sampling indices.
2. Receive measurement vector `y` from Arduino via Modbus.
3. Call `irls(A, y)` from a Python Node in LabVIEW.