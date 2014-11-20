---
layout: page
---

# Generating site
When you have written your documentation, it's time to generate the resulting
website. cldoc was written with minimal configuration to your exist project in
mind. The main cldoc command is the following:

    cldoc generate [CXXFLAGS] -- [options] [files]

The `CXXFLAGS` are the flags used for compiling your project files. All flags
passed before the `--` are passed along to the compiler. Normally you can use
the flags from your build system and pass them directly. `options` are cldoc
specific options (more details below). Finally, `files` are the remaining
command arguments and are the C++ headers and sources of your project.

# Main available options
The following are the main options used for generating documentation. See
`cldoc generate --help` for all options.

* \-\-output: the output directoy to write the generated files
* \-\-type: the type of output to generate. The default is `html`. If you want
  to generate only the `xml` description use `xml` instead.
* \-\-basedir: the project base directory. This is only used currently to determine
  relative paths for display in the report.
* \-\-merge: the directory in which to find .md files to merge
* \-\-static: generate files which can be served statically
* \-\-report: add a documentation coverage report to the website. Use this to
  include a coverage report section in the generated website.

## Merging external documentation
External documentation can be merged by specifying a directory with the `--merge`
option. All `.md` files in that directory will be merged when the documentation
is generated. It can sometimes be useful to filter files to be merged, for example
to automatically transform some custom markdown content. To do so, you can
specify a program using `--merge-filter` which receives the path to file as its
first argument and should output the filtered content on `stdout`.
