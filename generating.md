---
layout: page
---

# Generating site
When you have written your documentation, it's time to generate the resulting
website. cldoc was written with minimal configuration to your exist project in
mind. The main cldoc command is the following:

    cldoc [CXXFLAGS] -- [options] [files]

The `CXXFLAGS` are the flags used for compiling your project files. All flags
passed before the `--` are passed along to the compiler. Normally you can use
the flags from your build system and pass them directly. `options` are cldoc
specific options (more details below). Finally, `files` are the remaining
command arguments and are the C++ headers and sources of your project.

# Available options

* --output: the output directoy to write the generated files
* --type: the type of output to generate. The default is `html`. If you want
  to generate only the `xml` description use `xml` instead.
* --basedir: the project base directory. This is only used currently to determine
  relative paths for display in the report.
* --merge: the directory in which to find .md files to merge
* --report: add a documentation coverage report to the website. Use this to
  include a coverage report section in the generated website.
* --serve: serve the generated site locally. This starts a local webserver and
  serves the generated documentation from the directory specified with `--output`.

## Merging external documentation
External documentation can be merged by specifying a directory with the `--merge`
option. All `.md` files in that directory will be merged when the documentation
is generated.
