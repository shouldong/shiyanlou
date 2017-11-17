#!/usr/bin/env python3

import sys

if __name__ == '__main__':
	try:
		taxSalary = int(sys.argv[1]) - 3500
		if taxSalary <= 1500:
			print(format(taxSalary*0.03,".2f"))
		elif taxSalary <= 4500:
			print(format(taxSalary*0.1 - 105,".2f"))
		elif taxSalary <= 9000:
			print(format(taxSalary*0.2 - 555,".2f"))
		elif taxSalary <= 35000:
			print(format(taxSalary*0.25 - 1005,".2f"))
		elif taxSalary <= 55000:
			print(format(taxSalary*0.3 - 2755,".2f"))
		elif taxSalary <= 80000:
			print(format(taxSalary*0.35 - 5505,".2f"))
		else:
			print(format(taxSalary*0.45 - 13505,".2f"))
	except: 
		print("Parameter Error")
