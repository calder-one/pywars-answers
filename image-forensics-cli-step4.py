import argparse
parser=argparse.ArgumentParser()

parser.add_argument('image_directory', help='A file path containing images to process')
parser.add_argument('-d','--display',action="store_true", dest="show", help='Display the image')
parser.add_argument('-v','--verbose',action="count", help='Be verbose.  More -v is more verbose.')

args=parser.parse_args()

print("Here is what was extracted from the command line.")
print(args)

print("Image Directory", args.image_directory)
print("Display images?", args.show)
print("How verbose?", args.verbose)



