import numpy as np 
import csv
import operator

# 13-17
# 18-24
# 25-35
# 35-65
# 65-80
# >75

# Countries
users_file = 'profiles.csv'
countries = {'Brazil': 1, 'Canada': 1, 'Italy': 1, 'Czech Republic': 1, 'India': 1, 'Lithuania': 1, 'Costa Rica': 1, 'France': 1, 
'Slovakia': 1, 'Ireland': 1, 'Argentina': 1, 'Norway': 1, 'Thailand': 1, 'Israel': 1, 'Australia': 1, 'Indonesia': 1, 
'Singapore': 1, 'Venezuela': 1, 'Malaysia': 1, 'Slovenia': 1, 'Germany': 1, 'Chile': 1, 'Belgium': 1, 'China': 1, 
'Philippines': 1, 'Poland': 1, 'Spain': 1, 'Ukraine': 1, 'Netherlands': 1, 'Denmark': 1, 'Turkey': 1, 'Finland': 1, 
'United States': 1, 'Russian Federation': 1, 'Sweden': 1, 'Latvia': 1, 'Croatia': 1, 'Hungary': 1, 'Switzerland': 1, 
'Belarus': 1, 'New Zealand': 1, 'Bulgaria': 1, 'Romania': 1, 'Estonia': 1, 'Portugal': 1, 'Mexico': 1, 'South Africa': 1, 
'Serbia': 1, 'Peru': 1, 'United Kingdom': 1, 'Iceland': 1, 'Austria': 1, 'Colombia': 1, 'Greece': 1, 'Japan': 1}

teen_female = []
teen_male = []
young_female = []
young_male = {}
young_unsp = []
late_twenties_female = []
late_twenties_male = []
old_female = []
old_male = []
older_female = []
older_male = []
oldest_female = []
oldest_male = []

with open(users_file, 'r') as users_fh:
    users_csv = csv.reader(users_fh, delimiter=',', quotechar='"')
    next(users_csv, None)
    for row in users_csv:
        user_hash = row[0]
        gender = row[1]
        age = 0
        country = row[3]
        if not row[2] == '':
            age = int(row[2])
        if gender == 'f' and age in xrange(13,18):
            teen_female.append(user_hash)
        if gender == 'm' and age in xrange(13,18):
            teen_male.append(user_hash)
        if gender == 'f' and age in xrange(18,25):
            young_female.append(user_hash)
        if gender == 'm' and age in xrange(18,25):
            young_male[user_hash] = 1
        if gender == '' and age in xrange(18, 25):
            young_unsp.append(user_hash)
        if gender == 'f' and age in xrange(25, 35):
            late_twenties_female.append(user_hash)
        if gender == 'm' and age in xrange(25, 35):
            late_twenties_male.append(user_hash)
        if gender == 'f' and age in xrange(35, 65):
            old_female.append(user_hash)
        if gender == 'm' and age in xrange(35, 65):
            old_male.append(user_hash)
        if gender == 'f' and age in xrange(65, 80):
            older_female.append(user_hash)
        if gender == 'f' and age >= 80:
            oldest_female.append(user_hash)
        if gender == 'm' and age >= 80:
            oldest_male.append(user_hash)


        
print len(young_male)


sorted_countries = [('United States', 48944), ('United Kingdom', 22681), ('Germany', 20214), ('Poland', 12054), ('Sweden', 9922), ('Brazil', 9488), ('Russian Federation', 8263), ('Spain', 8180), ('Finland', 7825), ('Netherlands', 6891), ('Canada', 6165), ('Australia', 5477), ('Italy', 4517), ('France', 4380), ('Norway', 4080), ('Turkey', 3549), ('Mexico', 3086), ('Czech Republic', 2784), ('Belgium', 2649), ('Portugal', 2400), ('Austria', 2061), ('Switzerland', 2033), ('Denmark', 1899), ('Ukraine', 1842), ('Romania', 1813), ('Bulgaria', 1753), ('Chile', 1717), ('Japan', 1648), ('Argentina', 1622), ('Ireland', 1279), ('Croatia', 1269), ('Latvia', 1212), ('Lithuania', 1193), ('Colombia', 1149), ('Greece', 1147), ('Hungary', 1033), ('New Zealand', 961), ('Slovakia', 957), ('Serbia', 800), ('Israel', 782), ('Estonia', 743), ('India', 647), ('Belarus', 524), ('South Africa', 488), ('China', 483), ('Venezuela', 479), ('Slovenia', 440), ('Philippines', 388), ('Singapore', 330), ('Indonesia', 318), ('Peru', 292), ('Iceland', 291), ('Thailand', 275), ('Malaysia', 228), ('Costa Rica', 215)]
sorted_countries_trunc = sorted_countries[:10]

#print sorted_countries_trunc
