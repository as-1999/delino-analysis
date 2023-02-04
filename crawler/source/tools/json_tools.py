from json import dumps, load
from os import path
#from tools.logging_tools import exception

def storage(items: list, fileName: str, method: str, savePath: str='') -> None:
        dirname = path.dirname(__file__) if savePath == '' else savePath
        try:
            with open(dirname + "/{file}".format(file=fileName), method, encoding='utf-8') as writeFile:
                tmpDict = {'items':items}
                json_object = dumps(tmpDict, indent=4, sort_keys=True)
                writeFile.write(json_object)
        except Exception as error:
            pass
            #exception(error)

def reader(fileName: str, method: str, savePath: str='') -> list:
    dirname = dirname = path.dirname(__file__) if savePath == '' else savePath
    try:
        with open(dirname + "/{file}".format(file=fileName), method, encoding='utf-8') as readFile:
            List = load(readFile)['items']
            for item in List:
                yield item
    except Exception as error:
        pass
        #exception(error)

def appender(items: list, fileName: str, savePath: str='') -> None:
    dirname = dirname = path.dirname(__file__) if savePath == '' else savePath
    try:
        data = []
        for item in reader(fileName, 'r', dirname):
            data.append(item)
        for item in items:
            data.append(item)
        storage(data, fileName, 'w', dirname)
    except Exception as error:
        pass
        #exception(error)
