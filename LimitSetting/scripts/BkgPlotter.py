from ROOT import *
from math import sqrt

def MakeBkgPlot(data, pdf, var, label, lumi, cat, analysis, doBands, fname, binning):

	gROOT.SetBatch(kTRUE)

#	pdf.fitTo(data)

	frame = var.frame(RooFit.Title(" "),RooFit.Bins(binning))

	data.plotOn(frame,RooFit.DataError(RooAbsData.SumW2),RooFit.XErrorSize(0))

	pdf.plotOn(frame,RooFit.LineColor(kRed+1),RooFit.Precision(1E-10))

	curve = frame.getObject( int(frame.numItems()-1) )
	datah = frame.getObject( int(frame.numItems()-2) )
	datah.SetLineWidth(1)
#	datah.SetMarkerStyle(20)

#	sigmas = MakeBands(data, pdf, var, frame, curve)
#	sigmas[0].SetFillColor(kBlue-5)
#	sigmas[1].SetFillColor(kCyan)

	Max = frame.GetMaximum()
	c = TCanvas("c", "c", 800, 600)
#	c.SetLogy()
	frame.Draw()
	xmax = frame.GetXaxis().GetXmax()
	xmin = frame.GetXaxis().GetXmin()

	deltabin = (xmax - xmin)/binning
	sigmas = MakeBands(data, pdf, var, frame, curve, xmin, xmax, deltabin)
	print xmax, xmin
	sigmas[0].SetFillColor(kAzure-4)
	sigmas[0].SetLineColor(kAzure-4)
	sigmas[1].SetFillColor(kCyan)
	sigmas[1].SetLineColor(kCyan)

	sigmas[1].Draw("AE3")
	sigmas[1].SetMaximum(Max*1.75)
	sigmas[1].SetMinimum(0.00001)
	sigmas[1].GetXaxis().SetTitle(label)
	sigmas[1].GetXaxis().SetTitleSize(0.045)
	sigmas[1].GetYaxis().SetTitleSize(0.045)
	sigmas[1].GetXaxis().SetRangeUser(xmin*1.0001, xmax*0.9999)
	sigmas[1].GetYaxis().SetTitle("Events/("+str(int(deltabin))+" GeV)")
	if deltabin < 1:
		sigmas[1].GetYaxis().SetTitle("Events/("+"%.01f"%deltabin+" GeV)")

	c.Update()
	sigmas[0].Draw("E3same")
	frame.Draw("same")
	
	datah.Draw("EPsame")

	tlatex = TLatex()
	tlatex.SetNDC()
	tlatex.SetTextAngle(0)
	tlatex.SetTextColor(kBlack)
	tlatex.SetTextFont(63)
	tlatex.SetTextAlign(11)
	tlatex.SetTextSize(25)
	tlatex.DrawLatex(0.11, 0.91, "CMS")
	tlatex.SetTextFont(53)
	tlatex.DrawLatex(0.18, 0.91, "Preliminary")
	tlatex.SetTextFont(43)
	tlatex.SetTextSize(20)
	tlatex.DrawLatex(0.68, 0.91, "L = " + str(lumi) + " fb^{-1} (13 TeV)")
	tlatex.SetTextSize(25)
	Cat = "High Purity Category"
	if int(cat) == 1:
		Cat = "Medium Purity Category"
	if int(cat) == -1:
		Cat = "High Mass (Single Cat.)"
	print cat, Cat
	if "|" in analysis:
		an = analysis.split("|")
#		tlatex.SetTextFont(63)
		tlatex.DrawLatex(0.14, 0.85, an[0])
#		tlatex.SetTextFont(43)
		tlatex.DrawLatex(0.14, 0.79, an[1])	
		tlatex.DrawLatex(0.14, 0.73, Cat)
	else:
#		tlatex.SetTextFont(63)
		tlatex.DrawLatex(0.14, 0.85, analysis)
#		tlatex.SetTextFont(43)
		tlatex.DrawLatex(0.14, 0.79, Cat)

	leg = TLegend(0.50, 0.60, 0.89, 0.9)

	leg.SetFillStyle(0)
	leg.SetLineWidth(0)
	leg.SetBorderSize(0)

	nBkgParams = pdf.getParameters(data).getSize()
	print "Number of background parameters:", nBkgParams

	bkgModel = "#splitline{Background model}{"
	if nBkgParams == 2:
		bkgModel += "(1st Order Bernstein Pol.)}"
	if nBkgParams == 3:
		bkgModel += "(2nd Order Bernstein Pol.)}"
	
	leg.AddEntry(datah, "Data", "pe")
	leg.AddEntry(curve, bkgModel, "l")
	leg.AddEntry(sigmas[0], "Fit #pm 1#sigma", "f")
	leg.AddEntry(sigmas[1], "Fit #pm 2#sigma", "f")
	leg.Draw()

	c.SaveAs(fname+".pdf")
	c.SaveAs(fname+".png")

