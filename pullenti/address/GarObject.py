﻿# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.address.RoomAttributes import RoomAttributes
from pullenti.address.internal.gar.HouseObject import HouseObject
from pullenti.address.internal.gar.RoomObject import RoomObject
from pullenti.address.GarStatus import GarStatus
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.address.GarLevel import GarLevel
from pullenti.address.AddressService import AddressService
from pullenti.address.GarParam import GarParam
from pullenti.address.internal.NameAnalyzer import NameAnalyzer
from pullenti.address.AddressHelper import AddressHelper

class GarObject(object):
    """ Адресный объект ГАР
    
    """
    
    def __init__(self, attrs_ : 'BaseAttributes') -> None:
        self.attrs = None;
        self.level = GarLevel.UNDEFINED
        self.expired = False
        self.guid = None;
        self.region_number = 0
        self.status = GarStatus.OK
        self.id0_ = None;
        self.parent_ids = list()
        self.actual_object_id = None;
        self.source_text = None;
        self.tag = None;
        self._internal_tag = 0
        self.children_count = 0
        self.__m_params = None
        self.attrs = attrs_
    
    def __str__(self) -> str:
        if (self.attrs is None): 
            return "?"
        aa = Utils.asObjectOrNull(self.attrs, AreaAttributes)
        if (aa is not None and len(aa.types) > 0 and len(aa.names) > 0): 
            return "{0} {1}".format(aa.types[0], aa.names[0])
        if (self.source_text is not None): 
            return self.source_text
        return str(self.attrs)
    
    def get_param_value(self, ty : 'GarParam') -> str:
        """ Получить значение параметра (код КЛАДР, почтовый индекс и т.п.)
        
        Args:
            ty(GarParam): тип параметра
        
        Returns:
            str: значение или null
        """
        if (ty == GarParam.GUID): 
            return self.guid
        self.__load_params()
        res = None
        wrapres220 = RefOutArgWrapper(None)
        inoutres221 = Utils.tryGetValue(self.__m_params, ty, wrapres220)
        res = wrapres220.value
        if (self.__m_params is not None and inoutres221): 
            return res
        return None
    
    def get_params(self) -> typing.List[tuple]:
        """ Получить все параметры
        
        """
        self.__load_params()
        return self.__m_params
    
    def out_info(self, res : io.StringIO, out_name_analyze_info : bool=True) -> None:
        """ Вывести подробную текстовую информацию об объекте (для отладки)
        
        Args:
            res(io.StringIO): куда выводить
        """
        from pullenti.address.internal.NumberAnalyzer import NumberAnalyzer
        from pullenti.address.internal.GarHelper import GarHelper
        if (self.attrs is not None): 
            self.attrs.out_info(res)
        print("\r\nУровень: {0} - {1}\r\n".format(self.level, AddressHelper.get_gar_level_string(self.level)), end="", file=res, flush=True)
        if (self.expired): 
            print("Актуальность: НЕТ\r\n".format(), end="", file=res, flush=True)
        if (self.__m_params is None): 
            self.__load_params()
        if (self.__m_params is not None): 
            for p in self.__m_params.items(): 
                print("{0}: {1}\r\n".format(Utils.enumToString(p[0]), p[1]), end="", file=res, flush=True)
        print("\r\nПолный путь: {0}\r\n".format(self.get_full_path(None, False, None)), end="", file=res, flush=True)
        aa = Utils.asObjectOrNull(self.attrs, AreaAttributes)
        if (out_name_analyze_info and aa is not None and len(aa.types) > 0): 
            print("\r\nАнализ объекта: ", end="", file=res)
            na = NameAnalyzer()
            na.process_ex(self)
            na.out_info(res)
        elif (out_name_analyze_info and (isinstance(self.attrs, HouseAttributes))): 
            ho = GarHelper.GAR_INDEX.get_house(int(self.id0_[1:]))
            if (ho is not None): 
                print("\r\nИсходная строка: {0}".format(ho.source_text), end="", file=res, flush=True)
            print("\r\nАнализ объекта: ", end="", file=res)
            print(("ОШИБКА" if self.status != GarStatus.OK else "ОК"), end="", file=res)
            ho2 = HouseObject._new181(("" if ho is None else ho.source_text))
            NumberAnalyzer.set_gar_loading_house_number_attrs(ho2, self.level == GarLevel.PLOT)
            if (self.status == GarStatus.ERROR or ho2.to_string_ex() != ho.to_string_ex()): 
                if (ho2.status == GarStatus.OK): 
                    print(" (новый вариант: {0})".format(ho2.to_string_ex()), end="", file=res, flush=True)
        elif (out_name_analyze_info and (isinstance(self.attrs, RoomAttributes))): 
            try: 
                ho = GarHelper.GAR_INDEX.get_room(int(self.id0_[1:]))
                print("\r\nИсходная строка: {0}".format(ho.source_text), end="", file=res, flush=True)
                print("\r\nАнализ объекта: ", end="", file=res)
                print(("ОШИБКА" if self.status != GarStatus.OK else "ОК"), end="", file=res)
                ho2 = RoomObject._new182(("" if ho is None else ho.source_text))
                NumberAnalyzer.set_gar_loading_room_number_attrs(ho2)
                if (self.status == GarStatus.ERROR or ho.to_string_ex() != ho2.to_string_ex()): 
                    if (ho2.status == GarStatus.OK): 
                        print(" (новый вариант: {0})".format(ho2.to_string_ex()), end="", file=res, flush=True)
            except Exception as ex224: 
                pass
        if (self.actual_object_id is not None and out_name_analyze_info): 
            act_obj = AddressService.get_object(self.actual_object_id)
            if (act_obj is not None): 
                print("\r\n\r\n-------------------------------------------------\r\nДанный объект был заменён более новым объектом:\r\n".format(), end="", file=res, flush=True)
                act_obj.out_info(res, False)
                print("\r\n-------------------------------------------------\r\n".format(), end="", file=res, flush=True)
    
    def __load_params(self) -> None:
        from pullenti.address.internal.GarHelper import GarHelper
        from pullenti.address.internal.ServerHelper import ServerHelper
        if (self.__m_params is not None): 
            return
        self.__m_params = dict()
        pars = None
        if (ServerHelper.SERVER_URI is not None): 
            pars = ServerHelper.get_object_params(self.id0_)
        else: 
            pars = GarHelper.get_object_params(self.id0_)
        if (pars is not None): 
            for kp in pars.items(): 
                if (kp[0] != GarParam.GUID): 
                    self.__m_params[kp[0]] = kp[1]
        if (not GarParam.GUID in self.__m_params): 
            self.__m_params[GarParam.GUID] = self.guid
    
    def get_full_path(self, delim : str=None, correct : bool=False, addr : 'TextAddress'=None) -> str:
        """ Получить полную строку адреса с учётом родителей
        
        Args:
            delim(str): разделитель (по умолчанию, запятая с пробелом)
            addr(TextAddress): если объект выделен внутри адреса, то для скорости можно указать этот адрес, чтобы родителей искал там , а не в индексе
        
        Returns:
            str: результат
        """
        if (delim is None): 
            delim = ", "
        path = list()
        o = self
        while o is not None: 
            path.insert(0, o)
            if (len(o.parent_ids) == 0): 
                break
            if (addr is not None): 
                oo = addr.find_gar_by_ids(o.parent_ids)
                if (oo is not None): 
                    o = oo
                    continue
            o = AddressService.get_object(o.parent_ids[0])
        tmp = io.StringIO()
        i = 0
        while i < len(path): 
            if (i > 0): 
                print(delim, end="", file=tmp)
            if (correct and (isinstance(path[i].attrs, AreaAttributes))): 
                a = Utils.asObjectOrNull(path[i].attrs, AreaAttributes)
                if (len(a.names) > 0): 
                    print("{0} {1}".format(("?" if len(a.types) == 0 else a.types[0]), NameAnalyzer.correct_fias_name((a.names[0] if len(a.names) > 0 else "?"))), end="", file=tmp, flush=True)
            elif (path[i].attrs is None): 
                print("?", end="", file=tmp)
            else: 
                print(str(path[i].attrs), end="", file=tmp)
            i += 1
        return Utils.toStringStringIO(tmp)
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("gar")
        xml0_.write_element_string("id", self.id0_)
        xml0_.write_element_string("level", Utils.enumToString(self.level).lower())
        for p in self.parent_ids: 
            xml0_.write_element_string("parent", p)
        xml0_.write_element_string("guid", Utils.ifNotNull(self.guid, ""))
        if (self.expired): 
            xml0_.write_element_string("expired", "true")
        xml0_.write_element_string("reg", str(self.region_number))
        if (self.status != GarStatus.OK): 
            xml0_.write_element_string("status", Utils.enumToString(self.status).lower())
        if (self.children_count > 0): 
            xml0_.write_element_string("chcount", str(self.children_count))
        self.attrs.serialize(xml0_)
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "id"): 
                self.id0_ = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "parent"): 
                self.parent_ids.append(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "guid"): 
                self.guid = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "expired"): 
                self.expired = Utils.getXmlInnerText(x) == "true"
            elif (Utils.getXmlLocalName(x) == "chcount"): 
                self.children_count = int(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "reg"): 
                self.region_number = int(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "status"): 
                try: 
                    self.status = (Utils.valToEnum(Utils.getXmlInnerText(x), GarStatus))
                except Exception as ex225: 
                    pass
            elif (Utils.getXmlLocalName(x) == "level"): 
                try: 
                    self.level = (Utils.valToEnum(Utils.getXmlInnerText(x), GarLevel))
                except Exception as ex226: 
                    pass
            elif (Utils.getXmlLocalName(x) == "area"): 
                self.attrs = (AreaAttributes())
                self.attrs.deserialize(x)
            elif (Utils.getXmlLocalName(x) == "house"): 
                self.attrs = (HouseAttributes())
                self.attrs.deserialize(x)
            elif (Utils.getXmlLocalName(x) == "room"): 
                self.attrs = (RoomAttributes())
                self.attrs.deserialize(x)
    
    def compareTo(self, other : 'GarObject') -> int:
        if ((self.level) < (other.level)): 
            return -1
        if ((self.level) > (other.level)): 
            return 1
        aa1 = Utils.asObjectOrNull(self.attrs, AreaAttributes)
        aa2 = Utils.asObjectOrNull(other.attrs, AreaAttributes)
        if (aa1 is not None and aa2 is not None): 
            if (len(aa1.names) > 0 and len(aa2.names) > 0): 
                return Utils.compareStrings(aa1.names[0], aa2.names[0], False)
        return Utils.compareStrings(str(self), str(other), False)