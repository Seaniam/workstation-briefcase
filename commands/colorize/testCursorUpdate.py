import sys, time, random

count = 1

while count < 101:
  print '\r>> You have finished %d%%' % count,
  sys.stdout.flush()
  time.sleep(0.01)
  count+=1
print
print "Finished!"
