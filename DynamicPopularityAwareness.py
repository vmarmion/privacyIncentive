from __future__ import division
from decimal import *
import math
import sys
import scipy
import matplotlib.pyplot as plt

"""
Simulations with a strategy game.

popularity commences with dominant market share of Cvast

"""
N = 10000
NUMRUNS = 3000

NONE = 0
EXPLOIT = 1
RESPECT = 2
UNDEFINED = 3
Strategy_Options = ["None", "Exploit", "Respect", "Undefined"]

Clight = 0
Cvast = 1

Clight_HH = 0
Cvast_HH = 1
Clight_HL = 2
Cvast_HL = 3
Clight_LH = 4
Cvast_LH = 5
Clight_LL = 6
Cvast_LL = 7

QUAD_ONE = 0
QUAD_TWO = 1
QUAD_THREE = 2
QUAD_FOUR = 3

QUADS = ["Respect - Respect", "Respect - Exploit", "Exploit - Respect", "Exploit - Exploit"]

def print_parameters(parameters):
	
	print "------------PARAMETERS--------------------"
	print "POPULATION\t\t", N
	print "AWARENESS\t\t" , parameters[0]
	print "NAIVENESS\t\t" , parameters[1]
	print "POPULARITY_CVAST\t", parameters[2]
	print "POPULARITY_CLIGHT\t", parameters[3]
	print "OPT_OUT\t\t\t", parameters[4]
	print "-------------------------------------------"
	
def calcResults(parameters):
	#Calculates each revenue senario 
	AWARENESS = parameters[0]
	NAIVENESS = parameters[1]
	POPULARITY_CVAST = parameters[2]
	POPULARITY_CLIGHT = parameters[3]
	OPT_OUT = parameters[4]
	POP = N - (OPT_OUT * N)
	Aware_pop = int(AWARENESS* N)
	Naive_pop = N - Aware_pop
	print Aware_pop, Naive_pop, "-----"
	Clight_HH_rev = math.pow((POPULARITY_CLIGHT * POP), (0.1 * math.e))
	Cvast_HH_rev = math.pow((POPULARITY_CVAST * POP), (0.1 * math.e)) 
	
	Clight_HL_rev = math.pow(((POPULARITY_CLIGHT * Naive_pop) + Aware_pop), (0.1 * math.e))
	Cvast_HL_rev = math.pow((POPULARITY_CVAST * Naive_pop), (0.13 * math.e))
	
	Clight_LH_rev = math.pow((POPULARITY_CLIGHT * Naive_pop), (0.13 * math.e))
	Cvast_LH_rev = math.pow(((POPULARITY_CVAST * Naive_pop)+ Aware_pop), (0.1 * math.e)) 
	
	Clight_LL_rev = math.pow((POPULARITY_CLIGHT * POP), (0.13 * math.e))
	Cvast_LL_rev = math.pow((POPULARITY_CVAST * POP), (0.13 * math.e))

	results = [Clight_HH_rev, Cvast_HH_rev, Clight_HL_rev, Cvast_HL_rev, Clight_LH_rev, Cvast_LH_rev,  Clight_LL_rev, Cvast_LL_rev]
	
	return results

def printResults(result):
	print "--------------------------------------------"
	print""
	print "           Cvast Strategy"
	print "       Respect   ||   Exploit     Clight Strategy"
	print "|",result[Clight_HH],",",result[Cvast_HH], " ||", result[Clight_HL],",",result[Cvast_HL],"|", "    Respect"
	print "|",result[Clight_LH],",",result[Cvast_LH], " ||", result[Clight_LL],",",result[Cvast_LL],"|", "    Exploit"
	print ""
	print "-----------------------------------------------------"

