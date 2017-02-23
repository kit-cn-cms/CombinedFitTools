# can be used to prepare shell scripts to run coupling fits on cluster

import fitconfig
# script will be stored here
fitconfig.workdir='/afs/desy.de/user/h/hmildner/workdir/'        

# define workspaces here
path='/afs/desy.de/user/h/hmildner/workspaces/'
ws_mc=path+'new_comb_workspace.root'
ws_asi=path+'asimov.root'
ws_data=path+'new_comb_workspace.root'
ws_mc_cpv=path+'new_comb_workspace_cpv.root'
ws_asi_cpv=path+'asimov_cpv.root'
ws_data_cpv=path+'new_comb_workspace_cpv.root'

fitconfig.outname='testfits'
# example:
# run fits of single POI, in given range, with 60 points, freeze kappa_tilde_t, dont freeze remaining POI
fitconfig.run([ws_mc,ws_data,ws_asi],['kappa_t'],[(0.3,1.7)],60,True,False)
fitconfig.run([ws_mc,ws_data,ws_asi],['kappa_W'],[(0.4,1.6)],60,True,False)
fitconfig.run([ws_mc,ws_data,ws_asi],['kappa_Z'],[(0.4,1.6)],60,True,False)
fitconfig.run([ws_mc,ws_data,ws_asi],['kappa_b'],[(0.0,2.3)],60,True,False)
fitconfig.run([ws_mc,ws_data,ws_asi],['kappa_tau'],[(0.3,1.7)],60,True,False)
fitconfig.run([ws_mc_cpv,ws_data_cpv,ws_asi_cpv],['kappa_t','kappa_tilde_t'],[(-1.3,2.2),(-0.1,1.3)],2000,False,False)
