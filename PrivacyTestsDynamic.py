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

NUM_ORGS = 3
NUM_CUSTOMERS = 5

RUNS = 100


def AssignRandomInter():
	interactionArray = []
	total = 0
	for o in range(NUM_ORGS):
		num = randrange(2)
		interactionArray.append(num)
	return interactionArray

def setCustomers():
	CustInteractionArray = []
	for c in range(NUM_CUSTOMERS):
		IR = AssignRandomInter()
		CustInteractionArray.append(IR)
		temp = [0,0]
		CustStrategyArray.append(temp)
	return CustInteractionArray, CustStrategyArray

def setOrgs():
	orgStrategy = []
	for x in range(NUM_ORGS):
		orgStrategy.append(randrange(2))
	return  orgStrategy

def calcEngagement(CA, CS):
	res = CS
	for c in CA:
		CI = 0

		for o in range(NUM_ORGS):
			CI += c[o]
			res[0] = CI
	return res

def calcUtility(CA, OS):
	U = 0
	res = []
	for c in CA:
		U = 0
		print "customer", c
		for o in range(NUM_ORGS):
			if c[o] == 1: 
				#print "interacting"
				if OS[o] == 1:
					print "Defecting"
					U +=1
		print U
		c[NUM_ORGS+1] = U
		print c
		res.append(c)
	return res

def calcOrgHealth(CA):
	OH = []
	for o in range(NUM_ORGS):
		total = 0
		for c in CA:
			total += c[o]
		OH.append(total)
	return OH



def display(CA, OH, OS, CI):

	print "Orgs --> \t\t| total"
	for c in range(NUM_CUSTOMERS):
		print CA[c], "Customer: ",c+1

	print "Engagement:\t", CI
	print "Org Health:\t", OH
	print "Org Strategy:\t", OS

def run():
	print "\n///////////////START/////////////////\n"
	OS = setOrgs()

	CA, CS = setCustomers()
	
	CI = calcEngagement(CA, CS)
	OH = calcOrgHealth(CA)

	calcUtility(CA, OS)

	display(CA, OH, OS, CI)


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
	per = count/NUM_CUSTOMERS
	return per

def perOA(OA):
	count = 0.0
	for o in OA:
		count += o
	per = count/NUM_ORGS
	return per

def begin():
	CA = setCustomers()
	OA = setOrgs()
	Cdecision = 0
	Odecision = 0
	for run in range(RUNS):
		perTestCust = perCA(CA)
		perRespectOrg = perOA(OA)
		print perTestCust, perRespectOrg, "pars---------"
		pars = GameParameters(perTestCust, perRespectOrg)
		
		
		ranCust = randrange(NUM_CUSTOMERS-1)
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
	
	plt.plot(custT,"g", label="Customers Testing")
	plt.plot(orgR,"r", label="Companies Respecting")
	plt.ylabel("Percentage")
	plt.axis([-1,100000,-1,1.5])
	plt.legend(bbox_to_anchor=(0.5, 1), loc=2, borderaxespad=0.)

	plt.show()




