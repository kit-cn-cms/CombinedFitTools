#include "/usr/lib64/root/cint/cint/include/typeinfo.h"
void addFlatNuisances2(std::string fi,float mH=-1, std::string snap="", std::string suffix="", TString copyData=""){
  gSystem->Load("libHiggsAnalysisCombinedLimit.so");
  TFile *fin = TFile::Open(fi.c_str());
  TFile *fsnap;  RooWorkspace *wsnap;
  if(snap!="") {
		fsnap= TFile::Open(snap.c_str());
		wsnap = (RooWorkspace*)fsnap->Get("w");
		wsnap -> loadSnapshot("MultiDimFit");
  }
  RooWorkspace *wspace = (RooWorkspace*)fin->Get("w");

  if (mH > 0 && wspace->var("MH")) wspace->var("MH")->setVal(mH);

  RooStats::ModelConfig *mc = (RooStats::ModelConfig*)wspace->genobj("ModelConfig");
  RooArgSet *nuis = (RooArgSet*)mc->GetNuisanceParameters();
  std::cout << "Before...." << std::endl;
  nuis->Print();

  RooArgSet discreteParameters_C = wspace->allCats();
  TIterator *dp = discreteParameters_C.createIterator();
  RooCategory *cat;
  while (cat = (RooCategory*)dp->Next()) {
        if ( (std::string(cat->GetName()).find("pdfindex") != std::string::npos )) {
	  if(snap!="") {
		int snapindex = wsnap->cat(cat->GetName())->getIndex();
		if (cat -> getIndex() != snapindex)
		{ 
			std::cout<<"Prefit "<<cat->GetName()<<" = "<<cat->getIndex()<<"; postfit = "<<snapindex<<std::endl;
			cat->setIndex(snapindex);
		}
	  }
	  cat->setConstant();
	  std::cout << "Set " << cat->GetName() << " to constant " << std::endl;
	}
  }
  
  RooRealVar *mgg = (RooRealVar*)wspace->var("CMS_hgg_mass");
  // Get all of the "flat" nuisances to be added to the nusiances:
  RooArgSet pdfs = (RooArgSet)wspace->allPdfs();
  RooAbsReal *pdf;
  TIterator *it_pdf = pdfs.createIterator();
  
  while (pdf=(RooAbsReal*)it_pdf->Next() ){
        if (pdf->IsA()->InheritsFrom(RooMultiPdf::Class()) ){
	  pdf->Print();
          pdf->setAttribute("NOCacheAndTrack");
	  RooMultiPdf *pdf_c = dynamic_cast<RooMultiPdf*>(pdf);
	  RooArgSet* pdfpars = (RooArgSet*)pdf_c->getCurrentPdf()->getParameters(RooArgSet(*mgg));
	  RooRealVar *vnorm = (RooRealVar*)wspace->var((std::string(pdf_c->GetName())+std::string("__norm")).c_str());
	  std::string newname = (std::string("u_CMS_Hgg_")+std::string(vnorm->GetName()));
	  //wspace->import(*vnorm,RooFit::RenameVariable(vnorm->GetName(),newname.c_str()));
	  vnorm->SetName(newname.c_str());
	  vnorm->setRange(0,3*vnorm->getVal()+10*vnorm->getError());
          vnorm->setAttribute("statUnc");
	  nuis->add(*vnorm);
	  TIterator *itpar = pdfpars->createIterator(); 
	  RooRealVar *vv;
	  while(vv = (RooRealVar*)itpar->Next()){
	    std::string newname_v = (std::string("u_CMS_Hgg_")+std::string(vv->GetName()));
	    //wspace->import(*vv,RooFit::RenameVariable(vv->GetName(),newname_v.c_str()));
	    vv->SetName(newname_v.c_str());
            vv->setAttribute("statUnc");
	    nuis->add(*vv);
	  }
	}
  }
  RooArgSet allvars = wspace->allVars();
  TIterator *itpar = allvars.createIterator(); 
  RooRealVar *vv;
  while(vv = (RooRealVar*)itpar->Next()){

	if ((std::string(vv->GetName()).find("u_CMS_Hgg_") != std::string::npos )) continue;
        if ((std::string(vv->GetName()).find("env_") != std::string::npos )) {
	   vv->setConstant();
	   std::cout << "Set " << vv->GetName() << " to constant " << std::endl;
	}
  } 


  std::cout << "After..." << std::endl;
  nuis->Print();
  mc->SetNuisanceParameters(*nuis);
 
  if(copyData!=""){
    TFile *fInDN = new TFile("higgsCombinecms_all_prefit_asimov.GenerateOnly.mH125.09.123456.root");
    wspace->import(*(RooDataSet*)(fInDN->Get("toys/toy_asimov")), RooFit::Rename("asimovData_prefit"));
    fInDN->Close();
  }

  TFile *finew = new TFile((std::string(TString(fin->GetName()).ReplaceAll(".root",suffix+".root"))+std::string("_unconst.root")).c_str(),"RECREATE");
  finew->WriteTObject(wspace);
  finew->Close();
}
