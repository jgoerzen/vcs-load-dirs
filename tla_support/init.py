# arch-tag: tla_load_dirs initializatoin

from optparse import OptionParser
from tla_support import util, commandver
import sys

def run(darcsdefault):
    version = '1.0.14'

    parser = OptionParser(usage="usage: %prog [options] newpath",
                          version=version)
    parser.add_option("-w", "--wc", dest="wc", default=".",
                      help="Set working copy to WC (defaults to current directory)", metavar="WC")
    parser.add_option("-l", "--log", dest="changelog", metavar="FILE", default=None,
                      help="Get changelog text from FILE")
    parser.add_option("-L", "--log-message", dest="logtext", metavar="TEXT",
                      default='', help="Log with TEXT")
    parser.add_option("-s", "--summary", dest="summary", metavar="MSG",
                      default=None, help="Set log summary message to MSG, overriding the default")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      default=False, help="Show more status information")
    parser.add_option("-n", "--no-commit", action="store_false", dest="docommit",
                      default=True, help="Do not commit the changes.")

    (options, args) = parser.parse_args()
    util.verbose = options.verbose

    log = options.logtext + "\n"
    if options.changelog:
        fd = open(options.changelog, "r")
        log += fd.read()
        fd.close()

    if len(args) != 1:
        parser.error("Failed to specify a path to import.")

    commandver.setdarcs(darcsdefault)

    from tla_support import tla_wc, tla_interact

    wc = tla_wc.wc(options.wc, verbose = options.verbose)
    if not wc.gettaggingmethod() in ['explicit', 'tagline']:
        print "Working directory uses unsupported tagging method %s" % \
              wc.gettaggingmethod()
        sys.exit(1)


    tla_interact.interaction(wc, args[0], options.docommit, log = log,
                             verbose = options.verbose,
                             summary = options.summary).main()
    
