# SDK Pullenti Address, version 4.21, october 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import pathlib
import xml.etree.ElementTree as ET
from pullenti.unisharp.Utils import Utils

from pullenti.address.ProcessTextParams import ProcessTextParams
from pullenti.address.SearchParams import SearchParams
from pullenti.address.AddressService import AddressService

class Program:
    
    @staticmethod
    def main(args : typing.List[str]) -> None:
        # Можно работать через сервер, тогда инициалиация не нужна
        if (AddressService.set_server_connection("http://localhost:2222")): 
            server_version = AddressService.get_server_version("http://localhost:2222")
            print("Server version: {0}".format(Utils.ifNotNull(server_version, "?")), flush=True)
        else: 
            # Обязательная инициализация один раз перед использованием SDK
            print("Initialize SDK Pullenti Address v.{0} ... ".format(AddressService.VERSION), end="", flush=True)
            AddressService.initialize()
            print("OK", flush=True)
            # Указание SDK папки с индексом ГАР
            gar_path = "Gar77"
            if (not pathlib.Path(gar_path).is_dir()): 
                print("Gar path {0} not exists".format(gar_path), flush=True)
                return
            AddressService.set_gar_index_path(gar_path)
        info = AddressService.get_gar_statistic()
        if (info is not None): 
            print(str(info), flush=True)
        # дополнительные параметры анализа
        pars = ProcessTextParams()
        text = "Москва, ул. 16-я Парквая 2 3"
        saddr = AddressService.process_single_address_text(text, pars)
        print("\nAnalyze address: {0}".format(text), flush=True)
        if (saddr is None): 
            print("Fatal process error", flush=True)
        else: 
            print("Coefficient: {0}".format(saddr.coef), flush=True)
            if saddr.coef > 41:
                if (saddr.error_message is not None):
                    print("Message: {0}".format(saddr.error_message), flush=True)
                for item in saddr.items:
                    #print("Item: {0}".format(str(item)), end="", flush=True)
                    #print("", flush=True)
                    print(item)

if __name__ == "__main__":
    Program.main(None)
