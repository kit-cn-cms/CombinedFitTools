# checks which fits didnt end successfully
# usage: python check.py somefolder/*sh
import sys
import re
import os
import ROOT

scriptnames=sys.argv[1:]

mass='125.1'
nameoption=' \-n'
regexname=r'(?<=\b'+nameoption+'\s)(\w+)'

resubmit=[]
print 'checking',len(scriptnames),'jobs'
for script in scriptnames:
    f = open(script)
    data=f.read()
    f.close()
    name=re.search(regexname,data).group(0)
    path=script.split('/')[:-1]
    rootfilename='higgsCombine'+name+'.MultiDimFit.mH'+mass+'.root'
    rootfilename=('/'.join(path))+'/'+rootfilename
    if not os.path.exists(rootfilename):
        print 'didnt find ',rootfilename
        resubmit.append(script)
    else:
        rootfile=ROOT.TFile(rootfilename)
        t=rootfile.Get('limit')
        if not isinstance(t,ROOT.TTree):
            print 'didnt find limit ROOT Tree in ',rootfilename
            resubmit.append(script)

if len(resubmit)>0:
    print 'please resubmit'
    print ' '.join(resubmit)
else:
    print 'everything is fine'

