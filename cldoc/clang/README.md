# libclang Python Bindings

This is an import of the python bindings for libclang taken from the
`bindings/python/clang` directory of the
[clang](https://github.com/llvm-mirror/clang) repository.

The files are taken from commit 54f5752c3600d39ee8de62ba9ff304154baf5e80
(SVN commit 288149), with the modifications listed in
`cldoc/clang/cindex-updates.patch`.

To apply the cldoc changes, run:

	cp ${CLANG_DIR}/bindings/python/clang/cindex.py cldoc/clang/cindex.py
	patch -p1 < cldoc/clang/cindex-updates.patch

To revert the custom modifications, run:

	patch -R -p1 < cldoc/clang/cindex-updates.patch

To create a new patch (e.g. after applying the cldoc changes on top of
a new clang version), run:

	git add cldoc/clang/cindex.py
	cp ${CLANG_DIR}/bindings/python/clang/cindex.py cldoc/clang/cindex.py
	git diff -R cldoc/clang/cindex.py > cldoc/clang/cindex-updates.patch
