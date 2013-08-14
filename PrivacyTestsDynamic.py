from __future__ import division
from decimal import *
import math
import sys
import scipy

import matplotlib.pyplot as plt
from random import randrange


NUM_ORGS = 30
POPULATION = 10000

NUMBER_BOUNDS = NUM_ORGS*POPULATION

NUM_RUNS = 50

EXPLOIT = 0
RESPECT = 1

CHANGECOST = 0

UTILITYFACTOR = 1.2

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

def calaOrgTrend():
	#is a company growing or falling
	orgTrend = []
	for org in range(NUM_ORGS):
		#reset counter
		trend = 0
		orgTrend.append(trend)
	#return array of each orgs health
	return orgTrend
	

def calcUtility(populationArray, orgStrategyArray):
	popUtility = []
	testCost = 5
	#for each person count how many private orgs
	for person in populationArray:
		balance = 0
		#print "calcUtility", person
		for org in range(NUM_ORGS):
			if person[org] == 1: 
				if orgStrategyArray[org] == RESPECT:
					balance +=1
					# is the benefit for transaction greater than the negative of not?
				else:
					balance -= UTILITYFACTOR
		utility = balance - testCost
		popUtility.append(utility)
		#need to work in the cost of testing!
		# utility now has to be a factor of over all situation
	return popUtility

def countArray(array):
	total = 0
	#print "Counting Array"
	for a in array:
		total += a
	return total

def killOrg(org,orgHealth, populationArray):
	print "KILL-------------------"
	orgHealth[org] = -1
	for person in range(POPULATION):
		interaction = populationArray[person]
		interaction[org] = 0
		populationArray[person] = interaction
	return populationArray, orgHealth

def popReduceInteraction(person, populationArray, orgStrategy, orgHealth):	
	minHealth = POPULATION
	interaction = populationArray[person]
	choiceArray = []
	choice = 0
	for org in range(NUM_ORGS):
		if orgHealth[org] == -1:
			print "?//////////////////////////DEAD"
			if interaction[org] == 1:
				if orgStrategy[org] == EXPLOIT:
					choiceArray.append(org)
					choice += 1
	if choice > 0:
		orgPosition = choiceArray[randrange(choice)]		
		interaction[orgPosition] = 0
		if orgHealth[orgPosition] < POPULATION/20:
			populationArray, orgHealth = killOrg(org, orgHealth, populationArray)
		populationArray[person] = interaction
	return populationArray

def popIncreaseInteraction(person, populationArray, orgStrategy, orgHealth):
	maxHealth = 0
	choice = 0
	choiceArray = []
	interaction = populationArray[person]

	for org in range(NUM_ORGS):
		if interaction[org] == 0:
			if orgHealth >= 0:
				if orgStrategy[org] == RESPECT:
					choiceArray.append(org)
					choice +=1
	if choice > 0:
		orgPosition = choiceArray[randrange(choice)]
		interaction[orgPosition] = 1
		populationArray[person] = interaction

	return populationArray



def plotting():
	totalHealthResults = []
	totalEngagementResults = []
	totalPopUtilityResults = []
	totalStrategyResults = []
	o1 = []
	o2 = []
	o3 = []
	o4 = []

	f=open("GameThreeResultsB.txt", "r")
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
		o1.append(int(row[5]))
		o2.append(int(row[6]))
		o3.append(int(row[7]))
		o4.append(int(row[8]))

	fig2 = plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
	fig2.suptitle("TITLE")
	
	plt.subplot(411)
	plt.plot(totalPopUtilityResults, "r.", label="Utility")
	plt.ylabel("Population Utility")
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	#plt.axis([0,NUM_RUNS,(-UTILITYFACTOR *NUMBER_BOUNDS),NUMBER_BOUNDS])

	plt.subplot(412)
	plt.plot(totalEngagementResults, "r.", label="Engagement")
	plt.ylabel("Engagement")
	#plt.axis([0,NUM_RUNS,0,NUMBER_BOUNDS])
	

	plt.subplot(413)
	plt.plot(o1, "r.", label="o1")
	plt.plot(o2, "b.", label="o2")
	plt.plot(o3, "g.", label="o3")
	plt.plot(o4, "c.", label="o4")
	plt.ylabel("Health")
	#plt.axis([0,NUM_RUNS,0,POPULATION])
	
	plt.subplot(414)
	plt.plot(totalStrategyResults, "b.", label = "Strategy")
	plt.ylabel("Strategy\n")
	#plt.axis([0,NUM_RUNS,0,NUM_ORGS])

	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.savefig("gameThreeResults.pdf")
	plt.show()

def calcRelaxed(popUtility):

	count= 0.0
	for personUtility in popUtility:
		if personUtility >= 0:
			count += 1.0
	relaxed = count/POPULATION
	return relaxed




