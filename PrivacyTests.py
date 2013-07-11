from __future__ import division
from decimal import *
import math
import sys

import matplotlib.pyplot as plt

CUST_BENEFIT = 0
CUST_TEST_COST = 1
CUST_VIOLATION_COST = 2
COMP_PROFIT = 3
COMP_PRIVACY_COST = 4
COMP_DATA_PROFIT = 5

NUM_RESPECT_COMP = 6
NUM_DEFEAT_COMP = 7
NUM_TEST_CUST = 8
NUM_DONT_CUST = 9

RUNS = 1000


def GameParameters(nrc, ntc):
	custBenefit = 2
	custTestCost = 1
	custViolationCost = 14
	compProfit = 8
	compPrivacyCost = 1
	compDataProfit = 2

	numRespectComps = nrc
	numDefectComps = 1 - numRespectComps

	numTestCust = ntc
	numDontCust = 1 - numTestCust

	parameters = [custBenefit, custTestCost, custViolationCost, compProfit, compPrivacyCost, compDataProfit, numRespectComps, numDefectComps, numTestCust, numDontCust]
	return parameters

def utilityCust(pars):
	Ua = -1 * (pars[NUM_DEFEAT_COMP])
	Ub = pars[CUST_BENEFIT] - pars[CUST_VIOLATION_COST]
	Uc = pars[CUST_TEST_COST]
	U = (Ua*Ub )- Uc

	

	return U
	 

def utilityComp(pars):

	Ua = -1 * (pars[COMP_PRIVACY_COST] - pars[COMP_DATA_PROFIT])
	Ub = pars[NUM_RESPECT_COMP] * pars[COMP_PROFIT]
	Uc = pars[NUM_RESPECT_COMP] * pars[COMP_DATA_PROFIT]
	U = (Ua*Ub )- Uc
	return U
	

def play():
	custU = []
	compU = []
	for n in xrange(RUNS+1):
		m = n/RUNS
		#print m
		pars = GameParameters(m,m)

		custU.append(utilityCust(pars))
		compU.append(utilityComp(pars))
		#print pars, m
	#print custU

	fig = plt.figure(num=None, figsize=(8, 8), dpi=80, facecolor='w', edgecolor='k')
	fig.suptitle("Lemons ")
	
	plt.subplot(211)
	plt.plot(custU,"g", label="Customer Utility to  Test")
	plt.plot(compU,"r", label="Company Utility to Respect")
	plt.ylabel("Utility")
	#plt.axis([0,100,0,6000])
	plt.legend(bbox_to_anchor=(0.5, 1), loc=2, borderaxespad=0.)

	plt.show()
play()
