#!/usr/bin/env python3

"""
binsmith.py v1.0.1
Create Avid bins (.avb) with custom display settings

By Michael Jordan <michael@glowingpixel.com>
https://github.com/mjiggidy/binsmith

With pyavb from Mark Reid
https://github.com/markreidvfx/pyavb

Usage: binsmith.py my_new_bin.avb [another_new_bin.avb ...] [-t path/to/template.avb]
"""

import avb
import sys, pathlib, copy, typing, pathlib, enum, argparse

class ViewModes(enum.IntEnum):
	"""Avid Bin View Modes"""
	
	LIST   = 0
	FRAME  = 1
	SCRIPT = 2

class BinDisplays(enum.IntFlag):
	"""Types of data to display in the bin (from Set Bin Display... dialog)"""

	MASTER_CLIPS               = 0b00000000000000001
	SUBCLIPS                   = 0b00000000000000010
	SEQUENCES                  = 0b00000000000000100
	SOURCES                    = 0b00000000000001000
	EFFECTS                    = 0b00000000000010000
	GROUPS                     = 0b00000000000100000
	PRECOMP_RENDERED_EFFECTS   = 0b00000000001000000
	MOTION_EFFECTS             = 0b00000000010000000
	SHOW_CLIPS_CREATED_BY_USER = 0b00000001000000000
	SHOW_REFERENCE_CLIPS       = 0b00000010000000000
	PRECOMP_TITLES_MATTEKEYS   = 0b00000100000000000
	STEREOSCOPIC_CLIPS         = 0b01000000000000000
	LINKED_MASTER_CLIPS        = 0b10000000000000000

	@classmethod
	def get_options(cls, settings:"BinDisplays") -> list["BinDisplays"]:
		"""Return a list of individual options set in the bitmask"""

		return [option for option in BinDisplays if option in settings]

def parse_arguments(argv:list[str]):
	"""Parse the command-line arguments"""

	parser = argparse.ArgumentParser(description="The fun and cool way to batch-create Avid bins.")
	parser.add_argument("-t","--template", metavar="existing_bin_path", nargs="?", help="Optional path to an existing bin to use as a template")
	parser.add_argument("new_bin_path", nargs='+', help="Create a new Avid bin for a given path")
	return parser.parse_args(argv)

def get_binview_from_file(path_avb:str) -> avb.core.AVBPropertyData:
	"""Copy BinView data from a given path to an AVB"""

	with avb.open(path_avb) as avb_file:
		return copy.deepcopy(avb_file.content.view_setting.property_data), ViewModes(avb_file.content.display_mode), BinDisplays(avb_file.content.display_mask)

def copy_binview_to_avb(binview:avb.core.AVBPropertyData, avb_file:avb.file.AVBFile) -> avb.bin.BinViewSetting:
	"""Return a new binview"""

	view_new = avb_file.create.BinViewSetting()
	view_new.property_data.update(binview)
	view_new.attributes = avb_file.create.Attributes()
	view_new.attributes.update(binview.get("attributes"))
	return view_new

def create_bin(path_avb:str, bin_view:typing.Optional[avb.core.AVBPropertyData]=None, view_mode:typing.Optional[ViewModes]=None, bin_display=typing.Optional[BinDisplays]):
	"""Create a new Avid bin at a given path with an optional BinView"""

	with avb.file.AVBFile() as avb_new:

		# Update BinView if given
		if bin_view is not None:
			avb_new.content.view_setting = copy_binview_to_avb(bin_view, avb_new)
		if view_mode is not None:
			avb_new.content.display_mode = view_mode
		if bin_display is not None:
			avb_new.content.display_mask = bin_display
		
		avb_new.write(path_avb)

def resolve_path(path_bin:str, allow_existing:bool=False) -> str:
	"""Build the final path"""

	# Ensure file extension is ".avb"
	path_bin = pathlib.Path(path_bin).with_suffix(".avb")

	# Ensure file does not exist
	if not allow_existing and path_bin.exists():
		raise FileExistsError(f"Bin already exists")

	return str(path_bin)

def main(paths_newbins:list[str], path_template:typing.Optional[str]=None):
	"""Create an Avid bins with an optional template"""

	bin_view    = None
	view_mode   = None
	bin_display = None

	# Load an existing bin as a template for bin settings, if provided
	if path_template is not None:
		bin_view, view_mode, bin_display = get_binview_from_file(input_args.template)
		print(f"Using view setting \"{bin_view.get('name','Untitled')}\" in {view_mode.name.title()} mode with bin display options: {', '.join(' '.join(opt.name.split('_')).title() for opt in BinDisplays.get_options(bin_display))}")
	
	# Create a new bin for each path provided
	for path_newbin in paths_newbins:
		try:
			path_newbin = resolve_path(path_newbin)
			create_bin(path_newbin, bin_view, view_mode, bin_display)
		except Exception as e:
			print(f"Skipping {path_newbin}: {e}", file=sys.stderr)
		else:
			print(f"Created bin at {path_newbin}")
	
if __name__ == "__main__":

	input_args = parse_arguments(sys.argv[1:])

	try:
		main(paths_newbins=input_args.new_bin_path, path_template=input_args.template)
	except Exception as e:
		sys.exit(str(e))
