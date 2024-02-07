# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.AddrLevel import AddrLevel
from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.address.internal.RegionHelper import RegionHelper
from pullenti.address.AddrObject import AddrObject
from pullenti.address.internal.AbbrTreeNode import AbbrTreeNode
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.address.internal.PullentiAddressInternalResourceHelper import PullentiAddressInternalResourceHelper
from pullenti.address.AreaAttributes import AreaAttributes

class CorrectionHelper:
    
    @staticmethod
    def correct(txt : str, second_var : str, details : str) -> str:
        second_var.value = (None)
        details.value = (None)
        txt = txt.strip()
        if (Utils.isNullOrEmpty(txt)): 
            return txt
        ii = txt.find("областьг")
        if (ii > 0): 
            tmp = Utils.newStringIO(txt)
            Utils.insertStringIO(tmp, ii + 7, ' ')
            txt = Utils.toStringStringIO(tmp)
        if ("снт Тверь" in txt): 
            txt = txt.replace("снт Тверь", "г.Тверь")
        if ("Санкт-Петербур " in txt): 
            txt = txt.replace("Санкт-Петербур ", "Санкт-Петербург ")
        txt = txt.replace("кл-ще", "кладбище")
        txt = txt.replace("областьасть", "область")
        txt = txt.replace("ж/д_ст", "железнодорожная станция")
        txt = txt.replace(" - ", "-")
        txt = txt.replace("\\\\", "\\")
        txt = txt.replace("\\\"", "\"")
        txt = txt.replace('\t', ' ')
        if (txt.endswith("д., , ,")): 
            txt = txt[0:0+len(txt) - 7].strip()
        if (txt.find('*') > 0): 
            txt = txt.replace('*', '-')
        if (txt[len(txt) - 1] == '/'): 
            txt = txt[0:0+len(txt) - 1]
        if (Utils.startsWithString(txt, "НЕТ,", True)): 
            txt = txt[4:].strip()
        if (Utils.startsWithString(txt, "СУБЪЕКТ", True)): 
            txt = txt[7:].strip()
        if (Utils.startsWithString(txt, "ФЕДЕРАЦИЯ.", True)): 
            txt = "{0} {1}".format(txt[0:0+9], txt[10:])
        i0 = 0
        if (Utils.startsWithString(txt, "РОССИЯ", True)): 
            i0 = 6
        elif (Utils.startsWithString(txt, "РФ", True)): 
            i0 = 2
        elif (Utils.startsWithString(txt, "RU", True)): 
            i0 = 2
        elif (Utils.startsWithString(txt, "Р.Ф.", True)): 
            i0 = 4
        elif (Utils.startsWithString(txt, "г. Москва и Московская область", True)): 
            i0 = 30
            txt1 = txt[i0:]
            if ("Москва" in txt1 or "Москов" in txt1): 
                pass
            else: 
                i0 = 12
        elif (Utils.startsWithString(txt, "г. Санкт-Петербург и Ленинградская область", True)): 
            i0 = 42
        if (i0 > 0 and ((i0 + 1) < len(txt)) and ((not str.isalpha(txt[i0]) or ((ord(txt[i0 - 1])) < 0x80)))): 
            while i0 < len(txt): 
                if (str.isalpha(txt[i0])): 
                    txt = txt[i0:]
                    break
                i0 += 1
        if (Utils.startsWithString(txt, "МО", True) and len(txt) > 3): 
            if (txt[2] == ' ' or txt[2] == ','): 
                txt = ("Московская область" + txt[2:])
        if (((Utils.startsWithString(txt, "М\\О", True) or ((Utils.startsWithString(txt, "М/О", True))))) and len(txt) > 3): 
            txt = ("Московская область " + txt[3:])
        i = 0
        while i < len(txt): 
            if (txt[i] == ' ' or txt[i] == ','): 
                if (i < 4): 
                    break
                ppp = txt[0:0+i].upper()
                countr = None
                wrapcountr126 = RefOutArgWrapper(None)
                inoutres127 = Utils.tryGetValue(CorrectionHelper.__m_cities, ppp, wrapcountr126)
                countr = wrapcountr126.value
                if (inoutres127): 
                    txt = "{0}, город {1}".format(str(countr), txt)
                else: 
                    wrapcountr124 = RefOutArgWrapper(None)
                    inoutres125 = Utils.tryGetValue(CorrectionHelper.__m_regions, ppp, wrapcountr124)
                    countr = wrapcountr124.value
                    if (inoutres125): 
                        txt = "{0}, {1}".format(str(countr), txt)
                break
            i += 1
        if (CorrectionHelper.__m_root is None): 
            return txt
        i = 0
        while i < (len(txt) - 5): 
            if (txt[i] == 'у' and txt[i + 1] == 'л' and str.isupper(txt[i + 2])): 
                txt = "{0}.{1}".format(txt[0:0+i + 2], txt[i + 2:])
                break
            i += 1
        i = 10
        while i < (len(txt) - 3): 
            if (txt[i - 1] == ' ' or txt[i - 1] == ','): 
                if (((CorrectionHelper.__is_start_of(txt, i, "паспорт", False) or CorrectionHelper.__is_start_of(txt, i, "выдан", False) or CorrectionHelper.__is_start_of(txt, i, "Выдан", False)) or CorrectionHelper.__is_start_of(txt, i, "серия", False) or CorrectionHelper.__is_start_of(txt, i, "док:", False)) or CorrectionHelper.__is_start_of(txt, i, "док.:", False)): 
                    txt = Utils.trimEndString(txt[0:0+i])
                    break
                elif (CorrectionHelper.__is_start_of(txt, i, "ОКАТО", False) and i >= (len(txt) - 20)): 
                    txt = Utils.trimEndString(txt[0:0+i])
                    break
                elif (CorrectionHelper.__is_start_of(txt, i, "адрес ориентира:", False)): 
                    details.value = txt[0:0+i]
                    txt = txt[i + 16:].strip()
                    i = 0
                elif ((CorrectionHelper.__is_start_of(txt, i, "ОВД", False) or CorrectionHelper.__is_start_of(txt, i, "УВД", False) or CorrectionHelper.__is_start_of(txt, i, "РОВД", False)) or CorrectionHelper.__is_start_of(txt, i, "ГОВД", False)): 
                    kk = 0
                    br = False
                    kk = 10
                    while kk < (i - 2): 
                        if (CorrectionHelper.__is_start_of(txt, kk, "кв", False) or CorrectionHelper.__is_start_of(txt, kk, "Кв", False)): 
                            if (txt[kk + 2] == '.' or txt[kk + 2] == ' '): 
                                kk += 2
                                while kk < (i - 2): 
                                    if (txt[kk] != ' ' and txt[kk] != '.'): 
                                        break
                                    kk += 1
                                if (str.isdigit(txt[kk])): 
                                    while kk < i: 
                                        if (not str.isdigit(txt[kk])): 
                                            break
                                        kk += 1
                                    txt = txt[0:0+kk]
                                    br = True
                                break
                        kk += 1
                    if (br): 
                        break
                    j = i - 2
                    sp = 0
                    while j > 0: 
                        if (txt[j] == ' ' and txt[j - 1] != ' '): 
                            sp += 1
                            if (sp >= 4): 
                                break
                        j -= 1
                    if (j > 10 and sp == 4): 
                        txt = Utils.trimEndString(txt[0:0+j])
                        break
            i += 1
        txt0 = txt.upper()
        i = 0
        first_pass3103 = True
        while True:
            if first_pass3103: first_pass3103 = False
            else: i += 1
            if (not (i < len(txt0))): break
            if (not str.isalpha(txt0[i])): 
                continue
            if (((i > 10 and str.isdigit(txt[i - 1]) and str.isupper(txt[i])) and ((i + 2) < len(txt)) and txt[i + 1] == 'к') and str.isdigit(txt[i + 2])): 
                txt = "{0} {1}".format(txt[0:0+i + 1], txt[i + 1:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "РНД", True)): 
                txt = "{0}Ростов-на-Дону {1}".format(txt[0:0+i], txt[i + 3:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "РСО", True)): 
                txt = "{0}республика Северная Осетия {1}".format(txt[0:0+i], txt[i + 3:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "РС(Я)", False)): 
                txt = "{0}республика Саха (Якутия){1}".format(txt[0:0+i], txt[i + 5:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "РС (Я)", False)): 
                txt = "{0}республика Саха (Якутия){1}".format(txt[0:0+i], txt[i + 6:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "СПБ", True)): 
                txt = "{0}Санкт-Петербург {1}".format(txt[0:0+i], txt[i + 3:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "ДО ВОСТРЕБ", False)): 
                txt = txt[0:0+i].strip()
                txt0 = txt.upper()
                break
            if (i == 0 or txt[i - 1] == ',' or txt[i - 1] == ' '): 
                pass
            else: 
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "ХХХ", False) or CorrectionHelper.__is_start_of(txt0, i, "XXX", False)): 
                txt = (txt[0:0+i] + txt[i + 3:])
                txt0 = txt.upper()
                continue
            tn = CorrectionHelper.__m_root.find(txt0, i)
            if (tn is None): 
                continue
            j = i + tn.len0_
            ok = False
            if (tn.len0_ == 2 and txt0[i] == 'У' and txt0[i + 1] == 'Л'): 
                continue
            if (tn.len0_ == 2 and txt0[i] == 'С' and txt0[i + 1] == 'Т'): 
                continue
            if ((tn.len0_ == 3 and txt0[i] == 'П' and txt0[i + 1] == 'Е') and txt0[i + 2] == 'Р'): 
                continue
            while j < len(txt0): 
                if (txt0[j] == '.' or txt0[j] == ' '): 
                    ok = True
                else: 
                    break
                j += 1
            if (j >= len(txt0) or not ok or tn.corrs is None): 
                continue
            for kp in tn.corrs.items(): 
                if (not CorrectionHelper.__is_start_of(txt0, j, kp[0], False)): 
                    continue
                if (tn.len0_ == 8 and CorrectionHelper.__is_start_of(txt0, i, "НОВГОРОД", False)): 
                    continue
                if (tn.len0_ == 2 and CorrectionHelper.__is_start_of(txt0, i, "ПР", False)): 
                    continue
                tmp = Utils.newStringIO(txt)
                Utils.removeStringIO(tmp, i, tn.len0_)
                if (Utils.getCharAtStringIO(tmp, i) == '.'): 
                    Utils.removeStringIO(tmp, i, 1)
                Utils.insertStringIO(tmp, i, kp[1] + " ")
                txt = Utils.toStringStringIO(tmp)
                txt0 = txt.upper()
                break
        i = 0
        first_pass3104 = True
        while True:
            if first_pass3104: first_pass3104 = False
            else: i += 1
            if (not (i < len(txt))): break
            if (not str.isalpha(txt[i]) and txt[i] != '-'): 
                city = txt[0:0+i]
                if (RegionHelper.is_big_city(city) is None): 
                    continue
                ok = False
                j = i
                first_pass3105 = True
                while True:
                    if first_pass3105: first_pass3105 = False
                    else: j += 1
                    if (not (j < len(txt))): break
                    if (Utils.isWhitespace(txt[j])): 
                        continue
                    if (txt[j] == 'г' or txt[j] == 'Г'): 
                        ok = True
                    break
                if (not ok): 
                    txt = "г.{0},{1}".format(txt[0:0+i], txt[i:])
                break
        i = 0
        while i < len(txt): 
            if (txt[i] == ' '): 
                if (CorrectionHelper.__is_start_of(txt, i + 1, "филиал", False) or CorrectionHelper.__is_start_of(txt, i + 1, "ФИЛИАЛ", False)): 
                    reg = txt[0:0+i]
                    city = None
                    tn = CorrectionHelper.__m_root.find(reg.upper(), 0)
                    if (tn is not None and tn.corrs is not None): 
                        for kp in tn.corrs.items(): 
                            if (kp[0] == "ОБ"): 
                                nam = kp[1]
                                reg = (nam + " область")
                                r = RegionHelper.find_region_by_adj(nam)
                                if (r is not None and r.capital is not None): 
                                    city = r.capital
                                break
                    if (city is not None): 
                        second_var.value = "г.{0}, {1}".format(city, txt[i + 7:])
                    txt1 = "{0}, {1}".format(reg, txt[i + 7:])
                    txt = txt1
                break
            i += 1
        txt0 = txt.upper()
        if (CorrectionHelper.__is_start_of(txt0, 0, "ФИЛИАЛ ", False)): 
            txt = txt[7:]
        if (len(txt) > 10 and txt[0] == 'г' and txt[1] == ','): 
            txt = ("г." + txt[2:])
        if (len(txt) < 20): 
            return txt
        if (str.isalpha(txt[len(txt) - 1])): 
            for i in range(len(txt) - 7, 10, -1):
                if (str.isalpha(txt[i])): 
                    if (txt[i - 1] == '.' and str.isupper(txt[i]) and (ord(txt[i])) > 0x80): 
                        if (txt[i + 1] == '.'): 
                            continue
                        if (str.isupper(txt[i - 2])): 
                            continue
                        has_cap = False
                        for j in range(i - 3, 10, -1):
                            if (txt[j] == ','): 
                                p0 = txt[0:0+j + 1]
                                p1 = txt[i:]
                                p2 = txt[j + 1:j + 1+i - j - 2]
                                txt = "{0}{1},{2}".format(p0, p1, p2)
                                break
                            elif (not has_cap and not str.isalpha(txt[j]) and str.isalpha(txt[j + 1])): 
                                if (not str.isupper(txt[j + 1])): 
                                    break
                                has_cap = True
                        break
                else: 
                    break
        return txt
    
    @staticmethod
    def __is_start_of(txt : str, i : int, sub : str, check_non_let_surr : bool=False) -> bool:
        no_casesens = False
        if (i > 0 and txt[i - 1] == ' '): 
            no_casesens = True
        j = 0
        while j < len(sub): 
            if ((i + j) >= len(txt)): 
                return False
            elif (sub[j] == txt[i + j]): 
                pass
            elif (no_casesens and str.upper(sub[j]) == str.upper(txt[i + j])): 
                pass
            else: 
                return False
            j += 1
        if (check_non_let_surr): 
            if (i > 0 and str.isalpha(txt[i - 1])): 
                return False
            if (((i + len(sub)) < len(txt)) and str.isalpha(txt[i + len(sub)])): 
                return False
        return True
    
    @staticmethod
    def initialize() -> None:
        CorrectionHelper.__m_root = AbbrTreeNode()
        for r in RegionHelper.REGIONS: 
            a = Utils.asObjectOrNull(r.attrs, AreaAttributes)
            if (a is None): 
                continue
            if (len(a.types) == 0 or "город" in a.types): 
                continue
            if (len(a.names) == 0): 
                continue
            if (a.types[0] == "республика"): 
                CorrectionHelper.__add(a.names[0], "респ")
            elif (a.types[0] == "край"): 
                CorrectionHelper.__add(a.names[0], "кр")
                if (a.names[0].endswith("ий")): 
                    CorrectionHelper.__add(a.names[0][0:0+len(a.names[0]) - 2] + "ая", "об")
            elif (a.types[0] == "область"): 
                CorrectionHelper.__add(a.names[0], "об")
                if (a.names[0].endswith("ая")): 
                    CorrectionHelper.__add(a.names[0][0:0+len(a.names[0]) - 2] + "ий", "р")
            elif (a.types[0] == "автономная область"): 
                CorrectionHelper.__add(a.names[0], "об")
                CorrectionHelper.__add(a.names[0], "ао")
            elif (a.types[0] == "автономный округ"): 
                CorrectionHelper.__add(a.names[0], "ок")
                CorrectionHelper.__add(a.names[0], "ао")
            elif (a.types[0] == "город"): 
                CorrectionHelper.__add(a.names[0], "г")
            else: 
                pass
    
    @staticmethod
    def initialize0() -> None:
        dat = PullentiAddressInternalResourceHelper.get_string("CitiesNonRus.txt")
        country = None
        for line in Utils.splitString(dat, '\n', False): 
            if (line.startswith("//")): 
                continue
            if (line.startswith("*")): 
                aa = AreaAttributes()
                country = AddrObject._new122(aa, AddrLevel.COUNTRY)
                aa.names.append(line[1:].strip())
                continue
            if (country is None): 
                continue
            is_city = True
            if (line.find("область") >= 0 or line.find("район") >= 0): 
                is_city = False
            for v in Utils.splitString(line, ';', False): 
                city = v.upper().strip()
                if (Utils.isNullOrEmpty(city)): 
                    continue
                if (is_city): 
                    if (not city in CorrectionHelper.__m_cities): 
                        CorrectionHelper.__m_cities[city] = country
                    continue
                ii = city.find("ОБЛАСТЬ")
                if (ii < 0): 
                    ii = city.find("РАЙОН")
                if (ii > 0): 
                    city = city[0:0+ii].strip()
                if (not city in CorrectionHelper.__m_regions): 
                    CorrectionHelper.__m_regions[city] = country
    
    __m_root = None
    
    __m_cities = None
    
    __m_regions = None
    
    @staticmethod
    def find_country(obj : 'AddrObject') -> 'AddrObject':
        aa = Utils.asObjectOrNull(obj.attrs, AreaAttributes)
        if (aa is None): 
            return None
        res = None
        for nam in aa.names: 
            wrapres131 = RefOutArgWrapper(None)
            inoutres132 = Utils.tryGetValue(CorrectionHelper.__m_cities, nam.upper(), wrapres131)
            res = wrapres131.value
            if (inoutres132): 
                return res
            wrapres129 = RefOutArgWrapper(None)
            inoutres130 = Utils.tryGetValue(CorrectionHelper.__m_regions, nam.upper(), wrapres129)
            res = wrapres129.value
            if (inoutres130): 
                return res
        return None
    
    @staticmethod
    def __add(corr : str, typ : str) -> None:
        typ = typ.upper()
        corr = corr.upper()
        i = 1
        while i < (len(corr) - 2): 
            if (not LanguageHelper.is_cyrillic_vowel(corr[i])): 
                str0_ = corr[0:0+i + 1]
                if (RegionHelper.is_big_city(str0_) is not None): 
                    pass
                else: 
                    CorrectionHelper.__m_root.add(str0_, 0, corr, typ)
            i += 1
    
    @staticmethod
    def correct_country(addr : 'TextAddress') -> None:
        if (len(addr.items) == 0): 
            return
        if (addr.items[0].level == AddrLevel.COUNTRY): 
            return
        if (len(addr.items[0].gars) == 0): 
            return
        reg = addr.items[0].gars[0].region_number
        if ((reg == 90 or reg == 93 or reg == 94) or reg == 95): 
            addr.items.insert(0, CorrectionHelper.create_country("UA", None))
        else: 
            addr.items.insert(0, CorrectionHelper.create_country("RU", None))
    
    @staticmethod
    def create_country(alpha : str, geo : 'GeoReferent') -> 'AddrObject':
        aa = AreaAttributes()
        if (alpha == "RU"): 
            aa.names.append("Россия")
        elif (alpha == "UA"): 
            aa.names.append("Украина")
        elif (alpha == "BY"): 
            aa.names.append("Белоруссия")
        elif (alpha == "KZ"): 
            aa.names.append("Казахстан")
        elif (alpha == "KG"): 
            aa.names.append("Киргизия")
        elif (alpha == "MD"): 
            aa.names.append("Молдавия")
        elif (alpha == "GE"): 
            aa.names.append("Грузия")
        elif (alpha == "AZ"): 
            aa.names.append("Азербайджан")
        elif (alpha == "AM"): 
            aa.names.append("Армения")
        elif (geo is not None): 
            aa.names.append(str(geo))
        else: 
            return None
        res = AddrObject(aa)
        res.level = AddrLevel.COUNTRY
        return res
    
    # static constructor for class CorrectionHelper
    @staticmethod
    def _static_ctor():
        CorrectionHelper.__m_cities = dict()
        CorrectionHelper.__m_regions = dict()

CorrectionHelper._static_ctor()