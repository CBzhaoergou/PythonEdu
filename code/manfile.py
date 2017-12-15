import re
import os
import sys
import getopt

def manTabfile(filename):
	pattern = re.compile(r".*\t.*")
	if os.path.exists(filename):
		file = open(filename,'r+')
		content = file.read()
		file.close()
		a = content.split('\n')
		for i in range(len(a)):
			mach = pattern.match(a[i])
			if mach:
				a[i] = re.sub('\t','    ',a[i],999)
				print(a[i])
		s = '\n'.join(a)
		fp = open(filename, 'w')
		fp.write(s)
		fp.close()


def main():
	manTabfile(sys.argv[1])

if __name__ == '__main__':
	main()

# if __name__ == '__main__':
# 	try:
#         opts, args = getopt.getopt(sys.argv[1:], "a:o:c:", ["help", "output="])

#         print("============ opts ==================")
#         print(opts)
#         print len(opts)

#         print("============ args ==================")
#         print(args)
#         print len(args)

#         # check all param
#         for opt, arg in opts:
#             if opt in ("-h", "--help"):
#                 usage()
#                 sys.exit(1)
#             elif opt in ("-t", "--test"):
#                 print("for test option")
#             else:
#                 print("%s  ==> %s" % (opt, arg))

#     except getopt.GetoptError:
#         print("getopt error!")
#         usage()
#         sys.exit(1)