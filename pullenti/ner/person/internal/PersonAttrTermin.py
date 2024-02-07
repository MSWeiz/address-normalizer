# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.core.Termin import Termin
from pullenti.ner.person.internal.PersonAttrTerminType2 import PersonAttrTerminType2
from pullenti.ner.person.internal.PersonAttrTerminType import PersonAttrTerminType

class PersonAttrTermin(Termin):
    
    def __init__(self, v : str, lang_ : 'MorphLang'=None) -> None:
        super().__init__(None, lang_, False)
        self.typ = PersonAttrTerminType.OTHER
        self.typ2 = PersonAttrTerminType2.UNDEFINED
        self.can_be_unique_identifier = False
        self.can_has_person_after = 0
        self.can_be_same_surname = False
        self.can_be_independant = False
        self.is_boss = False
        self.is_kin = False
        self.is_military_rank = False
        self.is_nation = False
        self.is_post = False
        self.is_profession = False
        self.is_doubt = False
        self.init_by_normal_text(v, lang_)
    
    @staticmethod
    def _new2530(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'PersonAttrTerminType') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2561(_arg1 : str, _arg2 : 'PersonAttrTerminType') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.typ = _arg2
        return res
    
    @staticmethod
    def _new2563(_arg1 : str, _arg2 : 'PersonAttrTerminType', _arg3 : 'MorphGender') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.typ = _arg2
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new2564(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'PersonAttrTerminType', _arg4 : 'MorphGender') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1, _arg2)
        res.typ = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new2572(_arg1 : str, _arg2 : str, _arg3 : 'PersonAttrTerminType2', _arg4 : 'PersonAttrTerminType') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.canonic_text = _arg2
        res.typ2 = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new2573(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str, _arg4 : 'PersonAttrTerminType2', _arg5 : 'PersonAttrTerminType') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1, _arg2)
        res.canonic_text = _arg3
        res.typ2 = _arg4
        res.typ = _arg5
        return res
    
    @staticmethod
    def _new2578(_arg1 : str, _arg2 : 'PersonAttrTerminType2', _arg3 : 'PersonAttrTerminType') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.typ2 = _arg2
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2579(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'PersonAttrTerminType2', _arg4 : 'PersonAttrTerminType') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1, _arg2)
        res.typ2 = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new2598(_arg1 : str, _arg2 : str, _arg3 : 'PersonAttrTerminType', _arg4 : 'PersonAttrTerminType2') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.canonic_text = _arg2
        res.typ = _arg3
        res.typ2 = _arg4
        return res
    
    @staticmethod
    def _new2600(_arg1 : str, _arg2 : 'PersonAttrTerminType2', _arg3 : 'PersonAttrTerminType', _arg4 : 'MorphLang') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.typ2 = _arg2
        res.typ = _arg3
        res.lang = _arg4
        return res
    
    @staticmethod
    def _new2605(_arg1 : str, _arg2 : 'PersonAttrTerminType', _arg3 : 'MorphLang') -> 'PersonAttrTermin':
        res = PersonAttrTermin(_arg1)
        res.typ = _arg2
        res.lang = _arg3
        return res