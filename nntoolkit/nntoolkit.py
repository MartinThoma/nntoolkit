import sys
import difflib
import argparse
import evaluate
import utils

def execute_command(args):
    if args.command=="evaluate":
        evaluate.main_bash(args.modelfile, args.inputvec)
    else:
        print "egg or chicken?"


def main():

    ops = ['evaluate', 'train']

    def msg(name=None):
        return 'help message'
    parser = argparse.ArgumentParser(usage=msg())

    parser.add_argument('command', type=str, help='lots of help')

    parser.add_argument("-m", "--model",
                        dest="modelfile",
                        help="where is the model file (.tar)?",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        required=True)
    parser.add_argument("-i", "--input",
                        dest="inputvec",
                        help="""a file which contains an input vector
                               [[0.12, 0.312, 1.21 ...]]""",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        required=True)

    args = parser.parse_args()

    try:
        args.command = args.command.lower()
        ops.index(args.command)
    except:
        didyoumean = difflib.get_close_matches(args.command, ops, 1)
        if didyoumean:
            print 'Did you mean: ' + didyoumean.pop() + '?'
        sys.exit()
    execute_command(args)

if __name__ == '__main__':
    main()