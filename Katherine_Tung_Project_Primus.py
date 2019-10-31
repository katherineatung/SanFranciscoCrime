"""
Name: Katherine Tung
Block: G
Date: 10/18/19

Project Primus

Description: This program contains several plots regarding vandalism and drugs in the
Tenderloin district of San Francisco. Plots described in comments below.

"""


import pandas as pd
import matplotlib.pyplot as plt

sf_crime = pd.read_csv("SFCrime__2018_to_Present.csv")
sf_district = pd.read_csv("SF_Police_Districts.csv")
sf_crime_old = pd.read_csv("SFCrime_2003_to_May_2018.csv")

sf_crime = sf_crime[sf_crime['Police District'] != 'Out of SF']

# Throw out an outlier - the location of the crime doesn't appear to be the Tenderloin.
# -122.44 is appx boundary point for longitude
tenderloin = sf_crime[(sf_crime["Police District"] == "Tenderloin") & (sf_crime['Longitude'] > -122.44)]
tloin_old = sf_crime_old[(sf_crime_old["PdDistrict"] == "TENDERLOIN")]
tenderloin_vandalism_old = tloin_old[tloin_old['Category'] == 'VANDALISM']
tenderloin_drugs_old = tloin_old[tloin_old['Category'] == 'DRUG/NARCOTIC']
crime_2010 = sf_crime_old[sf_crime_old['Date'].str.contains('2010')]
vandalism_2010 = crime_2010[ crime_2010['Category'] == 'VANDALISM']
drugs_2010 = crime_2010[ crime_2010['Category'] == 'DRUG/NARCOTIC']

# Plots crime per unit (e.g., crime per capita, crime per square mile) for each police district in San Francisco.
# x axis plots police districts, y axis plots crimes per unit
def crime_per_unit(data_frame, div_by, title, ylabel):
    counts_per_unit = data_frame['IncidntNum'].div(data_frame[div_by])
    plt.bar(x=data_frame['PdDistrict'], height=counts_per_unit)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("SF Police Districts")
    plt.show()

# Plots number of crimes for each police district in San Francisco.
# x axis plots police districts, y axis plots number of crimes
def basic_crime_barchart(data_frame, title, ylabel):
    ax = data_frame.plot.bar(y='IncidntNum')
    ax.get_legend().remove()
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("SF Police Districts")
    plt.show()

# Plots number of crimes for each police district in San Francisco for each of the top 5
# categories of crime in the form of a stacked bar chart.
# x axis plots police districts, y axis plots number of crimes for top 5 crime categories
def crime_subcat_stacked_barchart(crime_cat, top_5, title, ylabel):
    cat_of_crime = sf_crime[sf_crime['Incident Subcategory'].notnull() &
                            sf_crime['Incident Subcategory'].str.contains(crime_cat)]
    description = cat_of_crime.groupby(['Police District', 'Incident Description'])['Police District'].count().unstack()
    description[top_5].plot.bar(stacked=True)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("SF Police Districts")
    plt.show()

# Plots crimes by location in the form of a heat map.
def heatmap_crime_location(data_frame, title):
    fig = plt.figure()
    # hardcoded coordinates reflect approximate boundaries of Tenderloin district
    # grid size set manually for optimal appearance of heat map
    ax = plt.hexbin(x=data_frame['X'], y=data_frame['Y'], gridsize=20,
                    extent=(-122.42, -122.4, 37.772, 37.788))
    plt.title(title)
    fig.colorbar(ax)
    plt.show()

# Plots crimes by hour in a bar chart.
def crime_by_hour(data_frame, title, ylabel):
    data_frame.loc[:, 'Time'] = pd.to_datetime(data_frame['Time'])
    data_frame = data_frame.set_index(['Time'])
    xvalues = data_frame.groupby(pd.Grouper(freq='h')).count()['X']  # group by hour
    ax = xvalues.plot(kind='bar')
    data_frame.rename_axis("Hours")
    plt.title(title)
    # the date and time used to be separated by a space
    ax.set_xticklabels([t.get_text().split()[1] for t in ax.get_xticklabels()])
    plt.ylabel(ylabel)
    plt.show()

