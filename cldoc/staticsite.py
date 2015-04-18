import shutil, subprocess, os, sys

def check():
    with open(os.devnull) as devnull:
        try:
            subprocess.call(['nodejs', '-v'], stdout=devnull)
        except OSError as e:
            if e.errno == 2:
                try:
                    subprocess.call(['node', '-v'], stdout=devnull)
                except OSError:
                    return (False, e)

                return (True, 'node')
            else:
                return (False, e)

        return (True, 'nodejs')

def check_dependency(node, dependency):
    with open(os.devnull) as devnull:
        try:
            sp = subprocess.Popen([node, '-e', 'require("' + dependency + '")'], stdout=devnull, stderr=devnull)
            return sp.wait() == 0
        except:
            return False

def check_dependencies(node):
    dependencies = ['jsdom', 'xmldom']
    missing = False

    for dependency in dependencies:
        if not check_dependency(node, dependency):
            sys.stderr.write("Missing node dependency: " + dependency + "\n")
            missing = True

    if missing:
        sys.stderr.write("\nPlease install missing dependencies using npm\n")

    return not missing

def generate(baseout, opts):
    # Call node to generate the static website at the actual output
    # directory
    datadir = os.path.join(os.path.dirname(__file__), 'data')
    jsfile = os.path.join(datadir, 'staticsite', 'staticsite.js')

    print('Generating static website...')
    ok, obj = check()

    if not ok:
        sys.stderr.write("\nFatal: Failed to call static site generator. The static site generator uses node.js (http://nodejs.org/). Please make sure you have node installed on your system and try again.\n")

        message = str(obj.message)

        if message:
            sys.stderr.write("  Error message: " + message + "\n")

        sys.stderr.write("\n")

        shutil.rmtree(baseout)
        sys.exit(1)

    if not check_dependencies(obj):
        sys.exit(1)

    subprocess.call([obj, jsfile, baseout, opts.output])
    shutil.rmtree(baseout)
