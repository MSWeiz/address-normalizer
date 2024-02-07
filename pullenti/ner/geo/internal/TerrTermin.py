# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.core.Termin import Termin

class TerrTermin(Termin):
    
    def __init__(self, source : str, lang_ : 'MorphLang'=None) -> None:
        super().__init__(None, lang_, False)
        self.is_state = False
        self.is_region = False
        self.is_adjective = False
        self.is_always_prefix = False
        self.is_doubt = False
        self.is_moscow_region = False
        self.is_strong = False
        self.is_specific_prefix = False
        self.is_sovet = False
        self.init_by_normal_text(source, lang_)
    
    @staticmethod
    def _new1502(_arg1 : str, _arg2 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.gender = _arg2
        return res
    
    @staticmethod
    def _new1503(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new1504(_arg1 : str, _arg2 : bool, _arg3 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new1505(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new1507(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        res.is_doubt = _arg3
        return res
    
    @staticmethod
    def _new1508(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new1509(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        return res
    
    @staticmethod
    def _new1510(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        return res
    
    @staticmethod
    def _new1511(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        res.is_adjective = _arg3
        return res
    
    @staticmethod
    def _new1512(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        res.is_adjective = _arg4
        return res
    
    @staticmethod
    def _new1513(_arg1 : str, _arg2 : bool, _arg3 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new1515(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        return res
    
    @staticmethod
    def _new1516(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new1517(_arg1 : str, _arg2 : bool, _arg3 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new1518(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1523(_arg1 : str, _arg2 : bool, _arg3 : bool, _arg4 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_always_prefix = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new1527(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool, _arg5 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_always_prefix = _arg4
        res.gender = _arg5
        return res
    
    @staticmethod
    def _new1531(_arg1 : str, _arg2 : bool, _arg3 : 'MorphGender', _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.gender = _arg3
        res.is_always_prefix = _arg4
        return res
    
    @staticmethod
    def _new1532(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_always_prefix = _arg3
        return res
    
    @staticmethod
    def _new1537(_arg1 : str, _arg2 : bool, _arg3 : 'MorphGender', _arg4 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.gender = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1539(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_strong = _arg3
        return res
    
    @staticmethod
    def _new1542(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_strong = _arg4
        return res
    
    @staticmethod
    def _new1546(_arg1 : str, _arg2 : str, _arg3 : bool, _arg4 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.canonic_text = _arg2
        res.is_sovet = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new1549(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_adjective = _arg3
        return res
    
    @staticmethod
    def _new1550(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_adjective = _arg4
        return res
    
    @staticmethod
    def _new1551(_arg1 : str, _arg2 : bool, _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_specific_prefix = _arg3
        res.is_always_prefix = _arg4
        return res
    
    @staticmethod
    def _new1552(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool, _arg5 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_specific_prefix = _arg4
        res.is_always_prefix = _arg5
        return res
    
    @staticmethod
    def _new1553(_arg1 : str, _arg2 : str, _arg3 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.acronym = _arg2
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new1554(_arg1 : str, _arg2 : str, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.acronym = _arg2
        res.is_region = _arg3
        return res
    
    @staticmethod
    def _new1555(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.canonic_text = _arg2
        res.acronym = _arg3
        res.is_region = _arg4
        return res
    
    @staticmethod
    def _new1556(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_moscow_region = _arg2
        return res