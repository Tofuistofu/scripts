#!/usr/bin/env python

''' horoscope.py: Checks horoscope for the current day from astrology.com given an inputted birth date'''

import sys
import requests
from bs4 import BeautifulSoup

def Zodiac(birthday):
    # Returns zodiac sign given a birthday in form mm-dd
    Zodiac = [ 'aquarius', 'pisces', 'aries', 'taurus', 'gemini', 'cancer',
               'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricon']
    CutOffDay = { '01': 20, '02': 19, '03': 21, '04': 20, '05': 21, '06': 21,
                  '07': 23, '08': 23, '09': 23, '10': 23, '11': 22, '12': 19 }
    month, day = birthday.split('-')
    if int(day) < CutOffDay[month]:
        zodiacsign = Zodiac[int(month)-2] #adjusted to fit list
    else:
        zodiacsign = Zodiac[int(month)-1]
    return zodiacsign

def Horoscope(zodiacsign):
    # Returns today's horoscope for given zodiac sign
    url = 'http://www.astrology.com/horoscope/daily/%s.html' % sign
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    textelem = soup.select('.page-horoscope-text')
    text = textelem[0].getText()
    return text

if __name__ == '__main__':
    try:
        sign = Zodiac(sys.argv[1])
        print 'Your horoscope for today is: \n\n' + Horoscope(sign)         
    except IndexError:
        birthday = raw_input('Enter your birthday (mm-dd) ie. 01-03:')
        sign = Zodiac(birthday)
        print 'Your horoscope for today is: \n\n' + Horoscope(sign) 