def orgUpdateStrategy(org, orgStrategy, orgHealth, totalPopUtility, totalStrategy, totalEngagement, relaxed):
	#if population utility is low
	# number testing could be
	"""if aware of other org strategies and the current utility or awareness of the 
	population you can make an informed decision as to exploit of respect
	eg current Health V health if change
	"""
	OS = orgStrategy[org]
	OH = orgHealth[org]

	engagement = totalEngagement/NUMBER_BOUNDS

	concerned = 1-relaxed
	P = 10 
	S = 3
	I = 4
	#u_RESPECT = math.pow(OH, (0.2 * math.e))  * concerned * POPULATION
	#u_EXPLOIT = math.pow(OH, (0.24 * math.e)) * relaxed * engagement * POPULATION
	u_RESPECT = P - S
	u_EXPLOIT = (P + I) - (concerned * P) - (concerned * I)

	U = u_RESPECT - u_EXPLOIT
	if U > CHANGECOST:
		if OS == EXPLOIT:
			temp = "- +"
			orgStrategy[org] = RESPECT
		elif OS == RESPECT:
			temp = "+ +"
			
	elif U < -CHANGECOST:
		if OS == RESPECT:
			temp = "+ -"
			orgStrategy[org] = EXPLOIT
		elif OS == EXPLOIT:
			temp = "- -"
	else:
		temp = "= ="
			
	

	""" option one
		if orgHealth[org] < (POPULATION/8):
		# assess strategy
		if orgStrategy[org] == EXPLOIT:
			print ">>>>>>>>>>>>>>>>>>>>>>>>>>>EXPLOIT to RESPECT :)"
			orgStrategy[org] = RESPECT
	if orgHealth[org] > (POPULATION - (POPULATION/8)):
		if orgStrategy[org] == RESPECT:
			print "---------------------------RESPECT to EXPLOIT"
			orgStrategy[org] = EXPLOIT
	"""
	return orgStrategy

def run():
	outfile = open("GameThreeResultsA.txt", "w")
	outfileB = open("GameThreeResultsB.txt", "w")
	
	#set up
	orgStrategy = setOrgStrategy()
	populationArray = setPopulationInteraction()
	
	engagement = calcEngagement(populationArray)
	orgHealth = calcOrgHealth(populationArray)
	popUtility = calcUtility(populationArray, orgStrategy)
	relaxed = calcRelaxed(popUtility)
			

	for run in range(NUM_RUNS):
		
		for loop in range(50):#10% swings
			
			personA = randrange(POPULATION)
			personUtility = popUtility[personA]

			if relaxed <= 0.5:
				#print "LEAVING --- "
				populationArray = popReduceInteraction(personA, populationArray, orgStrategy, orgHealth)
			else:	
				#print "JOINING ++"
				populationArray = popIncreaseInteraction(personA, populationArray, orgStrategy, orgHealth)
			
			engagement = calcEngagement(populationArray)
			orgHealth = calcOrgHealth(populationArray)
			popUtility = calcUtility(populationArray, orgStrategy)
			relaxed = calcRelaxed(popUtility)
			
			totalPopUtility = countArray(popUtility)
			totalEngagement = countArray(engagement)
			totalHealth = countArray(orgHealth)
			totalStrategy = countArray(orgStrategy)
			
			outfileB.write("--totals\t")
			outfileB.write("%02d\t %02d\t %02d\t %02d\t " % (totalPopUtility, totalHealth, totalEngagement, totalStrategy))
			outfileB.write("%02d\t %02d\t %02d\t %02d\t " % (orgHealth[0], orgHealth[1], orgHealth[2], orgHealth[3] ))
			outfileB.write("\n") 
			print loop, "loop", run, "RESPECTING", '%.2f' % totalStrategy,  "RELAXED",  '%.2f' % relaxed, "ENGAGED",  '%.2f' % totalEngagement, "UTILITY",  '%.2f' % totalPopUtility
	

		organisation = randrange(NUM_ORGS)
		orgStrategy = orgUpdateStrategy(organisation, orgStrategy, orgHealth, totalPopUtility, totalStrategy, totalEngagement, relaxed)
		
		outfileB.write("--totals\t")
		outfileB.write("%02d\t %02d\t %02d\t %02d\t " % (totalPopUtility, totalHealth, totalEngagement, totalStrategy))
		outfileB.write("%02d\t %02d\t %02d\t %02d\t " % (orgHealth[0], orgHealth[1], orgHealth[2], orgHealth[3] ))
		outfileB.write("\n")
	

	print "\n///////////////END/////////////////\n"
	print "individuals\t", engagement[0], engagement[1], engagement[2], engagement[3]
	print "Engagement:\t", totalEngagement, "/",NUMBER_BOUNDS
	print "Org Health:\t", totalHealth, "/",NUMBER_BOUNDS, "=>", orgHealth
	print "Org Strategy:\t", totalStrategy, "/", NUM_ORGS, "=>", orgStrategy
	print "Utility:\t" , totalPopUtility, "/", NUMBER_BOUNDS


	outfile.close()
	outfileB.close()
	plotting()

run()




