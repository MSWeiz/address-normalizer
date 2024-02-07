# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class ProcessTextParams:
    """ Параметры обработки текста """
    
    def __init__(self) -> None:
        self.default_regions = list()
        self.default_object = None
        self.is_plot = False
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (len(self.default_regions) == 1): 
            print("Регион: {0}".format(self.default_regions[0]), end="", file=tmp, flush=True)
        elif (len(self.default_regions) > 0): 
            print("Регионы: {0}".format(self.default_regions[0]), end="", file=tmp, flush=True)
            i = 1
            while i < len(self.default_regions): 
                print(",{0}".format(self.default_regions[i]), end="", file=tmp, flush=True)
                i += 1
        if (self.default_object is not None): 
            print(" Объект: {0}".format(str(self.default_object)), end="", file=tmp, flush=True)
        if (self.is_plot): 
            print(" Участок: да", end="", file=tmp)
        if (tmp.tell() == 0): 
            print("Нет", end="", file=tmp)
        return Utils.toStringStringIO(tmp)