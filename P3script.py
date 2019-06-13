# Purpose of script is to provide k-anonymity, meaning that one entry can be confused with at least k others
# The second function is to obtain 1/b differential privacy by adding laplacian distribution noise to the quasi-
# identifiers to prevent an attacker from differentiating between two versions of the dataset. This prevents the
# attacker from being able to reverse engineer the simple query algorithm to deanonymize subjects. 

# library for importing / dealing with .csv files
import pandas as pd
# library for scientific computations 
import numpy as np
from scipy.stats import laplace
import warnings
warnings.filterwarnings("ignore")

#########################################################################################

# C2
# reading in the dataset and creafing a dataframe
df = pd.read_csv("heart.csv")

# masking values with new generalized value in specific range
df['age'] = df['age'].mask(df['age'].between(20,30), '20-30') \
.mask(df['age'].between(31,40), '30-40') \
.mask(df['age'].between(41,50), '40-50') \
.mask(df['age'].between(51,60), '50-60') \
.mask(df['age'].between(61,70), '60-70') \
.mask(df['age'].between(71,80), '70-80')

# masking bloodpressure values with new generalized value in specific range
df['trestbps'] = df['trestbps'].mask(df['trestbps'].between(90,120), '90-120') \
.mask(df['trestbps'].between(121,150), '120-150') \
.mask(df['trestbps'].between(151,170), '150-170') \
.mask(df['trestbps'].between(171,200), '170-200') \
.mask(df['trestbps'].between(201,230), '200-230') 

# masking cholesterol values with new generalized value in specific range
df['chol'] = df['chol'].mask(df['chol'].between(100,200), '100-200') \
.mask(df['chol'].between(201,300), '200-300') \
.mask(df['chol'].between(301,400), '300-400') \
.mask(df['chol'].between(401,500), '400-500') \
.mask(df['chol'].between(501,600), '500-600')

# uncomment below line to see new datafram structure 
# print(df.head())

# exporting resulting dataframe to csv file
df.to_csv('C2.csv', sep='\t')

#########################################################################################

# C4 
print("\nC4:")
# creating a separate dataframe 
algo1df = df
# percentage of males between age of 40-50 with cholesterol between 400 & 500
totalSexCount = algo1df['sex'].value_counts() 
totalMales = totalSexCount[1]
# querying for the subjects with the combonation of each of the criteria 
result = algo1df[algo1df['age'].str.contains('40-50') & algo1df['chol'].str.contains('200-300')]
count = result.count()
# below we calculate the percentage in comparison to the total amount of males in the sample
result = (count[0]/totalMales)*100
print(round(result, 3),"%"," of males between the age of 40-50 have cholesterol between 200 & 300", sep = '')

#########################################################################################

# C6
print("\nC6:")
algo2df = df
# percentage of males between age of 40-50 with cholesterol between 400 & 500
totalSexCount = algo2df['sex'].value_counts() 
totalMales = totalSexCount[1]
# querying for the subjects with the combonation of each of the criteria 
result = algo2df[algo2df['age'].str.contains('40-50') & algo2df['chol'].str.contains('200-300')]
result = (count[0]/totalMales)*100
# the maximum effect that a single user can have on the output of the algorithm 
# is 25.604%-25.243% = .361%
# ^ determined by manual test -> remove a subject and rerun the query
# to change the level of 1/b differential privacy, choose b with input
# larger b increases range of output for quasi-identifiers, them it harder to cross-identify
bDifferential = input("Enter an int 'b' for 1/b-differential privacy level: ")
loc, scale = 0., 0.361*float(bDifferential)
s = np.random.laplace(loc, scale, 1000)
laplaceVal = s[500]
result = result + laplaceVal
# below we calculate the percentage in comparison to the total amount of males in the sample
print(round(result, 3),"%"," of males between the age of 40-50 have cholesterol between 200 & 300", sep = '')
