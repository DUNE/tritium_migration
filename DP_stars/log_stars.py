import ROOT
import math
from ROOT import TCut

c1 = ROOT.TCanvas()

# 1. Open the file in read mode

fluka_file = ROOT.TFile.Open("../dpipe_4mAu26_histos/log_fluka8.root", "READ")

fstars = fluka_file.Get("fluka")


#h1 = ROOT.TH2F("h1","Concrete facing top",49,230,720,400,-50,-10)
fstars.Draw("stars:r >> h1")


#concrete facing top
#h1 = ROOT.TH2F("h1","Concrete facing top",49,230,720,400,-50,-10)
#fstars.Draw("stars:r >> h1","tanphi>2.4&&r>230&&y<655")

#concrete facing slant
#h1 = ROOT.TH2F("h1","Concrete facing slant",49,230,720,400,-50,-10)
#h1 = ROOT.TH2F("h1","Decay Pipe",49,230,720,400,-50,-10)
#fstars.Draw("stars:r >> h1","tanphi>0.417&&tanphi<2.4&&r>230&&xp<663")


#concrete facing straight side 
#h1 = ROOT.TH2F("h1","Concrete facing vertical side",55,230,780,500,-60,-10)
#fstars.Draw("stars:r >> h1","tanphi>-0.649&&tanphi<0.432&&r>230&&x<655")

#concrete facing bottom slant
#h1 = ROOT.TH2F("h1","Concrete facing bottom slant",55,230,780,500,-60,-10)
#fstars.Draw("stars:r >> h1","tanphi>-1.58&&tanphi<-0.649&&r>230&&yp>-764")

#concrete facing bottom horizontal
#h1 = ROOT.TH2F("h1","Concrete facing bottom horizontal",55,230,780,500,-60,-10)
#fstars.Draw("stars:r >> h1","tanphi<-1.58&&r>230&&y>-662")







#bottom dirt
#h1 = ROOT.TH2F("h1","bottom dirt",11,-900,-790,400,-50,-10)
#fstars.Draw("stars:y >> h1","y<-790&&y>-900&&x<890")

#h1 = ROOT.TH2F("h1","bottom dirt",11,790,1040,500,-50,-10)
#fstars.Draw("stars:-y >> h1","y<-790&&y>-1040&&x<890")


#bottom
#h1 = ROOT.TH2F("h1","bottom wall",9,-790,-700,400,-50,-10)
#fstars.Draw("stars:y >> h1","y>-790&&y<-700&&x<890")
#h1 = ROOT.TH2F("h1","bottom wall",9,700,790,400,-50,-10)
#fstars.Draw("stars:-y >> h1","y>-790&&y<-700&&x<890")


#h1 = ROOT.TH2F("h1","bottom wall",9,0,890,400,-50,-10)
#fstars.Draw("stars:x >> h1","y>-710&&y<-700&&x<890")



#concrete facing bottom
#h1 = ROOT.TH2F("h1","Concrete facing bottom",32,230,650,400,-50,-10)
#fstars.Draw("stars:r >> h1","tanphi<-0.897&&r>230&&r<655")


#top dirt
#h1 = ROOT.TH2F("h1","top dirt",11,890,1000,400,-50,-10)
#fstars.Draw("stars:y >> h1","y>890&&y<1000&&x<370")


#top
#h1 = ROOT.TH2F("h1","top wall",11,780,890,400,-50,-10)
#fstars.Draw("stars:y >> h1","y>780&&y<890&&x<370")




#slant dirt
#h1 = ROOT.TH2F("h1","dirt out side slanted wall",11,891,1141,500,-50,-10)
#fstars.Draw("stars:xp >> h1","xp>891&&xp<11141&&yp>-322&&yp<322")

#slant
#h1 = ROOT.TH2F("h1","slanted wall",11,781,891,400,-50,-10)
#h1 = ROOT.TH2F("h1","Wall",61,281,891,400,-50,-10)
#fstars.Draw("stars:xp >> h1","xp>781&&xp<891&&yp>-322&&yp<322")





#dirt
#h1 = ROOT.TH2F("h1","Dirt out side Side wall",11,890,1000,400,-50,-10)
#fstars.Draw("stars:x>>h1","stars<0 && x>889 && y>-791 && y < 371")

#side wall
#h1 = ROOT.TH2F("h1","Side wall",11,780,890,400,-50,-10)
#fstars.Draw("stars:x >> h1","stars<0 && x>779 && x<891 && y>-791 && y<371")


#concrete facing wall
#h1 = ROOT.TH2F("h1","Concrete facing side",32,230,650,400,-50,-10)
#fstars.Draw("stars:r>>h1","tanphi>-0.897 && tanphi<0.417  && r>230 && r<655")

#sr = ROOT.gROOT.FindObject("sr")

#h1_pro = h1.ProfileX("h1_pro")

#efun = ROOT.TF1("line","[0] + [1]*x + [2]*x*x + [3]*x*x*x + [4]*x*x*x*x + [5]*x*x*x*x*x",0,1000000)
#efun = ROOT.TF1("line","[0] + [1]*x",0,1000000)

#efun = ROOT.TF1("line","[0]*exp(-0.5*(x-[1])*(x-[1])/[2]) + [3] + [4]*x + [5]*x*x + [6]*x*x*x + [7]*x*x*x*x",0,1000000)

#efun2 = ROOT.TF1("line","[0] + [1]*x +[2]*x*x + [3]*x*x*x + [4]*x*x*x*x",0,1000000)

#efun3 = ROOT.TF1("line","[0] + [1]*x + [2]*exp(-0.5*(x-[3])*(x-[3])/[4])",0,1000000)

#efun4 = ROOT.TF1("line","[0] + [1]*x + [2]*(x-[3])*(x-[3]) +[4]*(x-[3])*(x-[3])*(x-[3])",0,1000000)

#h1_pro.Fit(efun2,"","",230,700)
#h1_pro.Fit(efun,"","",781,891)





#Gauss fit
#efun.SetParameter(0,-7.0)
#efun.SetParameter(1,305)
#efun.SetParameter(2,1000)
#efun.SetParameter(3,-14)
#efun.SetParameter(4,-0.01)
#efun.SetParameter(5,-3e-6)
#efun.SetParameter(6,-5e-8)
#efun.SetParameter(7,6e-11)

#efun2.SetParameter(0,-1.24228)
#efun2.SetParameter(1,-0.113339)
#efun2.SetParameter(2,0.0002565)
#efun2.SetParameter(3,-3.2335e-7)
#efun2.SetParameter(4,1.5307e-10)


#h10 = ROOT.TH1F("h10","decay Pipe",50,230,730)

#h10.FillRandom(efun2, 10000)

#h10.Draw()



#efun4.SetParameter(3,350)

#h1_pro.Fit(efun)

#h1_pro.Fit(efun,"","",370,740)

#h1_pro.Fit(efun,"","",230,780)

#ROOT.gStyle.SetOptFit(1111)
#h1_pro.SetStats(0)
#ROOT.gStyle.SetOptFit(0)

#efun.GetHistogram().GetYaxis().SetRangeUser(-31,-19)


#efun.GetHistogram().GetXaxis().SetRangeUser(230, 900)
#efun.SetRange(230,900)
#efun.SetMinimum(-31)
#efun.SetMaximum(-19)


#h1_pro.Draw()
#efun.Draw("same")




