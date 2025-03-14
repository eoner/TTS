# -*- coding: utf-8 -*-

"""
Numeric to word convertor in Turkish

Copyright (c) 2017 Munich Artificial Intelligence Laboratories GmbH (M-AILABS)

Created: 2017-02-25 ??:?? CET, KA

eoner: Added ordinal, percent, .5 (bucuk) handling
"""

import sys
import os
import re

_comma_number_re = re.compile(r'([0-9][0-9\.]+[0-9])')
_decimal_number_re = re.compile(r'([0-9]+\,[0-9]+)')
_ordinal_re = re.compile(r'[0-9]+\.+\s')
_ordinal_re2 = re.compile(r"([0-9])+(\'|\’)+\S*")
_ordinal_re3 = re.compile(r"[0-9]+\,5")
_number_re = re.compile(r'[0-9]+')
_percent_re=re.compile(r'\%[0-9]')

_ordinal_suffixes = [
    ("sıfır","sıfırıncı"),
    ("bir","birinci"),
    ("iki","ikinci"),
    ("üç","üçüncü"),
    ("dört","dördüncü"),
    ("beş","beşinci"),
    ("altı","altıncı"),
    ("yedi","yedinci"),
    ("sekiz","sekizinci"),
    ("dokuz","dokuzuncu"),
    ("on","onuncu"),
    ("yirmi","yirminci"),
    ("otuz","otuzuncu"),
    ("kırk","kırkıncı"),
    ("elli","ellinci"),
    ("altmış","altmışıncı"),
    ("yetmiş","yetmişinci"),
    ("seksen","sekseninci"),
    ("doksan","doksanıncı"),
    ("yüz","yüzüncü"),
    ("bin","bininci"),
    ("milyon","milyonuncu")
]
   

def _get_decimal(decimalPart):
    """
    Returns decimal part numbers with the correct word of seperator
    """
    units = [u'sıfır', u'bir', u'iki', u'üç', u'dört', u'beş', u'altı', u'yedi', u'sekiz', u'dokuz']
    comma = u'virgül'
    return ' '.join([units[int(i)] for i in decimalPart]), comma


def _num_to_words(num):
    """
    Turkish converter
    Params:
        num(int/long): number to be converted
    Returns:
        wordString  
    """
    units = ['', u'bir', u'iki', u'üç', u'dört', u'beş', u'altı', u'yedi', u'sekiz', u'dokuz']
    teens = ['', u'onbir', u'oniki', u'onüç', u'ondört', u'onbeş', u'onaltı',  u'onyedi', u'onsekiz', u'ondokuz']
    tens = ['', u'on', u'yirmi', u'otuz', u'kırk', u'elli', u'altmış', u'yetmiş', u'seksen', u'doksan']
    thousands = ['', u'bin', u'milyon', u'milyar', u'trilyon', u'katrilyon', u'kentilyon']

    words = []
    if num==0: words.append(u'sıfır')
    else:
        # Convert num to string
        numStr = '%d'%num
        numStrLen = len(numStr)
        # Get the number of group with 3 digits 
        groups = (numStrLen+2)//3
        if groups>(len(thousands)):
            return ''
        # Pad the zereos to the missing digits
        numStr = numStr.zfill(groups*3)
        for i in range(0,groups*3,3):
            h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
            g = groups-(i//3+1)
            # Add hundreds
            if h>=1:
                # In order not to say 'bir yüz'
                if h!=1:
                    words.append(units[h])
                words.append(u'yüz')
            # Add tens
            if t>1:
                words.append(tens[t])
                if u>=1: words.append(units[u])
            # Add teens
            elif t==1:
                if u>=1: words.append(teens[u])
                else: words.append(tens[t])
            # If second digit is zero
            else:
                # In order not to say 'bir bin'
                if g!=1 or u!=1:
                    if u>=1: words.append(units[u])
            # Add thousands
            if (g>=1) and ((h+t+u)>0): words.append(thousands[g])
    return ' '.join(words)


def _ntow(num):
    if type(num)!=int and type(num)!=float and type(num)!=type(int): return ''
    if type(num)==float:
        numStr = str(num)
        if '.' in numStr:
            splitNum=numStr.split('.')                
        elif ',' in numStr:
            splitNum=numStr.split(',')
        dec,comma=_get_decimal(splitNum[1])
        comma=' ' + comma + ' '            
        return _num_to_words(int(num)) + comma + dec
    return _num_to_words(num)


def _remove_commas(m):
    return m.group(1).replace('.', '')


def _expand_ordinal(m):
    num = _num_to_words(int(m.group(0)[:-2]))
    for suffix, replacement in _ordinal_suffixes:
        if num.endswith(suffix):
            return num[:-len(suffix)] + replacement+ ' '
    return num + '.'

def _replace_apostroph(m):
    if("'" in m.group(0)):
        tokens=m.group(0).split("'")
    elif("’" in m.group(0)):
        tokens=m.group(0).split("’")
    return _ntow(int(tokens[0]))+tokens[1]

def _replace_bucuk(m):
    splitNum=m.group(0).split(',')
    return _ntow(int(splitNum[0]))+' '+'buçuk'

def _replace_percent(m):
	return 'yüzde '+m.group(0)[1:]
	
def _expand_number(m):
    num_str = m.group(0)
    if ',' in num_str:
        num_str = num_str.replace(',', '.')
        num = float(num_str)
    else:
        num = int(num_str)
    return _ntow(num)


def normalize_numbers_tr(text):
    text = re.sub(_percent_re, _replace_percent, text)
    text = re.sub(_ordinal_re, _expand_ordinal, text)
    text = re.sub(_ordinal_re2, _replace_apostroph, text)
    text = re.sub(_ordinal_re3, _replace_bucuk, text)
    text = re.sub(_comma_number_re, _remove_commas, text)
    text = re.sub(_decimal_number_re, _expand_number, text)
    text = re.sub(_number_re, _expand_number, text)
    return text

