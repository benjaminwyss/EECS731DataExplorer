import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.close('all')

#read csv data
populations = pd.read_csv('../data/raw/us_county_population_density.csv')
covidCases = pd.read_csv('../data/raw/us_county_covid19_cases.csv')
maskUse = pd.read_csv('../data/raw/us_county_mask_use.csv')

#clean data
populations = populations[['GEOID', 'B01001_001E', 'B01001_calc_PopDensity']]
populations = populations.rename(columns={'GEOID': 'fips_code', 'B01001_001E': 'population', 'B01001_calc_PopDensity': 'population_density'})
covidCases = covidCases[covidCases.county != 'Unknown']
covidCases = covidCases[['fips', 'county', 'state', 'cases']]
covidCases = covidCases.rename(columns={'fips': 'fips_code'})
maskUse = maskUse.rename(columns={'COUNTYFP': 'fips_code', 'NEVER': 'never', 'ALWAYS': 'always', 'RARELY': 'rarely', 'SOMETIMES': 'sometimes', 'FREQUENTLY': 'frequently'})

#merge data
df = pd.merge(populations, covidCases, on='fips_code')
df = pd.merge(df, maskUse, on='fips_code')

#transform data
df['mask_use'] = df['never'] + df['rarely'] * 2 + df['sometimes'] * 3 + df['frequently'] * 4 + df['always'] * 5
df['cases_per_population_percent'] = df['cases']/df['population'] * 100
df['never'] = df['never'] * 100
df['rarely'] = df['rarely'] * 100
df['sometimes'] = df['sometimes'] * 100
df['frequently'] = df['frequently'] * 100
df['always'] = df['always'] * 100

#grab useful columns
df = df[['fips_code', 'county', 'state', 'cases', 'population', 'population_density', 'cases_per_population_percent', 'never', 'always', 'mask_use']]

#export data
df.to_csv('../data/processed/us_county_covid_population_density_mask_use.csv')

#visualize data
print(df.describe())

df.plot.scatter(x='population_density', y='cases_per_population_percent', title='Covid-19 Cases as a Percent of Population vs Population Density')
plt.show()

df.plot.scatter(x='always', y='cases_per_population_percent', title='Covid-19 Cases as a Percent of Population vs. Percent of Individuals who Always Wear a Mask in Public')
plt.show()

df.plot.scatter(x='never', y='cases_per_population_percent', title='Covid-19 Cases as a Percent of Population vs. Percent of Individuals who Never Wear a Mask in Public')
plt.show()

df.plot.scatter(x='mask_use', y='cases_per_population_percent', title='Covid-19 Cases as a Percent of Population vs. Reported Mask Usage on a Linear 1-5 Scale')
plt.show()

df.plot.scatter(x='always', y='population_density', title='Population Density vs. Percent of Individuals who Always Wear a Mask in Public')
plt.show()

df.plot.scatter(x='never', y='population_density', title='Population Density vs. Percent of Individuals who Never Wear a Mask in Public')
plt.show()

df.plot.scatter(x='mask_use', y='population_density', title='Population Density vs. Reported Mask Usage on a Linear 1-5 Scale')
plt.show()