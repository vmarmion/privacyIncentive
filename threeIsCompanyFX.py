from __future__ import division
from decimal import *
import math
import sys
import scipy
import matplotlib.pyplot as plt

N = 1000000


REVENUE_PP = 10.0
COST_PP = 2.0
COST_PRIVACY = 1.0
REDUCED_REV = 2.0

BASE_PROFIT_PP = REVENUE_PP - COST_PP
PRIVACY_PROFIT_PP = BASE_PROFIT_PP - COST_PRIVACY - REDUCED_REV

POPULARITY_CVAST = 0.7
POPULARITY_CLIGHT = 1.0 - POPULARITY_CVAST


NONE = 0
NON_PRIVATE = 1
PRIVATE = 2
UNDEFINED = 3
Strategy_Options = ["None", "Defect", "Respect", "Undefined"]

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

QUADS = ["Privacy - Privacy", "Privacy - No Privacy", "No Privacy - Privacy", "No Privacy - No Privacy"]

	



def print_parameters(parameters):
	MINDFULNESS = parameters[0]
	NAIVENESS = parameters[1]
	print "------------PARAMETERS--------------------"
	print N, "\tN"
	print MINDFULNESS, "\tMINDFULNESS" 
	print NAIVENESS, "\tNAIVENESS" 
	print REVENUE_PP, "\tREVENUE_PP" 
	print COST_PP, "\tCOST_PP"  
	print REDUCED_REV, "\tREDUCED_REV" 
	print BASE_PROFIT_PP, "\tBASE_PROFIT_PP" 
	print PRIVACY_PROFIT_PP, "\tPRIVACY_PROFIT_PP" 
	print POPULARITY_CVAST, "\tPOPULARITY_CVAST"
	print POPULARITY_CLIGHT, "\tPOPULARITY_CLIGHT"
	print "-------------------------------------------"
	
def calcResults(parameters):
	#Calculates each revenue senario 
	MINDFULNESS = parameters[0]
	NAIVENESS = parameters[1]

	Clight_HH_rev = math.pow((POPULARITY_CLIGHT * N), (0.2 * math.e))
	Cvast_HH_rev = math.pow((POPULARITY_CVAST * N), (0.2 * math.e)) 
	
	Clight_HL_rev = math.pow((POPULARITY_CLIGHT * NAIVENESS), (0.2 * math.e)) + math.pow(MINDFULNESS, (0.2 * math.e))
	Cvast_HL_rev = math.pow((POPULARITY_CVAST * NAIVENESS), (0.21 * math.e))
	
	Clight_LH_rev = math.pow((POPULARITY_CLIGHT * NAIVENESS), (0.21 * math.e))
	Cvast_LH_rev = math.pow((POPULARITY_CVAST * NAIVENESS), (0.2 * math.e)) + math.pow(MINDFULNESS, (0.2 * math.e))
	
	Clight_LL_rev = math.pow((POPULARITY_CLIGHT * N), (0.21 * math.e))
	Cvast_LL_rev = math.pow((POPULARITY_CVAST * N), (0.21 * math.e))

	results = [Clight_HH_rev, Cvast_HH_rev, Clight_HL_rev, Cvast_HL_rev, Clight_LH_rev, Cvast_LH_rev,  Clight_LL_rev, Cvast_LL_rev]
	
	return results

def printResults(result):
	print "--------------------------------------------"
	print""
	print "           Cvast Strategy"
	print "       Privacy   ||   No Privacy     Clight Strategy"
	print "|",result[Clight_HH],",",result[Cvast_HH], " ||", result[Clight_HL],",",result[Cvast_HL],"|", "    Privacy"
	print "|",result[Clight_LH],",",result[Cvast_LH], " ||", result[Clight_LL],",",result[Cvast_LL],"|", "    No privacy"
	print ""
	print "-----------------------------------------------------"

def calcDomStrategy(result):
	Cvast_DS = Clight_DS = NONE 
	#if Cvast goes private, Clight should go private and if 
	#Cvast goes no privacy Clight should still go private
	if ((result[Clight_HH] > result[Clight_LH]) and (result[Clight_HL] > result[Clight_LL])):
		Clight_DS = PRIVATE
	elif ((result[Clight_HH] < result[Clight_LH]) and (result[Clight_HL] < result[Clight_LL])):
		Clight_DS = NON_PRIVATE

	if ((result[Cvast_HH] > result[Cvast_HL]) and (result[Cvast_LH] > result[Cvast_LL])):
		Cvast_DS = PRIVATE 
	elif ((result[Cvast_HH] < result[Cvast_HL]) and (result[Cvast_LH] < result[Cvast_LL])):
		Cvast_DS = NON_PRIVATE
	
	print "Dominant Strategies:\t\t",Strategy_Options[Clight_DS], "|", Strategy_Options[Cvast_DS]
	
	return Clight_DS, Cvast_DS
	