def calcDomStrategy(result):
	Cvast_DS = Clight_DS = NONE 
	#if Cvast goes RESPECT, Clight should go RESPECT and if 
	#Cvast goes Exploit Clight should still go RESPECT
	if ((result[Clight_HH] > result[Clight_LH]) and (result[Clight_HL] > result[Clight_LL])):
		Clight_DS = RESPECT
	elif ((result[Clight_HH] < result[Clight_LH]) and (result[Clight_HL] < result[Clight_LL])):
		Clight_DS = EXPLOIT

	if ((result[Cvast_HH] > result[Cvast_HL]) and (result[Cvast_LH] > result[Cvast_LL])):
		Cvast_DS = RESPECT 
	elif ((result[Cvast_HH] < result[Cvast_HL]) and (result[Cvast_LH] < result[Cvast_LL])):
		Cvast_DS = EXPLOIT
	
	print "Dominant Strategies:\t\t",Strategy_Options[Clight_DS], "|", Strategy_Options[Cvast_DS]
	
	return Clight_DS, Cvast_DS
	
def calc_strategies(result, DS):
	
	Clight_DS, Cvast_DS = DS
	
	Clight_strategy = Clight_DS
	Cvast_strategy = Cvast_DS

	if Clight_DS == NONE:
		if Cvast_DS == RESPECT:
			if result[Clight_HH] >= result[Clight_LH]:
				Clight_strategy = RESPECT
			else:
				Clight_strategy = EXPLOIT
		elif Cvast_DS == EXPLOIT:
			if result[Clight_HL] >= result[Clight_LL]:
				Clight_strategy = RESPECT
			else:
				Clight_strategy = EXPLOIT
		elif Cvast_DS == NONE:
			Clight_strategy = UNDEFINED

	if Cvast_DS == NONE:
		if Clight_DS == RESPECT:
			if result[Cvast_HH] > result[Cvast_HL]:
				Cvast_strategy = RESPECT
			else:
				Cvast_strategy = EXPLOIT
		elif Clight_DS == EXPLOIT:
			if result[Cvast_LH] >= result[Cvast_LL]:
				Cvast_strategy = RESPECT
			else:
				Cvast_strategy = EXPLOIT
		elif Clight_DS == NONE:
			Cvast_strategy = UNDEFINED

	print "Choosen Strategies:\t\t\t", Strategy_Options[Clight_strategy],"|", Strategy_Options[Cvast_strategy]

	return Clight_strategy, Cvast_strategy

def undefined_Strategies(result, player, lastOpponentStrategy):
	
	if player == Clight:
		if lastOpponentStrategy == RESPECT:
			a = result[Clight_HH]
			b = result[Clight_LH]
			if a > b:
				return RESPECT
			else:
				return EXPLOIT

		elif lastOpponentStrategy == EXPLOIT:
			a = result[Clight_HL]
			b = result[Clight_LL]
			if a > b:
				return RESPECT
			else:
				return EXPLOIT

	if player == Cvast:
		if lastOpponentStrategy == RESPECT:
			a = result[Cvast_HH]
			b = result[Cvast_HL]
			if a > b:
				return RESPECT
			else:
				return EXPLOIT

		elif lastOpponentStrategy == EXPLOIT:
			a = result[Cvast_LH]
			b = result[Cvast_LL]
			if a > b:
				return RESPECT
			else:
				return EXPLOIT
	return 0
"""
	if player == Clight:
		#if could have made more mney last time do that instead
		#eliminate lowest possible return
		a = result[Clight_HH]
		b = result[Clight_HL]
		c = result[Clight_LH]
		d = result[Clight_LL]

		P = (a+b)/2.0
		NP = (c+d)/2.0
		if P >= NP:
			return RESPECT
		else:
			return EXPLOIT
		

	elif player == Cvast:
	
		#eliminate lowest possible return
		a = result[Cvast_HH]
		b = result[Cvast_HL]
		c = result[Cvast_LH]
		d = result[Cvast_LL]
		
		P = (a+c)/2.0
		NP = (b+d)/2.0
		if P >= NP:
			return RESPECT
		else:
			return EXPLOIT
		"""
	

