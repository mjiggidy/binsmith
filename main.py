#!/usr/local/env python3

import sys, pathlib
import avb

def normalize_bin_path(bin_path:pathlib.Path|str) -> pathlib.Path:
	"""Validate and normalize a given file path"""

	bin_path = pathlib.Path(bin_path)
	
	if bin_path.suffix.lower() != ".avb":
		bin_path = bin_path.with_suffix(".avb")
	
	if bin_path.exists():
		raise FileExistsError(f"{bin_path} already exists.  Skipping.")
	
	return bin_path

def write_bin_to_path(bin_path:pathlib.Path):
	"""Create an Avid bin at a given path"""
	# TODO: Add more options?  Bin view?

	with avb.file.AVBFile() as bin:
		bin.write(str(bin_path))

def create_bin(bin_path:str) -> pathlib.Path:
	"""Main program: Create Avid bins (AVBs) at the given file path(s)"""

	bin_path = normalize_bin_path(bin_path)
	write_bin_to_path(bin_path)
	return bin_path

if __name__ == "__main__":

	if len(sys.argv) < 2:
		sys.exit(f"Usage: {pathlib.Path(__file__).name} new_bin1.avb [new_bin2.avb ...]")

	for bin_path in sys.argv[1:]:
		try:
			output_path = create_bin(bin_path)
		except Exception as e:
			print(f"Error creating bin {bin_path}: {e}", file=sys.stderr)
		else:
			print(f"Avid bin created at {output_path}")
	