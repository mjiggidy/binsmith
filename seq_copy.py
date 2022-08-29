import sys, pathlib
import avb
from avb.ioctx import AVBIOContext
from avb.core import walk_references

path_output = "/Users/Shared/AvidMediaComposer/Shared Avid Projects/LocalProject/Output from Script/output3.avb"
#path_output = "output.avb"

def newest_sequence(bin):
	return next(bin.toplevel())

if __name__ == "__main__":
	if len(sys.argv) < 2:
		sys.exit(f"Usage: {pathlib.Path(__file__).name} bin_path.avb [bin_path_2.avb ...]")

	with avb.file.AVBFile() as new_bin:

		for path_bin in sys.argv[1:]:

			with avb.open(path_bin) as orig_bin:

				print(f"Orig bin is {orig_bin}")
				print(f"New bin is  {new_bin}")
				print("Orig has ",len(orig_bin.content.items))

				seq = newest_sequence(orig_bin.content)

				print("Now walking...")
				
				for obj in walk_references(seq):
					obj.root = new_bin
					obj.mark_modified()
					print(f"Adding {obj}")
					if obj.root is not new_bin:
						print(f"Weird: {obj.root}")
					new_bin.content.add_mob(obj)
				
				print("New has ", len(new_bin.content.items))
				print(f"Writing bin to {path_output}")
				new_bin.large_bin = True
				new_bin.write(path_output)