def calc_revenue(result, strategies, parameters):
	AWARENESS = parameters[0]
	NAIVENESS = parameters[1]
	POPULARITY_CVAST = parameters[2]
	POPULARITY_CLIGHT = parameters[3]
	Clight_revenue = Cvast_revenue = 0
	if strategies[Clight] and strategies[Cvast] == RESPECT:
	
		Clight_revenue = result[Clight_HH]
		Cvast_revenue = result[Cvast_HH]
	
	elif ((strategies[Clight] == EXPLOIT) and (strategies[Cvast] == EXPLOIT)):
	
		Clight_revenue = result[Clight_LL]
		Cvast_revenue = result[Cvast_LL]

	elif ((strategies[Clight] == RESPECT) and (strategies[Cvast] == EXPLOIT)):
		
		Clight_revenue = result[Clight_HL]
		Cvast_revenue = result[Cvast_HL]
		

	elif ((strategies[Clight] == EXPLOIT) and (strategies[Cvast] == RESPECT)):
		Clight_revenue = result[Clight_LH]
		Cvast_revenue = result[Cvast_LH]
		

	
	print "Revenues:\t\t\t", Clight_revenue, "\t|",Cvast_revenue 
	
	return Clight_revenue, Cvast_revenue

def calc_popularity(strategies, parameters):
	AWARENESS = parameters[0]
	NAIVENESS = parameters[1]
	POPULARITY_CVAST = parameters[2]
	POPULARITY_CLIGHT = parameters[3]
	
	if ((strategies[Clight] == RESPECT) and (strategies[Cvast] == RESPECT)):
		if POPULARITY_CVAST > POPULARITY_CLIGHT:
			POPULARITY_CVAST  += (POPULARITY_CVAST * 0.01)
		else:
			POPULARITY_CVAST  -= (POPULARITY_CVAST * 0.01)
		return POPULARITY_CVAST
	elif ((strategies[Clight] == EXPLOIT) and (strategies[Cvast] == EXPLOIT)):
		return POPULARITY_CVAST
	elif ((strategies[Clight] == RESPECT) and (strategies[Cvast] == EXPLOIT)):
		POPULARITY_CVAST  -= (POPULARITY_CVAST * 0.01)
	elif ((strategies[Clight] == EXPLOIT) and (strategies[Cvast] == RESPECT)):
		POPULARITY_CVAST  += (POPULARITY_CVAST * 0.01)
	return POPULARITY_CVAST


def calc_awareness(strategies, parameters):
	AWARENESS = parameters[0]
	NAIVENESS = parameters[1]
	POPULARITY_CVAST = parameters[2]
	POPULARITY_CLIGHT = parameters[3]
	
	if ((strategies[Clight] == RESPECT) and (strategies[Cvast] == RESPECT)):
		if AWARENESS > 0.02:
			AWARENESS -= 0.02
			print "one"
	
	elif ((strategies[Clight] == EXPLOIT) and (strategies[Cvast] == EXPLOIT)):
		if AWARENESS < 0.99:
			AWARENESS += 0.01
			print "two"
	return AWARENESS
"""
	elif ((strategies[Clight] == RESPECT) and (strategies[Cvast] == EXPLOIT)):
		if POPULARITY_CVAST > POPULARITY_CLIGHT:
			if AWARENESS < 0.99:

				AWARENESS += 0.01
				print "three"

		else:
			if AWARENESS > 0.02:
				AWARENESS -= 0.02
				print "four"

	elif ((strategies[Clight] == EXPLOIT) and (strategies[Cvast] == RESPECT)):
		if POPULARITY_CVAST > POPULARITY_CLIGHT:
			if AWARENESS > 0.02:

				AWARENESS -= 0.02
				print "five"
		else:
			if AWARENESS < 0.99:
				AWARENESS += 0.01
				print "six"""
	

def calc_opt_out(strategies, parameters):
	AWARENESS = parameters[0]
	NAIVENESS = parameters[1]
	POPULARITY_CVAST = parameters[2]
	POPULARITY_CLIGHT = parameters[3]
	OPT_OUT = parameters[4]
	
	if ((strategies[Clight] == EXPLOIT) and (strategies[Cvast] == EXPLOIT)):
		if OPT_OUT < 0.999:
			OPT_OUT += 0.001
			print "***&&&***"
	
	elif ((strategies[Clight] == RESPECT) and (strategies[Cvast] == RESPECT)):
		if OPT_OUT > 0.001:
			OPT_OUT -= 0.001
			print "******"

	
	return OPT_OUT

