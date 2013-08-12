from __future__ import division
from decimal import *
import math
import sys
import scipy

import matplotlib.pyplot as plt
from random import randrange

CUST_BENEFIT = 0
CUST_TEST_COST = 1
CUST_VIOLATION_COST = 2
ORG_PROFIT = 3
ORG_PRIVACY_COST = 4
ORG_DATA_PROFIT = 5

NUM_ORGS = 10
POPULATION = 1000

NUMBER_BOUNDS = NUM_ORGS*POPULATION

NUM_RUNS = 1000

EXPLOIT = 0
RESPECT = 1


def AssignRandomInter():
	#assign randon interation with each organisation [0/1] 
	interactionArray = []
	num = 0
	for org in range(NUM_ORGS):
		num = randrange(2)
		interactionArray.append(num)
	return interactionArray

def setPopulationInteraction():
	#set both interaction with orgs
	populationInteractionArray = []
	for person in range(POPULATION):
		populationInteractionArray.append(AssignRandomInter())
	return populationInteractionArray

def setOrgStrategy():
	#sets each org startegy either respect or exploit
	orgStrategy = []
	for org in range(NUM_ORGS):
		orgStrategy.append(randrange(2))
	return  orgStrategy

def calcEngagement(populationArray):
	engagement = []
	for p in range(POPULATION):
		person = populationArray[p]
		#reset counter
		personEngagement = 0
		#for each person count interaction with orgs
		for org in range(NUM_ORGS):
			personEngagement += person[org]
		engagement.append(personEngagement)
	#arrary of each customer engagement level
	return engagement

def calcOrgHealth(populationArray):
	orgHealth = []
	for org in range(NUM_ORGS):
		#reset counter
		health = 0
		for person in populationArray:
			health += person[org]
		orgHealth.append(health)
	#return array of each orgs health
	return orgHealth

def calcUtility(populationArray, orgStrategyArray):
	popUtility = []
	#for each person count how many private orgs
	for person in populationArray:
		utility = 0
		#print "calcUtility", person
		for org in range(NUM_ORGS):
			if person[org] == 1: 
				if orgStrategyArray[org] == RESPECT:
					utility +=1
				else:
					utility -= 1
		popUtility.append(utility)
	return popUtility

def countArray(array):
	total = 0
	#print "Counting Array"
	for a in array:
		total += a
	return total


def popReduceInteraction(person, popUtility, populationArray, orgStrategy, orgHealth):
	#popoulation if negative utility will look to swap an organisation of least popularity with a high hih popularity one with privacy
	
	minHealth = POPULATION
	orgPosition = -1
	personUtility = popUtility[person]
	interaction = populationArray[person]
	
	if personUtility < 0:
		
			
		#look at orgs person interacting with and find lowest health (worst offender)
		for org in range(NUM_ORGS):
			if interaction[org] == 1:
				if orgStrategy[org] == EXPLOIT:
					
					if orgHealth[org] <= minHealth:
						
						minHealth = orgHealth[org]
						orgPosition = org
		
		# abandon lowest health org
		if orgPosition > -1:
			
			interaction[orgPosition] = 0
			populationArray[person] = interaction
			
	return populationArray

def popIncreaseInteraction(person, popUtility, populationArray, orgStrategy, orgHealth):
	#popoulation if negative utility will look to swap an organisation of least popularity with a high hih popularity one with privacy
	
	maxHealth = 0
	orgPosition = -1
	personUtility = popUtility[person]
	interaction = populationArray[person]
	choiceArray = []
	temp = -1
	
	if personUtility >= 0:
		
		print interaction, person
		#look at orgs person interacting with and find lowest health (worst offender)
		for org in range(NUM_ORGS):
			if interaction[org] == 0:
				choiceArray.append(org)
				temp = 0
		if temp > -1:
			temp = len(choiceArray)
			choice = randrange(temp)
			orgPosition = choiceArray[choice]
		if orgPosition > -1:
			interaction[orgPosition] = 1
			populationArray[person] = interaction
	return populationArray



