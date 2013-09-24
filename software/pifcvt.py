#----------------------------------------------------------------------
# Name:        pifload.py
# Purpose:     load a configuration into a pif board via the hidapi DLL/SO
#
# Author:      Tim
#
# Created:     01/07/2013
# Copyright:   (c) Tim 2013
# Licence:     Creative Commons Attribution-ShareAlike 3.0 Unported License.
#----------------------------------------------------------------------
#!/usr/bin/env python

import sys, pifglobs
from pifglobs import *

ofile = None

##---------------------------------------------------------
def processLine(line):
  global ofile
  l = line.strip('\n')
  n = len(l)
  v = []
  for i in range(0, CFG_PAGE_SIZE):
    s = line[(i*8):(i*8+8)]
    x = int(s, 2)
    v.append(x)
    if ofile:
      ofile.write('0x%02x,' % x)
  if ofile:
    ofile.write('\n')
  return v

##---------------------------------------------------------
def convert(fname):
  global ofile
  print('configuration file is ' + fname)

  data = []
  f = open(fname, 'r')
  print("reading JEDEC file ") ,
  lnum = 0;
  state = 'init'

  for line in f:
    lnum += 1
    if (lnum % 250) == 0:
      print('.') ,

    if len(line) < 1:
      continue
    c0 = line[0]
    valid = (c0=='0') or (c0=='1')
    if state == 'init':
      if valid:
        print("\nfirst data line: %d" % lnum)
        state = 'inData'
        v = processLine(line)
        data.append(v)
    elif state == 'inData':
      if valid:
        v = processLine(line)
        data.append(v)
      else:
        print("\nlast data line: %d" % (lnum-1))
        state = 'finished'
        break

##      if line.find('0x') >= 0:
##        bytes = line.strip(' ;{}\n\t').split(',')
##        for b in bytes:
##          try:
##            v = int(b, 16)
##            data.append(v)
##          except:
##            pass

  f.close()
  if ofile:
    ofile.close()
  print('%d frames' % data.__len__())
  print("convert finished.")
  return data

##---------------------------------------------------------
def readRaw():
  raw = []
  f = open('raw.c', 'r')
  print("reading configuration file ") ,
  lnum = 0;
  for line in f:
    if line.find('0x') >= 0:
      bytes = line.strip(' ;{}\n\t').split(',')
      for b in bytes:
        try:
          v = int(b, 16)
          raw.append(v)
        except:
          pass
    lnum += 1
    if (lnum % 250) == 0:
      print('.') ,
  f.close()
  print('%d bytes' % raw.__len__())
  return raw

##---------------------------------------------------------
def rawVec(raw, pageNum):
  frameData = []
  for i in range(0, CFG_PAGE_SIZE) :
    ## header byte + 16 bytes/frame + END_OF_FRAME
    dataIx = 1 + pageNum * (CFG_PAGE_SIZE+1) + i;
    if dataIx < len(raw):
      frameData.append(raw[dataIx])
  return frameData

##---------------------------------------------------------
def main():
  global ofile
  print("====================hello==========================")
  handle = None
  try:
    configFile = None
    try:
      configFile = sys.argv[1]
    except:
      print 'pifxxxx.py <configFile>'
      sys.exit(2)

    if configFile:
      ofile = open('cvt.c', 'w')
      cvt = convert(configFile)
      nc = len(cvt)
      raw = readRaw()
      err = False
      for i in range (0, nc):
        xc = cvt[i]
        xr = rawVec(raw, i)
        ok = (xc == xr)
        if not ok:
          print('!different. frame %d' % i)
          err = True

      i = nc;
      while True:
        xr = rawVec(raw, i)
        if len(xr) < CFG_PAGE_SIZE:
          break
        if xr != [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]:
          err = True
        i = i+1

      if err:
        print('\nERROR - data differences')
      else:
        print('\ndata matches')

  except:
    e = sys.exc_info()[0]
    print("\nException caught %s\n" % e)

  print("\n==================== bye ==========================")

##---------------------------------------------------------
if __name__ == '__main__':
  main()

# EOF -----------------------------------------------------------------
