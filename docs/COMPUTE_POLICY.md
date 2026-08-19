# Compute policy

The frozen result is designed for CPU reproduction on Python 3.11 or newer.
Core dependencies are NumPy, pandas, and SciPy. Bootstrap randomness is fixed at
seed 42. Public figures use seed 7.

CI verifies unit contracts and release checksums. It intentionally does not
re-download market data or rerun every historical strategy search. Full campaign
reconstruction belongs to a separately versioned raw-data workflow and must not
overwrite a frozen evidence release.
