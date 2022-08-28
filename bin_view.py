import avb
import sys, pathlib, copy, typing, pathlib

def get_binview_from_file(path_avb:str) -> avb.core.AVBPropertyData:
	"""Copy BinView data from a given path to an AVB"""

	with avb.open(path_avb) as avb_file:
		return copy.deepcopy(avb_file.content.view_setting.property_data)

def copy_binview_to_avb(binview:avb.core.AVBPropertyData, avb_file:avb.file.AVBFile) -> avb.bin.BinViewSetting:
	"""Return a new binview"""

	view_new = avb_file.create.BinViewSetting()
	view_new.property_data.update(binview)
	view_new.attributes = avb_file.create.Attributes()
	view_new.attributes.update(binview.get("attributes"))
	return view_new
	

def create_bin(path_avb:str, binview:typing.Optional[avb.core.AVBPropertyData]=None):
	"""Create a new Avid bin at a given path with an optional BinView"""

	with avb.file.AVBFile() as avb_new:

		# Update BinView if given
		if binview:
			avb_new.content.view_setting = copy_binview_to_avb(binview, avb_new)
		
		avb_new.write(path_avb)

def main(avb_path:str, binview:avb.core.AVBPropertyData):
	"""Create an Avid bin with a given binview"""

	avb_path = pathlib.Path(avb_path).with_suffix(".avb")
	if avb_path.exists():
		raise FileExistsError(f"Bin already exists")
	
	create_bin(avb_path, binview)


if __name__ == "__main__":
	
	if len(sys.argv) < 3:
		sys.exit(f"Usage: {pathlib.Path(__file__).name} path_to_binview.avb new_bin_1.avb [new_bin_2.avb ...]")
	
	try:
		binview = get_binview_from_file(sys.argv[1])
	except Exception as e:
		sys.exit(f"Cannot read the binview from {sys.argv[1]}: {e}")
	
	for avb_path in sys.argv[2:]:
		
		try:
			main(avb_path, binview)
		
		except Exception as e:
			print(f"Skipping {avb_path}: {e}")
		
		else:
			print(f"Created bin at {avb_path} with binview {binview.get('name','Untitled')}")