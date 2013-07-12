from __future__ import division
from decimal import *
import math
import sys

import matplotlib.pyplot as plt
from random import randrange

CUST_BENEFIT = 0
CUST_TEST_COST = 1
CUST_VIOLATION_COST = 2
ORG_PROFIT = 3
ORG_PRIVACY_COST = 4
ORG_DATA_PROFIT = 5

NUM_RESPECT_ORG = 6
NUM_DEFEAT_ORG = 7
NUM_TEST_CUST = 8
NUM_DONT_CUST = 9

RUNS = 10000
NUM_CUSTOMERS = 100
NUM_ORGS = 100

def setCustomers():
	CustArray = []
	for x in range(NUM_CUSTOMERS):
		cust = 0
		CustArray.append(cust)
	return CustArray

def setOrgs():
	orgArray = []
	for x in range(NUM_ORGS):
		org = 0
		orgArray.append(org)
	return orgArray



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
	custT = []
	orgR = []
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




begin()