def plotting():
	totalHealthResults = []
	totalEngagementResults = []
	totalPopUtilityResults = []
	totalStrategyResults = []

	f=open("GameThreeResults.txt", "r")
	resultsFile = []
	numbers = []
	for line in f:
		
		if line != "\n":
			numbers = line.split()
			resultsFile.append(numbers)#appends each line as a list of strings  
    
	for row in resultsFile:
		totalPopUtilityResults.append(int(row[1]))
		totalEngagementResults.append(int(row[2]))
		totalHealthResults.append(int(row[3]))
		totalStrategyResults.append(int(row[4]))

	fig2 = plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
	fig2.suptitle("TITLE")
	
	plt.subplot(411)
	plt.plot(totalPopUtilityResults, "r.", label="Utility")
	plt.ylabel("Population Utility")
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.subplot(412)
	plt.plot(totalEngagementResults, "r.", label="Engagement")
	plt.ylabel("Engagement")
	#plt.axis([0,NUMRUNS,-1,3])
	#plt.yticks([0 ,1,2], Strategy_Options)

	plt.subplot(413)
	plt.plot(totalHealthResults, "r.", label="Health")
	plt.ylabel("Health")
	
	plt.subplot(414)
	plt.plot(totalStrategyResults, "b.", label = "Strategy")
	plt.ylabel("Strategy\n")

	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.savefig("gameThreeResults.pdf")
	plt.show()

def orgUpdateStrategy(org, orgStrategy, orgHealth, totalPopUtility):
	#if population utility is low
	# number testing could be
	if orgHealth[org] < (POPULATION/4):
		if orgStrategy[org] == EXPLOIT:
			print "E to R"
			orgStrategy[org] = RESPECT
	if orgHealth[org] > (POPULATION - (POPULATION/4)):
		if orgStrategy[org] == RESPECT:
			print "R to E"
			orgStrategy[org] = EXPLOIT
	return orgStrategy

def run():
	outfile = open("GameThreeResults.txt", "w")
	print "\n///////////////START/////////////////\n"
	
	orgStrategy = setOrgStrategy()
	populationArray = setPopulationInteraction()

	engagement = calcEngagement(populationArray)
	orgHealth = calcOrgHealth(populationArray)
	popUtility = calcUtility(populationArray, orgStrategy)
	
	totalPopUtility = countArray(popUtility)
	totalEngagement = countArray(engagement)
	totalHealth = countArray(orgHealth)
	totalStrategy = countArray(orgStrategy)

	print "Orgs --> \t\t| total"
	for person in range(POPULATION):
		print populationArray[person], "person: ",person+1

	print "Engagement:\t", totalEngagement, "/",NUMBER_BOUNDS, "=>", engagement
	print "Org Health:\t", totalHealth, "/",NUMBER_BOUNDS, "=>", orgHealth
	print "Org Strategy:\t", totalStrategy, "/", NUM_ORGS, "=>", orgStrategy
	print "Utility:\t" , totalPopUtility, "/", NUMBER_BOUNDS, "=>", popUtility


	for run in range(NUM_RUNS):
		print run
		for loop in range(1000):
			personA = randrange(POPULATION)
			personB = randrange(POPULATION)
			
		
			populationArray = popReduceInteraction(personA, popUtility, populationArray, orgStrategy, orgHealth)
			populationArray = popIncreaseInteraction(personB, popUtility, populationArray, orgStrategy, orgHealth)
			
		organisation = randrange(NUM_ORGS)
		orgStrategy = orgUpdateStrategy(organisation, orgStrategy, orgHealth, totalPopUtility)
		
		engagement = calcEngagement(populationArray)
		orgHealth = calcOrgHealth(populationArray)
		popUtility = calcUtility(populationArray, orgStrategy)

		totalPopUtility = countArray(popUtility)
		totalEngagement = countArray(engagement)
		totalHealth = countArray(orgHealth)
		totalStrategy = countArray(orgStrategy)
		outfile.write("--totals\t")
		outfile.write("%02d\t %02d\t %02d\t %02d\t " % (totalPopUtility, totalEngagement, totalHealth, totalStrategy))
		outfile.write("\n")
	

	print "\n///////////////END/////////////////\n"

	

	print "Orgs --> \t\t| total"
	for person in range(POPULATION):
		print populationArray[person], "person: ",person+1

	print "Engagement:\t", totalEngagement, "/",POPULATION*NUM_ORGS, "=>", engagement
	print "Org Health:\t", totalHealth, "/",POPULATION*NUM_ORGS, "=>", orgHealth
	print "Org Strategy:\t", totalStrategy, "/", NUM_ORGS, "=>", orgStrategy
	print "Utility:\t" , totalPopUtility, "/", POPULATION*NUM_ORGS, "=>", popUtility


	outfile.close()
	plotting()

