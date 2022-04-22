import os
import subprocess
from urllib import response

dataFolder = None

ssgaPath = None


def setDataFolder(path):
    global dataFolder

    while path[-1] == '\\' or path[-1] == '/':
        path = path[:-1]

    if not (os.path.exists(path) and os.path.isdir(path)):
        print("Data folder missing. An empty folder will be created")
        os.mkdir(path)

    dataFolder = path


def setSSGAPath(path):
    global ssgaPath

    while path[-1] == '\\' or path[-1] == '/':
        path = path[:-1]

    if path[0] != '/' and path[0] != '\\':
        path = './' + path

    if not (os.path.exists(path) and os.path.isfile(path)):
        raise Exception(f"SSGA path provided: {path} is not a valid file")

    if not os.access(path, os.X_OK):
        raise Exception(
            f"SSGA path provided: {path} is not an executable file")

    ssgaPath = path

    checkSSGA()  # this will either error out or conclude and leave


def checkSSGA():

    testString = "testing.tld"
    knownCorrect = [574, 138, 559, 578, 253, 396, 207, 829, 581, 333]

    session = subprocess.Popen(
        [ssgaPath, testString], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = session.communicate()

    stdout = stdout.decode()

    breakline = '\r\n' if os.name == 'nt' else '\n'

    if stdout.endswith(breakline):
        stdout = stdout[:-len(breakline)]

    response = [int(line) for line in stdout.split(breakline)]

    if response != knownCorrect:
        raise Exception(
            "SSGA generated unexpected output. Check path and executable")


def fetchDomainFile(domainName, forCreation=False):
    filePath = os.path.join(dataFolder, domainName + ".json")

    exists = os.path.exists(filePath) and os.path.isfile(filePath)

    if exists and forCreation:
        raise Exception(f"Domain `{domainName}` already exists")

    elif not exists and not forCreation:
        raise Exception(f"Domain `{domainName}` does not exist")

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
