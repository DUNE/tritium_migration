import ROOT
import math

c1 = ROOT.TCanvas()

# 1. Open the file in read mode
fluka_file = ROOT.TFile.Open("dpipe_4mAu26_clay_2026_hs1.root", "READ")

fstars = fluka_file.Get("usrbin")

out_file = ROOT.TFile("log_fluka1.root", "RECREATE")

#fstars.Draw()

ftuple = ROOT.TNtuple("fluka","fluka stars","x:y:r:tanphi:xp:yp:stars")

for i in range(1,fstars.GetNbinsX() + 1):

    for j in range(1,fstars.GetNbinsY() + 1):

        x = fstars.GetXaxis().GetBinCenter(i)

        y = fstars.GetYaxis().GetBinCenter(j)

        r = math.sqrt(x*x + y*y)

        tanphi = y/x

        xp = 0.707*x+0.707*y

        yp = -0.707*x + 0.707*y
        
        stars = fstars.GetBinContent(i,j)

        if stars > 0:

            stars = math.log(stars)
        
        ftuple.Fill(x, y, r,tanphi,xp,yp,stars)

        print(x, y, stars)
        


ftuple.Draw("stars")        

ftuple.Write()
out_file.Close()
        
