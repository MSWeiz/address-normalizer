﻿# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.internal.SearchLevel import SearchLevel
from pullenti.address.internal.gar.AreaObject import AreaObject
from pullenti.address.GarLevel import GarLevel
from pullenti.address.SearchResult import SearchResult
from pullenti.address.internal.AddrSearchFormal import AddrSearchFormal
from pullenti.address.GarParam import GarParam
from pullenti.address.internal.GarHelper import GarHelper
from pullenti.address.internal.SearchAddressItem import SearchAddressItem

class AddressSearchHelper:
    
    @staticmethod
    def search(sp : 'SearchParams') -> 'SearchResult':
        res = SearchResult._new85(sp)
        if (sp.param_typ != GarParam.UNDEFINED and not Utils.isNullOrEmpty(sp.param_value)): 
            if (GarHelper.GAR_INDEX is None): 
                return None
            ids = GarHelper.GAR_INDEX.find_by_param(sp.param_typ, sp.param_value)
            if (ids is None): 
                return res
            res.total_count = len(ids)
            i = 0
            first_pass3084 = True
            while True:
                if first_pass3084: first_pass3084 = False
                else: i += 1
                if (not (i < len(ids))): break
                if (len(res.objects) >= sp.max_count): 
                    break
                id0_ = ids[i]
                if ((((id0_) & 0x80000000)) == 0): 
                    aa = GarHelper.create_gar_aby_id(id0_)
                    if (aa is not None): 
                        res.objects.append(aa)
                    continue
                if ((((id0_) & 0x40000000)) == 0): 
                    ho = GarHelper.GAR_INDEX.get_house(((id0_) & 0x3FFFFFFF))
                    gh = GarHelper.create_gar_house(ho)
                    if (gh is not None): 
                        res.objects.append(gh)
                else: 
                    ro = GarHelper.GAR_INDEX.get_room(((id0_) & 0x3FFFFFFF))
                    rh = GarHelper.create_gar_room(ro)
                    if (rh is not None): 
                        res.objects.append(rh)
            return res
        ain = list()
        if (sp.region > 0): 
            ain.append(SearchAddressItem._new86(SearchLevel.REGION, str(sp.region)))
        if (not Utils.isNullOrEmpty(sp.area)): 
            ain.append(SearchAddressItem._new87(SearchLevel.DISTRICT, sp.area))
        if (not Utils.isNullOrEmpty(sp.city)): 
            ain.append(SearchAddressItem._new87(SearchLevel.CITY, sp.city))
        if (not Utils.isNullOrEmpty(sp.street)): 
            ain.append(SearchAddressItem._new87(SearchLevel.STREET, sp.street))
        if (len(ain) > 0): 
            ain[len(ain) - 1].search = True
        total = 0
        wraptotal90 = RefOutArgWrapper(0)
        sain = AddressSearchHelper.process(ain, sp.max_count, wraptotal90)
        total = wraptotal90.value
        res.total_count = total
        if (sain is not None): 
            for a in sain: 
                if (isinstance(a.tag, AreaObject)): 
                    ga = GarHelper.create_gar_area(Utils.asObjectOrNull(a.tag, AreaObject))
                    if (ga is not None): 
                        res.objects.append(ga)
        return res
    
    M_ONTO_REGS = None
    
    @staticmethod
    def process(ain : typing.List['SearchAddressItem'], max_count : int, total : int) -> typing.List['SearchAddressItem']:
        total.value = 0
        if (ain is None or len(ain) == 0): 
            return None
        ain1 = list()
        reg_id = 0
        for a in ain: 
            if (a.level == SearchLevel.REGION): 
                if (AddressSearchHelper.M_ONTO_REGS is not None): 
                    for it in AddressSearchHelper.M_ONTO_REGS.values(): 
                        if (it.text == a.text): 
                            nn = 0
                            wrapnn91 = RefOutArgWrapper(0)
                            inoutres92 = Utils.tryParseInt(Utils.ifNotNull(it.id0_, ""), wrapnn91)
                            nn = wrapnn91.value
                            if (inoutres92): 
                                reg_id = nn
                                a.id0_ = it.id0_
                                a.text = (None)
                            break
                if (reg_id == 0): 
                    nn = 0
                    wrapnn93 = RefOutArgWrapper(0)
                    inoutres94 = Utils.tryParseInt(Utils.ifNotNull(a.id0_, ""), wrapnn93)
                    nn = wrapnn93.value
                    if (inoutres94): 
                        reg_id = nn
            else: 
                ain1.append(a)
        if (reg_id == 0 and len(ain1) == 0): 
            return None
        inoutres95 = AddressSearchHelper.__process(ain1, reg_id, max_count, total)
        return inoutres95
    
    @staticmethod
    def __calc_search_level(ao : 'AreaObject') -> 'SearchLevel':
        lev = Utils.valToEnum(ao.level, GarLevel)
        if (lev == GarLevel.REGION): 
            return SearchLevel.REGION
        if (lev == GarLevel.ADMINAREA or lev == GarLevel.MUNICIPALAREA): 
            return SearchLevel.DISTRICT
        if (lev == GarLevel.SETTLEMENT or lev == GarLevel.CITY): 
            return SearchLevel.CITY
        if (lev == GarLevel.LOCALITY): 
            if (ao.typ is not None and ao.typ.name == "территория"): 
                return SearchLevel.STREET
            return SearchLevel.CITY
        if (lev == GarLevel.AREA or lev == GarLevel.STREET): 
            return SearchLevel.STREET
        return SearchLevel.UNDEFINED
    
    @staticmethod
    def __get_id(id0_ : int) -> str:
        return "a{0}".format(id0_)
    
    @staticmethod
    def __process(ain : typing.List['SearchAddressItem'], reg_id : int, max_count : int, total : int) -> typing.List['SearchAddressItem']:
        total.value = 0
        mai = None
        for a in ain: 
            if (a.search): 
                mai = AddrSearchFormal(a)
                mai.reg_id = reg_id
                break
        if (GarHelper.GAR_INDEX is None): 
            return None
        if (mai is None): 
            if (reg_id == 0): 
                return None
            ao = GarHelper.GAR_INDEX.getaoby_reg(reg_id)
            if (ao is None): 
                return None
            rr = SearchAddressItem._new96(AddressSearchHelper.__get_id(ao.id0_), SearchLevel.REGION, ao, "{0} {1}".format(ao.names[0], ao.typ.name))
            if (rr.id0_ in AddressSearchHelper.M_ONTO_REGS): 
                reg = AddressSearchHelper.M_ONTO_REGS[rr.id0_]
                rr.text = reg.text
                rr.id0_ = (Utils.ifNotNull(reg.id0_, reg.text))
            res0 = list()
            res0.append(rr)
            return res0
        if (Utils.isNullOrEmpty(mai.src.text) and mai.src.level != SearchLevel.REGION and len(ain) > 0): 
            ain0 = list()
            ai_max = None
            for a in ain: 
                if (((a.level) < (mai.src.level)) and not Utils.isNullOrEmpty(a.text)): 
                    aa = SearchAddressItem._new87(a.level, a.text)
                    ain0.append(aa)
                    if (ai_max is None): 
                        ai_max = aa
                    elif ((aa.level) > (ai_max.level)): 
                        ai_max = aa
            if (ai_max is not None): 
                ai_max.search = True
            res0 = AddressSearchHelper.__process(ain0, reg_id, max_count, total)
            if (res0 is None or len(res0) != 1): 
                return None
            total.value = 0
            ao = Utils.asObjectOrNull(res0[0].tag, AreaObject)
            if (ao is None): 
                return None
            all0 = GarHelper.GAR_INDEX.getaochildren(ao)
            res00 = list()
            ggg0 = dict()
            if (all0 is not None): 
                for ao0 in all0: 
                    if (len(res00) >= max_count): 
                        total.value = len(all0)
                        break
                    slev = AddressSearchHelper.__calc_search_level(ao0)
                    ai0 = SearchAddressItem._new98(AddressSearchHelper.__get_id(ao0.id0_), ao0, slev, res0[0], "{0} {1}".format(ao0.names[0], ao0.typ.name))
                    if (slev == mai.src.level): 
                        if (ao0.id0_ in ggg0): 
                            continue
                        res00.append(ai0)
                        ggg0[ao0.id0_] = True
                        continue
                    if ((slev) > (mai.src.level)): 
                        continue
                    all1 = GarHelper.GAR_INDEX.getaochildren(ao0)
                    if (all1 is not None): 
                        for ao1 in all1: 
                            if (len(res00) >= max_count): 
                                total.value = (len(res00) + len(all1))
                                break
                            slev = AddressSearchHelper.__calc_search_level(ao1)
                            if (slev == mai.src.level): 
                                if (ao1.id0_ in ggg0): 
                                    continue
                                sai1 = SearchAddressItem._new98(AddressSearchHelper.__get_id(ao1.id0_), ao1, slev, ai0, "{0} {1}".format(ao1.names[0], ao1.typ.name))
                                res00.append(sai1)
                                ggg0[ao1.id0_] = True
                                continue
            return res00
        res = list()
        mai.reg_id = reg_id
        all0_ = mai.search()
        if (all0_ is None or len(all0_) == 0): 
            return res
        for a in ain: 
            if (not a.search and ((a.level) < (mai.src.level))): 
                par = AddrSearchFormal(a)
                pars = par.search()
                if (len(pars) == 0): 
                    continue
                for i in range(len(all0_) - 1, -1, -1):
                    has_par = False
                    for p in pars: 
                        if (p.id0_ in all0_[i].parent_ids): 
                            has_par = True
                            break
                        elif (all0_[i].parent_parent_ids is not None and p.id0_ in all0_[i].parent_parent_ids): 
                            has_par = True
                            break
                    if (not has_par): 
                        del all0_[i]
        ggg = dict()
        for k in range(2):
            for a in all0_: 
                if (len(res) >= max_count): 
                    total.value = len(all0_)
                    break
                ao = GarHelper.GAR_INDEX.getao(a.id0_)
                if (ao is None): 
                    continue
                if (ao.id0_ in ggg): 
                    continue
                if (not mai.check(ao, k > 0)): 
                    continue
                slev = AddressSearchHelper.__calc_search_level(ao)
                if (slev != mai.src.level): 
                    if (slev == SearchLevel.REGION and mai.src.level == SearchLevel.CITY and ao.level == (1)): 
                        pass
                    else: 
                        continue
                ai = SearchAddressItem._new100(AddressSearchHelper.__get_id(ao.id0_), ao, slev, "{0} {1}".format(ao.names[0], ao.typ.name))
                res.append(ai)
                total.value = len(res)
                ggg[ao.id0_] = True
                parids = a.parent_ids
                while parids is not None and len(parids) > 0:
                    ok = False
                    for pid in parids: 
                        pao = GarHelper.GAR_INDEX.getao(pid)
                        if (pao is None): 
                            continue
                        slev0 = AddressSearchHelper.__calc_search_level(pao)
                        if (slev0 == SearchLevel.UNDEFINED): 
                            continue
                        if (slev0 == slev): 
                            continue
                        pai = SearchAddressItem._new100(AddressSearchHelper.__get_id(pao.id0_), pao, slev0, "{0} {1}".format(pao.names[0], pao.typ.name))
                        ai.parent = pai
                        ai = pai
                        slev = slev0
                        parids = pao.parent_ids
                        ok = True
                        break
                    if (slev == SearchLevel.REGION or not ok): 
                        break
                if (ai.level == SearchLevel.REGION and ai.id0_ in AddressSearchHelper.M_ONTO_REGS): 
                    reg = AddressSearchHelper.M_ONTO_REGS[ai.id0_]
                    ai.text = reg.text
                    ai.id0_ = (Utils.ifNotNull(reg.id0_, reg.text))
            if (len(res) > 0): 
                break
        i = 0
        while i < (len(res) - 1): 
            j = 0
            while j < (len(res) - 1): 
                if (res[j].compareTo(res[j + 1]) > 0): 
                    r = res[j]
                    res[j] = res[j + 1]
                    res[j + 1] = r
                j += 1
            i += 1
        return res
    
    # static constructor for class AddressSearchHelper
    @staticmethod
    def _static_ctor():
        AddressSearchHelper.M_ONTO_REGS = dict()

AddressSearchHelper._static_ctor()