def find_NE(result):
	NEs = [0,0,0,0]
	
	if result[Clight_HH] > result[Clight_LH] and result[Cvast_HH] > result[Cvast_HL]:
		NEs[QUAD_ONE] = 1 
	
	if result[Clight_HL] > result[Clight_LL] and result[Cvast_HL] > result[Cvast_HH]:
		NEs[QUAD_TWO] = 1
	
	if result[Clight_LH] > result[Clight_HH] and result[Cvast_LH] > result[Cvast_LL]:
		NEs[QUAD_THREE] = 1
	
	if result[Clight_LL] > result[Clight_HL] and result[Cvast_LL] > result[Cvast_LH]:
		NEs[QUAD_FOUR] = 1
	
	print "Nash Equilibirum Matrix:\t", NEs
	for x in xrange(4):
		if NEs[x] == 1:
			print "Nash Equilibirum at:\t\t",QUADS[x]
	
	return NEs

def play(outfile, parameters):
	
	AWARENESS = parameters[0]
	NAIVENESS = parameters[1]
	POPULARITY_CVAST = parameters[2]
	POPULARITY_CLIGHT = parameters[3]
	OPT_OUT = parameters[4]
	LASTSTRATEGY_CVAST = parameters[5]
	LASTSTRATEGY_CLIGHT = parameters[6]
	#GR
	gameResults = calcResults(parameters)
	printResults(gameResults)
	print_parameters(parameters)

	#DS
	dominantStrategies = calcDomStrategy(gameResults)

	#Strategies
	Clight_strategy, Cvast_strategy = calc_strategies(gameResults, dominantStrategies)

	if Clight_strategy == UNDEFINED:
		Clight_strategy =  undefined_Strategies(gameResults, Clight, LASTSTRATEGY_CVAST)
		#Clight_strategy = LASTSTRATEGY_CLIGHT
		print "Avoiding Low:\t\t\t", Strategy_Options[Clight_strategy]
	if Cvast_strategy == UNDEFINED:
		Cvast_strategy = undefined_Strategies(gameResults, Cvast, LASTSTRATEGY_CLIGHT)
		#Cvast_strategy = LASTSTRATEGY_CVAST
		print "Avoiding Low:\t\t\t",Strategy_Options[Cvast_strategy]

	strategies = Clight_strategy, Cvast_strategy 

	LASTSTRATEGY_CVAST, LASTSTRATEGY_CLIGHT = strategies
	#Rev
	revenues = calc_revenue(gameResults, strategies, parameters)
	AWARENESS = calc_awareness(strategies, parameters)
	OPT_OUT = calc_opt_out(strategies, parameters)

	NAIVENESS = 1.0 - AWARENESS
	POPULARITY_CVAST = calc_popularity(strategies, parameters)
	POPULARITY_CLIGHT = 1.0 - POPULARITY_CVAST
	
	#NE
	NE = find_NE(gameResults)
	
	for x in xrange(len(gameResults)):
		num =  int(gameResults[x])
		outfile.write("%03d\t" % num)
	
	outfile.write("--DS8\t")
	outfile.write("%02d\t %02.2d\t " % (dominantStrategies[0], dominantStrategies[1]))

	outfile.write("--Ss11\t")
	outfile.write("%02d\t %02d\t " % (strategies[0], strategies[1]))

	outfile.write("--Rv14\t")
	outfile.write("%02d\t %02d\t " % (revenues[0], revenues[1]))

	outfile.write("--POPS17\t")
	outfile.write("%02.2f\t %02.2f\t " % ( POPULARITY_CVAST, POPULARITY_CLIGHT))
	
	outfile.write("--M&N20\t")
	outfile.write("%02f\t %.2f\t %.2f\t %.2f\t " % (AWARENESS, NAIVENESS, OPT_OUT, N))
	outfile.write("--NE?\t")
	
	for x in xrange(len(NE)):
		num = NE[x]
		outfile.write("%01d\t" % num)

	
	outfile.write("\n")

	
	return POPULARITY_CVAST, AWARENESS, OPT_OUT, LASTSTRATEGY_CVAST, LASTSTRATEGY_CLIGHT

