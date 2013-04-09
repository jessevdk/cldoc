---
layout: page
---

# Known issues
There are a few known issues when using cldoc, most of which are related to
clang. The following list is non-exclusive. Please file
[issues on github](https://github.com/jessevdk/cldoc/issues) when you encounter
any other problems.

1. **Unsupported compiler flags**  
   There seem to be certain compiler flags which are not supported when using
   clang as a library. At the moment, at least `-arch` on OS X seems to cause
   clang not to parse any files.

2. **Missing system include paths**  
   This is not directly related to cldoc, but it will suffer from this problem.
   At least on Ubuntu precise, when `gcc-4.7-base` is installed, clang++ will
   assume to only look for g++ 4.7 system include paths, which cannot be found
   since g++ 4.7 is not available for Ubuntu precise. I'm not sure at this time
   how to work around this issue, apart from uninstalling `gcc-4.7-base`.
