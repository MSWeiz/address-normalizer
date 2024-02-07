﻿# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class ParamType(IntEnum):
    """ Дополнительные параметры адреса """
    UNDEFINED = 0
    ORDER = 1
    """ Очередь (например, в ГСК) """
    PART = 2
    """ Часть """
    FLOOR = 3
    """ Этаж """
    GENPLAN = 4
    """ Генплан """
    DELIVERYAREA = 5
    """ Доставочный участок """
    ZIP = 6
    """ Индекс """
    SUBSCRIBERBOX = 7
    """ Абон.ящик """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)