﻿# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class NumberItemClass(IntEnum):
    UNDEFINED = 0
    HOUSE = 1
    GARAGE = 2
    PLOT = 3
    FLAT = 4
    ROOM = 5
    CARPLACE = 6
    SPACE = 7
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)