# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.address.AddrLevel import AddrLevel

class AreaAttributes(BaseAttributes):
    """ Атрибуты города, региона, района, квартала, улиц и т.п. """
    
    def __init__(self) -> None:
        super().__init__()
        self.types = list()
        self.names = list()
        self.number = None;
        self.miscs = list()
    
    def __str__(self) -> str:
        return self.to_string_ex(AddrLevel.UNDEFINED, False)
    
    def to_string_ex(self, lev : 'AddrLevel', is_gar : bool) -> str:
        res = (self.types[0] if len(self.types) > 0 else "")
        out_num = False
        if ((lev == AddrLevel.STREET and len(self.types) > 1 and self.types[1] != "улица") and res == "улица"): 
            res = self.types[1]
        br = False
        if (res == "территория" or lev == AddrLevel.TERRITORY): 
            if (len(self.miscs) > 0 and not is_gar and self.miscs[0] != "дорога"): 
                if (len(self.names) > 0 and self.miscs[0] in self.names[0]): 
                    pass
                elif (len(self.names) > 0 or self.number is not None): 
                    res = "{0} {1}".format(res, self.miscs[0])
                    if (len(self.names) > 0): 
                        br = True
        if (self.number is not None and lev == AddrLevel.STREET and not self.number.endswith("км")): 
            res = "{0} {1}".format(res, self.number)
            out_num = True
        if (len(self.names) > 0): 
            if (res == "километр" and not str.isdigit(self.names[0][0])): 
                res = "{0} километр".format(self.names[0])
            elif (br): 
                if (self.number is not None and not out_num): 
                    res = "{0} \"{1}-{2}\"".format(res, self.names[0], self.number)
                    out_num = True
                else: 
                    res = "{0} \"{1}\"".format(res, self.names[0])
            else: 
                res = "{0} {1}".format(res, self.names[0])
                if (lev == AddrLevel.LOCALITY or lev == AddrLevel.SETTLEMENT): 
                    if (len(self.miscs) > 0 and not self.miscs[0] in self.types): 
                        res = "{0} {1}".format(res, MiscHelper.convert_first_char_upper_and_other_lower(self.miscs[0]))
        elif (((lev == AddrLevel.STREET or lev == AddrLevel.TERRITORY)) and len(self.types) > 1): 
            if (self.types[1] != "улица"): 
                res = "{0} {1}".format(res, MiscHelper.convert_first_char_upper_and_other_lower(self.types[1]))
            else: 
                res = self.types[1]
                if (self.number is not None and lev == AddrLevel.STREET): 
                    res = "{0} {1}".format(res, self.number)
                    out_num = True
                res = "{0} {1}".format(res, MiscHelper.convert_first_char_upper_and_other_lower(self.types[0]))
        if (self.number is not None and not out_num): 
            if (res == "километр"): 
                res = "{0} километр".format(self.number)
            else: 
                nnn = 0
                if (lev == AddrLevel.TERRITORY): 
                    if (len(self.number) > 3): 
                        res = "{0} №{1}".format(res, self.number)
                    else: 
                        res = "{0}-{1}".format(res, self.number)
                else: 
                    wrapnnn218 = RefOutArgWrapper(0)
                    inoutres219 = Utils.tryParseInt(self.number, wrapnnn218)
                    nnn = wrapnnn218.value
                    if (inoutres219): 
                        res = "{0}-{1}".format(res, self.number)
                    else: 
                        res = "{0} {1}".format(res, self.number)
        if (len(self.names) == 0 and self.number is None and len(self.miscs) > 0): 
            res = "{0} {1}".format(res, MiscHelper.convert_first_char_upper_and_other_lower(self.miscs[0]))
        return res.strip()
    
    def out_info(self, res : io.StringIO) -> None:
        if (len(self.types) > 0): 
            print("Тип: {0}".format(self.types[0]), end="", file=res, flush=True)
            i = 1
            while i < len(self.types): 
                print(" / {0}".format(self.types[i]), end="", file=res, flush=True)
                i += 1
            print("\r\n", end="", file=res)
        if (len(self.names) > 0): 
            print("Наименование: {0}".format(self.names[0]), end="", file=res, flush=True)
            i = 1
            while i < len(self.names): 
                print(" / {0}".format(self.names[i]), end="", file=res, flush=True)
                i += 1
            print("\r\n", end="", file=res)
        if (self.number is not None): 
            print("Номер: {0}\r\n".format(self.number), end="", file=res, flush=True)
        if (len(self.miscs) > 0): 
            print("Дополнительно: {0}".format(self.miscs[0]), end="", file=res, flush=True)
            i = 1
            while i < len(self.miscs): 
                print(" / {0}".format(self.miscs[i]), end="", file=res, flush=True)
                i += 1
            print("\r\n", end="", file=res)
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("area")
        for ty in self.types: 
            xml0_.write_element_string("type", ty)
        for nam in self.names: 
            xml0_.write_element_string("name", nam)
        for misc in self.miscs: 
            xml0_.write_element_string("misc", misc)
        if (self.number is not None): 
            xml0_.write_element_string("num", self.number)
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "type"): 
                self.types.append(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "name"): 
                self.names.append(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "misc"): 
                self.miscs.append(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "num"): 
                self.number = Utils.getXmlInnerText(x)
    
    def has_equal_type(self, typs : typing.List[str]) -> bool:
        if (typs is None): 
            return False
        for ty in self.types: 
            if (ty in typs): 
                return True
            if ("поселок" in ty): 
                for tyy in typs: 
                    if ("поселок" in tyy): 
                        return True
        return False
    
    def find_misc(self, miscs_ : typing.List[str]) -> str:
        if (miscs_ is not None): 
            for m in miscs_: 
                if (m in self.miscs): 
                    return m
        return None
    
    def contains_name(self, sub_name : str) -> bool:
        for n in self.names: 
            if (sub_name in n): 
                return True
            elif (Utils.compareStrings(n, sub_name, True) == 0): 
                return True
        return False
    
    def clone(self) -> 'BaseAttributes':
        res = AreaAttributes()
        res.types.extend(self.types)
        res.names.extend(self.names)
        res.miscs.extend(self.miscs)
        res.number = self.number
        return res