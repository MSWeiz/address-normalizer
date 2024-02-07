# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import xml.etree
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.AddrLevel import AddrLevel
from pullenti.address.internal.RegionInfo import RegionInfo
from pullenti.ner.core.Termin import Termin
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.ner.core.TerminCollection import TerminCollection

class RegionHelper:
    
    REGIONS = None
    
    @staticmethod
    def load_from_file(fname : str) -> None:
        if (not pathlib.Path(fname).is_file()): 
            return
        RegionHelper.REGIONS.clear()
        xml0_ = None # new XmlDocument
        xml0_ = xml.etree.ElementTree.parse(fname)
        for x in xml0_.getroot(): 
            if (Utils.getXmlLocalName(x) == "reg"): 
                r = RegionInfo()
                r.deserialize(x)
                RegionHelper.REGIONS.append(r)
        RegionHelper.__init()
    
    @staticmethod
    def __init() -> None:
        RegionHelper.__m_city_regs.clear()
        RegionHelper.__m_adj_regs.clear()
        for r in RegionHelper.REGIONS: 
            r.term_cities = TerminCollection()
            for c in r.cities: 
                city = c.upper()
                if (not city in RegionHelper.__m_city_regs): 
                    RegionHelper.__m_city_regs[city] = r
                r.term_cities.add(Termin(city))
            for d in r.districts: 
                nam = d.upper()
                r.term_cities.add(Termin._new123(nam, d))
            for s in r.names.ref.slots: 
                if (s.type_name == "NAME"): 
                    if (not Utils.asObjectOrNull(s.value, str) in RegionHelper.__m_adj_regs): 
                        RegionHelper.__m_adj_regs[Utils.asObjectOrNull(s.value, str)] = r
    
    __m_city_regs = None
    
    __m_adj_regs = None
    
    @staticmethod
    def is_big_city(nam : str) -> 'RegionInfo':
        if (nam is None): 
            return None
        res = None
        wrapres184 = RefOutArgWrapper(None)
        inoutres185 = Utils.tryGetValue(RegionHelper.__m_city_regs, nam.upper(), wrapres184)
        res = wrapres184.value
        if (inoutres185): 
            return res
        return None
    
    @staticmethod
    def is_big_citya(ao : 'AddrObject') -> 'RegionInfo':
        if (ao.level != AddrLevel.CITY and ao.level != AddrLevel.REGIONCITY): 
            return None
        aa = Utils.asObjectOrNull(ao.attrs, AreaAttributes)
        if (aa is None or len(aa.names) == 0): 
            return None
        if (aa.number is not None): 
            return None
        for n in aa.names: 
            r = RegionHelper.is_big_city(n)
            if (r is not None): 
                return r
        return None
    
    @staticmethod
    def get_regions_by_abbr(abbr : str) -> typing.List['RegionInfo']:
        res = None
        for r in RegionHelper.REGIONS: 
            if (abbr in r.acronims): 
                if (res is None): 
                    res = list()
                res.append(r)
        return res
    
    @staticmethod
    def find_region_by_adj(adj : str) -> 'RegionInfo':
        adj = adj.upper()
        ri = None
        wrapri186 = RefOutArgWrapper(None)
        inoutres187 = Utils.tryGetValue(RegionHelper.__m_adj_regs, adj, wrapri186)
        ri = wrapri186.value
        if (not inoutres187): 
            return None
        return ri
    
    # static constructor for class RegionHelper
    @staticmethod
    def _static_ctor():
        RegionHelper.REGIONS = list()
        RegionHelper.__m_city_regs = dict()
        RegionHelper.__m_adj_regs = dict()

RegionHelper._static_ctor()