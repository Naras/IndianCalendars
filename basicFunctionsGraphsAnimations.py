# import random
import transliterate
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

'''def rashiOrnakshatraFromNumber(num=1, clas='राशि'):
    noof = 8 if clas == 'राशि' else 3 # if clas == 'नक्षत्र' else 0
    if clas in ['राशि', 'नक्षत्र']:
        num = num % 12 - 1 if clas == 'राशि' else num % 27 - 1
        paadaNum = num * 9 + 1 if clas == 'राशि' else num  * 4  + 1
        sign = f'{basicDictsLists['राशि'][num]}' if clas == 'राशि' else f'{basicDictsLists['नक्षत्र'][num]}'
        signKannada = transliterate.transliterate(sign, 'kannada') # if clas in ['राशि', 'नक्षत्र'] else ''
        return sign, signKannada, paadaNum, paadaNum + noof
    else:
        raise ValueError(f'invalid parameter clas - {clas}') # return num % 108, num % 108, num % 108, num % 108 + noof'''
def rashiOrnakshatraFrom108Paada(padanum=1, clas='राशि'):
    padanum %= 108; padanum -= 1
    pada = padanum % 9 if clas == 'राशि' else padanum % 4
    signNo = padanum // 9 if clas == 'राशि' else padanum // 4
    sign = f'{basicDictsLists['राशि'][signNo]}' if clas == 'राशि' else f'{basicDictsLists['नक्षत्र'][signNo]}'
    return sign, pada + 1
