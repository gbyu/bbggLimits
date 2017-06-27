from ROOT import *
from array import array

#masses = [250, 260, 300, 400, 500, 600, 700, 750, 800, 900]
masses = [ 257, 267, 277, 287, 297, 307, 317, 327, 337, 347, 357, 367, 377, 387, 397, 407, 417, 427, 437, 447, 457, 467, 477, 487, 497, 507, 517, 527, 537, 547, 557, 567, 577, 587, 597, 607, 617, 627, 637, 647, 657, 667, 677, 687, 697, 707, 717, 727, 737, 747, 757, 767, 777, 787, 797, 807, 817, 827, 837, 847, 857, 867, 877, 887, 897, 907, 917, 927, 937, 947, 957, 967, 977, 987, 997 ]

#k/pl = 0.5
#grav_0p5kpl = [1e-8, 5.35e-02, 1.06e+00, 1.81e+00, 9.58e-01, 4.47e-01, 2.21e-01, 1.59e-01, 1.17e-01, 6.36e-02]
grav_0p1kpl_HH_pb = [0.00054498, 0.00384556, 0.00784357, 0.01151152, 0.01500024, 0.01841199, 0.02135109, 0.02378763, 0.02580229, 0.02746830, 0.02834321, 0.02859377, 0.02849578, 0.02813961, 0.02759314, 0.02630053, 0.02474755, 0.02325762, 0.02186012, 0.02056485, 0.01926533, 0.01801182, 0.01684954, 0.01577402, 0.01477365, 0.01372861, 0.01269527, 0.01172508, 0.01082307, 0.00999220, 0.00923788, 0.00855628, 0.00794221, 0.00739112, 0.00689746, 0.00641983, 0.00596454, 0.00554363, 0.00515568, 0.00479900, 0.00447169, 0.00417167, 0.00389669, 0.00364435, 0.00341214, 0.00318992, 0.00298213, 0.00279105, 0.00261535, 0.00245365, 0.00230275, 0.00216262, 0.00203318, 0.00191356, 0.00180287, 0.00169598, 0.00159387, 0.00149797, 0.00140803, 0.00132381, 0.00124506, 0.00117152, 0.00110294, 0.00103904, 0.00097958, 0.00092426, 0.00087284, 0.00082502, 0.00078054, 0.00073911, 0.00070046, 0.00066431, 0.00063036, 0.00059835, 0.00056798 ]
#k/pl = 1.0
grav_0p1kpl = [0.0026*1000*x for x in grav_0p1kpl_HH_pb]
grav_0p5kpl = [25*x for x in grav_0p1kpl]
grav_1p0kpl = [4*x for x in grav_0p5kpl]

gr_grav_0p5kpl = TGraph(len(masses), array('d', masses), array('d', grav_0p5kpl))
gr_grav_1p0kpl = TGraph(len(masses), array('d', masses), array('d', grav_1p0kpl))
grav_0p5kpl_leg = "Bulk Graviton, #kappa/M_{Pl} = 0.5"
grav_1p0kpl_leg = "Bulk Graviton, #kappa/M_{Pl} = 1.0"

#LR = 3 TeV
#rad_3tev = [6.7, 6.62e+00, 6.17e+00, 2.53e+00, 1.30e+00, 7.87e-01, 5.06e-01, 4.11e-01, 3.40e-01, 2.34e-01]
rad_3tev_HH_pb = [2.48572, 2.52729, 2.51165, 2.45392, 2.36613, 2.23782, 2.08558, 1.92620, 1.76649, 1.61136, 1.46420, 1.32717, 1.20148, 1.08766, 0.98571, 0.90395, 0.83468, 0.77309, 0.71845, 0.67007, 0.62728, 0.58946, 0.55599, 0.52630, 0.49982, 0.47283, 0.44684, 0.42302, 0.40116, 0.38108, 0.36261, 0.34557, 0.32983, 0.31523, 0.30164, 0.28807, 0.27495, 0.26260, 0.25097, 0.24000, 0.22965, 0.21988, 0.21064, 0.20189, 0.19359, 0.18557, 0.17791, 0.17067, 0.16381, 0.15733, 0.15125, 0.14553, 0.14011, 0.13498, 0.13010, 0.12532, 0.12066, 0.11619, 0.11188, 0.10775, 0.10377, 0.09996, 0.09630, 0.09278, 0.08941, 0.08618, 0.08309, 0.08012, 0.07729, 0.07457, 0.07198, 0.06949, 0.06712, 0.06485, 0.06268 ]
#LR = 1 TeV
#rad_1tev = [60, 5.96e+01, 5.56e+01, 2.28e+01, 1.17e+01, 7.08e+00, 4.55e+00, 3.70e+00, 3.06e+00, 2.10e+00]
rad_3tev = [0.0026*1000*x for x in rad_3tev_HH_pb]
rad_1tev = [9*x for x in rad_3tev]
rad_1tev_leg = "Bulk Radion, #Lambda_{R} = 1 TeV"
rad_3tev_leg = "Bulk Radion, #Lambda_{R} = 3 TeV"

gr_rad_1tev = TGraph(len(masses), array('d', masses), array('d', rad_1tev))
gr_rad_3tev = TGraph(len(masses), array('d', masses), array('d', rad_3tev))

gr_grav_0p5kpl.SetLineColor(kRed)
gr_grav_0p5kpl.SetLineStyle(2)
gr_grav_0p5kpl.SetLineWidth(3)

gr_grav_1p0kpl.SetLineColor(kRed+3)
gr_grav_1p0kpl.SetLineStyle(2)
gr_grav_1p0kpl.SetLineWidth(3)

gr_rad_3tev.SetLineColor(kRed)
gr_rad_3tev.SetLineStyle(2)
gr_rad_3tev.SetLineWidth(3)

gr_rad_1tev.SetLineColor(kRed+3)
gr_rad_1tev.SetLineStyle(2)
gr_rad_1tev.SetLineWidth(3)