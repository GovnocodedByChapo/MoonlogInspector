import os
import re
import json
import requests
import sys

list = [
    # {
    #     'pattern':'text',
    #     'text':'text',
    #     'tip':'text'
    # },
    {
        'pattern':'attempt to call field \'(.+)\' (a nil value)',
        'text':'Невозможно вызвать "[VAR1]", значение [VAR1] == nil',
        'tip':'Убедитесь что функция/переменная "[VAR1]" существует и не равна nil'
    },
    {
        'pattern':'\'(.+)\' expected \(to close \'(.+)\' at line (.+)\) near \'(.+)\'',
        'text':'[VAR1] ожидается на строке [VAR3] (рядом с [VAR4]) для закрытия [VAR2]',
        'tip':'[VAR1] ожидается на строке [VAR3] (рядом с [VAR4]) для закрытия [VAR2]'
    },
   
    
    {
        'pattern':'\'(.+)\' has no \'(.+)\' metamethod',
        'text':'Метод [VAR2] отсутствует в структуре "[VAR1]"',
        'tip':'Метод [VAR2] отсутствует в структуре "[VAR1]"'
    },    
    
    {
        'pattern':'attempt to index a nil value',
        'text':'attempt to index a nil value',
        'tip':'Значение вызываемой переменной/значения из массива равно nil'
    },
    {
        'pattern':"module '(.+)' not found:",
        'tip':'Модуль [VAR1] не найден',
        'tip':'Установите библиотеку "[VAR1]"'
    },

    {
        'pattern':"unexpected symbol near '(.+)'",
        'text':'Неизвестный символ рядом с "[VAR1]"',
        'tip':'Неизвестный символ рядом с "[VAR1]"',
    },

    {
        'pattern':"'(.+)' expected near '(.+)'",
        'text':'"[VAR1]" ожидается рядом с "[VAR2]"',
        'tip':'"[VAR1]" ожидается рядом с "[VAR2]"',
    },

    {
        'pattern':"'(.+)' expected %(to close '(.+)' at line (.+)%) near '<eof>'",
        'text':'ожидается "[VAR1]" для закрытия "[VAR2]", которая начинается со строки [VAR3]',
        'tip':'ожидается "[VAR1]" для закрытия "[VAR2]", которая начинается со строки [VAR3]',
    },

    {
        'pattern':"attempt to call global '(.+)' %(a nil value%)",
        'text':'Не удается вызвать [VAR1] (пустое значение)',
        'tip':'Убедитесь что функция/переменная "[VAR1]" существует и не равна nil',
    },

    {
        'pattern':"bytecode",
        'text':'Скрипту требуется другая версия MoonLoader',
        'tip':'Попробуйте использовать конвертер: https://www.blast.hk/threads/35380/',
    },

    {
        'pattern':'table overflow',
        'text':'Таблица переполнена',
        'tip':'Достигнут "лимит памяти" таблицы',
    },

    {
        'pattern':"attempt to index (.+) '(.+)' %(a nil value%)",
        'text':'не удается получить доступ к [VAR1], значение "[VAR2]" не указано ([VAR2] == nil)',
        'tip':'Убедитесь что переменной "[VAR1]" присвоено значение. Попробуйте заменить "[VAR1]" на тернарный оператор https://user.su/lua/index.php?id=19',
    },

    {
        'pattern':'samp.events requires SAMPFUNCS',
        'text':'Для работы SAMP.lua необходимо установить SAMPFUNCS',
        'tip':'Установите SAMPFUNCS: https://www.blast.hk/threads/17/',
    }
]

class MoonLog:
    def LoadErrors():
        response = requests.get('https://raw.githubusercontent.com/GovnocodedByChapo/MoonlogInspector/main/errors.json')
        return response.status_code == 200, response.status_code == 200 and response.json() or [str(response.status_code)]
        
    def GetErrors(Path):
        errorsResult = []
        if len(list) > 0:
            if os.path.isfile(Path):
                F = open(Path, "r")
                for Line in F.readlines():
                    IsError = re.search('\[.+\]\s+\(error\)\s+(.+):\s+(.+):(\d+):\s+(.+)', Line)
                    if IsError:
                        Full, File, FilePath, ErrorLine, Error = IsError.group(0, 1, 2, 3, 4)
                        rText, rTip = Error, 'Возможное решение не найдено :('
                        for ErrorData in list:
                            ErrorData['text'] = ErrorData['tip']
                            IsErrorInList = re.search(ErrorData['pattern'], Error)
                            if IsErrorInList:
                                rText, rTip = ErrorData['text'], ErrorData['tip']
                                tVars, tVarIndex = [], -1
                                for tCurrentVar in IsErrorInList.groups():                                
                                    tVarIndex = tVarIndex + 1
                                    rText = rText.replace(f'[VAR{str(tVarIndex + 1)}]', str(tCurrentVar))
                                    rTip = rTip.replace(f'[VAR{str(tVarIndex + 1)}]', str(tCurrentVar))
                                rText = rText.replace('[LINE]', Line)
                                rTip = rTip.replace(f'[LINE]', Line)
                        errorsResult.append(f'● Ошибка #{str(len(errorsResult) + 1)}:\n  ├-▸ Файл: {File}\n  ├-▸ Строка: {ErrorLine}\n  ├-▸ Ошибка: {Error}\n  ├-▸ Суть ошибки: {rText}\n  └-▸ Возможное решение: {rTip}\n')
                return True, len(errorsResult) > 0 and errorsResult or ['errors_not_found']
            else:
                return False, ['file_not_found']
        else:
            return False, ['errors_list_is_empty']


        
def Scan(FilePath):
    Status, Errors = MoonLog.GetErrors(FilePath)
    if Status:
        print(f'Найденные ошибки: (всего: {str(len(Errors))})')
        for Error in Errors:
            print(Error)

def main():
    file = input('moonloader.log file: ')
    if os.path.isfile(file):
        Scan(file)
    else:
        print(f'File "{file}" not found!')
        main()

if __name__ == '__main__':
    main()
