# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.address.ParamType import ParamType
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.address.internal.CoefHelper import CoefHelper
from pullenti.address.AddrObject import AddrObject
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.geo.internal.GeoOwnerHelper import GeoOwnerHelper
from pullenti.address.internal.CorrectionHelper import CorrectionHelper
from pullenti.address.internal.GarHelper import GarHelper
from pullenti.address.internal.RestructHelper import RestructHelper
from pullenti.ner.Referent import Referent
from pullenti.address.DetailType import DetailType
from pullenti.address.AddrLevel import AddrLevel
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.GarLevel import GarLevel
from pullenti.address.AddressHelper import AddressHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.address.GarStatus import GarStatus
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.address.internal.HouseRoomHelper import HouseRoomHelper
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.address.internal.RegionHelper import RegionHelper
from pullenti.address.AddressService import AddressService
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.address.internal.NameAnalyzer import NameAnalyzer
from pullenti.address.TextAddress import TextAddress

class AnalyzeHelper:
    
    def __init__(self) -> None:
        self.__m_gar_hash = dict()
        self.__m_houses = dict()
        self.__m_rooms = dict()
        self.index_read_count = 0
        self.litera_variant = None;
        self.m_params = None;
        self.corrected_text = None;
        self.create_alts_regime = False
        self.zip0_ = None;
    
    def __remove_gars(self, addr : 'TextAddress') -> bool:
        ret = False
        for j in range(len(addr.items) - 1, 0, -1):
            it1 = addr.items[j]
            if (len(it1.gars) < 2): 
                continue
            for k in range(j - 1, -1, -1):
                it0 = addr.items[k]
                if (len(it0.gars) == 0): 
                    continue
                cou = 0
                real = None
                is_actual = False
                for g in it1.gars: 
                    if (it0._find_gar_by_ids(g.parent_ids) is not None): 
                        cou += 1
                        real = g
                    elif (not g.expired): 
                        is_actual = True
                if (cou == 1): 
                    if (is_actual and real.expired): 
                        break
                    else: 
                        it1.gars.clear()
                        it1.gars.append(real)
                        ret = True
        for j in range(len(addr.items) - 1, -1, -1):
            it1 = addr.items[j]
            if (len(it1.gars) != 1): 
                continue
            if (AddressHelper.compare_levels(it1.level, AddrLevel.STREET) > 0): 
                continue
            for k in range(j - 1, -1, -1):
                it0 = addr.items[k]
                if (len(it0.gars) == 0): 
                    break
                g1 = it1.gars[0]
                cou = 0
                par = None
                for g in it0.gars: 
                    if (g.id0_ in g1.parent_ids): 
                        cou += 1
                        par = g
                if (cou == 1 and len(it0.gars) > 1): 
                    it0.gars.clear()
                    it0.gars.append(par)
                    ret = True
                break
        i = 0
        first_pass3086 = True
        while True:
            if first_pass3086: first_pass3086 = False
            else: i += 1
            if (not (i < (len(addr.items) - 1))): break
            it0 = addr.items[i]
            if (len(it0.gars) < 2): 
                continue
            it1 = addr.items[i + 1]
            if (len(it1.gars) != 1): 
                continue
            has_par = 0
            for g in it0.gars: 
                if (it1._find_gar_by_ids(g.parent_ids) is not None): 
                    has_par += 1
            if (has_par > 0 and (has_par < len(it0.gars))): 
                for j in range(len(it0.gars) - 1, -1, -1):
                    if (it1._find_gar_by_ids(it0.gars[j].parent_ids) is None): 
                        del it0.gars[j]
        return ret
    
    @staticmethod
    def __correct_object_by_gars(it : 'AddrObject') -> None:
        aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
        if (aa is None): 
            return
        typs = list()
        levs = list()
        for g in it.gars: 
            is_road = False
            for ty in g.attrs.types: 
                if (not ty in typs): 
                    typs.append(ty)
                    if ("дорога" in ty): 
                        is_road = True
            gl = g.level
            if (is_road and gl == GarLevel.LOCALITY): 
                gl = GarLevel.AREA
            if (not gl in levs): 
                levs.append(gl)
        if (len(aa.types) > 0 and ((aa.types[0] == "населенный пункт" or aa.types[0] == "почтовое отделение")) and len(typs) == 1): 
            aa.types[0] = typs[0]
            if (it.level == AddrLevel.LOCALITY and len(levs) == 1 and levs[0] == GarLevel.CITY): 
                it.level = AddrLevel.CITY
        elif (len(typs) == 1 and len(aa.types) > 1 and Utils.indexOfList(aa.types, typs[0], 0) > 0): 
            aa.types.remove(typs[0])
            aa.types.insert(0, typs[0])
        if (len(aa.types) == 0 and len(typs) == 1): 
            aa.types.append(typs[0])
        if (len(aa.types) > 1 and len(typs) == 1): 
            if ("проезд" in aa.types and "проспект" in aa.types): 
                aa.types.clear()
                aa.types.append(typs[0])
        if (len(aa.types) == 1 and aa.types[0] == "район" and len(typs) == 1): 
            aa.types.clear()
            aa.types.append(typs[0])
        if (len(aa.types) == 0): 
            aa.types.extend(typs)
        if ((len(typs) == 1 and it.level == AddrLevel.STREET and aa.types[0] != typs[0]) and typs[0] != "территория"): 
            if ((len(aa.types) == 1 and aa.types[0] == "улица" and len(levs) == 1) and levs[0] == GarLevel.AREA and len(it.gars) == 1): 
                aa.types.clear()
                aa.types.append("территория")
                aa.miscs.extend(it.gars[0].attrs.miscs)
                it.level = AddrLevel.TERRITORY
            else: 
                if (typs[0] in aa.types): 
                    aa.types.remove(typs[0])
                aa.types.insert(0, typs[0])
        if (len(aa.types) > 1 and aa.types[0] == "улица"): 
            del aa.types[0]
            aa.types.append("улица")
        if (len(aa.names) == 0): 
            return
        for g in it.gars: 
            ga = Utils.asObjectOrNull(g.attrs, AreaAttributes)
            for n in aa.names: 
                for gn in ga.names: 
                    if (gn in aa.names): 
                        if (gn != aa.names[0]): 
                            aa.names.remove(gn)
                            aa.names.insert(0, gn)
                        return
                    elif (n in gn): 
                        if (len(gn) <= (len(n) + 1)): 
                            aa.names.insert(0, gn)
                        elif (n != aa.names[0]): 
                            aa.names.remove(n)
                            aa.names.insert(0, n)
                        return
        for g in it.gars: 
            ga = Utils.asObjectOrNull(g.attrs, AreaAttributes)
            na = NameAnalyzer()
            na.process(ga.names, (None if len(ga.types) == 0 else ga.types[0]))
            aa2 = AreaAttributes()
            AnalyzeHelper.__set_name(aa2, na.ref, "NAME")
            if (len(aa2.names) > 0): 
                if (not aa2.names[0] in aa.names): 
                    aa.names.insert(0, aa2.names[0])
                elif (len(ga.names[0]) == len(aa.names[0])): 
                    aa.names.insert(0, ga.names[0])
                break
        if (len(aa.types) == 0 and it.level == AddrLevel.STREET and len(aa.names) > 0): 
            if (aa.names[0].endswith("ая")): 
                aa.types.append("улица")
    
    @staticmethod
    def __correct_levels(addr : 'TextAddress') -> None:
        i = 0
        first_pass3087 = True
        while True:
            if first_pass3087: first_pass3087 = False
            else: i += 1
            if (not (i < len(addr.items))): break
            it = addr.items[i]
            AnalyzeHelper.__correct_object_by_gars(it)
            if (it.cross_object is not None): 
                AnalyzeHelper.__correct_object_by_gars(it.cross_object)
            if ((i + 1) >= len(addr.items)): 
                continue
            aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
            it1 = addr.items[i + 1]
            if (it.level == AddrLevel.DISTRICT): 
                if (it1.level == AddrLevel.TERRITORY or it1.level == AddrLevel.STREET): 
                    if ("улус" in it.attrs.types): 
                        it.level = AddrLevel.LOCALITY
            elif (it.level == AddrLevel.LOCALITY and it1.level == AddrLevel.LOCALITY): 
                if (len(it1.gars) > 0 and it1.gars[0].level == GarLevel.AREA): 
                    it1.level = AddrLevel.TERRITORY
            elif (((it.level == AddrLevel.TERRITORY and i > 0 and (AddressHelper.compare_levels(addr.items[i - 1].level, AddrLevel.LOCALITY) < 0)) and ((it1.level == AddrLevel.TERRITORY or it1.level == AddrLevel.STREET)) and len(it.gars) == 1) and ((it.gars[0].level == GarLevel.LOCALITY or it.gars[0].level == GarLevel.CITY))): 
                if (it.level == AddrLevel.TERRITORY and "дорога" in aa.miscs): 
                    pass
                else: 
                    it.level = AddrLevel.LOCALITY
                    if ("территория" in aa.types): 
                        aa.types.remove("территория")
                    ty = it.gars[0].attrs.types[0]
                    if (not ty in aa.types): 
                        aa.types.append(ty)
            elif ((it.level == AddrLevel.CITY and len(it.gars) > 0 and it.gars[0].level == GarLevel.SETTLEMENT) and it1.level == AddrLevel.LOCALITY): 
                it.level = AddrLevel.SETTLEMENT
                aa.types.clear()
                aa.types.extend(it.gars[0].attrs.types)
            elif ((it.level == AddrLevel.LOCALITY and AddressHelper.compare_levels(it1.level, AddrLevel.STREET) >= 0 and i > 0) and addr.items[i - 1].level == AddrLevel.CITY): 
                if (len(it.gars) > 0 and it.gars[0].level == GarLevel.AREA): 
                    it.level = AddrLevel.TERRITORY
                    aa.types.clear()
                    aa.types.extend(it.gars[0].attrs.types)
    
    @staticmethod
    def __get_id(v : str) -> int:
        return int(v[1:])
    
    @staticmethod
    def __add_par_ids(par_ids : typing.List[int], ao : 'AddrObject') -> None:
        for p in ao.gars: 
            id0_ = AnalyzeHelper.__get_id(p.id0_)
            if (not id0_ in par_ids): 
                par_ids.append(id0_)
    
    @staticmethod
    def __can_search_gars(r : 'NameAnalyzer', addr : 'TextAddress', i : int) -> bool:
        if (r.level == AddrLevel.TERRITORY or r.level == AddrLevel.STREET): 
            j = 0
            while j < i: 
                if (len(addr.items[j].gars) > 0): 
                    it = addr.items[j]
                    if (((it.level == AddrLevel.REGIONCITY or it.level == AddrLevel.CITY or it.level == AddrLevel.SETTLEMENT) or it.level == AddrLevel.LOCALITY or it.level == AddrLevel.UNDEFINED) or it.level == AddrLevel.TERRITORY): 
                        return True
                    if (it.level == AddrLevel.DISTRICT): 
                        if ("улус" in it.attrs.types or "городской округ" in it.attrs.types or "муниципальный округ" in it.attrs.types): 
                            return True
                        if (len(it.gars) > 0): 
                            if ("городской округ" in it.gars[0].attrs.types): 
                                return True
                    if (r.level == AddrLevel.TERRITORY): 
                        if (j == (i - 1) and ((it.level == AddrLevel.DISTRICT or it.level == AddrLevel.SETTLEMENT))): 
                            return True
                        if (j == (i - 2) and it.level == AddrLevel.DISTRICT and ((addr.items[j + 1].detail_typ != DetailType.UNDEFINED or addr.items[j + 1].level == AddrLevel.TERRITORY))): 
                            return True
                    if (r.level == AddrLevel.STREET and i == 1): 
                        nam = r.ref.get_string_value("NAME")
                        if (nam is not None and nam.find(' ') > 0): 
                            return True
                        if (it.gars[0].region_number == 50): 
                            return True
                j += 1
            return False
        if (r.level == AddrLevel.LOCALITY and i == 0): 
            return False
        return True
    
    def _process_address(self, addr : 'TextAddress', has_sec_var : bool) -> 'AddressReferent':
        has_sec_var.value = False
        if (len(addr.items) == 0): 
            return None
        ar = None
        regions = bytearray()
        other_country = False
        par_ids = list()
        ua_country = None
        rev = False
        i = 0
        first_pass3088 = True
        while True:
            if first_pass3088: first_pass3088 = False
            else: i += 1
            if (not (i < len(addr.items))): break
            it = addr.items[i]
            aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
            if (aa is None): 
                break
            if (GarHelper.GAR_INDEX is None or other_country): 
                continue
            if (i == 0 and it.level == AddrLevel.COUNTRY): 
                if ("Украина" in aa.names): 
                    ua_country = it
                    del addr.items[0]
                    i -= 1
                    continue
                other_country = True
                continue
            if (len(it.gars) > 0): 
                if (len(regions) == 0): 
                    regions.append(it.gars[0].region_number)
                continue
            r = Utils.asObjectOrNull(it.tag, NameAnalyzer)
            if (r is None): 
                continue
            max_count = 50
            if (addr.items[0].level == AddrLevel.REGIONCITY): 
                max_count = 100
            elif (r.level == AddrLevel.TERRITORY): 
                max_count = 200
            par_ids.clear()
            pcou = 0
            for j in range(i - 1, -1, -1):
                it0 = addr.items[j]
                if (len(it0.gars) == 0): 
                    continue
                if (AddressHelper.compare_levels(it0.level, it.level) >= 0 and not AddressHelper.can_be_parent(it0.level, it.level)): 
                    break
                AnalyzeHelper.__add_par_ids(par_ids, it0)
                pcou += 1
                if (it0.level == AddrLevel.LOCALITY): 
                    break
                if (it.level == AddrLevel.TERRITORY and pcou > 1): 
                    break
                if (it0.level == AddrLevel.CITY): 
                    if (it.level == AddrLevel.LOCALITY): 
                        for g in it0.gars: 
                            if (len(g.parent_ids) == 0): 
                                continue
                            gg = self.get_gar_object(g.parent_ids[0])
                            if (gg is not None and gg.level == GarLevel.MUNICIPALAREA): 
                                par_ids.append(AnalyzeHelper.__get_id(gg.id0_))
                    break
            if (len(par_ids) == 0): 
                if (i > 0): 
                    if (i == 1 and r.level == AddrLevel.CITY and len(addr.items[0].gars) == 0): 
                        cou = CorrectionHelper.find_country(it)
                        if (cou is not None): 
                            addr.items.insert(0, cou)
                            break
                    if (it.level == AddrLevel.CITY and RegionHelper.is_big_citya(it) is not None): 
                        pass
                    else: 
                        continue
                if (AddressHelper.compare_levels(it.level, AddrLevel.LOCALITY) >= 0): 
                    if (self.m_params is None): 
                        continue
                    if (self.m_params.default_object is None): 
                        for rid in self.m_params.default_regions: 
                            regions.append(rid)
                        if (len(regions) == 0): 
                            continue
                    else: 
                        par_ids.append(AnalyzeHelper.__get_id(self.m_params.default_object.id0_))
                        if (self.m_params.default_object.region_number > 0): 
                            regions.append(self.m_params.default_object.region_number)
                        to1 = GarHelper.create_addr_object(self.m_params.default_object)
                        addr.items.insert(0, to1)
                        i += 1
            if (i > 0 and ((it.level == AddrLevel.STREET or it.level == AddrLevel.TERRITORY)) and self.zip0_ is not None): 
                has_loc = False
                for ii in range(i - 1, -1, -1):
                    it0 = addr.items[ii]
                    if ((it0.level == AddrLevel.CITY or it0.level == AddrLevel.REGIONCITY or it0.level == AddrLevel.LOCALITY) or it0.level == AddrLevel.SETTLEMENT): 
                        has_loc = True
                zip0__ = 0
                wrapzip103 = RefOutArgWrapper(0)
                Utils.tryParseInt(self.zip0_, wrapzip103)
                zip0__ = wrapzip103.value
                if (not has_loc and zip0__ > 0): 
                    ids = GarHelper.GAR_INDEX.get_ao_ids_by_zip(zip0__)
                    cities = list()
                    if (ids is not None): 
                        for id0_ in ids: 
                            go = self.get_gar_object("a{0}".format(id0_))
                            if (go is not None): 
                                if (go.level == GarLevel.CITY or go.level == GarLevel.LOCALITY): 
                                    if (len(cities) == 0 or cities[0].level == go.level): 
                                        cities.append(go)
                                    elif (cities[0].level == GarLevel.CITY and go.level == GarLevel.LOCALITY): 
                                        cities.clear()
                                        cities.append(go)
                    if (len(cities) > 1): 
                        for ii in range(len(cities) - 1, -1, -1):
                            pars0 = list()
                            pars0.append(AnalyzeHelper.__get_id(cities[ii].id0_))
                            probs0 = GarHelper.GAR_INDEX._get_string_entries(r, regions, pars0, max_count)
                            if (probs0 is None): 
                                del cities[ii]
                    if (len(cities) == 1): 
                        ao = GarHelper.create_addr_object(cities[0])
                        if (ao is not None): 
                            if (AddressHelper.compare_levels(addr.items[i - 1].level, ao.level) < 0): 
                                addr.items.insert(i, ao)
                                continue
            if (not AnalyzeHelper.__can_search_gars(r, addr, i)): 
                if (self.m_params is None or ((len(self.m_params.default_regions) == 0 and self.m_params.default_object is None))): 
                    continue
            probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
            if (probs is None and i > 0 and addr.items[i - 1].detail_typ != DetailType.UNDEFINED): 
                par_ids.clear()
                for g in addr.items[i - 1].gars: 
                    for p in g.parent_ids: 
                        if (not AnalyzeHelper.__get_id(p) in par_ids): 
                            par_ids.append(AnalyzeHelper.__get_id(p))
                if (len(par_ids) == 0 and i > 1): 
                    for g in addr.items[i - 2].gars: 
                        par_ids.append(AnalyzeHelper.__get_id(g.id0_))
                if (len(par_ids) > 0): 
                    probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
            if ((probs is None and i == 0 and it.level == AddrLevel.DISTRICT) and len(addr.items) > 1 and addr.items[1].level == AddrLevel.CITY): 
                if (RegionHelper.is_big_citya(addr.items[1]) is not None and not rev): 
                    del addr.items[0]
                    addr.items.insert(1, it)
                    i -= 1
                    rev = True
                    continue
            if ((probs is None and i == 1 and it.level == AddrLevel.REGIONCITY) and addr.items[0].level == AddrLevel.REGIONAREA): 
                del addr.items[0]
                i = -1
                regions.clear()
                continue
            if (probs is None and i == 0 and r.level == AddrLevel.CITY): 
                cou = CorrectionHelper.find_country(it)
                if (cou is not None): 
                    addr.items.insert(0, cou)
                    break
            if (probs is not None and r.level == AddrLevel.DISTRICT and ((i + 1) < len(addr.items))): 
                if (addr.items[i + 1].level == AddrLevel.STREET or ((addr.items[i + 1].level == AddrLevel.LOCALITY and (i + 2) == len(addr.items)))): 
                    alt = r.try_create_alternative(False, (addr.items[i - 1] if i > 0 else None), (addr.items[i + 1] if (i + 1) < len(addr.items) else None))
                    if (alt is not None): 
                        par_ids0 = list()
                        for p in probs: 
                            par_ids0.append(p.id0_)
                        probs2 = GarHelper.GAR_INDEX._get_string_entries(alt, regions, par_ids0, max_count)
                        if (probs2 is not None): 
                            setls = 0
                            for p in probs2: 
                                if (p.level == AddrLevel.SETTLEMENT): 
                                    setls += 1
                            if (setls > 0 and (setls < len(probs2))): 
                                for jj in range(len(probs2) - 1, -1, -1):
                                    if (probs2[jj].level == AddrLevel.SETTLEMENT): 
                                        del probs2[jj]
                        if (probs2 is not None and len(probs2) == 1): 
                            it1 = addr.items[i + 1]
                            ok2 = True
                            if (it1.level == AddrLevel.LOCALITY and probs2[0].level == it1.level): 
                                ok2 = False
                                r2 = Utils.asObjectOrNull(it1.tag, NameAnalyzer)
                                alt2 = r2.try_create_alternative(True, None, None)
                                if (alt2 is not None): 
                                    par_ids2 = list()
                                    par_ids2.append(probs2[0].id0_)
                                    probs3 = GarHelper.GAR_INDEX._get_string_entries(alt2, regions, par_ids2, max_count)
                                    if (probs3 is not None and len(probs3) == 1): 
                                        ok2 = True
                            elif (it1.level == AddrLevel.STREET and ((alt.level == AddrLevel.LOCALITY or alt.level == AddrLevel.CITY))): 
                                ok2 = False
                                par_ids2 = list()
                                par_ids2.append(probs2[0].id0_)
                                probs3 = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(it1.tag, NameAnalyzer), regions, par_ids2, max_count)
                                if (probs3 is not None and len(probs3) == 1): 
                                    ok2 = True
                            if (not ok2): 
                                pass
                            elif (not self.create_alts_regime): 
                                has_sec_var.value = True
                            else: 
                                probs = probs2
                                it.level = probs2[0].level
                                aa.types.clear()
                                aa.types.extend(alt.types)
                                aa.miscs.clear()
                                if (alt.miscs is not None): 
                                    aa.miscs.extend(alt.miscs)
                                it.tag = (alt)
                                r = alt
            if (probs is None): 
                alt = r.try_create_alternative(False, (addr.items[i - 1] if i > 0 else None), (addr.items[i + 1] if (i + 1) < len(addr.items) else None))
                if (alt is not None): 
                    if (not self.create_alts_regime): 
                        has_sec_var.value = True
                    else: 
                        if (AnalyzeHelper.__can_search_gars(alt, addr, i)): 
                            probs = GarHelper.GAR_INDEX._get_string_entries(alt, regions, par_ids, max_count)
                        if (probs is not None and ((len(probs) == 1 or it.level == AddrLevel.DISTRICT))): 
                            it.tag = (alt)
                            r = alt
                            it.level = probs[0].level
                            for p in probs: 
                                if (p.level != it.level): 
                                    it.level = AddrLevel.UNDEFINED
                                    break
                            aa.types.clear()
                            aa.types.extend(alt.types)
                            aa.miscs.clear()
                            if (alt.miscs is not None): 
                                aa.miscs.extend(alt.miscs)
                        else: 
                            alt2 = r.try_create_alternative(True, (addr.items[i - 1] if i > 0 else None), (addr.items[i + 1] if (i + 1) < len(addr.items) else None))
                            if (alt2 is not None): 
                                probs2 = None
                                if (AnalyzeHelper.__can_search_gars(alt2, addr, i)): 
                                    probs2 = GarHelper.GAR_INDEX._get_string_entries(alt2, regions, par_ids, max_count)
                                if (probs2 is not None and ((len(probs2) == 1 or ((len(probs2) == 2 and probs2[0].level == probs2[1].level))))): 
                                    probs = probs2
                                    it.tag = (alt2)
                                    r = alt2
                                    it.level = probs[0].level
                                    aa.types.clear()
                                    aa.types.extend(alt2.types)
                                    aa.miscs.clear()
                                    if (alt2.miscs is not None): 
                                        aa.miscs.extend(alt2.miscs)
            if (probs is not None and len(probs) == 1 and it.level != probs[0].level): 
                if (r.level == AddrLevel.TERRITORY or ((r.level == AddrLevel.LOCALITY and ((i == (len(addr.items) - 1) or addr.items[i + 1].level != AddrLevel.TERRITORY))))): 
                    par_ids2 = list()
                    par_ids2.append(probs[0].id0_)
                    probs2 = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids2, max_count)
                    if (probs2 is not None and ((i + 1) < len(addr.items))): 
                        prob3 = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(addr.items[i + 1].tag, NameAnalyzer), regions, par_ids2, max_count)
                        if (prob3 is not None): 
                            probs2 = (None)
                    if (probs2 is not None): 
                        probs = probs2
            if ((probs is not None and len(probs) >= 2 and len(regions) == 0) and ((i + 1) < len(addr.items)) and RegionHelper.is_big_citya(addr.items[i + 1]) is not None): 
                probs1 = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(addr.items[i + 1].tag, NameAnalyzer), regions, par_ids, max_count)
                if (probs1 is not None): 
                    for p in probs1: 
                        if (not p.region in regions): 
                            regions.append(p.region)
                if (len(regions) > 0): 
                    probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
            if ((probs is None and len(regions) == 1 and len(par_ids) > 0) and ((it.level == AddrLevel.LOCALITY or it.level == AddrLevel.CITY))): 
                if ((i > 1 and RegionHelper.is_big_citya(addr.items[i - 1]) is not None and addr.items[i - 2].level == AddrLevel.DISTRICT) and len(addr.items[i - 2].gars) > 0): 
                    pars0 = list()
                    AnalyzeHelper.__add_par_ids(pars0, addr.items[i - 2])
                    probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, pars0, max_count)
            all_terrs = True
            if (probs is not None): 
                for p in probs: 
                    if (p.level != AddrLevel.TERRITORY): 
                        all_terrs = False
            if (all_terrs): 
                if (len(regions) == 1 and len(par_ids) > 0 and ((it.level == AddrLevel.LOCALITY or it.level == AddrLevel.CITY))): 
                    if (probs is None): 
                        if (RestructHelper.restruct(self, addr, i)): 
                            regions.clear()
                            i = -1
                            continue
                    probs2 = GarHelper.GAR_INDEX._get_string_entries(r, regions, None, max_count)
                    if (it.level == AddrLevel.CITY and probs2 is None): 
                        probs2 = GarHelper.GAR_INDEX._get_string_entries(r, None, None, max_count)
                    if (probs2 is not None): 
                        for k in range(len(probs2) - 1, -1, -1):
                            pp = probs2[k]
                            ids = list()
                            for p in pp.parent_ids: 
                                ids.append("a{0}".format(p))
                            if (addr.find_gar_by_ids(ids) is None): 
                                del probs2[k]
                    if (probs2 is not None and ((len(probs2) == 0 or len(probs2) > 30))): 
                        probs2 = (None)
                    if ((probs2 is not None and len(probs2) <= 2 and i > 0) and RegionHelper.is_big_citya(addr.items[i - 1]) is not None): 
                        if (probs is not None and probs2[0] in probs): 
                            pass
                        else: 
                            del addr.items[i - 1]
                            i -= 1
                    if (probs is None): 
                        probs = probs2
                    if (probs is not None and len(probs) > 1): 
                        if (r.level == AddrLevel.CITY and "ТРОИЦК" in r.strings): 
                            for k in range(len(probs) - 1, -1, -1):
                                if (probs[k].region != (77)): 
                                    del probs[k]
                            if (len(probs) == 1): 
                                if (i > 0): 
                                    del addr.items[0:0+i]
                                    i = 0
                                    regions.clear()
                                    regions.append(77)
            if ((probs is None and ((it.level == AddrLevel.CITY or it.level == AddrLevel.REGIONCITY or it.level == AddrLevel.LOCALITY)) and aa.number is not None) and ((i + 1) < len(addr.items)) and addr.items[i + 1].level == AddrLevel.STREET): 
                num = aa.number
                cit = r.ref.clone()
                cit.add_slot("NUMBER", None, True, 0)
                naa = NameAnalyzer()
                naa.init_by_referent(cit, False)
                probs2 = GarHelper.GAR_INDEX._get_string_entries(naa, regions, par_ids, max_count)
                if (probs2 is not None): 
                    aa.number = (None)
                    it.tag = (naa)
                    r = naa
                    pars1 = list()
                    pars1.append(probs2[0].id0_)
                    probs3 = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(addr.items[i + 1].tag, NameAnalyzer), regions, pars1, max_count)
                    if (probs3 is not None): 
                        pass
                    else: 
                        stret = addr.items[i + 1].tag.ref
                        stret.add_slot("NUMBER", num, False, 0)
                        addr.items[i + 1].attrs.number = num
                        naa = NameAnalyzer()
                        naa.init_by_referent(stret, False)
                        addr.items[i + 1].tag = (naa)
                    probs = probs2
            if (((len(regions) < 3) and i == (len(addr.items) - 1) and probs is None) and (((it.level == AddrLevel.CITY or it.level == AddrLevel.LOCALITY or it.level == AddrLevel.TERRITORY) or it.level == AddrLevel.STREET))): 
                cont = False
                for nn in it.attrs.names: 
                    ii = nn.find(' ')
                    if (ii < 0): 
                        continue
                    if (it.attrs.number is not None): 
                        break
                    rr = None
                    if (isinstance(r.ref, GeoReferent)): 
                        rr = (GeoReferent())
                        rr.add_slot(GeoReferent.ATTR_NAME, nn[0:0+ii].upper(), False, 0)
                        for ty in r.ref.typs: 
                            rr.add_slot(GeoReferent.ATTR_TYPE, ty, False, 0)
                    elif (isinstance(r.ref, StreetReferent)): 
                        rr = (StreetReferent())
                        rr.kind = r.ref.kind
                        rr.add_slot(StreetReferent.ATTR_NAME, nn[0:0+ii].upper(), False, 0)
                        for ty in r.ref.typs: 
                            rr.add_slot(StreetReferent.ATTR_TYPE, ty, False, 0)
                    else: 
                        continue
                    naa = NameAnalyzer()
                    naa.init_by_referent(rr, False)
                    probs2 = GarHelper.GAR_INDEX._get_string_entries(naa, regions, par_ids, max_count)
                    if (probs2 is None and i > 0 and (AddressHelper.compare_levels(addr.items[i - 1].level, AddrLevel.CITY) < 0)): 
                        rr = (GeoReferent())
                        rr.add_slot(StreetReferent.ATTR_NAME, nn[0:0+ii].upper(), False, 0)
                        rr.add_slot("TYPE", "город", False, 0)
                        naa = NameAnalyzer()
                        naa.init_by_referent(rr, False)
                        probs2 = GarHelper.GAR_INDEX._get_string_entries(naa, regions, par_ids, max_count)
                    if (probs2 is not None): 
                        for jj in range(len(probs2) - 1, -1, -1):
                            if (probs2[jj].level == AddrLevel.STREET): 
                                del probs2[jj]
                    if (probs2 is not None and len(probs2) > 0 and (len(probs2) < 20)): 
                        ss = StreetReferent()
                        ss.add_slot("NAME", nn[ii + 1:].upper(), False, 0)
                        ss.add_slot(StreetReferent.ATTR_TYPE, "улица", False, 0)
                        if (isinstance(rr, GeoReferent)): 
                            ss.add_slot("GEO", rr, False, 0)
                        else: 
                            ss.higher = Utils.asObjectOrNull(rr, StreetReferent)
                        naa2 = NameAnalyzer()
                        naa2.init_by_referent(ss, False)
                        ok = False
                        pars0 = list()
                        for pp in probs2: 
                            pars0.clear()
                            pars0.append(pp.id0_)
                            probs3 = GarHelper.GAR_INDEX._get_string_entries(naa2, regions, pars0, max_count)
                            if (probs3 is not None): 
                                ok = True
                                break
                        if (not ok): 
                            continue
                        tmp = TextAddress()
                        AnalyzeHelper._create_address_items(tmp, ss, None, 0)
                        if (len(tmp.items) == 2): 
                            del addr.items[i]
                            addr.items[i:i] = tmp.items
                            i -= 1
                            cont = True
                            break
                if (cont): 
                    continue
            if (((probs is None and i == 0 and it.level == AddrLevel.CITY) and ((i + 1) < len(addr.items)) and addr.items[i + 1].level == AddrLevel.DISTRICT) and not rev): 
                del addr.items[0]
                addr.items.insert(1, it)
                i -= 1
                rev = True
                continue
            if (((probs is None and ((it.level == AddrLevel.STREET or it.level == AddrLevel.TERRITORY or it.level == AddrLevel.LOCALITY)) and i == (len(addr.items) - 1)) and aa.number is not None and len(aa.names) > 0) and ar is None): 
                last_num = False
                if (len(r.ref.occurrence) > 0): 
                    occ = r.ref.occurrence[0].get_text()
                    if (occ.endswith(aa.number)): 
                        last_num = True
                if (last_num): 
                    na2 = NameAnalyzer()
                    r.ref.add_slot(StreetReferent.ATTR_NUMBER, None, True, 0)
                    na2.init_by_referent(r.ref, False)
                    probs = GarHelper.GAR_INDEX._get_string_entries(na2, regions, par_ids, max_count)
                    r.ref.add_slot(StreetReferent.ATTR_NUMBER, aa.number, True, 0)
                    if (probs is not None): 
                        ar = AddressReferent()
                        ii = aa.number.find('-')
                        if (ii < 0): 
                            ar.house_or_plot = aa.number
                        else: 
                            ar.house = aa.number[0:0+ii]
                            ar.flat = aa.number[ii + 1:]
                        aa.number = (None)
            if ((probs is not None and len(probs) > 10 and i == 0) and len(regions) == 0): 
                probs = (None)
            if (it.level == AddrLevel.STREET and probs is not None and len(probs) > 5): 
                if (i == 0): 
                    probs = (None)
                else: 
                    it0 = addr.items[i - 1]
                    if (it0.level == AddrLevel.DISTRICT): 
                        if (len(it0.gars) > 0): 
                            for chi in GarHelper.get_children_objects(it0.gars[0].id0_, True): 
                                if (chi.level != GarLevel.CITY): 
                                    continue
                                if (len(chi.attrs.names) > 0 and chi.attrs.names[0] in it0.gars[0].attrs.names): 
                                    pass
                                else: 
                                    continue
                                pars = list()
                                pars.append(AnalyzeHelper.__get_id(chi.id0_))
                                probs1 = GarHelper.GAR_INDEX._get_string_entries(r, regions, pars, max_count)
                                if (probs1 is not None and (len(probs1) < 3)): 
                                    probs = probs1
                        if (len(probs) > 3): 
                            if (i == 1): 
                                probs = (None)
                            elif (addr.items[i - 2].level != AddrLevel.CITY and addr.items[i - 2].level != AddrLevel.REGIONCITY): 
                                probs = (None)
            if (probs is None and i >= 2 and ((it.level == AddrLevel.STREET or it.level == AddrLevel.TERRITORY))): 
                it0 = addr.items[i - 1]
                it00 = addr.items[i - 2]
                if (len(it0.gars) > 0 and it0.gars[0].expired and len(it00.gars) == 1): 
                    pars = list()
                    pars.append(AnalyzeHelper.__get_id(it00.gars[0].id0_))
                    probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, pars, max_count)
            if ((probs is None and i >= 2 and it.level == AddrLevel.STREET) and addr.items[0].level == AddrLevel.REGIONCITY): 
                probs1 = GarHelper.GAR_INDEX._get_string_entries(r, regions, None, max_count)
                if (probs1 is not None and len(probs1) == 1): 
                    probs = probs1
                    if (len(addr.items[i - 1].gars) > 0): 
                        addr.items[i - 1].gars.clear()
            if (probs is None and len(regions) == 1 and it.level == AddrLevel.CITY): 
                r.level = AddrLevel.LOCALITY
                probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
                r.level = AddrLevel.CITY
            if ((probs is None and it.level == AddrLevel.STREET and i > 0) and addr.items[i - 1].level == AddrLevel.TERRITORY and len(addr.items[i - 1].gars) == 0): 
                it0 = addr.items[i - 1]
                na = Utils.asObjectOrNull(it0.tag, NameAnalyzer)
                sr = StreetReferent()
                for n in na.ref.get_string_values("NAME"): 
                    sr.add_slot("NAME", n, False, 0)
                for s in r.ref.slots: 
                    if (s.type_name != "NAME"): 
                        sr.add_slot(s.type_name, s.value, False, 0)
                na1 = NameAnalyzer()
                na1.init_by_referent(sr, False)
                probs = GarHelper.GAR_INDEX._get_string_entries(na1, regions, par_ids, max_count)
                if (probs is not None): 
                    it.tag = (na1)
                    del addr.items[i - 1]
                    i -= 1
            if (probs is not None): 
                self.__add_gars(addr, probs, i, regions, False)
                if ((probs is not None and len(probs) > 0 and len(it.gars) == 0) and i > 0): 
                    it0 = addr.items[i - 1]
                    if (len(it0.gars) == 0 and it0.level == AddrLevel.DISTRICT and i > 1): 
                        it0 = addr.items[i - 2]
                    aa0 = Utils.asObjectOrNull(it0.attrs, AreaAttributes)
                    if ((((it.level == AddrLevel.STREET or it.level == AddrLevel.TERRITORY)) and it0.level == AddrLevel.DISTRICT and len(it0.gars) == 1) and len(aa0.names) > 0): 
                        nam = aa0.names[0]
                        if (len(nam) > 5): 
                            nam = nam[0:0+len(nam) - 3]
                        chils = AddressService.get_children_objects(it0.gars[0].id0_, True)
                        if (chils is not None): 
                            for ch in chils: 
                                ga = Utils.asObjectOrNull(ch.attrs, AreaAttributes)
                                if (ch.level != GarLevel.CITY and ch.level != GarLevel.LOCALITY): 
                                    continue
                                if (len(ga.names) == 0 or not Utils.startsWithString(ga.names[0], nam, True)): 
                                    continue
                                par_ids.clear()
                                par_ids.append(AnalyzeHelper.__get_id(ch.id0_))
                                probs0 = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
                                if (probs0 is not None): 
                                    it00 = GarHelper.create_addr_object(ch)
                                    if (it00 is not None): 
                                        addr.items.insert(i, it00)
                                        i += 1
                                        self.__add_gars(addr, probs0, i, regions, False)
                                break
            elif ((it.level == AddrLevel.TERRITORY and i > 0 and len(addr.items[i - 1].gars) == 1) and len(aa.names) > 0): 
                g0 = addr.items[i - 1].gars[0]
                if (g0.children_count < 500): 
                    childs = AddressService.get_children_objects(g0.id0_, True)
                    if (childs is not None): 
                        for ch in childs: 
                            if (ch.level != GarLevel.AREA or ch.expired): 
                                continue
                            aa0 = Utils.asObjectOrNull(ch.attrs, AreaAttributes)
                            if (aa0.number != aa.number): 
                                continue
                            if (aa.names[0].upper() in aa0.names[0].upper()): 
                                it.gars.append(ch)
                    if (len(it.gars) != 1): 
                        it.gars.clear()
            if (len(it.gars) == 0): 
                if (RestructHelper.restruct(self, addr, i)): 
                    regions.clear()
                    i = -1
                    continue
            if (((len(it.gars) == 0 and it.level == AddrLevel.DISTRICT and i == 1) and len(addr.items[0].gars) == 1 and len(aa.names) > 0) and len(aa.names[0]) > 5): 
                nam = aa.names[0][0:0+5]
                chi = AddressService.get_children_objects(addr.items[0].gars[0].id0_, True)
                if (chi is not None): 
                    for ch in chi: 
                        if (ch.level != GarLevel.MUNICIPALAREA and ch.level != GarLevel.ADMINAREA): 
                            continue
                        aaa = Utils.asObjectOrNull(ch.attrs, AreaAttributes)
                        if (len(aaa.names) == 0): 
                            continue
                        if (aaa.names[0].startswith(nam)): 
                            if (" " in aa.names[0] == " " in aaa.names[0]): 
                                it.gars.append(ch)
                it._sort_gars()
            if (((len(it.gars) == 0 and i > 1 and it.level == AddrLevel.STREET) and addr.items[i - 1].level == AddrLevel.TERRITORY and len(addr.items[i - 1].gars) == 0) and len(addr.items[i - 2].gars) == 1 and ((addr.items[i - 2].level == AddrLevel.CITY or addr.items[i - 2].level == AddrLevel.REGIONCITY))): 
                aa0 = Utils.asObjectOrNull(addr.items[i - 1].attrs, AreaAttributes)
                if (len(aa0.names) > 0 and aa0.number is None and len(aa0.names[0]) > 5): 
                    chi = AddressService.get_children_objects(addr.items[i - 2].gars[0].id0_, True)
                    nam = aa0.names[0][0:0+5]
                    for ch in chi: 
                        if (ch.level != GarLevel.AREA): 
                            continue
                        aaa = Utils.asObjectOrNull(ch.attrs, AreaAttributes)
                        if (len(aaa.names) == 0): 
                            continue
                        if (aaa.names[0].startswith(nam)): 
                            if (" " in aa0.names[0] == " " in aaa.names[0]): 
                                addr.items[i - 1].gars.append(ch)
                    if (len(addr.items[i - 1].gars) == 1): 
                        i -= 1
                        continue
                    addr.items[i - 1].gars.clear()
            if (it.level == AddrLevel.DISTRICT and len(it.gars) > 0): 
                all_area = True
                for g in it.gars: 
                    if (g.level != GarLevel.AREA and g.level != GarLevel.DISTRICT): 
                        all_area = False
                if (all_area): 
                    it.level = AddrLevel.TERRITORY
                    if (((i + 1) < len(addr.items)) and addr.items[i + 1].level == AddrLevel.CITY): 
                        del addr.items[i]
                        addr.items.insert(i + 1, it)
                        it.gars.clear()
                        i -= 1
                        continue
            if (it.level == AddrLevel.LOCALITY and i > 0 and len(it.gars) == 1): 
                it0 = addr.items[i - 1]
                if (it0.level == AddrLevel.CITY and it0._find_gar_by_ids(it.gars[0].parent_ids) is None): 
                    del addr.items[i - 1]
                    i -= 1
            if (len(it.gars) == 0): 
                if (it.level == AddrLevel.COUNTRY): 
                    other_country = True
            if (it.cross_object is not None): 
                r = (Utils.asObjectOrNull(it.cross_object.tag, NameAnalyzer))
                probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
                if (probs is not None): 
                    self.__add_gars(addr, probs, i, regions, True)
        j = 0
        first_pass3089 = True
        while True:
            if first_pass3089: first_pass3089 = False
            else: j += 1
            if (not (j < (len(addr.items) - 1))): break
            it0 = addr.items[j]
            it1 = addr.items[j + 1]
            if (len(it0.gars) > 0 or len(it1.gars) == 0): 
                continue
            ok = False
            if (it0.level == AddrLevel.LOCALITY and it1.level == AddrLevel.LOCALITY): 
                ok = True
            if (not ok): 
                continue
            par_ids.clear()
            for gg in it1.gars: 
                par_ids.append(AnalyzeHelper.__get_id(gg.id0_))
            probs = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(it0.tag, NameAnalyzer), regions, par_ids, 4)
            if (probs is not None): 
                addr.items[j] = it1
                addr.items[j + 1] = it0
                self.__add_gars(addr, probs, j + 1, regions, False)
        self.__remove_items(addr)
        self.__remove_gars(addr)
        j = 0
        while j < len(addr.items): 
            it = addr.items[j]
            if (len(it.gars) > 1): 
                for g in it.gars: 
                    gg = it._find_gar_by_ids(g.parent_ids)
                    if (gg is not None): 
                        if (AddressHelper.can_be_equal_levels(it.level, gg.level)): 
                            it.gars.remove(g)
                        else: 
                            it.gars.remove(gg)
                        break
            j += 1
        j = 0
        first_pass3090 = True
        while True:
            if first_pass3090: first_pass3090 = False
            else: j += 1
            if (not (j < len(addr.items))): break
            it = addr.items[j]
            if (((it.level == AddrLevel.CITY or it.level == AddrLevel.LOCALITY)) and len(it.gars) > 0 and not it.gars[0].expired): 
                pass
            else: 
                continue
            j0 = j
            j -= 1
            has_ok = False
            for jj in range(j, 0, -1):
                it = addr.items[jj]
                if (((len(it.gars) > 0 and it.gars[0].expired)) or len(it.gars) == 0): 
                    pass
                else: 
                    has_ok = True
            if (has_ok or it.level == AddrLevel.CITY): 
                while j > 0: 
                    it = addr.items[j]
                    if (len(it.gars) > 0 and it.gars[0].expired): 
                        del addr.items[j]
                    elif (len(it.gars) == 0): 
                        if (it.level == AddrLevel.DISTRICT): 
                            it.level = AddrLevel.CITYDISTRICT
                            if ((j0 + 1) <= len(addr.items)): 
                                addr.items.insert(j0 + 1, it)
                            else: 
                                addr.items.append(it)
                        del addr.items[j]
                    j -= 1
            break
        self.__add_miss_items(addr)
        k = 0
        while k < (len(addr.items) - 1): 
            j = 0
            while j < (len(addr.items) - 1): 
                if (AddressHelper.compare_levels(addr.items[j].level, addr.items[j + 1].level) > 0): 
                    it = addr.items[j]
                    addr.items[j] = addr.items[j + 1]
                    addr.items[j + 1] = it
                j += 1
            k += 1
        k = 0
        while k < (len(addr.items) - 1): 
            if (addr.items[k].level == addr.items[k + 1].level and addr.items[k].level != AddrLevel.TERRITORY): 
                it = addr.items[k]
                it1 = addr.items[k + 1]
                if (len(it.gars) == len(it1.gars) and len(it.gars) > 0 and it1.gars[0] in it.gars): 
                    del addr.items[k + 1]
                    k -= 1
                elif (len(it.gars) == 0 and len(it1.gars) > 0): 
                    del addr.items[k]
                    k -= 1
                elif (len(it.gars) > 0 and len(it1.gars) == 0): 
                    del addr.items[k + 1]
                    k -= 1
            k += 1
        if (ua_country is not None and ((len(addr.items) == 0 or addr.items[0].level != AddrLevel.COUNTRY))): 
            addr.items.insert(0, ua_country)
        return ar
    
    def _process_rest(self, addr : 'TextAddress', ar : 'AddressReferent', one : bool, aar : 'AnalysisResult') -> None:
        if (ar is not None): 
            if ((ar.house_or_plot is not None and self.m_params is not None and self.m_params.is_plot) and ar.plot is None): 
                ar.plot = ar.house_or_plot
                ar.house_or_plot = None
            HouseRoomHelper.process_house_and_rooms(self, ar, addr)
            has_details = False
            for it in addr.items: 
                if (it.detail_typ != DetailType.UNDEFINED): 
                    has_details = True
            if (not has_details): 
                par = None
                wrappar104 = RefOutArgWrapper(None)
                det = HouseRoomHelper.create_dir_details(ar, wrappar104)
                par = wrappar104.value
                if (det != DetailType.UNDEFINED and addr.last_item is not None): 
                    ao = addr.last_item
                    if (len(addr.items) > 1 and ((addr.items[len(addr.items) - 2].level == addr.last_item.level or ((addr.last_item.level == AddrLevel.PLOT and addr.last_item.attrs.number == "б/н"))))): 
                        if (par == "часть" and len(addr.items) > 2 and addr.items[len(addr.items) - 3].level == AddrLevel.TERRITORY): 
                            ao = addr.items[len(addr.items) - 3]
                        else: 
                            ao = addr.items[len(addr.items) - 2]
                    ao.detail_typ = det
                    ao.detail_param = par
            else: 
                j = 0
                first_pass3091 = True
                while True:
                    if first_pass3091: first_pass3091 = False
                    else: j += 1
                    if (not (j < (len(addr.items) - 1))): break
                    it = addr.items[j]
                    if (it.detail_typ == DetailType.UNDEFINED or len(it.gars) == 0): 
                        continue
                    it2 = addr.items[j + 1]
                    if (len(it2.gars) == 0): 
                        continue
                    for g in it2.gars: 
                        if (it._find_gar_by_ids(g.parent_ids) is not None): 
                            it.detail_typ = DetailType.UNDEFINED
                            it.detail_param = (None)
                            break
            HouseRoomHelper.process_other_details(addr, ar)
            ar.tag = (addr)
        elif (addr.text is not None): 
            i = addr.end_char + 1
            first_pass3092 = True
            while True:
                if first_pass3092: first_pass3092 = False
                else: i += 1
                if (not (i < len(addr.text))): break
                ch = addr.text[i]
                if (ch == ' ' or ch == ',' or ch == '.'): 
                    continue
                txt = addr.text[i:]
                rt = AddressItemToken.create_address(txt)
                if (rt is None and str.isdigit(txt[0])): 
                    rt = AddressItemToken.create_address("дом " + txt)
                if (rt is not None): 
                    ar = (Utils.asObjectOrNull(rt.referent, AddressReferent))
                    HouseRoomHelper.process_house_and_rooms(self, ar, addr)
                    addr.end_char = (i + rt.end_char)
                break
        if (addr.last_item is not None): 
            if (AddressHelper.compare_levels(addr.last_item.level, AddrLevel.STREET) > 0): 
                if (self.__remove_gars(addr)): 
                    self.__add_miss_items(addr)
                if (one): 
                    HouseRoomHelper.try_parse_list_items(self, addr, aar)
        AnalyzeHelper.__correct_levels(addr)
    
    def __remove_items(self, res : 'TextAddress') -> None:
        j = 0
        first_pass3093 = True
        while True:
            if first_pass3093: first_pass3093 = False
            else: j += 1
            if (not (j < (len(res.items) - 1))): break
            it = res.items[j]
            it1 = res.items[j + 1]
            if (len(it1.gars) == 0): 
                continue
            aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
            aa1 = Utils.asObjectOrNull(it1.attrs, AreaAttributes)
            ok = False
            for g in it1.gars: 
                if (it._find_gar_by_ids(g.parent_ids) is not None): 
                    ok = True
            if (ok): 
                continue
            if (it.level == AddrLevel.DISTRICT and it1.level == AddrLevel.CITY): 
                if (len(aa.names) > 0 and len(aa1.names) > 0 and len(aa1.names[0]) > 3): 
                    if (aa.names[0].startswith(aa1.names[0][0:0+3])): 
                        ok = True
                if (not ok and ((j + 2) < len(res.items))): 
                    it2 = res.items[j + 2]
                    if (it2.level == AddrLevel.LOCALITY or it2.level == AddrLevel.CITY or it2.level == AddrLevel.SETTLEMENT): 
                        for g in it2.gars: 
                            if (it._find_gar_by_ids(g.parent_ids) is not None): 
                                ok = True
                        if (ok): 
                            del res.items[j + 1]
                            it1 = it2
                if (j == 0 and len(it1.gars) == 1): 
                    del res.items[0]
                    j -= 1
                    continue
            if ((not ok and it.level == AddrLevel.CITY and ((it1.level == AddrLevel.LOCALITY or it1.level == AddrLevel.TERRITORY))) and j > 0): 
                it0 = res.items[j - 1]
                aa0 = Utils.asObjectOrNull(it0.attrs, AreaAttributes)
                if (it0.level == AddrLevel.DISTRICT): 
                    for g in it1.gars: 
                        if (it0._find_gar_by_ids(g.parent_ids) is not None): 
                            ok = True
                    if (ok): 
                        del res.items[j]
                        j -= 1
                        continue
    
    def __add_miss_items(self, addr : 'TextAddress') -> None:
        j = 0
        first_pass3094 = True
        while True:
            if first_pass3094: first_pass3094 = False
            else: j += 1
            if (not (j < (len(addr.items) - 1))): break
            it0 = addr.items[j]
            it1 = addr.items[j + 1]
            if (len(it1.gars) == 0): 
                continue
            if (AnalyzeHelper.__contains_one_of_parent(addr, it1.gars)): 
                if (((it0.level == AddrLevel.REGIONCITY or it0.level == AddrLevel.REGIONAREA)) and it1.level == AddrLevel.LOCALITY): 
                    pass
                else: 
                    continue
            par = self.__get_common_parent(addr, it1.gars)
            if (par is None): 
                continue
            if (addr.find_item_by_gar_level(par.level) is not None): 
                continue
            par2 = None
            par3 = None
            if (addr.find_gar_by_ids(par.parent_ids) is not None): 
                pass
            else: 
                if (len(par.parent_ids) == 0): 
                    continue
                par2 = self.get_gar_object(par.parent_ids[0])
                if (par2 is None): 
                    continue
                if (addr.find_gar_by_ids(par2.parent_ids) is not None): 
                    pass
                else: 
                    if (len(par2.parent_ids) == 0): 
                        continue
                    par3 = self.get_gar_object(par2.parent_ids[0])
                    if (par3 is None): 
                        continue
                    if (addr.find_gar_by_ids(par3.parent_ids) is not None): 
                        pass
                    else: 
                        continue
            to1 = GarHelper.create_addr_object(par)
            if (to1 is not None): 
                exi = addr.find_item_by_level(to1.level)
                if (exi is None): 
                    addr.items.insert(j + 1, to1)
                elif (not par in exi.gars): 
                    exi.gars.append(par)
            if (par2 is not None): 
                to2 = GarHelper.create_addr_object(par2)
                if (to2 is not None): 
                    exi = addr.find_item_by_level(to2.level)
                    if (exi is None): 
                        addr.items.insert(j + 1, to2)
                    elif (not par2 in exi.gars): 
                        exi.gars.append(par2)
                if (par3 is not None): 
                    to3 = GarHelper.create_addr_object(par3)
                    if (to3 is not None): 
                        exi = addr.find_item_by_level(to3.level)
                        if (exi is None): 
                            addr.items.insert(j + 1, to3)
                        elif (not par2 in exi.gars): 
                            exi.gars.append(par3)
        if (len(addr.items) > 0 and len(addr.items[0].gars) >= 1 and len(addr.items[0].gars[0].parent_ids) > 0): 
            p = self.get_gar_object(addr.items[0].gars[0].parent_ids[0])
            while p is not None: 
                to1 = GarHelper.create_addr_object(p)
                if (to1 is not None): 
                    addr.items.insert(0, to1)
                if (len(p.parent_ids) == 0): 
                    break
                p = self.get_gar_object(p.parent_ids[0])
    
    @staticmethod
    def __contains_one_of_parent(a : 'TextAddress', gos : typing.List['GarObject']) -> bool:
        for g in gos: 
            if (a.find_gar_by_ids(g.parent_ids) is not None): 
                return True
        return False
    
    def __get_common_parent(self, a : 'TextAddress', gos : typing.List['GarObject']) -> 'GarObject':
        id0_ = None
        for g in gos: 
            if (len(g.parent_ids) > 0): 
                if (id0_ is None or id0_ in g.parent_ids): 
                    id0_ = (g.parent_ids[0] if len(g.parent_ids) > 0 else None)
                elif (id0_ is not None and id0_ in g.parent_ids): 
                    pass
                else: 
                    return None
        if (id0_ is None): 
            return None
        return self.get_gar_object(id0_)
    
    def __add_gars(self, addr : 'TextAddress', probs : typing.List['AreaTreeObject'], i : int, regions : bytearray, cross : bool) -> None:
        if (probs is None or len(probs) == 0): 
            return
        it = addr.items[i]
        if (cross): 
            it = it.cross_object
        it.gars.clear()
        aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
        if (it.level == AddrLevel.LOCALITY): 
            has_street = False
            j = i + 1
            while j < len(addr.items): 
                if (addr.items[j].level == AddrLevel.STREET): 
                    has_street = True
                j += 1
            if (has_street): 
                for j in range(len(probs) - 1, -1, -1):
                    if (probs[j].level == AddrLevel.STREET): 
                        del probs[j]
        if (len(probs) > 1 and self.m_params is not None and len(self.m_params.default_regions) > 0): 
            has_reg = 0
            for g in probs: 
                if (Utils.indexOfList(self.m_params.default_regions, g.region, 0) >= 0): 
                    has_reg += 1
            if (has_reg > 0 and (has_reg < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (Utils.indexOfList(self.m_params.default_regions, probs[k].region, 0) < 0): 
                        del probs[k]
        if (len(probs) > 1 and len(aa.miscs) > 0 and it.level != AddrLevel.TERRITORY): 
            has_equ_misc = 0
            for g in probs: 
                if (aa.find_misc(g.miscs) is not None): 
                    has_equ_misc += 1
            if (has_equ_misc > 0 and (has_equ_misc < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (aa.find_misc(probs[k].miscs) is None): 
                        del probs[k]
        if (((len(probs) > 1 and it.level != AddrLevel.TERRITORY and it.level != AddrLevel.DISTRICT) and not "населенный пункт" in aa.types and not "станция" in aa.types) and not "поселение" in aa.types): 
            has_equ_type = 0
            for g in probs: 
                if (aa.has_equal_type(g.typs)): 
                    has_equ_type += 1
            if (has_equ_type > 0 and (has_equ_type < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (not aa.has_equal_type(probs[k].typs)): 
                        del probs[k]
        if (len(probs) > 1 and it.level != AddrLevel.UNDEFINED): 
            has_equ_level = 0
            gstat2 = 0
            for g in probs: 
                if (it.level == g.level): 
                    has_equ_level += 1
                if (g.status == GarStatus.OK2): 
                    gstat2 += 1
            if (gstat2 == 0 and has_equ_level > 0 and (has_equ_level < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (it.level != probs[k].level): 
                        del probs[k]
        if (len(probs) > 1): 
            has_err = 0
            for g in probs: 
                if (g.status == GarStatus.ERROR): 
                    has_err += 1
            if (has_err > 0 and (has_err < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (probs[k].status == GarStatus.ERROR): 
                        del probs[k]
        if (len(probs) > 1): 
            has_act = 0
            oktyp = 0
            pars = list()
            for g in probs: 
                if (g.level == AddrLevel.DISTRICT or g.check_type(Utils.asObjectOrNull(it.tag, NameAnalyzer)) > 0): 
                    oktyp += 1
                if (g.expired): 
                    has_act += 1
                if (g.parent_ids is not None): 
                    for p in g.parent_ids: 
                        if (not p in pars): 
                            pars.append(p)
            if (has_act > 0 and (has_act < oktyp) and (len(pars) < 2)): 
                for k in range(len(probs) - 1, -1, -1):
                    if (probs[k].expired): 
                        del probs[k]
        if (i > 0 and len(probs) > 1): 
            it0 = addr.items[i - 1]
            if ((it.level == AddrLevel.STREET or it.level == AddrLevel.TERRITORY or ((it.level == AddrLevel.LOCALITY and it0.level == AddrLevel.DISTRICT)))): 
                has_dir_parent = 0
                for g in probs: 
                    if (AnalyzeHelper.__find_parent_prob(it0, g) is not None and not g.expired): 
                        has_dir_parent += 1
                if (has_dir_parent > 0 and (has_dir_parent < len(probs))): 
                    for k in range(len(probs) - 1, -1, -1):
                        g = probs[k]
                        if (AnalyzeHelper.__find_parent_prob(it0, g) is not None): 
                            continue
                        del probs[k]
        if (i > 0 and len(probs) > 1): 
            it0 = addr.items[i - 1]
            aa0 = Utils.asObjectOrNull(it0.attrs, AreaAttributes)
            if (len(aa0.names) > 0 and ((it.level == AddrLevel.LOCALITY or it.level == AddrLevel.TERRITORY)) and it0.level == AddrLevel.DISTRICT): 
                probs0 = None
                for p in probs: 
                    if (p.parent_ids is None or len(p.parent_ids) == 0): 
                        continue
                    par = self.get_gar_object("a{0}".format(p.parent_ids[0]))
                    if (par is None): 
                        continue
                    for kk in range(2):
                        aa1 = Utils.asObjectOrNull(par.attrs, AreaAttributes)
                        if (len(aa1.names) > 0 and len(aa1.names[0]) >= 4): 
                            if (aa0.names[0].startswith(aa1.names[0][0:0+4])): 
                                if (probs0 is None): 
                                    probs0 = list()
                                probs0.append(p)
                                break
                        if (kk > 0): 
                            break
                        if (par.parent_ids is None or len(par.parent_ids) == 0): 
                            break
                        par2 = self.get_gar_object(par.parent_ids[0])
                        if (par2 is None): 
                            break
                        par = par2
                if (probs0 is not None): 
                    probs.clear()
                    probs.extend(probs0)
        if ((len(probs) > 1 and it.level == AddrLevel.STREET and len(aa.types) > 1) and "улица" in aa.types): 
            typ0 = (aa.types[1] if aa.types[0] == "улица" else aa.types[0])
            has_typ = 0
            for p in probs: 
                if (typ0 in p.typs): 
                    has_typ += 1
            if (has_typ > 0 and (has_typ < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (not typ0 in probs[k].typs): 
                        del probs[k]
        if (len(probs) > 1 and it.level == AddrLevel.STREET and len(aa.types) > 0): 
            has_typ = 0
            for p in probs: 
                if (p.typs is not None and len(p.typs) == len(aa.types)): 
                    has_typ += 1
            if (has_typ > 0 and (has_typ < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (probs[k].typs is not None and len(probs[k].typs) != len(aa.types)): 
                        del probs[k]
        ignore_gars = False
        for p in probs: 
            if (it.level == AddrLevel.STREET and i > 0): 
                ok = False
                ids = list()
                if (p.parent_ids is not None): 
                    for id0_ in p.parent_ids: 
                        ids.clear()
                        ids.append("a{0}".format(id0_))
                        gg = addr.find_gar_by_ids(ids)
                        if (gg is None): 
                            continue
                        if (gg.level == GarLevel.CITY or gg.level == GarLevel.LOCALITY or gg.level == GarLevel.AREA): 
                            ok = True
                            break
                        if (((gg.level == GarLevel.ADMINAREA or gg.level == GarLevel.REGION)) and "город" in gg.attrs.types): 
                            ok = True
                            break
                if (p.parent_parent_ids is not None and not ok and not "километр" in aa.types): 
                    for id0_ in p.parent_parent_ids: 
                        ids.clear()
                        ids.append("a{0}".format(id0_))
                        gg = addr.find_gar_by_ids(ids)
                        if (gg is None): 
                            continue
                        if ((gg.level == GarLevel.CITY or gg.level == GarLevel.LOCALITY or gg.level == GarLevel.AREA) or gg.level == GarLevel.SETTLEMENT): 
                            ok = True
                            break
                        if (((gg.level == GarLevel.ADMINAREA or gg.level == GarLevel.REGION)) and "город" in gg.attrs.types): 
                            ok = True
                            break
                if (not ok): 
                    continue
            g = self.get_gar_object("a{0}".format(p.id0_))
            if (g is None): 
                continue
            if (i == 0 and it.level == AddrLevel.DISTRICT): 
                if (g.level == GarLevel.REGION and g.attrs.types[0] in it.attrs.types): 
                    it.level = AddrLevel.REGIONAREA
                    it.gars.clear()
                    it.gars.append(g)
                    break
            if (p.miscs is not None and len(p.miscs) > 0): 
                g.attrs.miscs.extend(p.miscs)
            ga = Utils.asObjectOrNull(g.attrs, AreaAttributes)
            na = NameAnalyzer()
            na.process(ga.names, (ga.types[0] if len(ga.types) > 0 else None))
            co = na.calc_equal_coef(Utils.asObjectOrNull(it.tag, NameAnalyzer))
            if (co < 0): 
                continue
            if (((it.level == AddrLevel.LOCALITY or it.level == AddrLevel.TERRITORY)) and i >= 2): 
                ok = False
                if (addr.find_gar_by_ids(g.parent_ids) is not None): 
                    ok = True
                else: 
                    for kk in range(i - 1, 0, -1):
                        it0 = addr.items[kk]
                        if (p.parent_parent_ids is not None): 
                            for ppid in p.parent_parent_ids: 
                                if (it0._find_gar_by_id("a{0}".format(ppid)) is not None): 
                                    ok = True
                                    break
                        if (ok): 
                            break
                        for pid in g.parent_ids: 
                            par = self.get_gar_object(pid)
                            if (par is None): 
                                continue
                            ga0 = Utils.asObjectOrNull(par.attrs, AreaAttributes)
                            if (len(ga0.names) == 0 or (len(ga0.names[0]) < 4)): 
                                continue
                            sub = ga0.names[0][0:0+4]
                            aa0 = Utils.asObjectOrNull(it0.attrs, AreaAttributes)
                            if (len(aa0.names) > 0 and Utils.startsWithString(aa0.names[0], sub, True)): 
                                ok = True
                                break
                        if (ok): 
                            break
                        if (p.parent_parent_ids is not None): 
                            for ppid in p.parent_parent_ids: 
                                par = self.get_gar_object("a{0}".format(ppid))
                                if (par is None): 
                                    continue
                                ga0 = Utils.asObjectOrNull(par.attrs, AreaAttributes)
                                if (len(ga0.names) == 0 or (len(ga0.names[0]) < 4)): 
                                    continue
                                sub = ga0.names[0][0:0+4]
                                aa0 = Utils.asObjectOrNull(it0.attrs, AreaAttributes)
                                if (len(aa0.names) > 0 and Utils.startsWithString(aa0.names[0], sub, True)): 
                                    ok = True
                                    break
                        if (ok): 
                            break
                if (not ok): 
                    continue
            if (na.sec is not None or p.status == GarStatus.OK2): 
                if (p.id0_ == 4001): 
                    pass
                if ((i + 1) >= len(addr.items) or na.sec is None): 
                    continue
                it1 = addr.items[i + 1]
                na1 = Utils.asObjectOrNull(it1.tag, NameAnalyzer)
                if (na1 is None): 
                    continue
                if (not na1.can_be_equals(na.sec)): 
                    continue
                it1.gars.append(g)
                ignore_gars = True
                it.gars.clear()
                it.is_reconstructed = True
            if (g.level == GarLevel.REGION and it.level == AddrLevel.CITY and i == 0): 
                it.level = AddrLevel.REGIONCITY
            elif (g.level == GarLevel.REGION and it.level != AddrLevel.REGIONCITY): 
                it.level = AddrLevel.REGIONAREA
            if (not it.can_be_equals_glevel(g)): 
                if (len(probs) == 1 and it.level == AddrLevel.STREET and g.level == GarLevel.AREA): 
                    pass
                else: 
                    continue
            if (not ignore_gars): 
                it.gars.append(g)
        if (i == 0 and len(it.gars) > 1 and ((it.level == AddrLevel.CITY or it.level == AddrLevel.LOCALITY))): 
            ok = False
            for g in it.gars: 
                if (g.level == GarLevel.CITY): 
                    ga = Utils.asObjectOrNull(g.attrs, AreaAttributes)
                    for n in ga.names: 
                        if (RegionHelper.is_big_city(n) is not None): 
                            ok = True
                    if (ok): 
                        break
            if (ok): 
                for k in range(len(it.gars) - 1, -1, -1):
                    ga = Utils.asObjectOrNull(it.gars[k].attrs, AreaAttributes)
                    ok = False
                    if (it.gars[k].level == GarLevel.CITY): 
                        for n in ga.names: 
                            if (RegionHelper.is_big_city(n) is not None): 
                                ok = True
                    if (not ok): 
                        del it.gars[k]
                    if (len(aa.types) > 0 and aa.types[0] == "населенный пункт"): 
                        aa.types.clear()
                        aa.types.append(ga.types[0])
        if (len(it.gars) > 1 and it.level == AddrLevel.CITY): 
            g1 = it.find_gar_by_level(GarLevel.MUNICIPALAREA)
            if (g1 is not None and it.find_gar_by_level(GarLevel.CITY) is not None): 
                it.gars.remove(g1)
        if (len(it.gars) > 1 and i > 0 and ((it.level == AddrLevel.LOCALITY or it.level == AddrLevel.CITY or it.level == AddrLevel.TERRITORY))): 
            for j in range(i - 1, -1, -1):
                it0 = addr.items[j]
                if (len(it0.gars) == 0): 
                    continue
                ap = Utils.asObjectOrNull(it0.gars[0].attrs, AreaAttributes)
                if (ap is None or len(ap.names) == 0): 
                    break
                gars = None
                eq_parens = False
                lev = GarLevel.UNDEFINED
                for g in it.gars: 
                    if (len(g.parent_ids) == 0): 
                        continue
                    par = self.get_gar_object(g.parent_ids[0])
                    if (par is None): 
                        continue
                    if (lev == GarLevel.UNDEFINED or par.level == lev): 
                        lev = par.level
                    else: 
                        gars = (None)
                        break
                    pp = Utils.asObjectOrNull(par.attrs, AreaAttributes)
                    if (pp is None or len(pp.names) == 0): 
                        continue
                    if (par in it.gars): 
                        gars = (None)
                        break
                    str0 = ap.names[0]
                    str1 = pp.names[0]
                    k = 0
                    k = 0
                    while (k < len(str0)) and (k < len(str1)): 
                        if (str0[k] != str1[k]): 
                            break
                        k += 1
                    if (k >= (len(str0) - 1) or k >= (len(str1) - 1)): 
                        if (gars is None): 
                            gars = list()
                        gars.append(g)
                        if (par in it0.gars): 
                            eq_parens = True
                if (gars is not None and (len(gars) < len(it.gars))): 
                    it.gars = gars
                    if (not eq_parens and j > 0): 
                        del addr.items[j]
                break
            if (len(it.gars) > 1): 
                for j in range(i - 1, -1, -1):
                    it0 = addr.items[j]
                    if (len(it0.gars) == 0): 
                        continue
                    gars = None
                    for g in it.gars: 
                        ok = False
                        if (it0._find_gar_by_ids(g.parent_ids) is not None): 
                            ok = True
                        else: 
                            for pid in g.parent_ids: 
                                p = self.get_gar_object(pid)
                                if (p is None): 
                                    continue
                                if (it0._find_gar_by_ids(p.parent_ids) is not None): 
                                    ok = True
                                    break
                        if (ok): 
                            if (gars is None): 
                                gars = list()
                            gars.append(g)
                    if (gars is None): 
                        continue
                    if (len(gars) < len(it.gars)): 
                        it.gars = gars
                    break
        if (len(it.gars) > 1 and it.level == AddrLevel.STREET and len(aa.names) > 0): 
            has_nam = 0
            for g in it.gars: 
                if (aa.names[0] in g.attrs.names or aa.names[0] in g.attrs.names[0]): 
                    has_nam += 1
            if (has_nam > 0 and (has_nam < len(it.gars))): 
                for k in range(len(it.gars) - 1, -1, -1):
                    if (not aa.names[0] in it.gars[k].attrs.names and not aa.names[0] in it.gars[k].attrs.names[0]): 
                        del it.gars[k]
        if ((i > 0 and len(it.gars) > 1 and it.level == AddrLevel.STREET) and addr.items[i - 1].level == AddrLevel.TERRITORY and len(addr.items[i - 1].gars) == 1): 
            g0 = addr.items[i - 1].gars[0]
            has_nam = 0
            for g in it.gars: 
                if (g.id0_ in g0.parent_ids): 
                    has_nam += 1
            if (has_nam > 0 and (has_nam < len(it.gars))): 
                for k in range(len(it.gars) - 1, -1, -1):
                    if (not it.gars[k].id0_ in g0.parent_ids): 
                        del it.gars[k]
        if ((len(it.gars) > 1 and i > 0 and it.level == AddrLevel.STREET) and len(addr.items[i - 1].gars) == 1): 
            g0 = addr.items[i - 1].gars[0]
            has_nam = 0
            for g in it.gars: 
                if (len(g.parent_ids) == 1 and g.parent_ids[0] == g0.id0_ and not g.expired): 
                    has_nam += 1
            if (has_nam > 0 and (has_nam < len(it.gars))): 
                for k in range(len(it.gars) - 1, -1, -1):
                    if (len(it.gars[k].parent_ids) != 1 or it.gars[k].parent_ids[0] != g0.id0_): 
                        del it.gars[k]
        if (len(it.gars) > 1 and i > 0 and ((it.level == AddrLevel.STREET or "улица" in aa.types))): 
            if (len(aa.miscs) == 0): 
                has = 0
                for g in it.gars: 
                    if (len(g.attrs.miscs) > 0): 
                        has += 1
                if (has > 0 and (has < len(it.gars))): 
                    for k in range(len(it.gars) - 1, -1, -1):
                        if (len(it.gars[k].attrs.miscs) > 0): 
                            del it.gars[k]
                elif (has == len(it.gars) and it.tag.ref is not None and len(it.tag.ref.occurrence) > 0): 
                    txt = it.tag.ref.occurrence[0].get_text()
                    ii = txt.rfind(',')
                    if (ii > 0): 
                        txt = txt[ii + 1:].strip()
                    txt = txt.upper()
                    gars = list()
                    for g in it.gars: 
                        ga = Utils.asObjectOrNull(g.attrs, AreaAttributes)
                        if (len(ga.miscs) == 0): 
                            continue
                        mi = ga.miscs[0]
                        if (mi in txt or "{0}.".format(mi[0]) in txt): 
                            gars.append(g)
                    if (len(gars) > 0 and (len(gars) < len(it.gars))): 
                        it.gars = gars
            else: 
                has = 0
                for g in it.gars: 
                    if (aa.miscs[0] in g.attrs.miscs): 
                        has += 1
                if (has > 0 and (has < len(it.gars))): 
                    for k in range(len(it.gars) - 1, -1, -1):
                        if (not aa.miscs[0] in it.gars[k].attrs.miscs): 
                            del it.gars[k]
            if (len(it.gars) > 1 and len(aa.types) > 1 and "улица" in aa.types): 
                typ = (aa.types[1] if aa.types[0] == "улица" else aa.types[0])
                has = 0
                for g in it.gars: 
                    if (typ in g.attrs.types): 
                        has += 1
                if (has > 0 and (has < len(it.gars))): 
                    for k in range(len(it.gars) - 1, -1, -1):
                        if (not typ in it.gars[k].attrs.types): 
                            del it.gars[k]
        if ((len(it.gars) > 1 and i == 0 and it.level == AddrLevel.CITY) and len(aa.names) > 0): 
            gars1 = None
            for g in it.gars: 
                gg = g
                while gg is not None: 
                    if (gg.level != GarLevel.REGION): 
                        if (gg.parent_ids is None or len(gg.parent_ids) == 0): 
                            break
                        gg = self.get_gar_object(gg.parent_ids[0])
                        continue
                    aaa = Utils.asObjectOrNull(gg.attrs, AreaAttributes)
                    if (len(aaa.names) > 0 and len(aa.names[0]) > 3): 
                        if (aaa.names[0].startswith(aa.names[0][0:0+len(aa.names[0]) - 3])): 
                            if (gars1 is None): 
                                gars1 = list()
                            gars1.append(g)
                    break
            if (gars1 is not None): 
                it.gars = gars1
        if (i == 0): 
            for g in it.gars: 
                if (g.region_number != 0 and not g.region_number in regions): 
                    regions.append(g.region_number)
        if (len(it.gars) > 10): 
            it.gars.clear()
        it._sort_gars()
    
    @staticmethod
    def __find_parent_prob(it : 'AddrObject', ato : 'AreaTreeObject') -> 'GarObject':
        if (len(ato.parent_ids) == 0): 
            return None
        for ii in ato.parent_ids: 
            go = it._find_gar_by_id("a{0}".format(ii))
            if (go is not None): 
                return go
        return None
    
    __m_proc0 = None
    
    __m_proc1 = None
    
    @staticmethod
    def init() -> None:
        AnalyzeHelper.__m_proc0 = ProcessorService.create_empty_processor()
        AnalyzeHelper.__m_proc1 = ProcessorService.create_processor()
        for a in AnalyzeHelper.__m_proc1.analyzers: 
            if (((a.name == "GEO" or a.name == "ADDRESS" or a.name == "NAMEDENTITY") or a.name == "DATE" or a.name == "PHONE") or a.name == "URI"): 
                pass
            else: 
                a.ignore_this_analyzer = True
    
    def get_gar_object(self, id0_ : str) -> 'GarObject':
        if (id0_ is None): 
            return None
        res = None
        wrapres105 = RefOutArgWrapper(None)
        inoutres106 = Utils.tryGetValue(self.__m_gar_hash, id0_, wrapres105)
        res = wrapres105.value
        if (inoutres106): 
            return res
        res = GarHelper.get_object(id0_)
        if (res is None): 
            return None
        self.__m_gar_hash[id0_] = res
        if (id0_[0] != 'a'): 
            self.index_read_count += 1
        return res
    
    def get_houses_in_street(self, id0_ : str) -> 'HousesInStreet':
        if (id0_ is None): 
            return None
        res = None
        wrapres107 = RefOutArgWrapper(None)
        inoutres108 = Utils.tryGetValue(self.__m_houses, id0_, wrapres107)
        res = wrapres107.value
        if (inoutres108): 
            return res
        res = GarHelper.GAR_INDEX.getaohouses(AnalyzeHelper.__get_id(id0_))
        if (res is not None): 
            self.index_read_count += 1
        self.__m_houses[id0_] = res
        return res
    
    def get_rooms_in_object(self, id0_ : str) -> 'RoomsInHouse':
        if (id0_ is None): 
            return None
        res = None
        wrapres109 = RefOutArgWrapper(None)
        inoutres110 = Utils.tryGetValue(self.__m_rooms, id0_, wrapres109)
        res = wrapres109.value
        if (inoutres110): 
            return res
        if (id0_[0] == 'h'): 
            res = GarHelper.GAR_INDEX.get_rooms_in_house(AnalyzeHelper.__get_id(id0_))
        elif (id0_[0] == 'r'): 
            res = GarHelper.GAR_INDEX.get_rooms_in_rooms(AnalyzeHelper.__get_id(id0_))
        if (res is not None): 
            self.index_read_count += 1
        self.__m_rooms[id0_] = res
        return res
    
    def analyze(self, txt : str, corr : typing.List[tuple], one_addr : bool, pars : 'ProcessTextParams') -> typing.List['TextAddress']:
        if (Utils.isNullOrEmpty(txt)): 
            return None
        self.m_params = pars
        co = None
        if (corr is not None and "" in corr): 
            co = corr[""]
        second_var = None
        detail = None
        if (one_addr): 
            wrapsecond_var111 = RefOutArgWrapper(None)
            wrapdetail112 = RefOutArgWrapper(None)
            txt = CorrectionHelper.correct(txt, wrapsecond_var111, wrapdetail112)
            second_var = wrapsecond_var111.value
            detail = wrapdetail112.value
            self.corrected_text = txt
        res = self.__analyze(txt, co, one_addr)
        res2 = (None if second_var is None else self.__analyze(second_var, co, one_addr))
        if ((res is not None and one_addr and len(res) == 1) and len(res[0].items) > 0 and AddressHelper.compare_levels(res[0].items[0].level, AddrLevel.TERRITORY) >= 0): 
            ii = txt.find(' ')
            if (ii > 0): 
                txt1 = "город {0}, {1}".format(txt[0:0+ii], txt[ii + 1:])
                res1 = self.__analyze(txt1, co, one_addr)
                if ((res1 is not None and len(res1) > 0 and res1[0].coef > res[0].coef) and res1[0].coef >= 80): 
                    res = res1
        if (res is not None and len(res) == 1 and res[0].last_item is not None): 
            if (res2 is not None and len(res2) == 1 and res2[0].coef > res[0].coef): 
                HouseRoomHelper.try_process_details(res2[0], detail)
                return res2
            if (len(res[0].last_item.gars) > 0): 
                HouseRoomHelper.try_process_details(res[0], detail)
                return res
        if (res2 is not None and len(res2) == 1): 
            if (res is None or len(res) == 0 or (res[0].coef < res2[0].coef)): 
                HouseRoomHelper.try_process_details(res2[0], detail)
                return res2
        if (res is not None and detail is not None): 
            for r in res: 
                HouseRoomHelper.try_process_details(r, detail)
        return res
    
    def __analyze(self, txt : str, co : typing.List[tuple], one_addr : bool) -> typing.List['TextAddress']:
        if (AnalyzeHelper.__m_proc1 is None): 
            return list()
        ar = None
        ar = AnalyzeHelper.__m_proc1.process(SourceOfAnalysis._new113(txt, co, False, ("ADDRESS" if one_addr else None)), None, None)
        res = self._analyze1(ar, txt, co, one_addr)
        if (len(res) > 0): 
            return res
        if ((isinstance(ar.first_token, TextToken)) and ar.first_token.length_char > 4): 
            txt = ("г." + txt)
            ar = AnalyzeHelper.__m_proc1.process(SourceOfAnalysis._new113(txt, co, False, ("ADDRESS" if one_addr else None)), None, None)
            res = self._analyze1(ar, txt, co, one_addr)
        return res
    
    def _analyze1(self, ar : 'AnalysisResult', txt : str, co : typing.List[tuple], one_addr : bool) -> typing.List['TextAddress']:
        res = list()
        if (ar is None or ar.first_token is None): 
            return res
        reg_acr = None
        acr_end = None
        if (((one_addr and (isinstance(ar.first_token, TextToken)) and ar.first_token.chars.is_letter) and ar.first_token.length_char > 1 and (ar.first_token.length_char < 4)) and ar.first_token.next0_ is not None): 
            reg_acr = ar.first_token.term
            acr_end = ar.first_token
        elif ((((one_addr and (isinstance(ar.first_token, TextToken)) and ar.first_token.chars.is_letter) and ar.first_token.length_char == 1 and ar.first_token.next0_ is not None) and ar.first_token.next0_.is_char('.') and (isinstance(ar.first_token.next0_.next0_, TextToken))) and ar.first_token.next0_.next0_.chars.is_letter and ar.first_token.next0_.next0_.length_char == 1): 
            reg_acr = (ar.first_token.term + ar.first_token.next0_.next0_.term)
            acr_end = ar.first_token.next0_.next0_
            if (acr_end.next0_ is not None and acr_end.next0_.is_char('.')): 
                acr_end = acr_end.next0_
        if (reg_acr is not None and acr_end.next0_ is not None): 
            regs = RegionHelper.get_regions_by_abbr(reg_acr)
            if (regs is not None): 
                try: 
                    ar1 = ProcessorService.get_empty_processor().process(SourceOfAnalysis(txt), None, None)
                    for r in regs: 
                        ok = False
                        t = ar1.first_token
                        first_pass3095 = True
                        while True:
                            if first_pass3095: first_pass3095 = False
                            else: t = t.next0_
                            if (not (t is not None)): break
                            if (t.end_char <= acr_end.end_char): 
                                continue
                            toks = r.term_cities.try_parse_all(t, TerminParseAttr.NO)
                            if (toks is not None and len(toks) == 1): 
                                ok = True
                                break
                        if (not ok): 
                            continue
                        txt = "{0}, {1}".format(str(r.attrs), txt[acr_end.next0_.begin_char:])
                        ar = AnalyzeHelper.__m_proc1.process(SourceOfAnalysis._new113(txt, co, False, ("ADDRESS" if one_addr else None)), None, None)
                        break
                except Exception as ex116: 
                    pass
        if (ar.first_token.kit.corrected_tokens is not None): 
            for kp in ar.first_token.kit.corrected_tokens.items(): 
                if (isinstance(kp[0], TextToken)): 
                    pass
        unknown_names = None
        t = ar.first_token
        first_pass3096 = True
        while True:
            if first_pass3096: first_pass3096 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (isinstance(t, ReferentToken)): 
                r = t.get_referent()
                if (r is None): 
                    continue
                aaa = Utils.asObjectOrNull(r, AddressReferent)
                if (aaa is not None and aaa.zip0_ is not None and self.zip0_ is None): 
                    self.zip0_ = aaa.zip0_
                if (r.type_name == "PHONE" or r.type_name == "URI"): 
                    if (len(res) > 0): 
                        res[len(res) - 1].end_char = t.end_char
                    continue
                addr = TextAddress()
                addr.begin_char = t.begin_char
                addr.end_char = t.end_char
                AnalyzeHelper._create_address_items(addr, r, Utils.asObjectOrNull(t, ReferentToken), 0)
                if (len(addr.items) == 0): 
                    continue
                addr.sort_items()
                add = True
                if (len(res) > 0 and ((addr.items[0].level == AddrLevel.STREET or addr.items[0].level == AddrLevel.TERRITORY))): 
                    a0 = res[len(res) - 1]
                    for ii in range(len(a0.items) - 1, -1, -1):
                        it = a0.items[ii]
                        if (not (isinstance(it.attrs, AreaAttributes))): 
                            continue
                        if (it.level == AddrLevel.CITY or it.level == AddrLevel.LOCALITY or it.level == AddrLevel.REGIONCITY): 
                            add = False
                            if ((ii + 1) < len(a0.items)): 
                                del a0.items[ii + 1:ii + 1+len(a0.items) - ii - 1]
                            a0.end_char = addr.end_char
                            a0.items.extend(addr.items)
                            addr = a0
                        break
                if (add): 
                    res.append(addr)
                r.tag = (addr)
                if (one_addr and t.next0_ is not None and t.next0_.is_char('(')): 
                    br = BracketHelper.try_parse(t.next0_, BracketParseAttr.NO, 100)
                    if (br is not None and (br.length_char < 20)): 
                        t = br.end_token
                        addr.end_char = t.end_char
                tt = t.next0_
                if (tt is not None and tt.is_comma): 
                    tt = tt.next0_
                if (one_addr and (isinstance(tt, TextToken))): 
                    ait = AddressItemToken.try_parse_pure_item(tt, None, None)
                    if ((ait is not None and ait.typ == AddressItemType.NUMBER and not Utils.isNullOrEmpty(ait.value)) and str.isalpha(ait.value[0])): 
                        ait.building_type = AddressBuildingType.LITER
                    if ((ait is None and tt.length_char == 1 and tt.chars.is_all_upper) and tt.chars.is_letter): 
                        ait = AddressItemToken._new117(AddressItemType.BUILDING, tt, tt, AddressBuildingType.LITER, tt.term)
                    if (ait is not None and ait.building_type == AddressBuildingType.LITER): 
                        self.litera_variant = ait
                        t = ait.end_token
                        addr.end_char = t.end_char
            elif ((isinstance(t, TextToken)) and t.length_char > 3 and one_addr): 
                mc = t.get_morph_class_in_dictionary()
                if ((((((((mc.is_verb or t.is_value("ТОВАРИЩЕСТВО", None) or t.is_value("МУНИЦИПАЛЬНЫЙ", None)) or t.is_value("ГОРОДСКОЙ", None) or t.is_value("СТРАНА", None)) or t.is_value("ПОЧТОВЫЙ", None) or t.is_value("ОКАТО", None)) or t.is_value("СУБЪЕКТ", None) or t.is_value("СТОЛИЦА", None)) or t.is_value("КОРДОН", None) or t.is_value("КОРПУС", None)) or t.is_value("НОМЕР", None) or t.is_value("УЧЕТНЫЙ", None)) or t.is_value("ЗАПИСЬ", None) or t.is_value("ГОСУДАРСТВЕННЫЙ", None)) or t.is_value("РЕЕСТР", None) or t.is_value("ЛЕСНОЙ", None)): 
                    pass
                elif (t.is_value("ИНДЕКС", None)): 
                    if (len(res) > 0): 
                        if ((isinstance(t.next0_, NumberToken)) and t.next0_.length_char > 4): 
                            t = t.next0_
                        res[len(res) - 1].end_char = t.end_char
                else: 
                    if (NumberHelper.try_parse_roman(t) is not None): 
                        continue
                    uuu = t.get_source_text()
                    if (Utils.startsWithString(uuu, "РОС", True) or Utils.startsWithString(uuu, "ФЕДЕР", True)): 
                        pass
                    else: 
                        if (unknown_names is None): 
                            unknown_names = list()
                        unknown_names.append(uuu)
        if (unknown_names is None and len(res) > 0): 
            res[0].begin_char = 0
        i = 0
        first_pass3097 = True
        while True:
            if first_pass3097: first_pass3097 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if ((res[i].end_char + 30) > res[i + 1].begin_char): 
                if (len(res[i].items) == 1 and res[i].items[0].level == AddrLevel.COUNTRY and str(res[i].items[0]) == "Россия"): 
                    res[i + 1].begin_char = res[i].begin_char
                    del res[i]
                    i -= 1
                    continue
                if (str(res[i].last_item) == str(res[i + 1].items[0])): 
                    res[i].end_char = res[i + 1].end_char
                    res[i].items.remove(res[i].last_item)
                    res[i].items.extend(res[i + 1].items)
                    del res[i + 1]
                    i -= 1
                    continue
                str0 = str(res[i])
                str1 = str(res[i + 1])
                if (len(res[i].items) == len(res[i + 1].items) and str0 == str1 and res[i].last_item.tag == res[i + 1].last_item.tag): 
                    if ((res[i + 1].end_char - res[i + 1].begin_char) > 10): 
                        res[i].end_char = res[i + 1].end_char
                    del res[i + 1]
                    i -= 1
                    continue
                if (str1.startswith(str0)): 
                    if ((res[i + 1].end_char - res[i + 1].begin_char) < 10): 
                        del res[i + 1]
                        i -= 1
                        continue
                    res[i + 1].begin_char = res[i].begin_char
                    del res[i]
                    i -= 1
                    continue
                if (str0.startswith(str1)): 
                    if (res[i + 1].end_char > res[i].end_char): 
                        res[i].end_char = res[i + 1].end_char
                    del res[i + 1]
                    i -= 1
                    continue
                ok = res[i].last_item.can_be_parent_for(res[i + 1].items[0], None)
                if (len(res[i].items) == 1 and res[i].items[0].level == AddrLevel.CITY and res[i + 1].items[0].level == AddrLevel.CITY): 
                    ok = True
                    res[i].items[0].level = AddrLevel.REGIONCITY
                if (ok): 
                    res[i].end_char = res[i + 1].end_char
                    res[i].items.extend(res[i + 1].items)
                    del res[i + 1]
                    i -= 1
        k = 0
        first_pass3098 = True
        while True:
            if first_pass3098: first_pass3098 = False
            else: k += 1
            if (not (k < len(res))): break
            r = res[k]
            if (one_addr): 
                r.text = txt
            ad = Utils.asObjectOrNull(r.last_item.tag, AddressReferent)
            if (ad is not None): 
                del r.items[len(r.items) - 1]
            r2 = r.clone()
            r3 = r.clone()
            has_sec_var = False
            self.create_alts_regime = False
            wraphas_sec_var119 = RefOutArgWrapper(False)
            ad2 = self._process_address(r, wraphas_sec_var119)
            has_sec_var = wraphas_sec_var119.value
            self._process_rest(r, Utils.ifNotNull(ad, ad2), one_addr, ar)
            CoefHelper.calc_coef(self, r, one_addr, txt, unknown_names)
            if (r.coef == 100 and not has_sec_var): 
                continue
            if (has_sec_var): 
                self.create_alts_regime = True
                wraphas_sec_var118 = RefOutArgWrapper(False)
                ad2 = self._process_address(r2, wraphas_sec_var118)
                has_sec_var = wraphas_sec_var118.value
                self._process_rest(r2, Utils.ifNotNull(ad, ad2), one_addr, ar)
                CoefHelper.calc_coef(self, r2, one_addr, txt, unknown_names)
                if (r2.coef > r.coef): 
                    res[k] = r2
                    r = r2
                elif ((r2.coef == r.coef and r2.error_message is None and r.error_message is not None) and r2.last_item_with_gar is not None and r.last_item_with_gar is not None): 
                    if (AddressHelper.compare_levels(r2.last_item_with_gar.level, r.last_item_with_gar.level) > 0): 
                        res[k] = r2
                        r = r2
            if (r.coef >= 95): 
                continue
            if (not one_addr): 
                continue
            if ((len(r3.items) < 2) or len(res) > 1): 
                continue
            reg = RegionHelper.is_big_citya(r3.items[0])
            if (reg is not None and reg.capital is not None and r3.items[0].attrs.contains_name(reg.capital)): 
                pass
            elif (len(r3.items) > 1 and r3.items[0].level == AddrLevel.DISTRICT and r3.items[1].level == AddrLevel.CITY): 
                reg = RegionHelper.is_big_citya(r3.items[1])
                if (reg is not None and reg.capital is not None and r3.items[1].attrs.contains_name(reg.capital)): 
                    it = r3.items[0]
                    del r3.items[0]
                    r3.items.insert(1, it)
                else: 
                    continue
            else: 
                continue
            txt1 = reg.replace_capital_by_region(txt)
            if (txt1 is not None and txt != txt1): 
                res2 = self.analyze(txt1, None, True, self.m_params)
                if (res2 is not None and len(res2) == 1 and res2[0].coef > r.coef): 
                    return res2
        if (len(res) > 1 and one_addr): 
            if (res[0].end_char > res[0].begin_char): 
                del res[1:1+len(res) - 1]
        if (len(res) > 1 and one_addr): 
            res[0].coef = math.floor(res[0].coef / len(res))
            msg = "В строке выделилось {0} адрес{1}, второй: {2}. ".format(len(res), ("а" if len(res) < 5 else "ов"), str(res[1]))
            if (res[0].error_message is None): 
                res[0].error_message = msg
            else: 
                res[0].error_message = "{0} {1}".format(res[0].error_message, msg)
        for r in res: 
            CorrectionHelper.correct_country(r)
        return res
    
    def create_text_address_by_referent(self, r : 'Referent') -> 'TextAddress':
        addr = TextAddress()
        AnalyzeHelper._create_address_items(addr, r, None, 0)
        if (len(addr.items) == 0): 
            return None
        addr.sort_items()
        r.tag = (addr)
        ad = Utils.asObjectOrNull(addr.last_item.tag, AddressReferent)
        if (ad is not None): 
            del addr.items[len(addr.items) - 1]
        r2 = r.clone()
        r3 = r.clone()
        has_sec_var = False
        self.create_alts_regime = False
        wraphas_sec_var120 = RefOutArgWrapper(False)
        ad2 = self._process_address(addr, wraphas_sec_var120)
        has_sec_var = wraphas_sec_var120.value
        self._process_rest(addr, Utils.ifNotNull(ad, ad2), True, None)
        CoefHelper.calc_coef(self, addr, True, None, None)
        CorrectionHelper.correct_country(addr)
        return addr
    
    @staticmethod
    def _create_address_items(addr : 'TextAddress', r : 'Referent', rt : 'ReferentToken', lev : int) -> None:
        if (lev > 10 or r is None): 
            return
        own = None
        own2 = None
        sown = None
        sown2 = None
        sown22 = None
        detail_typ = DetailType.UNDEFINED
        detail_param = None
        detail_org = None
        if (isinstance(r, GeoReferent)): 
            geo = Utils.asObjectOrNull(r, GeoReferent)
            if (geo.is_state): 
                if (geo.is_state and geo.alpha2 is not None): 
                    if (geo.alpha2 == "RU" and lev > 0): 
                        return
                    cou = CorrectionHelper.create_country(geo.alpha2, geo)
                    if (cou is not None): 
                        if (len(addr.items) > 0 and addr.items[0].level == AddrLevel.COUNTRY): 
                            pass
                        else: 
                            addr.items.append(cou)
                        return
            aa = AreaAttributes()
            res = AddrObject(aa)
            if ((isinstance(r, GeoReferent)) and Utils.compareStrings(str(r), "ДНР", True) == 0): 
                r = (GeoReferent())
                r.add_slot(GeoReferent.ATTR_TYPE, "республика", False, 0)
                r.add_slot(GeoReferent.ATTR_NAME, "ДОНЕЦКАЯ", False, 0)
                res.level = AddrLevel.REGIONAREA
            elif ((isinstance(r, GeoReferent)) and Utils.compareStrings(str(r), "ЛНР", True) == 0): 
                r = (GeoReferent())
                r.add_slot(GeoReferent.ATTR_TYPE, "республика", False, 0)
                r.add_slot(GeoReferent.ATTR_NAME, "ЛУГАНСКАЯ", False, 0)
                res.level = AddrLevel.REGIONAREA
            if (str(geo) == "область Читинская"): 
                geo = GeoReferent()
                geo.add_slot(GeoReferent.ATTR_NAME, "ЗАБАЙКАЛЬСКИЙ", False, 0)
                geo.add_slot(GeoReferent.ATTR_TYPE, "край", False, 0)
                r = (geo)
            typs = r.get_string_values(GeoReferent.ATTR_TYPE)
            if ((geo.alpha2 == "UA" or geo.alpha2 == "BY" or geo.alpha2 == "KZ") or geo.alpha2 == "KG"): 
                aa.types.append("республика")
            elif (len(typs) > 0): 
                aa.types.extend(typs)
            AnalyzeHelper.__set_name(aa, r, GeoReferent.ATTR_NAME)
            AnalyzeHelper.__set_misc(aa, r, GeoReferent.ATTR_MISC)
            aa.number = r.get_string_value("NUMBER")
            na = NameAnalyzer()
            na.init_by_referent(r, False)
            res.tag = (na)
            addr.items.append(res)
            own = geo.higher
            if (res.level == AddrLevel.UNDEFINED): 
                res.level = na.level
            else: 
                na.level = res.level
            r.tag = (res)
            if (r.ontology_items is not None and len(r.ontology_items) > 0): 
                if (isinstance(r.ontology_items[0].ext_id, str)): 
                    res.ext_id = (Utils.asObjectOrNull(r.ontology_items[0].ext_id, str))
        elif (isinstance(r, StreetReferent)): 
            sown = r.higher
            uni = NameAnalyzer.merge_objects(sown, r)
            if (uni is not None): 
                AnalyzeHelper._create_address_items(addr, uni, rt, lev + 1)
                r.tag = (addr)
                sown.tag = (addr)
                return
            aa = AreaAttributes()
            res = AddrObject(aa)
            aa.types.extend(r.typs)
            if (len(aa.types) > 1 and "улица" in aa.types): 
                aa.types.remove("улица")
                aa.types.append("улица")
            AnalyzeHelper.__set_name(aa, r, StreetReferent.ATTR_NAME)
            AnalyzeHelper.__set_misc(aa, r, StreetReferent.ATTR_MISC)
            ki = r.kind
            if (ki == StreetKind.ROAD): 
                aa.miscs.append("дорога")
            aa.number = r.numbers
            if ((aa.number is not None and aa.number.endswith("км") and len(aa.names) == 0) and ki != StreetKind.ROAD): 
                aa.types.append("километр")
                aa.number = aa.number[0:0+len(aa.number) - 2]
            na = NameAnalyzer()
            na.init_by_referent(r, False)
            res.tag = (na)
            addr.items.append(res)
            own = (Utils.asObjectOrNull(r.get_slot_value(StreetReferent.ATTR_GEO), GeoReferent))
            res.level = na.level
            if (ki == StreetKind.ROAD and res.level == AddrLevel.STREET): 
                res.level = AddrLevel.TERRITORY
            r.tag = (res)
        elif (isinstance(r, AddressReferent)): 
            ar = Utils.asObjectOrNull(r, AddressReferent)
            sown = (Utils.asObjectOrNull(ar.get_slot_value(AddressReferent.ATTR_STREET), StreetReferent))
            streets = ar.streets
            if (len(streets) > 1): 
                if (ar.detail == AddressDetailType.CROSS): 
                    sown2 = (Utils.asObjectOrNull(streets[1], StreetReferent))
                elif ("очередь" in sown.typs or "очередь" in ar.streets[1].typs): 
                    sown2 = (Utils.asObjectOrNull(streets[1], StreetReferent))
                else: 
                    sown2 = (Utils.asObjectOrNull(streets[1], StreetReferent))
            if (len(streets) > 2): 
                sown22 = (Utils.asObjectOrNull(streets[2], StreetReferent))
            geos = ar.geos
            if (len(geos) > 0): 
                own = geos[0]
                if (len(geos) > 1): 
                    own2 = geos[1]
            if (ar.detail != AddressDetailType.UNDEFINED and ar.detail != AddressDetailType.CROSS): 
                wrapdetail_param121 = RefOutArgWrapper(None)
                detail_typ = HouseRoomHelper.create_dir_details(ar, wrapdetail_param121)
                detail_param = wrapdetail_param121.value
                own3 = Utils.asObjectOrNull(ar.get_slot_value(AddressReferent.ATTR_DETAILREF), GeoReferent)
                if (own3 is not None): 
                    if (own3.higher is None): 
                        own3.higher = own
                    if (own is None): 
                        own = own3
                    elif (own3.higher == own): 
                        own = own3
                    elif (own3.higher is not None and ((own3.higher.higher is None or own3.higher.higher == own)) and GeoOwnerHelper.can_be_higher(own, own3.higher, None, None)): 
                        own3.higher.higher = own
                        if (sown is not None and sown.parent_referent == own): 
                            sown.add_slot(StreetReferent.ATTR_GEO, own3, True, 0)
                            own = (None)
                        else: 
                            own = own3
            else: 
                org0_ = Utils.asObjectOrNull(ar.get_slot_value(AddressReferent.ATTR_DETAILREF), OrganizationReferent)
                if (org0_ is not None): 
                    aa = AreaAttributes()
                    detail_org = AddrObject(aa)
                    detail_org.level = AddrLevel.TERRITORY
                    aa.types.append("территория")
                    AnalyzeHelper.__set_name(aa, org0_, OrganizationReferent.ATTR_NAME)
                    AnalyzeHelper.__set_misc(aa, org0_, OrganizationReferent.ATTR_TYPE)
                    aa.number = org0_.number
                    na = NameAnalyzer()
                    na.init_by_referent(org0_, False)
                    detail_org.tag = (na)
                    addr.items.append(detail_org)
            if (ar.block is not None): 
                sr = StreetReferent()
                sr.add_slot(StreetReferent.ATTR_TYPE, "блок", False, 0)
                sr.add_slot(StreetReferent.ATTR_NUMBER, ar.block, False, 0)
                aa = AreaAttributes()
                aa.types.append("блок")
                aa.number = ar.block
                ao = AddrObject._new122(aa, AddrLevel.STREET)
                na = NameAnalyzer()
                na.init_by_referent(sr, False)
                ao.tag = (na)
                addr.items.append(ao)
            ha = HouseAttributes()
            res = AddrObject(ha)
            res.level = AddrLevel.BUILDING
            res.tag = (ar)
            r.tag = (res)
            addr.items.append(res)
        if (sown is not None): 
            addr1 = TextAddress()
            AnalyzeHelper._create_address_items(addr1, sown, None, lev + 1)
            if (len(addr1.items) > 0): 
                if (addr1.last_item.can_be_parent_for(addr.items[0], None)): 
                    addr.items[0:0] = addr1.items
                    if (sown2 is not None): 
                        addr2 = TextAddress()
                        AnalyzeHelper._create_address_items(addr2, sown2, None, lev + 1)
                        if (addr2.last_item is not None and addr2.last_item.can_be_equals_level(addr1.last_item)): 
                            a1 = Utils.asObjectOrNull(addr1.last_item.attrs, AreaAttributes)
                            a2 = Utils.asObjectOrNull(addr2.last_item.attrs, AreaAttributes)
                            if ("очередь" in a1.types and a1.number is not None and len(a1.names) == 0): 
                                addr.params[ParamType.ORDER] = a1.number
                                addr.items[len(addr1.items) - 1] = addr2.last_item
                            elif ("очередь" in a2.types and a2.number is not None and len(a2.names) == 0): 
                                addr.params[ParamType.ORDER] = a1.number
                            elif (addr2.last_item.level == AddrLevel.TERRITORY): 
                                addr.items.insert(len(addr1.items), addr2.last_item)
                                if (sown22 is not None): 
                                    addr3 = TextAddress()
                                    AnalyzeHelper._create_address_items(addr3, sown22, None, lev + 1)
                                    if (addr3.last_item is not None and addr3.last_item.level == addr1.last_item.level): 
                                        addr.items.insert(len(addr1.items) + 1, addr3.last_item)
                            else: 
                                addr1.last_item.cross_object = addr2.last_item
                elif (addr1.last_item.level == AddrLevel.STREET and ((addr.items[0].level == AddrLevel.TERRITORY or addr.items[0].level == AddrLevel.STREET))): 
                    addr.items[0:0] = addr1.items
        if (own is not None): 
            addr1 = TextAddress()
            AnalyzeHelper._create_address_items(addr1, own, None, lev + 1)
            if (len(addr1.items) > 0): 
                if (detail_typ != DetailType.UNDEFINED and sown is not None): 
                    addr1.last_item.detail_typ = detail_typ
                    addr1.last_item.detail_param = detail_param
                ins = False
                if (AddressHelper.compare_levels(addr1.last_item.level, addr.items[0].level) < 0): 
                    ins = True
                elif (addr1.last_item.can_be_parent_for(addr.items[0], None)): 
                    ins = True
                elif (addr1.last_item.level == AddrLevel.CITY and ((addr.items[0].level == AddrLevel.DISTRICT or addr.items[0].level == AddrLevel.SETTLEMENT))): 
                    ins = True
                elif (addr1.last_item.level == AddrLevel.DISTRICT and addr.items[0].level == AddrLevel.LOCALITY): 
                    ins = True
                if (ins): 
                    if (str(addr).startswith(str(addr1))): 
                        pass
                    else: 
                        addr.items[0:0] = addr1.items
                elif (addr1.last_item.level == AddrLevel.SETTLEMENT and addr.items[0].level == AddrLevel.DISTRICT): 
                    if (str(addr).startswith(str(addr1))): 
                        pass
                    else: 
                        it0 = addr.items[0]
                        addr.items.clear()
                        addr.items.extend(addr1.items)
                        addr.items.insert(len(addr.items) - 1, it0)
                elif (detail_typ != DetailType.UNDEFINED and addr1.last_item.detail_typ != DetailType.UNDEFINED and (len(addr1.items) < len(addr.items))): 
                    i = 0
                    i = 0
                    while i < (len(addr1.items) - 1): 
                        if (str(addr1.items[i]) != str(addr.items[i])): 
                            break
                        i += 1
                    if (i == (len(addr1.items) - 1) and (AddressHelper.compare_levels(addr1.items[i].level, addr.items[i].level) < 0)): 
                        addr.items.insert(i, addr1.items[i])
        if (addr.last_item is not None): 
            aa = Utils.asObjectOrNull(addr.last_item.attrs, AreaAttributes)
            na = Utils.asObjectOrNull(addr.last_item.tag, NameAnalyzer)
            if ((aa is not None and len(aa.names) > 0 and aa.number is not None) and aa.number.endswith("км") and na.sec is not None): 
                aa1 = AreaAttributes()
                aa1.number = aa.number[0:0+len(aa.number) - 2]
                aa1.types.append("километр")
                km = AddrObject(aa1)
                km.level = AddrLevel.STREET
                addr.last_item.level = AddrLevel.TERRITORY
                km.tag = (na.sec)
                na.sec = (None)
                aa.number = (None)
                addr.items.append(km)
    
    @staticmethod
    def __set_name(a : 'AreaAttributes', r : 'Referent', typ : str) -> None:
        if (r is None): 
            return
        names = r.get_string_values(typ)
        if (names is None or len(names) == 0): 
            return
        long_name = None
        i = 0
        first_pass3099 = True
        while True:
            if first_pass3099: first_pass3099 = False
            else: i += 1
            if (not (i < len(names))): break
            nam = names[i]
            ii = nam.find('-')
            if (ii > 0 and ((ii + 1) < len(nam)) and str.isdigit(nam[ii + 1])): 
                a.number = nam[ii + 1:]
                r.add_slot("NUMBER", a.number, False, 0)
                ss = r.find_slot("NAME", nam, True)
                if (ss is not None): 
                    r.slots.remove(ss)
                nam = nam[0:0+ii]
                r.add_slot("NAME", nam, False, 0)
            if (nam == "МИКРОРАЙОН"): 
                if (not nam.lower() in a.types): 
                    a.types.append(nam.lower())
                del names[i]
                i -= 1
                continue
            names[i] = MiscHelper.convert_first_char_upper_and_other_lower(nam)
            if (long_name is None): 
                long_name = names[i]
            elif (len(long_name) > len(names[i])): 
                long_name = names[i]
        if (len(names) > 1 and names[0] != long_name): 
            names.remove(long_name)
            names.insert(0, long_name)
        a.names = names
    
    @staticmethod
    def __set_misc(a : 'AreaAttributes', r : 'Referent', nam : str) -> None:
        a.miscs = r.get_string_values(nam)
        if (len(a.miscs) > 0): 
            has_up = False
            for m in a.miscs: 
                if (str.isupper(m[0])): 
                    has_up = True
            if (has_up): 
                for i in range(len(a.miscs) - 1, -1, -1):
                    if (not str.isupper(a.miscs[i][0])): 
                        del a.miscs[i]