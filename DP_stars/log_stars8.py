import ROOT
import math
from ROOT import TCut

c1 = ROOT.TCanvas()

# 1. Open the file in read mode

fluka_file = ROOT.TFile.Open("../dpipe_4mAu26_histos/log_fluka8.root", "READ")

fstars = fluka_file.Get("fluka")



#concrete facing top
#h1 = ROOT.TH2F("h1","Concrete facing top",49,230,720,400,-50,-10)
#fstars.Draw("stars:r >> h1","tanphi>2.34&&r>230&&y<625")

#concrete facing slant
#h1 = ROOT.TH2F("h1","Concrete facing slant",49,230,720,400,-50,-10)
#fstars.Draw("stars:r >> h1","tanphi>0.428&&tanphi<2.34&&r>230&&xp<631")


#concrete facing straight side 
#h1 = ROOT.TH2F("h1","Concrete facing vertical side",55,230,780,500,-60,-10)
#fstars.Draw("stars:r >> h1","tanphi>-0.649&&tanphi<0.428&&r>230&&x<625")

#concrete facing bottom slant
#h1 = ROOT.TH2F("h1","Concrete facing bottom slant",55,230,780,500,-60,-10)
#fstars.Draw("stars:r >> h1","tanphi>-1.54&&tanphi<-0.650&&r>230&&yp>-728")

#concrete facing bottom horizontal
h1 = ROOT.TH2F("h1","Concrete facing bottom horizontal",55,230,780,500,-60,-10)
fstars.Draw("stars:r >> h1","tanphi<-1.54&&r>230&&y>-625")




h1_pro = h1.ProfileX("h1_pro")


efun2 = ROOT.TF1("line","[0] + [1]*x +[2]*x*x + [3]*x*x*x + [4]*x*x*x*x",0,1000000)

h1_pro.Fit(efun2,"","",230,730)

#h1_pro.Fit(efun,"","",781,891)


efun = ROOT.TF1("line","[0]*exp(-0.5*(x-[1])*(x-[1])/[2]) + [3] + [4]*x + [5]*x*x + [6]*x*x*x + [7]*x*x*x*x",0,1000000)




#Gauss fit
efun.SetParameter(0,-7.0)
efun.SetParameter(1,305)
efun.SetParameter(2,1000)
efun.SetParameter(3,-14)
efun.SetParameter(4,-0.01)
efun.SetParameter(5,-3e-6)
efun.SetParameter(6,-5e-8)
efun.SetParameter(7,6e-11)


#h1_pro.Fit(efun,"","",370,740)

#h1_pro.Fit(efun,"","",230,740)

ROOT.gStyle.SetOptFit(1111)
h1_pro.SetStats(0)
ROOT.gStyle.SetOptFit(0)

#efun.GetHistogram().GetYaxis().SetRangeUser(-31,-19)


#efun.GetHistogram().GetXaxis().SetRangeUser(230, 900)
#efun.SetRange(230,900)
#efun.SetMinimum(-31)
#efun.SetMaximum(-19)


h1_pro.Draw()