#group, merge vandalism data from 2010
grouped_vandalism_incidents_2010 = vandalism_2010.groupby('PdDistrict').count()
sf_district['PdDistrict'] = sf_district['PdDistrict'].str.upper() #turns district names to all caps for data merging
merged_vandalism_data_2010 = sf_district.merge(grouped_vandalism_incidents_2010, left_on='PdDistrict',
                                               right_on='PdDistrict', sort=True)
#2010 Vandalism Crimes per Land Mass
crime_per_unit(merged_vandalism_data_2010, 'Land Mass', "2010 Vandalism Crimes per Square Mile in each District",
               "Vandalism Crimes per Square Mile")


#2010 Vandalism Crimes per Person
crime_per_unit(merged_vandalism_data_2010, 'Population', "2010 Vandalism Crimes per Capita in each District",
               "Vandalism Crimes per Capita")


#2010 Vandalism Crimes
basic_crime_barchart(grouped_vandalism_incidents_2010, "2010 Vandalism Crimes in each District", "Vandalism Crimes")


#group, merge drug data from 2010
grouped_drug_incidents_2010 = drugs_2010.groupby('PdDistrict').count()
merged_drug_data_2010 = sf_district.merge(grouped_drug_incidents_2010, left_on='PdDistrict',
                                          right_on='PdDistrict', sort=True)
#2010 Drug Offenses per Land Mass
crime_per_unit(merged_drug_data_2010, 'Land Mass', "2010 Drug Offenses per Square Mile in each District",
               "Drug Offenses per Square Mile")


#2010 Drug Offenses per Person
crime_per_unit(merged_drug_data_2010, 'Population', "2010 Drug Offenses per Capita in each District",
               "Drug Offenses per Square Mile")


#2010 Drug Offenses
basic_crime_barchart(grouped_drug_incidents_2010, "2010 Drug Offenses in each District", "Drug Offenses")


#2018-Present Vandalism Crimes in each District
top_5_vandalism = ['Malicious Mischief, Vandalism to Property',
         'Malicious Mischief, Vandalism to Vehicle',
         'Malicious Mischief, Breaking Windows',
         'Malicious Mischief, Graffiti, Real or Personal Property',
         'Vehicle, Tampering']

crime_subcat_stacked_barchart('Vandalism', top_5_vandalism, '2018-Present Vandalism Crimes in each District',
                              'Vandalism Crimes')


#2018-Present Drug Offenses in each District
top_5_drugs = ['Narcotics Paraphernalia, Possession of',
         'Cocaine, Base/rock, Possession For Sale',
         'Methamphetamine Offense',
         'Heroin, Possession For Sale',
         'Methamphetamine, Possession For Sale']

crime_subcat_stacked_barchart('Drug', top_5_drugs, '2018-Present Drug Offenses in each District',
                              'Drug Offenses')


#2003-May 2018 Vandalism Incidents by Location in Tenderloin
heatmap_crime_location(tenderloin_vandalism_old, "Vandalism Incidents by Location in Tenderloin, 2003-May 2018")

#2003-May 2018 Drug Offenses by Location in Tenderloin
heatmap_crime_location(tenderloin_drugs_old, "Drug Offenses by Location in Tenderloin, 2003-May 2018")


#2003-May 2018 Vandalism cases in Tenderloin, by hour.
crime_by_hour(tenderloin_vandalism_old, "Vandalism Incidents by Hour in Tenderloin, 2003-May 2018", "Vandalism incidents")


#2003-May 2018 Drug cases in Tenderloin, by hour.
crime_by_hour(tenderloin_drugs_old, "Drug Offenses by Hour in Tenderloin, 2003-May 2018", "Drug Offenses")


input()