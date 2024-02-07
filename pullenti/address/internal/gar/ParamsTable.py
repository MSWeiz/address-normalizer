﻿# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.repository.BaseTable import BaseTable
from pullenti.util.repository.KeyBaseTable import KeyBaseTable
from pullenti.address.GarParam import GarParam

class ParamsTable(KeyBaseTable):
    
    def __init__(self, rep : 'IRepository', name_ : str) -> None:
        super().__init__(rep, name_, None)
    
    def get_params(self, id0_ : int) -> typing.List[tuple]:
        dat = self.read_key_data(id0_, 0)
        if (dat is None): 
            return None
        ind = 0
        res = dict()
        wrapind61 = RefOutArgWrapper(ind)
        ParamsTable._to_dic(res, dat, wrapind61)
        ind = wrapind61.value
        return res
    
    @staticmethod
    def _to_dic(res : typing.List[tuple], dat : bytearray, ind : int) -> None:
        cou = int.from_bytes(dat[ind.value:ind.value+2], byteorder="little")
        ind.value += 2
        while cou > (0): 
            typ = Utils.valToEnum(dat[ind.value], GarParam)
            ind.value += 1
            val = BaseTable.get_string_for_bytes(dat, ind, False, None)
            if (val is not None and not typ in res): 
                res[typ] = val
            cou -= 1
    
    @staticmethod
    def _get_val(dat : bytearray, ty : 'GarParam') -> str:
        ind = 0
        cou = int.from_bytes(dat[ind:ind+2], byteorder="little")
        ind += 2
        while cou > (0): 
            typ = Utils.valToEnum(dat[ind], GarParam)
            ind += 1
            if (ty == typ): 
                wrapind62 = RefOutArgWrapper(ind)
                inoutres63 = BaseTable.get_string_for_bytes(dat, wrapind62, False, None)
                ind = wrapind62.value
                return inoutres63
            wrapind64 = RefOutArgWrapper(ind)
            BaseTable.get_string_for_bytes(dat, wrapind64, True, None)
            ind = wrapind64.value
            cou -= 1
        return None
    
    @staticmethod
    def _from_dic(dat : bytearray, dic : typing.List[tuple]) -> None:
        dat.extend((len(dic)).to_bytes(2, byteorder="little"))
        for kp in dic.items(): 
            dat.append(kp[0])
            BaseTable.get_bytes_for_string(dat, kp[1], None)
    
    def put_params(self, id0_ : int, dic : typing.List[tuple], zip0_ : bool=False) -> None:
        dat = bytearray()
        ParamsTable._from_dic(dat, dic)
        b = self.auto_zip_data
        if (zip0_): 
            self.auto_zip_data = True
        self.write_key_data(id0_, bytearray(dat))
        self.auto_zip_data = b