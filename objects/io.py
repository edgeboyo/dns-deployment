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


def fetchDomainFile(domainName, forCreation=False):
    filePath = os.path.join(dataFolder, domainName + ".json")

    exists = os.path.exists(filePath) and os.path.isfile(filePath)

    if exists and forCreation:
        raise Exception(f"Domain `{domainName}` already exists")

    elif not exists and not forCreation:
        raise Exception(f"Domain `{domainName} does not exist")

    return filePath


def listDomainFiles():
    domains = os.listdir(dataFolder)
    domains = filter(lambda d: os.fsdecode(d).endswith(".json"), domains)
    domains = [os.path.join(dataFolder, domain) for domain in domains]
    return domains


def listDomainNames():
    domains = os.listdir(dataFolder)
    domains = filter(lambda d: os.fsdecode(d).endswith(".json"), domains)
    return [domain[:-5] for domain in domains]
