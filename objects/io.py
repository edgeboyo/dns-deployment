from msilib.schema import Error
import os

dataFolder = None


def setDataFolder(path):
    global dataFolder

    while path[-1] == '\\' or path[-1] == '/':
        path = path[:-1]

    if not (os.path.exists(path) and os.path.isdir(path)):
        print("Data folder missing. An empty folder will be created")
        os.mkdir(path)

    dataFolder = path


def fetchDomainFile(domainName):
    filePath = os.path.join(dataFolder, domainName + ".json")

    if os.path.exists(filePath) and os.path.isfile(filePath):
        raise Exception(f"Domain `{domainName}` already exists")

    return filePath


def listDomainFiles():
    domains = os.listdir(dataFolder)
    domains = filter(lambda d: os.fsdecode(d).endswith(".json"), domains)
    domains = [os.path.join(dataFolder, domain) for domain in domains]
    return domains


def listDomainNames():
    domains = os.listdir(dataFolder)
    domains = filter(lambda d: os.fsdecode(d).endswith(".json"), domains)
    return [os.path.basename(domain) for domain in domains]
