import os
import datetime
import json
import requests
import dotenv
from lxml import html
import matplotlib.pyplot as plt
import drawsvg as draw
import pygame as pg

# --- Rainfall Chart Plotting ---
import ast

def load_rainfall_data(xml_path):
	"""
	Parse the rainfall (RF) data from monthlyElement.xml.
	Returns: years (list of str), rainfall (list of list of float or None)
	"""
	with open(xml_path, 'r', encoding='utf-8') as f:
		content = f.read()
	# Find the RF section
	start = content.find('"code":"RF"')
	if start == -1:
		raise ValueError('Rainfall data (RF) not found in file.')
	# Find the monthData array for RF
	monthdata_start = content.find('"monthData":[', start)
	if monthdata_start == -1:
		raise ValueError('monthData not found for RF.')
	# Find the end of the monthData array
	bracket_count = 0
	i = monthdata_start + len('"monthData":[')
	while i < len(content):
		if content[i] == '[':
			bracket_count += 1
		elif content[i] == ']':
			if bracket_count == 0:
				break
			bracket_count -= 1
		i += 1
	monthdata_str = content[monthdata_start + len('"monthData":'):i+1]
	# Convert to Python list
	monthdata = ast.literal_eval(monthdata_str)
	years = []
	rainfall = []
	for row in monthdata:
		year = row[0]
		vals = []
		for v in row[1:]:
			v = v.strip()
			if v in ("Trace", "", "***"):  # treat as 0 or None
				vals.append(0.0)
			else:
				try:
					vals.append(float(v))
				except Exception:
					vals.append(0.0)
		years.append(year)
		rainfall.append(vals)
	return years, rainfall

def plot_rainfall_for_year(xml_path, year):
	"""
	Plot the monthly rainfall for a given year from the xml file.
	"""
	years, rainfall = load_rainfall_data(xml_path)
	if year not in years:
		raise ValueError(f"Year {year} not found in rainfall data.")
	idx = years.index(year)
	months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	plt.figure(figsize=(10,5))
	plt.bar(months, rainfall[idx], color='royalblue')
	plt.title(f"Monthly Rainfall in Hong Kong ({year})")
	plt.xlabel("Month")
	plt.ylabel("Rainfall (mm)")
	plt.tight_layout()
	plt.show()


if __name__ == "__main__":
	# Change the year as needed, or make this interactive
	try:
		plot_rainfall_for_year('monthlyElement.xml', '2023')
	except Exception as e:
		print(f"Error: {e}")
