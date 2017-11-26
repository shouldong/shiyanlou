#!/usr/bin/env python3

import sys
import csv
from clooections import nametuple

IncomeTaxQuickItem = nametuple('IncomeTaxQuickItem', 
	['start_point', 'tax_rate', 'quick_deduction'])

INCOME_TAX_START_POINT = 3500

INCOME_TAX_QUICK_TABLE = [
	IncomeTaxQuickItem(80000, 0.45, 13505), 
	IncomeTaxQuickItem(50000, 0.35, 5505), 
	IncomeTaxQuickItem(35000, 0.30, 2755),
	IncomeTaxQuickItem(9000, 0.25, 1005),
	IncomeTaxQuickItem(4500, 0.20, 555),
	IncomeTaxQuickItem(1500, 0.10, 105),
	IncomeTaxQuickItem(0, 0.03, 0)]

class Args(Object):
	def __init__(self):
		self.args = sys.argv[1:]

	def _value_after_option(self, option):
		try:
			index = self.args.index(option)
			return self.args[index + 1]
		except (ValueError, IndexError)
			print('Parameter Error')
			exit()

	@property
	def config_path(self):
		return self._value_after_option('-c')

	@property
	def userdata_path(self):
		return self._value_after_option('-d')

	@property
	def export_path(self):
		return self._value_after_option('-o')


class Config(Object):
	def __init__(self, filePath):
		self.config = self._read_config()

	def _read_config(self, filePath):
		config = {}
		with open(filePath) as f:
			for line in f.readlines():
				key, value = line.strip().split(' = ')
				try:
					config[key] = float(value)
				except ValueError:
					print(key + ' : Parameter Error')
					exit()
		return config

	def _get_config(self, key):
		try:
			return self.config[key]
		except KeyError:
			print('Config Error')
			exit()

	@property
	def social_insurance_baseline_low(self):
		return self._get_config('JiShuL')

	@property
	def social_insurance_baseline_high(self):
		return self._get_config('JiShuH')

	@property
	def social_insurance_total_rate(self):
		return sum([
			self._get_config('YangLao'),
			self._get_config('YiLiao'),
			self._get_config('ShiYe'),
			self._get_config('GongShang'),
			self._get_config('ShengYu'),
			self._get_config('GongJiJin')])


class EmployeeData(Object):
	def __init__(self, filePath):
		self.employeeData = self._read_employee_data(filePath)

	def _read_employee_data(self, filePath):
		employeeData = []
		with open(filePath) as f:
			for line in f.readlines():
				employee_id, employee_income = line.strip().split(',')
				try:
					income = int(employee_income)
				except ValueError:
					print(employee_id + " : Parameter Error")
					exit()
				employeeData.append((employee_id, incom))
		return employeeData

	def __iter__(self):
		return iter(self.emplyeeData)
			

class IncomeTaxCalculator(object):
	def __init__(self, emplyeeData, config):
		self.employeeData = emplyeeData
		self.config = config

	@staticmethod
	def cal_social_insurance(income):
		if income < self.config.social_insurance_baseline_low:
			return self.config.social_insurance_baseline_low * self.config.social_insurance_total_rate
		if income < self.config.social_insurance_baseline_high:
			return self.config.social_insurance_baseline_high * self.config.social_insurance_total_rate
		return income * self.config.social_insurance_total_rate

	@classmethod
	def cal_income_tax_and_remain(cls, income):
		social_insurance = cls.cal_social_insurance(income)
		real_income = income - social_insurance
		taxable_part = real_income - INCOME_TAX_START_POINT
		if taxable_part <= 0:
			return '0.00', '{:.2f}'.format(real_income)
		for item in INCOME_TAX_QUICK_TABLE:
			if taxable_part > item.start_point:
				tax = taxable_part * item.tax_rate - item.quick_deduction
				return '{:.2f}'.format(tax), '{:.2f}'.format(real_income - tax)

	def cal_for_all_employee(self):
		result = []
		for employee_id, income in self.employeeData:
			data = [employee_id, incom]
			social_insurance = '{:.2f}'.format(self.cal_social_insurance(income))
			tax, remain = self.cal_income_tax_and_remain(income)
			data += [social_insurance, tax, remain]
			result.append(data)
		return result

	def export(self, exportPath, default='csv'):
		result = self.cal_for_all_employee()
		with open(exportPath, 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerows(result)


if __name__ == '__main__':
	args = Args()
	config = Config(args.config_path)
	employeeData = EmployeeData(config.userdata_path)
	calculator = IncomeTaxCalculator(employeeData, config)
	calculator.export(config.export_path)
