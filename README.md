# Trailing Dir
Make some filesystem B mirror filesystem A. Works only on NAME basis, so contents are not checked.

Run using `python trailing_dir.py <src> <dest>`
where `src` is the path of the source filesystem you wish to clone, and wherer `dest` is the path to the filesystem you wish to BE a clone of `src`.
Both filesystems require, at their root, a file called `ANCHOR_FILE` with the same contents as each other. This is in place to make it harder for you to accidentally write to the wrong directory and screw everything up.
