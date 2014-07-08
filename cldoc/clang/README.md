# libclang Python Bindings

This is an import of the python bindings for libclang taken from the
`bindings/python/clang` directory of the
[clang](https://github.com/llvm-mirror/clang) repository.

The files are taken from commit 8c099d9b04f0b3025e713f76b42a50f3a67d404f
(SVN commit 193725), with the modifications listed in
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
