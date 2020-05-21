# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:56:56 2020

@author: CatsAndProcurement

The purpose of this script is to extract search-specific data from the
Government Accountability Office (GAO) Recommendations Database.
GAO is the primary legislative branch audit agency of the U.S. government.
This database contains recommendations made in GAO reports that have still 
not been addressed by agencies.

This script uses Pandas (a Python math module) to categorize unaddressed
recommendations by month and year and create a bar chart of the time-series
data.

Sample web API call:
https://www.gao.gov/index.php?system_action=newRecommendations_results_as_csv
&rec_type=all_open
&field=rectext_t
&q=acquisition

"""

# Pandas lets us do fancy calculations
import pandas as pd
# Datetime lets us convert date strings into integers and print today's date
import datetime as dt
from datetime import date
# Calendar lets us convert some date info to plain English text
import calendar

# Describes for the user what the code is supposed to do
print("\n"
      "Hi! This Python script will extract data from the Government"+
      " Accountability Office (GAO) Recommendations Database. GAO is the"+
      " primary legislative branch audit agency of the U.S. government."+
      " This database contains recommendations made in GAO reports that"+
      " have still not been addressed by agencies."
      "\n")

# Asks the user for a search term
callTerm = input("Please input a search term (or just hit Enter and "+
                 "the script will automatically search for acquisition-"+
                 "related recommendations): ")
print("\n")

# If no search term entered, searches the word 'acquisition' by default
if callTerm == "":
    callTerm = "acquisition"
else:
    callTerm = callTerm

# Builds the web API call using the user input or the word 'acquisition'
callURL = ("https://www.gao.gov/index.php?system_action=newRecommendations_results_as_csv"+
           "&rec_type=all_open"+
           "&field=rectext_t"+
           "&q="+callTerm)

# Lets the user know where their data is coming from
print("\nAccessing data from: \n" + callURL)

# Pulls specified data from GAO.gov into a Pandas dataframe
# We need to skip 5 rows because for some reason GAO's data starts on row 6
dfGAO = pd.read_csv(callURL,skiprows=5)
# Prints out the column headers so we can see the data we're working with
#print(dfGAO.columns)
# Prints out the publication issue dates so we can see the data structure
#print(dfGAO["Date Publication Issued"])

# Adds column with year and month ('YYYY-MM') to dataframe
# The str[:7] command just pulls out the first 7 characters of the original
# date variable, which are standardized as YYYY-MM
dfGAO["Year and Month"] = dfGAO["Date Publication Issued"].astype(str).str[:7]
#print(dfGAO["Year and Month"])

# Adds integer columns for year and month to the dataframe
dfGAO["Year"] = pd.to_numeric(dfGAO["Year and Month"].str[:4])
dfGAO["Month"] = pd.to_numeric(dfGAO["Year and Month"].str[-2:])
# Adds a simple column for us to count all recommendations later on
dfGAO["Number of Open Recommendations"] = 1

# Creates a new dataframe with only lowest available year
dfGAOmin = dfGAO[dfGAO.Year == dfGAO["Year"].min()].reset_index(drop=True)
# Creates dataframe with only highest available year
dfGAOmax = dfGAO[dfGAO.Year == dfGAO["Year"].max()].reset_index(drop=True)
# Stores the highest and lowest year/month information
minYear = dfGAO["Year"].min()
minMonth = dfGAOmin["Month"].min()
maxYear = dfGAO["Year"].max()
maxMonth = dfGAOmax["Month"].max()
# The reason we need the two dataframes above is to determine what are the 
# earliest and latest months in the earliest and latest years, respectively

# Summarizes data pull in English
currentDate = date.today()
print("\nCalculations based on GAO recommendations that have not reportedly "+
      "been addressed as of "+currentDate.strftime("%B %d, %Y")+".\n")

# Creates a new dataframe that we'll use to chart the FR notices for each
# YYYY-MM in the date range specified by the user
dfGAOPvt = pd.DataFrame(columns=("Year and Month","Number of Open Recommendations"))

# If earliest year is too early, sets it at 5 years prior to latest year
if minYear <= maxYear - 3:
    minYear = maxYear - 3
    minMonth = maxMonth + 1
else:
    minYear = minYear
    minMonth = minMonth

# This loop cycles through each possible YYYY-MM combination, min to max
# It inserts data into the dfGAOPvt dataframe, adding the number of open
# recommendations from each possible YYYY-MM
for y in range (minYear,maxYear+1):
    # If y is the initial year, starts the annual loop on selected month
    if y == minYear:
        startMonth = minMonth
    # If y isn't the initial year, starts the annual loop in January
    else:
        startMonth = 1
    # If y is the final year, ends the annual loop on selected month
    if y == maxYear:
        endMonth = maxMonth
    # If y isn't the final year, ends the annual loop in December
    else:
        endMonth = 12
    # Annual loop that cycles through each month in each year
    for m in range (startMonth,endMonth+1):
        # Creates variable for every YYYY-MM in the target range
        loopYearMonth = str("%04d" % y) + "-" + str("%02d" % m)
        # Counts the notices for each YYYY-MM variable in the dfFR dataframe
        sumYearMonth = dfGAO.loc[dfGAO["Year and Month"] == loopYearMonth,
                                "Number of Open Recommendations"].sum()
        # Creates a new row to add to the pivot dataframe
        appendRow = {"Year and Month":loopYearMonth,"Number of Open Recommendations":sumYearMonth}
        # Adds the new row to the pivot dataframe
        dfGAOPvt = dfGAOPvt.append(appendRow,ignore_index=True)

# Finding the minimum month and year again to address them in text
minYear = dfGAO["Year"].min()
minMonth = dfGAOmin["Month"].min()
# Using calendar module to find month name and creating phrase with year
minMonthYear = calendar.month_name[minMonth] + " " + str(minYear)

# Brief description of data and chart
print("\n"+minMonthYear+" was the earliest point at which GAO reportedly issued "+
      "one or more recommendations directly related to "+callTerm+" that "+
      "are still unaddressed. "+
      "The following chart displays the number of GAO's recent unaddressed "+
      "recommendations, by year and month of original issuance, for which "
      "the term '"+callTerm+"' appears in the recommendation text.\n")
# Creates a bar chart to visualize open GAO recommendations over time
dfGAOPvt.plot.bar(x="Year and Month",
                  y="Number of Open Recommendations",
                  title=("GAO's unaddressed recommendations related to "
                         +callTerm+", by year and month of issuance"),
                  figsize=(12,6))



