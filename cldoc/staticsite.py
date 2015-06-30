import shutil, subprocess, os, sys

def check_node():
    with open(os.devnull) as devnull:
        try:
            subprocess.call(['node', '-v'], stdout=devnull)
        except OSError as e:
            if e.errno == 2:
                try:
                    subprocess.call(['nodejs', '-v'], stdout=devnull)
                except OSError:
                    return (False, e)

                return (True, 'nodejs')
            else:
                return (False, e)

        return (True, 'node')

def generate(baseout, opts):
    # Call node to generate the static website at the actual output
    # directory
    datadir = os.path.join(os.path.dirname(__file__), 'data')

    if 'CLDOC_DEV' in os.environ:
        jsfile = os.path.join(os.path.dirname(__file__), '..', 'cldoc-static', 'lib', 'cldoc-static-run.js')
    else:
        jsfile = 'cldoc-static'

    print('Generating static website...')

    ok, obj = check_node()

    if not ok:
        sys.stderr.write("\nFatal: Failed to call static site generator. The static site generator uses node.js (http://nodejs.org/). Please make sure you have node installed on your system and try again.\n")

        message = str(obj.message)

        if message:
            sys.stderr.write("  Error message: " + message + "\n")

        sys.stderr.write("\n")

        shutil.rmtree(baseout)
        sys.exit(1)

    if opts.quiet:
        stdout = open(os.devnull, 'w')
    else:
        stdout = None

    try:
        subprocess.call([jsfile, baseout, opts.output], stdout=stdout)
    except OSError as e:
        sys.stderr.write("Failed to run " + jsfile + ", did you install cldoc-static using npm?\n")

    shutil.rmtree(baseout)
