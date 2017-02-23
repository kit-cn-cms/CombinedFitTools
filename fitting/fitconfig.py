# can be used to prepare shell scripts to run coupling fits on cluster
# start with test.py

import os
import stat
from itertools import product
workdir='workdir'
name=None

def createScript(command,folder,scriptname):
    script="#!/bin/bash \n"
    cmsswpath=os.environ['CMSSW_BASE']
    if cmsswpath!='':
        script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
        script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
        script+='cd '+cmsswpath+'/src\neval `scram runtime -sh`\n'
        script+='cd - \n'
    script+='cd '+folder+' \n'
    script+=command+'\n'
    f=open(folder+'/'+scriptname,'w')
    f.write(script)
    f.close()
    st = os.stat(folder+'/'+scriptname)
    os.chmod(folder+'/'+scriptname, st.st_mode | stat.S_IEXEC)

def makeJob(name,folder,number,ws,pois,rngs,npoints,freezePS,freezePOI,real,firstp,lastp,toysfile=None):
    cmd='combine -M MultiDimFit'.split()
    if real:
        cmd+='--minimizerStrategy 1 --minimizerTolerance 0.3 --cminApproxPreFitTolerance=25 --cminFallbackAlgo "Minuit2,migrad,0:0.3" --cminOldRobustMinimize=0 --X-rtd MINIMIZER_MaxCalls=9999999'.split()
    if not real:
        cmd+='-t -1'.split()
        if toysfile!=None:
            cmd+=['--toysFile',toysfile]
    cmd+='--saveInactivePOI 1 -m 125.1'.split()
#    cmd+=['--saveSpecifiedNuis','all']
    cmd+=('--redefineSignalPOIs '+','.join(pois)).split()
    cmd+=('--algo=grid --points='+str(npoints)).split()
    cmd+=['--firstPoint',str(firstp)]
    cmd+=['--lastPoint',str(lastp)]
    cmd+='--setPhysicsModelParameters kappa_W=1,kappa_Z=1,kappa_b=1,kappa_tau=1,kappa_tilde_t=0,zeta_t=1'.split()    
    cmd+=['--setPhysicsModelParameterRanges']
    first=True
    poistr=''
    for poi,rng in zip(pois,list(rngs)):
        if not first:
            poistr+=':'                
        first=False
        poistr+=poi+'='+str(round(rng[0],3))+','+str(round(rng[1],3))

    cmd+=poistr.split()
    suffix=str(number)
    if real:
        suffix+='_data'
    else:
        suffix+='_mc'
    cmd+=['-n',suffix]
#    if freezePS or freezePOI:
    cmd+=['--freezeNuisances']
    nps='kappa_mu'
    if freezePOI:      
        for k in ['kappa_W','kappa_Z','kappa_b','kappa_tau']:
            if k not in pois:
                nps+=k+','
        nps=nps[:-1]
    if freezePS or freezePOI:
        for k in ['kappa_tilde_t','zeta_t']:
            if k not in pois:
                nps+=','+k
    cmd+=[nps]

    cmd+=[ws]
    jobname=name+'_'+str(number)
    if real:
        jobname+='_data'
    else:
        jobname+='_mc'
    jobname+='.sh'
    createScript(' '.join(cmd),folder,jobname)

def run(wss,pois=['kappa_t'],rngs=[(0.0,2.0)],npoints=10,freezePS=True,freezePOI=False,points_per_job=5):

    if not os.path.exists(wss[0]):
        raw_input(wss[0]+' does not exist, ok? or better ctrl+c?')
    if not os.path.exists(wss[1]):
        raw_input(wss[1]+' does not exist, ok? or better ctrl+c?')
    asimov=None
    if len(wss)>2:
        if not os.path.exists(wss[2]):
            raw_input(wss[2]+' does not exist, ok? or better ctrl+c?')
        asimov=wss[2]
    
    if outname==None:
        name=wss[0].split('/')[-2]
    else:
        name=outname
    name+='_'+'_'.join(pois)

    if not freezePS:
        name+='_floatPS'
    if freezePOI:
        name+='_freezePOI'

    njobs=(npoints-1)/points_per_job+1

    folder=workdir+name
    while os.path.exists(folder):
        folder+='_'
    os.makedirs(folder)
    

    for i in range(njobs):
        # mc
        makeJob(name,folder,i,wss[0],pois,rngs,npoints,freezePS,freezePOI,False,i*points_per_job,(i+1)*points_per_job-1,asimov)
        # data
        makeJob(name,folder,i,wss[1],pois,rngs,npoints,freezePS,freezePOI,True,i*points_per_job,(i+1)*points_per_job-1)

