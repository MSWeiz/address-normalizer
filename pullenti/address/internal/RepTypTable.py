﻿# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.repository.KeyBaseTable import KeyBaseTable

class RepTypTable(KeyBaseTable):
    
    def __init__(self, base_dir : str, name_ : str="typs") -> None:
        super().__init__(None, name_, base_dir)
        self.__m_types_by_name = dict()
        self.__m_types_by_id = dict()
        max0_ = self.get_max_key()
        id0_ = 1
        first_pass3117 = True
        while True:
            if first_pass3117: first_pass3117 = False
            else: id0_ += 1
            if (not (id0_ <= max0_)): break
            dat = self.read_key_data(id0_, 0)
            if (dat is None): 
                continue
            typ = dat.decode("UTF-8", 'ignore')
            if (typ in self.__m_types_by_name): 
                continue
            self.__m_types_by_name[typ] = id0_
            self.__m_types_by_id[id0_] = typ
    
    def get_id(self, typ : str) -> int:
        if (Utils.isNullOrEmpty(typ)): 
            return 0
        id0_ = 0
        wrapid203 = RefOutArgWrapper(0)
        inoutres204 = Utils.tryGetValue(self.__m_types_by_name, typ, wrapid203)
        id0_ = wrapid203.value
        if (inoutres204): 
            return id0_
        id0_ = (self.get_max_key() + 1)
        self.write_key_data(id0_, typ.encode("UTF-8", 'ignore'))
        self.flush()
        self.__m_types_by_id[id0_] = typ
        self.__m_types_by_name[typ] = id0_
        return id0_
    
    def get_typ(self, id0_ : int) -> str:
        typ = None
        wraptyp205 = RefOutArgWrapper(None)
        inoutres206 = Utils.tryGetValue(self.__m_types_by_id, id0_, wraptyp205)
        typ = wraptyp205.value
        if (inoutres206): 
            return typ
        return None