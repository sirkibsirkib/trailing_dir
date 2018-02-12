import sys
import os
import filecmp
from shutil import copyfile

if len(sys.argv) != 3:
	print('USAGE: python trailing_dir.py <src_path> <dest_path>')
	exit(0)
AF = 'ANCHOR_FILE'
src_path = sys.argv[1]
dest_path = sys.argv[2]
anc_a = os.path.join(src_path, AF)
anc_b = os.path.join(dest_path, AF)

# CHECK ANCHOR FILES EXIST
if not os.path.isfile(anc_a):
	print('Expected src anchor file with path `{}`. Make sure you aren\'t using the wrong path!'.format(anc_a))
	exit(1)
if not os.path.isfile(anc_b):
	print('Expected dest anchor file with path `{}`. Make sure you aren\'t using the wrong path!'.format(anc_b))
	exit(1)
if not filecmp.cmp(anc_a, anc_b):
	print('Your anchor files at `{}` and `{}` do not match!'.format())
	exit(1)

# CONFIRM WITH USER
print('About to copy from {} to {}. ENTER if OK, CTRL+C if not!'.format(src_path, dest_path))
try: input()
except:
	print('Nevermind! Exiting!')
	exit(0)

src_path_len = len(src_path)
cpy_count_d, cpy_count_f = 0, 0
count_d, count_f = 0, 0


# DO THE THING
print('starting...')
for dirpath, dnames, fnames in os.walk(src_path):
	chopped = dirpath[src_path_len:]
	for dname in dnames:
		a = os.path.join(dirpath, dname)
		b = os.path.join(dest_path, *[chopped, dname])
		cpy_count_d += 1
		if not os.path.exists(b):
			os.makedirs(b)
			print('D+ {}'.format(b))
			count_d += 1
	
	for fname in fnames:
		if fname == AF: continue
		a = os.path.join(dirpath, fname)
		b = os.path.join(dest_path, *[chopped, fname])
		cpy_count_f += 1
		if not os.path.isfile(b): 
			copyfile(a, b)
			print('F+ {}'.format(b))
			count_f += 1

# PRINT STATS
print('Copied {}/{} directories.'.format(count_f, cpy_count_f))
print('Copied {}/{} files.'.format(count_d, cpy_count_d))