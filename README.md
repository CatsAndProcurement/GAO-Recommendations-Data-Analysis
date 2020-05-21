# GAO-Recommendations-Data-Analysis
Python script to extract and analyze data from GAO on open recommendation status

Created on Wed May 20 17:56:56 2020

@author: CatsAndProcurement

The purpose of this script is to extract search-specific data from the Government Accountability Office (GAO) Recommendations Database. GAO is the primary legislative branch audit agency of the U.S. government. This database contains recommendations made in GAO reports that have still not been addressed by agencies.

This script uses Pandas (a Python math module) to categorize unaddressed recommendations by month and year and create a bar chart of the time-series data.

Sample web API call:
https://www.gao.gov/index.php?system_action=newRecommendations_results_as_csv
&rec_type=all_open
&field=rectext_t
&q=acquisition

The above sample API call pulls data on still-open recommendations with the phrase 'acquisition' appearing in the recommendation text.

Nothing in this script is endorsed by the U.S. government. None of the data that the script might extract is verified by the author; neither raw data nor conclusions drawn from the data should be interpreted as authoritative.