def calc_strategies(result, DS):
	
	Clight_DS, Cvast_DS = DS
	
	Clight_strategy = Clight_DS
	Cvast_strategy = Cvast_DS

	if Clight_DS == NONE:
		if Cvast_DS == PRIVATE:
			if result[Clight_HH] >= result[Clight_LH]:
				Clight_strategy = PRIVATE
			else:
				Clight_strategy = NON_PRIVATE
		elif Cvast_DS == NON_PRIVATE:
			if result[Clight_HL] >= result[Clight_LL]:
				Clight_strategy = PRIVATE
			else:
				Clight_strategy = NON_PRIVATE
		elif Cvast_DS == NONE:
			Clight_strategy = UNDEFINED

	if Cvast_DS == NONE:
		if Clight_DS == PRIVATE:
			if result[Cvast_HH] > result[Cvast_HL]:
				Cvast_strategy = PRIVATE
			else:
				Cvast_strategy = NON_PRIVATE
		elif Clight_DS == NON_PRIVATE:
			if result[Cvast_LH] >= result[Cvast_LL]:
				Cvast_strategy = PRIVATE
			else:
				Cvast_strategy = NON_PRIVATE
		elif Clight_DS == NONE:
			Cvast_strategy = UNDEFINED

	print "Strategies:\t\t\t", Strategy_Options[Clight_strategy],"|", Strategy_Options[Cvast_strategy]

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
			return PRIVATE
		else:
			return NON_PRIVATE
		"""	
		low = min(a,b,c,d)
		if (a == low) or (b == low): 
			return NON_PRIVATE
		if (c == low) or (d == low): 
			return PRIVATE"""

	elif player == Cvast:
	
		#eliminate lowest possible return
		a = result[Cvast_HH]
		b = result[Cvast_HL]
		c = result[Cvast_LH]
		d = result[Cvast_LL]
		
		P = (a+c)/2.0
		NP = (b+d)/2.0
		if P > NP:
			return PRIVATE
		else:
			return NON_PRIVATE
		"""
		low = min(a,b,c,d)
		if (a == low) or (c == low):  
			
			return NON_PRIVATE
		if (b == low) or (d == low): 
			return PRIVATE
		"""
	print "ERROR!!!!!!!!"
	return 0

