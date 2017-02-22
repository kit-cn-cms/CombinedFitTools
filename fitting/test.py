import fitconfig
fitconfig.workdir='/nfs/dust/cms/user/hmildner/testrecipe/CombinedFitTools/fitting/workdir/'        
path='/nfs/dust/cms/user/hmildner/testrecipe/summer2013/'
ws_mc=path+'new_comb_workspace.root'
ws_asi=path+'asimov.root'
ws_data=path+'new_comb_workspace.root'
ws_mc_cpv=path+'new_comb_workspace_cpv.root'
ws_asi_cpv=path+'asimov_cpv.root'
ws_data_cpv=path+'new_comb_workspace_cpv.root'

fitconfig.outname='testfits'

fitconfig.run([ws_mc,ws_data,ws_asi],['kappa_t'],[(0.3,1.7)],60,True,False)
fitconfig.run([ws_mc,ws_data,ws_asi],['kappa_W'],[(0.4,1.6)],60,True,False)
fitconfig.run([ws_mc,ws_data,ws_asi],['kappa_Z'],[(0.4,1.6)],60,True,False)
fitconfig.run([ws_mc,ws_data,ws_asi],['kappa_b'],[(0.0,2.3)],60,True,False)
fitconfig.run([ws_mc,ws_data,ws_asi],['kappa_tau'],[(0.3,1.7)],60,True,False)
fitconfig.run([ws_mc_cpv,ws_data_cpv,ws_asi_cpv],['kappa_t','kappa_tilde_t'],[(-1.3,2.2),(-0.1,1.3)],2000,False,False)
