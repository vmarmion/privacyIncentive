from __future__ import division
from decimal import *
import math
import sys
import scipy
import matplotlib.pyplot as plt

N = 1000000

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
	print "-------------------------------------------"
	
def calcResults(parameters):
	#Calculates each revenue senario 
	AWARENESS = parameters[0]
	NAIVENESS = parameters[1]
	POPULARITY_CVAST = parameters[2]
	POPULARITY_CLIGHT = parameters[3]
	Clight_HH_rev = math.pow((POPULARITY_CLIGHT * N), (0.2 * math.e))
	Cvast_HH_rev = math.pow((POPULARITY_CVAST * N), (0.2 * math.e)) 
	
	Clight_HL_rev = math.pow(((POPULARITY_CLIGHT * NAIVENESS) + AWARENESS), (0.2 * math.e))
	Cvast_HL_rev = math.pow((POPULARITY_CVAST * NAIVENESS), (0.22 * math.e))


	
	Clight_LH_rev = math.pow((POPULARITY_CLIGHT * NAIVENESS), (0.22 * math.e))
	Cvast_LH_rev = math.pow(((POPULARITY_CVAST * NAIVENESS)+ AWARENESS), (0.2 * math.e)) 
	
	Clight_LL_rev = math.pow((POPULARITY_CLIGHT * N), (0.22 * math.e))
	Cvast_LL_rev = math.pow((POPULARITY_CVAST * N), (0.22 * math.e))

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

def undefined_Strategies(result, player):
	if player == Clight:
	
		#eliminate lowest possible return
		a = result[Clight_HH]
		b = result[Clight_HL]
		c = result[Clight_LH]
		d = result[Clight_LL]

		P = (a+b)/2.0
		NP = (c+d)/2.0
		if P > NP:
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
		if P > NP:
			return RESPECT
		else:
			return EXPLOIT
		
	return 0

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
	
	if strategies[Clight] and strategies[Cvast] == RESPECT:
		print "one"
	
	elif ((strategies[Clight] == EXPLOIT) and (strategies[Cvast] == EXPLOIT)):
		print "two"
	elif ((strategies[Clight] == RESPECT) and (strategies[Cvast] == EXPLOIT)):
		Temp = POPULARITY_CVAST*NAIVENESS
		POPULARITY_CVAST = Temp/N
		print "three"
	elif ((strategies[Clight] == EXPLOIT) and (strategies[Cvast] == RESPECT)):
		Temp = (POPULARITY_CVAST*NAIVENESS)+AWARENESS
		POPULARITY_CVAST = Temp/N
		print "four"
	return POPULARITY_CVAST

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
	#GR
	gameResults = calcResults(parameters)
	printResults(gameResults)
	print_parameters(parameters)

	#DS
	dominantStrategies = calcDomStrategy(gameResults)

	#Strategies
	Clight_strategy, Cvast_strategy = calc_strategies(gameResults, dominantStrategies)

	if Clight_strategy == UNDEFINED:
		Clight_strategy =  undefined_Strategies(gameResults, Clight)
		print "Avoiding Low:\t\t\t", Strategy_Options[Clight_strategy]
	if Cvast_strategy == UNDEFINED:
		Cvast_strategy = undefined_Strategies(gameResults, Cvast)
		print "Avoiding Low:\t\t\t",Strategy_Options[Cvast_strategy]

	strategies = Clight_strategy, Cvast_strategy 
		
	#Rev
	revenues = calc_revenue(gameResults, strategies, parameters)
	POPULARITY_CVAST = calc_popularity(strategies, parameters)
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
	outfile.write("--NE?\t")
	
	for x in xrange(len(NE)):
		num = NE[x]
		outfile.write("%01d\t" % num)

	outfile.write("--M&N\t")
	outfile.write("%02d\t %.2f\t %.2f\t " % (N, AWARENESS, NAIVENESS))
	outfile.write("\n")

	
	return POPULARITY_CVAST

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
	f=open("GameResults.txt", "r")
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
	


	fig2 = plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
	fig2.suptitle("Player Strategies and Revenue per AWARENESS Population\n Dynamic Popularity")
	
	plt.subplot(411)
	plt.plot(CL_rev, "r.", label="CLIGHT")
	plt.plot(CV_rev, "b.", label="CVAST ")
	#plt.plot(PC_rev, "g--", label = "Prviacy Comp Revenue")
	plt.ylabel("Potential\n Revenues\n\n")
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.subplot(412)
	plt.plot(CL_str, "r.", label="CLIGHT")
	plt.plot(CV_str, "b-", label="CVAST")
	plt.ylabel("Chosen \nStrategies\n")
	plt.yticks([0,1,2], Strategy_Options)
	plt.axis([0,100,-1,3])

	plt.subplot(413)
	plt.plot(CL_DS, "r.", label="CLIGHT")
	plt.plot(CV_DS,"b--", label="CVAST")
	plt.ylabel("Dominant \nStrategies\n")
	plt.xlabel("Aware Population %")
	plt.yticks([0,1,2], Strategy_Options)
	plt.axis([0,100,-1,3])

	"""plt.subplot(414)
	plt.plot(CL_pop, "r.", label="CLight")
	plt.plot(CV_pop,"b--", label="CVast")
	plt.ylabel("Popularity\n")
	plt.xlabel("Aware Population %")
	#plt.yticks([0,1,2], Strategy_Options)
	plt.axis([0,100,0,1])"""

	plt.savefig("gameTwoResults1.pdf")
	plt.show()

def runs():
	outfile = open("GameResults.txt", "w")
	numRuns = 100
	POPULARITY_CVAST = 0.95
	POPULARITY_CLIGHT = 1.0 - POPULARITY_CVAST
	up = N / numRuns
	for r in xrange(numRuns+1):
		print "\n||||||||||||||||||- START - ||||||||||||||||||||||||||"
		AWARENESS = r * up
		NAIVENESS = N - AWARENESS
		print "Run", r, "of", numRuns
		parameters = [AWARENESS, NAIVENESS, POPULARITY_CVAST, POPULARITY_CLIGHT]
		POPULARITY_CVAST = play(outfile, parameters)
		POPULARITY_CLIGHT = 1.0 - POPULARITY_CVAST
		print "pop", POPULARITY_CVAST, POPULARITY_CLIGHT
	
	outfile.close()
	analysis()
runs()
