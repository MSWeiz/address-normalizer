﻿# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.address.RoomType import RoomType
from pullenti.address.AddressHelper import AddressHelper

class RoomAttributes(BaseAttributes):
    """ Атрибуты внутридомовых помещений (квартиры, комнаты), гаражей и машиномест
    Внутридомовые помещения
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.typ = RoomType.UNDEFINED
        self.number = None;
        self.misc = None;
    
    def __str__(self) -> str:
        res = "{0}{1}".format(AddressHelper.get_room_type_string(self.typ, True), Utils.ifNotNull(self.number, "б/н"))
        if (self.misc is not None): 
            res = "{0} {1}".format(res, self.misc)
        return res
    
    def out_info(self, res : io.StringIO) -> None:
        typ_ = AddressHelper.get_room_type_string(self.typ, False)
        print("{0}{1}: {2}\r\n".format(str.upper(typ_[0]), typ_[1:], Utils.ifNotNull(self.number, "б/н")), end="", file=res, flush=True)
        if (self.misc is not None): 
            print("Дополнительно: {0}\r\n".format(self.misc), end="", file=res, flush=True)
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("room")
        if (self.typ != RoomType.UNDEFINED): 
            xml0_.write_element_string("type", Utils.enumToString(self.typ).lower())
        if (self.number is not None): 
            xml0_.write_element_string("num", self.number)
        if (self.misc is not None): 
            xml0_.write_element_string("misc", self.misc)
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "type"): 
                try: 
                    self.typ = (Utils.valToEnum(Utils.getXmlInnerText(x), RoomType))
                except Exception as ex229: 
                    pass
            elif (Utils.getXmlLocalName(x) == "num"): 
                self.number = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "misc"): 
                self.misc = Utils.getXmlInnerText(x)
    
    def clone(self) -> 'BaseAttributes':
        res = RoomAttributes()
        res.number = self.number
        res.typ = self.typ
        res.misc = self.misc
        return res
    
    @staticmethod
    def _new162(_arg1 : 'RoomType', _arg2 : str) -> 'RoomAttributes':
        res = RoomAttributes()
        res.typ = _arg1
        res.number = _arg2
        return res