def cycleRatios(list1, list2):
    # units  = [360 * 3600 / len(list1), 360 * 3600 / len(list2)]  # each list as a circle with n spokes in 360 degrees, as arc seconds
    angle1, angle2  = 360 * 3600 / len(list1), 360 * 3600 / len(list2)  # each list as a circle with len(list) spokes in 360 degrees
    secs1, secs2 = angle1 % 60, angle2 % 60
    mins1, mins2 = (angle1 // 60) % 60, (angle2 // 60) % 60
    degs1, degs2 = angle1 / 3600, angle2 // 3600
    # for one unit of angular rotation in list1, how much does the list2 rotate?
    unitRatio = len(list2) / len(list1)
    return unitRatio, angle1, degs1, mins1, secs1, angle2, degs2, mins2, secs2
def cycleMaps(list1, list2):
    map = {}
    unitRatio = len(list2) // len(list1) if len(list2) > len(list1) else len(list1) // len(list2)
    noremainder = (len(list2) % len(list1) == 0) if len(list2) > len(list1) else (len(list1) % len(list2) == 0)
    if noremainder:
        if unitRatio > 1:
            if len(list2) > len(list1):
                for i, k in enumerate(list1): map[k] = ','.join(list2[i*unitRatio:(i+1)*unitRatio])
            else:
                for i, k in enumerate(list2): map[','.join(list1[i*unitRatio:(i+1)*unitRatio])] = k
        return map
    
    # Special handling for nakshatra/rashi mapping (27/12 ratio with 108 padas)
    if set(list1) == set(basicDictsLists['नक्षत्र']) and set(list2) == set(basicDictsLists['राशि']):
        return generateNakshatraRashiMap()
    elif set(list2) == set(basicDictsLists['नक्षत्र']) and set(list1) == set(basicDictsLists['राशि']):
        return generateRashiNakshatraMap()
    
    return None
def generateNakshatraRashiMap():
    """Generate mapping from nakshatras to rashis based on 108 pada system"""
    map = {}
    nakshatras = basicDictsLists['नक्षत्र']
    rashis = basicDictsLists['राशि']
    
    # Each nakshatra spans 4 padas, each rashi spans 9 padas
    # Total 108 padas
    for i, nakshatra in enumerate(nakshatras):
        # Get the rashis that this nakshatra spans
        start_pada = i * 4
        end_pada = start_pada + 4
        
        rashis_in_nakshatra = []
        for pada in range(start_pada, end_pada):
            rashi_idx = pada // 9
            if rashi_idx < len(rashis):
                rashis_in_nakshatra.append(rashis[rashi_idx])
        
        # Remove duplicates while preserving order
        unique_rashis = list(dict.fromkeys(rashis_in_nakshatra))
        map[nakshatra] = ','.join(unique_rashis)
    
    return map
def generateRashiNakshatraMap():
    """Generate mapping from rashis to nakshatras based on 108 pada system"""
    map = {}
    nakshatras = basicDictsLists['नक्षत्र']
    rashis = basicDictsLists['राशि']
    
    # Each rashi spans 9 padas, each nakshatra spans 4 padas
    for i, rashi in enumerate(rashis):
        # Get the nakshatras that this rashi spans
        start_pada = i * 9
        end_pada = start_pada + 9
        
        nakshatras_in_rashi = []
        for pada in range(start_pada, end_pada):
            nakshatra_idx = pada // 4
            if nakshatra_idx < len(nakshatras):
                nakshatras_in_rashi.append(nakshatras[nakshatra_idx])
        
        # Count occurrences
        from collections import Counter
        counts = Counter(nakshatras_in_rashi)
        
        # Format as "nakshatra:count,nakshatra:count,..."
        formatted = []
        for nakshatra in nakshatras_in_rashi:
            if nakshatra not in [x.split(':')[0] for x in formatted]:
                formatted.append(f"{nakshatra}:{counts[nakshatra]}")
        
        map[rashi] = ','.join(formatted)

    return map

concepts = {'कोश':['राशि', 'नक्शत्र', 'काल', 'आकाश', 'ऋतु', 'ग्रह', 'वर्ष', 'मास', 'वासर', 'वार', 'रात्रि', 'घंट', 'निमिष']}
basicDictsLists = {
'ग्रह':['सूर्य', 'चंद्र', 'मंगळ', 'बुध', 'गुरु', 'शुक्र', 'शनि', 'राहु', 'केतु'],
'नक्षत्र':['अश्विनि', 'भरणि', 'कृत्तिक', 'रोहिणि', 'मृगशिर', 'आरिद्र', 'पुनर्वसु', 'पुष्य', 'आश्लेष', 'मखा', 'पूर्वफल्गुणि', 'उत्तरफल्गुणि', 'हस्त', 'चित्र', 'स्वाति', 'विशाख', 'अनुराध', 'जेष्ट', 'मूल', 'पूर्वाषाढ', 'उत्तराषाढ', 'श्रावण', 'धनिष्ट', 'शतभिष', 'पूर्वाभाद्र', 'उत्तराभाद्र', 'रेवति'],
'राशि':['मेष', 'वृषभ', 'मिथुन', 'कर्काटक', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन'],
'वार':[ 'रविवार', 'सोमवार', 'मंगलवार', 'बुधवार', 'गुरुवार', 'शुक्रवार', 'शनिवार'],
'तिथि':['प्रतिपाद', 'द्वितीय', 'तृतीय', 'चतुर्थि', 'पंचमि', 'षष्टि', 'सप्तमि', 'अष्टमि', 'नवमि', 'दशमि', 'एकादशि', 'द्वादशि', 'त्रयोदशि', 'चतुर्दशि', 'पूर्णिम/अमावास्य'],
'पक्ष':['शुक्ल', 'कृष्ण'],
'मास':['चैत्र', 'वैशाख', 'जेष्ट', 'आषाढ', 'श्रावण', 'भाद्रपद', 'आश्विन', 'कार्तिक', 'अग्रहायण', 'पौष', 'माघ', 'फाल्गुण'],
'ऋतु':['वसंत', 'ग्रीष्म', 'वर्ष', 'शरद्', 'हेमंत', 'शिशिर'],
# other mappings
'अधिपति':{'सूर्य':['सिंह'], 'चंद्र':['कर्कातक'], 'मंगळ':['मेष','वृश्चिक'], 'बुध':['कन्या','मिथुन'], 'गुरु':['धनु','मीन'], 'शुक्र':['वृषभ','तुला'], 'शनि':['कुंभ', 'मीन']},
'भूत':['अग्नि', 'पृथ्वि', 'वायु', 'जल'], 'तत्त्व':['सर', 'स्थिर', 'उभय'],
'Elements':['Fire', 'Earth', 'Air', 'Water'], 'Types':['Mutable', 'Fixed', 'Dual'],
'Zodiac':['Aries', 'Taurus',' Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'],
'Planets':['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Ascending Lunar Node', 'Descending Lunar Node'],
'Days': ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
}
basicDictsLists['शुक्ल तिथि'], basicDictsLists['कृष्ण तिथि'] = (['शुक्ल ' + item for item in basicDictsLists['तिथि'][:-1]] + ['पूर्णिम'], ['कृष्ण ' + item for item in basicDictsLists['तिथि'][:-1]] + ['अमावास्य'])
basicDictsLists['शुक्ल च कृष्णा तिथियाँ'] = basicDictsLists['शुक्ल तिथि'] + basicDictsLists['कृष्ण तिथि']
def mappables(argk, argv):
    mappable = {'वार':['ग्रह', 'तिथि', 'शुक्ल च कृष्णा तिथियाँ', 'Days'], 'राशि':['नक्षत्र', 'Zodiac', 'Planets', ], 'पक्ष':['शुक्ल च कृष्णा तिथियाँ'],
                'तिथि':['शुक्ल च कृष्णा तिथियाँ', 'वार'], 'ऋतु':['मास'], 'भूत':['राशि'], 'तत्त्व':['राशि'],
                'ग्रह':['Planets', 'Zodiac', 'राशि'], 'Planets':['Zodiac', 'राशि', 'ग्रह'],
                'भूत':['Elements', 'Zodiac', 'राशि'], 'तत्त्व':['Types', 'Zodiac', 'राशि'],
                }
    if argk in mappable.keys() and argv in mappable[argk]: return True, basicDictsLists[argk], basicDictsLists[argv]
    elif argv in mappable.keys() and argk in mappable[argv]: return True, basicDictsLists[argk], basicDictsLists[argv]
    elif argk == argv: return True, basicDictsLists[argk], basicDictsLists[argv]
    return False, None, None