def analysis():
	ClightREV_HH = []
	ClightREV_HL = []
	ClightREV_LH = []
	ClightREV_LL = []
	CvastREV_HH = []
	CvastREV_HL = []
	CvastREV_LH = []
	CvastREV_LL = []
	CL_DS = []
	CV_DS = []
	CL_str = []
	CV_str = []
	CL_rev = []
	CV_rev = []
	CV_pop = []
	CL_pop = []
	aware = []
	opt_out = []
	f=open("GameTwoResults.txt", "r")
	resultsFile = []
	numbers = []
	for line in f:
		
		if line != "\n":
			numbers = line.split()
			resultsFile.append(numbers)#appends each line as a list of strings  
    
	for r in resultsFile:
		ClightREV_HH.append(int(r[Clight_HH]))
		ClightREV_HL.append(int(r[Clight_HL]))
		ClightREV_LH.append(int(r[Clight_LH]))
		ClightREV_LL.append(int(r[Clight_LL]))
		
		CvastREV_HH.append(int(r[Cvast_HH]))
		CvastREV_HL.append(int(r[Cvast_HL]))
		CvastREV_LH.append(int(r[Cvast_LH]))
		CvastREV_LL.append(int(r[Cvast_LL]))

		CL_DS.append(int(r[9]))
		CV_DS.append(int(r[10]))
		CL_str.append(int(r[12]))
		CV_str.append(int(r[13]))
		CL_rev.append(int(r[15]))
		CV_rev.append(int(r[16]))
		CV_pop.append(r[18])
		CL_pop.append(r[19])
		aware.append(r[21])
		opt_out.append(r[23])
	


	fig2 = plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
	fig2.suptitle("Player Strategies and Revenue per AWARENESS in Population\n Popularity 80/20 split")
	
	plt.subplot(411)
	plt.plot(CL_rev, "r.", label="CLIGHT")
	plt.plot(CV_rev, "b.", label="CVAST ")
	plt.ylabel("Potential\n Revenues\n\n")
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.subplot(412)
	plt.plot(CL_str, "r.", label="CLIGHT")
	plt.plot(CV_str, "b-", label="CVAST")
	plt.ylabel("Chosen \nStrategies\n")
	plt.axis([0,NUMRUNS,-1,3])
	plt.yticks([0 ,1,2], Strategy_Options)

	plt.subplot(413)
	plt.plot(CL_DS, "r.", label="CLIGHT")
	plt.plot(CV_DS,"b--", label="CVAST")
	plt.ylabel("Dominant \nStrategies\n")
	plt.axis([0,NUMRUNS,-1,3])
	plt.yticks([0, 1, 2], Strategy_Options)
	


	plt.subplot(414)
	plt.plot(CL_pop, "b.", label = "CLight Pop")
	plt.plot(aware, "r.", label="AWARENESS")
	plt.plot(opt_out, "g.", label = "opt_out")
	plt.axis([0,NUMRUNS,0,1])
	plt.ylabel("AWARENESS\n")
	plt.xlabel("Run (time)")

	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.savefig("gameTwoResults.pdf")
	plt.show()

def runs():
	outfile = open("GameTwoResults.txt", "w")
	
	LASTSTRATEGY_CVAST = NONE
	LASTSTRATEGY_CLIGHT = NONE 
	POPULARITY_CVAST = 0.80
	POPULARITY_CLIGHT = 1.0 - POPULARITY_CVAST
	AWARENESS = 0.0
	NAIVENESS = 1.0 - AWARENESS
	OPT_OUT = 0.0
	for r in xrange(NUMRUNS+1):
		print "\n||||||||||||||||||- START - ||||||||||||||||||||||||||"
		print "Run", r, "of", NUMRUNS
		
		parameters = [AWARENESS, NAIVENESS, POPULARITY_CVAST, POPULARITY_CLIGHT, OPT_OUT, LASTSTRATEGY_CVAST, LASTSTRATEGY_CLIGHT]
		POPULARITY_CVAST, AWARENESS , OPT_OUT, LASTSTRATEGY_CVAST, LASTSTRATEGY_CLIGHT = play(outfile, parameters)
		NAIVENESS = 1.0 - AWARENESS
		POPULARITY_CLIGHT = 1.0 - POPULARITY_CVAST

	
	outfile.close()
	analysis()
runs()
