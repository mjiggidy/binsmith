import avb
import sys, pathlib, copy, typing, pathlib, enum

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

def main(avb_path:str, bin_view:typing.Optional[avb.core.AVBPropertyData]=None, view_mode:typing.Optional[ViewModes]=None, bin_display=typing.Optional[BinDisplays]):
	"""Create an Avid bin with a given binview"""

	avb_path = pathlib.Path(avb_path).with_suffix(".avb")
	if avb_path.exists():
		raise FileExistsError(f"Bin already exists")
	
	create_bin(avb_path, bin_view, view_mode, bin_display)

if __name__ == "__main__":
	
	if len(sys.argv) < 3:
		sys.exit(f"Usage: {pathlib.Path(__file__).name} path_to_binview.avb new_bin_1.avb [new_bin_2.avb ...]")
	
	try:
		bin_view, view_mode, bin_display = get_binview_from_file(sys.argv[1])
		print(f"Using view setting \"{bin_view.get('name','Untitled')}\" in {view_mode.name.title()} mode with bin display options: {', '.join(' '.join(opt.name.split('_')).title() for opt in BinDisplays.get_options(bin_display))}")
	except Exception as e:
		sys.exit(f"Cannot read the binview from {sys.argv[1]}: {e}")
	
	for avb_path in sys.argv[2:]:
		
		try:
			main(avb_path, bin_view=bin_view, view_mode=view_mode, bin_display=bin_display)
		
		except Exception as e:
			print(f"Skipping {avb_path}: {e}")
		
		else:
			print(f"Created bin at {avb_path} with binview {bin_view.get('name','Untitled')}")