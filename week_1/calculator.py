#!/usr/bin/env python3

import sys

def Config(Object):
	__config = {};

	def __init__(self, filePath):
		with open(filePath) as file:
			for line in file:
				list = line.split('=')
				self.__config[list[0].strip()] = list[1].strip()
	
	def get_config(self, key)
		return self.__config[key]

def EmployeeData(Object):
	__employee = {};

	def __init__(self, filePath):
		with open(filePath) as file:
			for line in file:
				list = line.split('=')
				self.__employee[list[0].strip()] = list[1].strip()

	def calculator(self, minBase, maxBase):
		for key, value in self__employee.items():
			
			

def getSalaryAfterTax(income):
	payment = income * 0.165
	if income <= 3500:
		return format(income - payment, ".2f")	

	taxPay = income - 3500 - payment
	if taxPay <= 0 :
		return format(income - payment, ".2f")		
	elif taxPay <= 1500:
		return format(income - payment - taxPay * 0.03, ".2f")
	elif taxPay <= 4500:
		return format(income - payment - taxPay * 0.1 + 105, ".2f")
	elif taxPay <= 9000:
		return format(income - payment - taxPay * 0.2 + 555, ".2f")
	elif taxPay <= 35000:
		return format(income - payment - taxPay * 0.25 + 1005, ".2f")
	elif taxPay <= 55000:
		return format(income - payment - taxPay * 0.3 + 2755, ".2f")
	elif taxPay <= 80000:
		return format(income - payment - taxPay * 0.35 + 5505, ".2f")
	else:
		return format(income - payment - taxPay * 0.45 + 13505, ".2f")

if __name__ == '__main__':
	for arg in sys.argv[1:]:
		employee = arg.split(':')
		try:
			income = int(employee[1]);
			print(employee[0], getSalaryAfterTax(income)) 
		except:
			print(employee[0], "Parameter Error")
