import avb
import sys, pathlib

def bin_info(avb_path:str):
	"""Display bin info"""

	with avb.open(avb_path) as avb_file:

		bin = avb_file.content
		view_source = bin.view_setting
		view_attributes = view_source.attributes.copy()

	with avb.file.AVBFile() as avb_new:

		view_new = avb_new.create.BinViewSetting()
		view_new_attributes = avb_new.create.Attributes()
		view_new_attributes.update(view_attributes)
		view_new.name = view_source.name
		view_new.kind = view_source.kind
		view_new.attr_count = view_source.attr_count
		view_new.attr_type = view_source.attr_type
		view_new.attributes = view_new_attributes
		view_new.columns = view_source.columns
		view_new.format_descriptors = view_source.format_descriptors
		avb_new.content.view_setting = view_new
		print(avb_new.content.view_setting)

		avb_new.write("NewBinView.avb")



if __name__ == "__main__":
	
	if len(sys.argv) < 2:
		sys.exit(f"Usage: {pathlib.Path(__file__).name} path_to_bin.avb [path_to_bin2.avb ...]")
	
	for avb_path in sys.argv[1:]:
		bin_info(avb_path)