def calc_revenue(result, strategies, parameters):
	MINDFULNESS = parameters[0]
	NAIVENESS = parameters[1]
	Clight_revenue = Cvast_revenue = 0
	PC_revenue = 0
	if strategies[Clight] and strategies[Cvast] == PRIVATE:
	
		Clight_revenue = result[Clight_HH]
		Cvast_revenue = result[Cvast_HH]
		PC_revenue = math.pow(N, (0.2 * math.e))
	
	elif ((strategies[Clight] == NON_PRIVATE) and (strategies[Cvast] == NON_PRIVATE)):
	
		Clight_revenue = result[Clight_LL]
		Cvast_revenue = result[Cvast_LL]
		PC_revenue = 0

	elif ((strategies[Clight] == PRIVATE) and (strategies[Cvast] == NON_PRIVATE)):
		
		Clight_revenue = result[Clight_HL]
		Cvast_revenue = result[Cvast_HL]
		PC_revenue = math.pow( ( (POPULARITY_CLIGHT * NAIVENESS) + MINDFULNESS), (0.2 * math.e))

	elif ((strategies[Clight] == NON_PRIVATE) and (strategies[Cvast] == PRIVATE)):
		Clight_revenue = result[Clight_LH]
		Cvast_revenue = result[Cvast_LH]
		PC_revenue = math.pow( ( (POPULARITY_CVAST * NAIVENESS) + MINDFULNESS), (0.2 * math.e))

	
	print "Revenues:\t\t\t", Clight_revenue, "\t|",Cvast_revenue 
	
	return Clight_revenue, Cvast_revenue, PC_revenue

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
	
	MINDFULNESS = parameters[0]
	NAIVENESS = parameters[1]
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
	
	#NE
	NE = find_NE(gameResults)
	
	for x in xrange(len(gameResults)):
		num =  int(gameResults[x])
		outfile.write("%03d\t" % num)
	
	outfile.write("--DS\t")
	outfile.write("%02d\t %02.2d\t " % (dominantStrategies[0], dominantStrategies[1]))

	outfile.write("--Ss\t")
	outfile.write("%02d\t %02d\t " % (strategies[0], strategies[1]))

	outfile.write("--Rv\t")
	outfile.write("%02d\t %02d\t %02d\t " % (revenues[0], revenues[1], revenues[2]))

	outfile.write("--NE\t")
	for x in xrange(len(NE)):
		num = NE[x]
		outfile.write("%01d\t" % num)


	outfile.write("--PARS\t")
	outfile.write("%02d\t %.2f\t %.2f\t " % (N, MINDFULNESS, NAIVENESS))
	outfile.write("--PARS2\t")
	outfile.write("%02.2f\t %02.2f\t %02.2f\t %02.2f\t " % (REVENUE_PP, COST_PP, COST_PRIVACY, REDUCED_REV)) 
	outfile.write("--PARS3\t")
	outfile.write("%02.2f\t %02.2f\t %02.2f\t %02.2f\t " % (BASE_PROFIT_PP, PRIVACY_PROFIT_PP, POPULARITY_CVAST, POPULARITY_CLIGHT))
	outfile.write("\n")

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
	PC_rev  =[]
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
		PC_rev.append(int(r[17]))
	
	

	fig = plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
	fig.suptitle("Player Strategies and Revenue per Mindfulness Population \n(CVAST POP = %s, CLIGHT POP = %s )" %(POPULARITY_CVAST, POPULARITY_CLIGHT))
	
	plt.subplot(511)
	plt.plot(ClightREV_HH,"g", label="CL_HH")
	plt.plot(ClightREV_HL,"g--",label="CL_HL")
	plt.plot(ClightREV_LH,"r--",label="CL_LH")
	plt.plot(ClightREV_LL,"r", label="CL_LL")
	plt.ylabel("Potential Revenues ")
	#plt.axis([0,100,0,6000])
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.subplot(512)
	plt.plot(CvastREV_HH,"g",label="CV_HH")
	plt.plot(CvastREV_HL,"r--",label="CV_HL")
	plt.plot(CvastREV_LH,"g--",label="CV_LH")
	plt.plot(CvastREV_LL,"r",label="CV_LL")
	plt.ylabel("Potential Revenues ")
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.subplot(513)
	plt.plot(CL_DS, "r.", label="CLight DS")
	plt.plot(CV_DS,"b--", label="CVast DS")
	plt.ylabel("Dominant Strategies")
	plt.yticks([0,1,2,3], Strategy_Options)
	#plt.axis([0,100,-1,4])
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.subplot(514)
	plt.plot(CL_str, "r.", label="CLight Strategy")
	plt.plot(CV_str, "b--", label="CVast Strategy")
	plt.xlabel("Mindfulness Population %")
	plt.ylabel("Chosen Strategies")
	plt.yticks([0,1,2,3], Strategy_Options)
	#plt.axis([0,100,-1,4])
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.subplot(515)
	plt.plot(CL_rev, "r.", label="CLight Revenue")
	plt.plot(CV_rev, "b--", label="CVast Revenue")
	plt.plot(PC_rev, "g.", label = "Prviacy Comp Revenue")
	plt.plot(ClightREV_LH,"r--",label="CL_LH")
	plt.plot(CvastREV_HL,"b--",label="CV_HL")
	plt.xlabel("Mindfulness Population %")
	plt.ylabel("Pridicted Revenues")
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	#plt.axis([0,100,0,6000])
	plt.show()

	fig2 = plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
	fig2.suptitle("Player Strategies and Revenue per Mindfulness Population \n(Cvast Popularity = %s, CLight Popularity = %s )" %(POPULARITY_CVAST, POPULARITY_CLIGHT))
	
	plt.subplot(311)
	plt.plot(CL_rev, "r.", label="CLight")
	plt.plot(CV_rev, "b.", label="CVast ")
	#plt.plot(PC_rev, "g--", label = "Prviacy Comp Revenue")
	plt.ylabel("Potential Revenues\n\n")
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.subplot(312)
	plt.plot(CL_str, "r.", label="CLight")
	plt.plot(CV_str, "b-", label="CVast")
	plt.ylabel("Chosen Strategies\n")
	plt.yticks([0,1,2], Strategy_Options)
	plt.axis([0,100,-1,3])
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.subplot(313)
	plt.plot(CL_DS, "r.", label="CLight")
	plt.plot(CV_DS,"b--", label="CVast")
	plt.ylabel("Dominant Strategies\n")
	plt.xlabel("Mindful Population %")
	plt.yticks([0,1,2], Strategy_Options)
	plt.axis([0,100,-1,3])

	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	plt.savefig("gameOneResults3.pdf")
	plt.show()

def runs():
	outfile = open("GameResults.txt", "w")
	numRuns = 100
	up = N / numRuns
	for r in xrange(numRuns+1):
		print "\n||||||||||||||||||- START - ||||||||||||||||||||||||||"
		MINDFULNESS = r * up
		NAIVENESS = N - MINDFULNESS
		print "Run", r, "of", numRuns
		parameters = [MINDFULNESS, NAIVENESS]
		play(outfile, parameters)

	
	outfile.close()
	analysis()
runs()
