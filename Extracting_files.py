import requests
#url='https://raw.githubusercontent.com/abhishek374/dream11/master/Data/ipl_scorecard_points_avg.csv'
#r = requests.get(url, allow_redirects=True)
#open('ipl_scorecard_points_avg.csv', 'wb').write(r.content)

#url='https://raw.githubusercontent.com/abhishek374/dream11/master/Data/ipl_scorecard_points.csv'
#r = requests.get(url, allow_redirects=True)
#open('ipl_scorecard_points.csv', 'wb').write(r.content)

#url='https://raw.githubusercontent.com/abhishek374/dream11/master/Data/matchdata.csv'
#r = requests.get(url, allow_redirects=True)
#open('matchdata.csv', 'wb').write(r.content)

url='https://raw.githubusercontent.com/abhishek374/dream11/master/ipl20/name_mapping_clean.csv'
r = requests.get(url, allow_redirects=True)
open('name_mapping.csv', 'wb').write(r.content)

url='https://raw.githubusercontent.com/abhishek374/dream11/master/ipl21/name_mapping_clean.csv'
r = requests.get(url, allow_redirects=True)
open('name_mapping_clean_final.csv', 'wb').write(r.content)
