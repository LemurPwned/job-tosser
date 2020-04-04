import pandas as pd
import numpy as np
import os, csv
from collections import defaultdict
import logging

class CityInfo:
    def __init__(self):

        # Make dict
        self.cities_data = {}
        self.cities_data_ascii_names = {}
        with open('worldcities.csv', encoding='utf-8') as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                self.cities_data[row[0]] = row[2:]
                self.cities_data_ascii_names[row[1]] = row[2:]

    def get_city_coord(self, city: str):
        city = city.title()
        city = city.split(',')[0]
        if city == "Cracow" or city == "Krakow":
            city = "Kraków"
        elif city == "Warszawa":
            city = "Warsaw"
        elif city == "Wroclaw":
            city = "Wrocław"
        elif city == "Helsingfors":
            city = "Helsinki"
            
        try:
            city_data = self.cities_data[city]
            return city_data[0], city_data[1]
        except:
            city_data = self.cities_data_ascii_names[city]
            return city_data[0], city_data[1]
        
def to_eur(money, currency):
    if currency == 'EUR' and currency == '€':
        return money
    elif currency == 'USD' and currency == '$':
        return money / 1.08
    elif currency == 'A$' and currency == 'AUD':
        return money / 1.80
    elif currency == 'PLN':
        return money / 4.58
    elif currency == 'kr':
        return money / 11.00
    elif currency == 'GBP' or currency == '£':
        return money / 0.88
    elif currency == 'CHF':
        return money / 1.06
    elif currency == 'CAD' or currency == 'C$':
        return money / 1.53
    elif currency == 'HUF':
        return money / 367.93
    elif currency == 'CZK':
        return money / 27.78
    elif currency == '₹' or currency == 'JPY':
        return money / 117.25
    else:
        None
    

if __name__ == "__main__":
    ci = CityInfo()

    min_low_salaries = {}
    max_high_salaries = {}

    with open('DATABASE.csv', encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        next(csvReader)
        for row in csvReader:
            salary = row[-2].strip()
            cities = row[-1]

            salary_high = row[-4]
            salary_low = row[-3]

            salary_high = int(float(salary_high))
            salary_low = int(float(salary_low))

            if salary_high == 0 or salary_low == 0:
                continue

            if row[-2] == 'PLN':

                # Per hour
                if salary_low <= 500:
                    salary_low *= 160
                if salary_high <= 500:
                    salary *= 160

                # Per day
                if salary_low > 500 and salary_low <= 2000:
                    salary_low *= 20
                if salary_high > 500 and salary_high <= 2000:
                    salary_high *= 20

                # To year
                salary_high *= 12
                salary_low *= 12

            if row[-2] == '$':
                # To year salary
                if salary_high < 1000:
                    salary_high *= 160 * 12
                if salary_low < 1000:
                    salary_low *= 160 * 12

            salary_high = to_eur(salary_high, row[-2])
            salary_low = to_eur(salary_low, row[-2])
            if salary_high == None or salary_low == None:
                continue

            for c in row[-6].split(','):
                c = c.strip()
                try:
                    latitude, longitude = ci.get_city_coord(c) 

                    try:
                        if min_low_salaries[(latitude, longitude)] > salary_low:
                            min_low_salaries[(latitude, longitude)] = salary_low
                    except:
                        min_low_salaries[(latitude, longitude)] = salary_low
                    try:
                        if max_high_salaries[(latitude, longitude)] < salary_high:
                            max_high_salaries[(latitude, longitude)] = salary_high
                    except:
                        max_high_salaries[(latitude, longitude)] = salary_high
                except KeyError as ex:
                    pass
                except Exception as ex:
                    #logging.exception("Something awful happened!")
                    pass

    db = defaultdict(list)
    for k in min_low_salaries.keys():
        db['latitude'].append(k[0])
        db['longitude'].append(k[1])
        db['salary_low'].append(min_low_salaries[k])
    df = pd.DataFrame.from_dict(db)
    df.to_csv(f'kepler_low.csv', index=False)

    db = defaultdict(list)
    for k in max_high_salaries.keys():
        db['latitude'].append(k[0])
        db['longitude'].append(k[1])
        db['salary_high'].append(max_high_salaries[k])
    df = pd.DataFrame.from_dict(db)
    df.to_csv(f'kepler_high.csv', index=False)

