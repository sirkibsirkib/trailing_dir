import os
import sys
from glob import glob
from shutil import copyfile

def print_help():
	print(
		("1. create trailing_dir files in all the appropriate\n"
		 "   places in the SRC dir tree. These files are called\n"
		 "   {TD_BLOCKFILES, TD_BLOCKDIRS, TD_IGNORE}. contents irrelevant\n"
		 "     TD_BLOCKFILES: prevents files in this shallow dir from being visited"
		 "     TD_BLOCKDIRS: prevents subdirectories from being visited"
		 "     TD_IGNORE: a text file with a line for each filename.\n"
		 "         TD will skip these files in the SHALLOW DIR"
		 "2. run script with args <src> and <dest>"
		)
	)
if len(sys.argv) >= 2 and ('-h' in sys.argv or "--help" in sys.argv):
	print_help()
	exit(0)

if len(sys.argv) != 3:
	print('USAGE: python trailing_dir.py <src_path> <dest_path>')
	exit(0)

	
	
def assert_dir(d):
	if not os.path.isdir(d):
		print('Dir `{}` is not a valid directory.'.format(d))
		exit(1)
	

src_path = sys.argv[1]
assert_dir(src_path)
src_len = len(src_path)

dest_path = sys.argv[2]
assert_dir(dest_path)
dest_len = len(dest_path)



def traverse(d, depth=0):
	files = []
	dirs = []
	ignored = {}
	files_enabled = True
	dirs_enabled = True
	try:
		with open(os.path.join(d, 'TD_IGNORE'), 'r') as ignore:
			ignored = list([ln.strip() for ln in ignore.readlines()])
	except: pass
	
	for x in os.listdir(d):
		if x in ignored:
			print('    ignoring {}'.format(x))
			continue
		if x == 'TD_BLOCKDIRS':
			dirs_enabled = False
			continue
		if x == 'TD_BLOCKFILES':
			files_enabled = False
			continue
		new_path = os.path.join(d, x)
		if os.path.isdir(new_path):
			dirs.append(new_path)
		else:
			#here check for conditions and set vars
			files.append(new_path)
	if files_enabled:
		for x in files:
		
			preamble = '   '
			d_path = os.path.join(dest_path + x[src_len:])
			if not os.path.exists(d_path):
				copyfile(x, d_path)
				preamble = '(+)'
			#print('<{}>'.format(d_path))
			print('{} {}visiting {}'.format(preamble, ' '*depth*2, x))
	if dirs_enabled:
		for x in dirs:
			preamble = '   '
			d_path = os.path.join(dest_path + x[src_len:])
			if not os.path.exists(d_path):
				os.makedirs(d_path)
				preamble = '(+)'
			#print('<{}>'.format(d_path))
			print('{} {}traversing {}'.format(preamble, ' '*depth*2, x))
			traverse(x, depth=depth+1)
	
traverse(src_path)