run()

def GameParameters(ntc, nro):

	# - (B-V) - T to be positive
	custBenefit = 10
	custViolationCost = 20
	custTestCost = 5

	orgProfit = 10 # P
	orgPrivacyCost = 5 # S
	orgDataProfit = 7 #I

	numRespectOrg = nro
	numDefectOrg = 1 - numRespectOrg

	numTestCust = ntc
	numDontCust = 1 - numTestCust

	parameters = [custBenefit, custTestCost, custViolationCost, orgProfit, orgPrivacyCost, orgDataProfit, numRespectOrg, numDefectOrg, numTestCust, numDontCust]
	return parameters

def utilityCust(pars):
	Ua = (1 - pars[NUM_RESPECT_ORG])
	Ub = (-1 * (pars[CUST_BENEFIT] - pars[CUST_VIOLATION_COST]))
	Uc = pars[CUST_TEST_COST]
	Ud = Ub - Uc
	U = Ua * Ud
	print Ua,Ub, Uc, Ud, "U1"
	return U
	 

def utilityOrg(pars):

	Ua = -1 * (pars[ORG_PRIVACY_COST] - pars[ORG_DATA_PROFIT])
	Ub = pars[NUM_TEST_CUST] * pars[ORG_PROFIT]
	Uc = pars[NUM_TEST_CUST] * pars[ORG_DATA_PROFIT]
	U = (Ua*Ub )- Uc
	U = (Ua*Ub )- Uc
	print Ua,Ub, Uc, "U"
	return U


def perCA(CA):
	count = 0.0
	for c in CA:
		count += c
	per = count/NUM_populationS
	return per

def perOA(OA):
	count = 0.0
	for o in OA:
		count += o
	per = count/NUM_ORGS
	return per

def begin():
	CA = setpopulations()
	OA = setOrgs()
	Cdecision = 0
	Odecision = 0
	for run in range(RUNS):
		perTestCust = perCA(CA)
		perRespectOrg = perOA(OA)
		print perTestCust, perRespectOrg, "pars---------"
		pars = GameParameters(perTestCust, perRespectOrg)
		
		
		ranCust = randrange(NUM_populationS-1)
		if utilityCust(pars) > 0:
			Cdecision = 1
		else:
			Cdecision = 0
		CA[ranCust] = Cdecision

		randOrg = randrange(NUM_ORGS-1)
		if utilityOrg(pars) >= 0:
			Odecision = 1
		else: 
			Odecision = 0
		OA[randOrg] = Odecision

		custT.append(perTestCust)
		orgR.append(perRespectOrg)
	
	plt.plot(custT,"g", label="populations Testing")
	plt.plot(orgR,"r", label="Companies Respecting")
	plt.ylabel("Percentage")
	plt.axis([-1,100000,-1,1.5])
	plt.legend(bbox_to_anchor=(0.5, 1), loc=2, borderaxespad=0.)

	plt.show()




