from basicFunctionsGraphsAnimations import *
if __name__ == '__main__':
    for k, v in basicDictsLists.items():
        if not k.isascii():
            strngVar = f'   देवनागरी             ಕನ್ನಡ            IAST          ITRANS\n{"-" * 15} {"-" * 15} {"-" * 15} {"-" * 15}'
            for text in v:
                strngVar += (f'\n{text:^15} {transliterate.transliterate(text, 'kannada'):^15} {transliterate.transliterate(text, 'IAST'):^15} {transliterate.transliterate(text, 'ITRANS'):^15}')
            print(f'\n{k:^55}\n{strngVar}')
    print(f'\npaada     Result\n{"-" * 5} {"-" * 15} ')
    for paada in range(1,11):
        # paada = random.randint(1,1000)
        print(f'{paada:^5} {rashiOrnakshatraFrom108Paada(paada)} {rashiOrnakshatraFrom108Paada(paada, 'नक्षत्र')}')
    nakshatras, rashis = [], {}
    for rashi in range(12):
        dictionary = {}
        for paada in range(1,10):
            rashii,rashiPada = rashiOrnakshatraFrom108Paada(paada + rashi*9)
            nakshatra,nakshatraPada = rashiOrnakshatraFrom108Paada(paada + rashi*9, 'नक्षत्र')
            if nakshatra in dictionary: dictionary[nakshatra] += f'{nakshatraPada}'
            else: dictionary[nakshatra] = f'{nakshatraPada}'
            # print(f'p {paada} r {rashi} {rashii} {rashiPada} {nakshatra} {nakshatraPada} {dic}')
            nakshatras.append(f'{rashii}:{rashiPada}-{nakshatra}:{nakshatraPada}')
        rashis[basicDictsLists['राशि'][rashi]] = dictionary
    # print(f'rashi & nakshatra by paada {nakshatras}\nrashis span nakshatras {rashis}')
    rashis2 = {}
    for k,v in rashis.items():
        dictionary = {}
        for k2, v2 in v.items():
            dictionary[transliterate.transliterate(k2,'kannada')] = len(v2)
        rashis2[transliterate.transliterate(k,'kannada')] = dictionary
    print(f'rashi & nakshatra by paada {nakshatras}\nrashis span nakshatras {rashis}\n...................... {rashis2}')

print('cycle Ratios\n          ratio, angle, degrees, mins, secs, angle, degrees, mins, secs')
for pairs in [["ऋतु","मास"], ["राशि","मास"], ["राशि","नक्षत्र"], ["तिथि","नक्षत्र"], ["वार", "तिथि"]]:
    if mappables(pairs[0], pairs[1]): print(f'{pairs[0]}:{pairs[1]}: {cycleRatios(basicDictsLists[pairs[0]], basicDictsLists[pairs[1]])}')
    else: print(f'{pairs[0]} incompatible with {pairs[1]}')

print(f'पक्ष:मास: {cycleRatios(basicDictsLists["पक्ष"], basicDictsLists["शुक्ल च कृष्णा तिथियाँ"])}\n'
      f'वार:मास {cycleRatios(basicDictsLists["वार"], basicDictsLists["शुक्ल च कृष्णा तिथियाँ"])}\n'
      f'नक्षत्र:मास {cycleRatios(basicDictsLists["नक्षत्र"], basicDictsLists["शुक्ल च कृष्णा तिथियाँ"])}')

print(f'\nmaps ऋतू:मास:{cycleMaps(basicDictsLists["ऋतु"], basicDictsLists["मास"])}\n'
      f'मास:ऋतु:{cycleMaps(basicDictsLists["मास"], basicDictsLists["ऋतु"])}\n'
      f'पक्ष:मास:{cycleMaps(basicDictsLists["पक्ष"], basicDictsLists["शुक्ल च कृष्णा तिथियाँ"])}\n'
      f'मास:पक्ष:{cycleMaps(basicDictsLists["शुक्ल च कृष्णा तिथियाँ"], basicDictsLists["पक्ष"])}'
      )
