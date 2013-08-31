#!/home/paulk/software/bin/python
import sys
f = open("/home/paulk/RP/bash_general/empty_subjob.sh")
script = f.readlines()
f.close()
cmd = "%s" % sys.argv[1]
print "".join(script) % cmd