def MakeBands(data, pdf, var, frame, curve, xmin, xmax, deltabin):

	onesigma = TGraphAsymmErrors()
	twosigma = TGraphAsymmErrors()

	bins = []
	bins.append([xmin*1.001, xmin, xmin+deltabin])
	for ibin in range(1,frame.GetXaxis().GetNbins()+1):
		lowedge = frame.GetXaxis().GetBinLowEdge(ibin)
		upedge  = frame.GetXaxis().GetBinUpEdge(ibin)
		center  = frame.GetXaxis().GetBinCenter(ibin)
		bins.append(  (center,lowedge,upedge) )
	bins.append([xmax*0.999, xmax-deltabin, xmax])


	allbins = []
	for ibin,bin in enumerate(bins):
		center,lowedge,upedge = bin

		nombkg = curve.interpolate(center)
		largeNum = nombkg*50#(1 + sqrt(nombkg)*2)
#		if nombkg < 1:
#			largeNum = 9999999999999999999999999999999999
		largeNum = max(1,largeNum)

		nlim = RooRealVar("nlim%s" % var.GetName(),"",0.,-largeNum,largeNum)
#		nlim.removeRange()

		onesigma.SetPoint(ibin,center,nombkg)
		twosigma.SetPoint(ibin,center,nombkg)

		nlim.setVal(nombkg)

		if 1:
			print "computing error band ", ibin, lowedge, upedge, nombkg, 

		var.setRange("errRange",lowedge,upedge)
		errm = 0
		errp = 0
		counter = 0
#		while errm == 0 or errp == 0:
		errmSum = 0
		countermSum = 0
		errpSum = 0
		counterpSum = 0
		epdf = RooExtendPdf("epdf","",pdf,nlim, "errRange")
		nll = epdf.createNLL(data,RooFit.Extended())
		minim = RooMinimizer(nll)
		for ct in range(0, 500):
#			epdf = RooExtendPdf("epdf","",pdf,nlim, "errRange")
#			nll = epdf.createNLL(data,RooFit.Extended())
	#		nll = pdf.createNLL(data)
			minim = RooMinimizer(nll)
			minim.setMinimizerType("Minuit2")
			minim.setStrategy(0)
			minim.setPrintLevel( -1 )#if not options.verbose else 2)
			minim.migrad()
#			minim.hesse()
#			minim.migrad()
#			minim.minos()
			minim.setStrategy(0)
			minim.minos(RooArgSet(nlim))

			errm, errp = -nlim.getErrorLo(),nlim.getErrorHi()
#			if errm !=0 and errp !=0: break

			if abs(errm) > nombkg*0.01:
				errmSum += -nlim.getErrorLo()
				countermSum+=1
#				if len(countermSum) < 3: countermSum.append(-nlim.getErrorLo())
			if abs(errp) > nombkg*0.01:
				errpSum += nlim.getErrorHi()
				counterpSum+=1
#				if len(counterpSum) < 3: counterpSum.append(nlim.getErrorHi())
#			del minim
#			del nll
#			del epdf
			if counterpSum > 10 and countermSum > 10: break

#			if len(counterpSum) > 2 and len(countermSum) > 2: break
#			counter +=1
#			if counter > 10: break



		errm = errmSum/float(countermSum)
		errp = errpSum/float(counterpSum)

#		if len(countermSum) == 3:
#			errm = sorted(countermSum)[1]
#		else:
#			errm = 0
#		if len(counterpSum) == 3:
#			errp = sorted(counterpSum)[1]
#		else:
#			errp = 0

		onesigma.SetPointError(ibin,center-lowedge,upedge-center,errm,errp)

		errm = 0
		errp = 0
		counter = 0
		errmSum = 0
		countermSum = []
		errpSum = 0
		counterpSum = []
#		while errm == 0 or errp == 0:
		for ct in range(0,2000):
#			epdf = RooExtendPdf("epdf","",pdf,nlim, "errRange")
#			nll = epdf.createNLL(data,RooFit.Extended())
	#		nll = pdf.createNLL(data)
#			minim = RooMinimizer(nll)
			minim.setMinimizerType("Minuit2")
#			minim.setStrategy(2)
			minim.setPrintLevel( -1 )#if not options.verbose else 2)
			minim.setErrorLevel(2.)
			minim.migrad()
			minim.minos(RooArgSet(nlim))

			errm, errp = -nlim.getErrorLo(),nlim.getErrorHi()
#			if errm != 0 and errp !=0: break

			if abs(errm) > nombkg*0.01:
				errmSum += -nlim.getErrorLo()
				if len(countermSum) < 3: countermSum.append(-nlim.getErrorLo())
			if abs(errp) > nombkg*0.01:
				errpSum += nlim.getErrorHi()
				if len(counterpSum) < 3: counterpSum.append(nlim.getErrorHi())

#			del epdf
#			del nll
#			del minim

			print len(counterpSum)
			if len(counterpSum) > 2 and len(countermSum) > 2: break
#			counter += 1
#			if counter > 10: break

#		errm = errmSum/float(countermSum)
#		errp = errpSum/float(counterpSum)
		errm = sorted(countermSum)[1]
		errp = sorted(counterpSum)[1]
		allbins.append([errm,errp,nombkg])
		twosigma.SetPointError(ibin,center-lowedge,upedge-center,errm,errp)
		
#		del minim
#		del nll

	print allbins
	return [onesigma,twosigma]
