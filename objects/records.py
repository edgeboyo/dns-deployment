from audioop import add
import time

from objects.utils import stampToISO

##################
# UTIL FUNCTIONS #
##################


from ipaddress import ip_address, IPv4Address, IPv6Address


def checkIfIP(address, addrType="IPv4"):
    prohibited = ['0:0::0:0:0'] if addrType == "IPv6" else ['0:0::0:0:0']
    addrType = IPv6Address if addrType == "IPv6" else IPv4Address

    if not isinstance(address, str):
        return False

    if address in prohibited:
        return False

    try:
        if type(ip_address(address)) is addrType:
            return True
        else:
            return False
    except:
        return False  # if errors assume record does not comply


def checkHostname(address, allowBlank=True):
    if not isinstance(address, str):
        return False

    if address == '':
        raise Exception("A blank hostname needs to be established with '@'")

    if (address == '@') and not allowBlank:
        raise Exception("'@' is not allowed in this mapping: " + address)
    elif address == '@':
        return True

    alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    numbers = [str(i) for i in range(0, 10)]
    # '*' is technically allowed it needs to be checked if its in the correct space in the correct segment
    allowedCharset = alphabet + numbers + ['-', '*']

    for i, segment in enumerate(address.lower().split('.')):
        if len(segment) == 0 or len(segment) >= 64:
            return False

        if i != 0 and '*' in segment:
            return False

        if i == 0 and '*' in segment and segment != '*':
            return False

        for c in segment:
            if c not in allowedCharset:
                return False

    return True


#####################
# RECORD GENERATORS #
#####################


def createARecord(hostname, mapping, ttl=3600, now=None):
    if not isinstance(ttl, int):
        raise Exception('"ttl" filed must be of type int')

    if not checkHostname(hostname):
        raise Exception(f"{hostname} is not a valid hostname")

    now = time.time() if now == None else now

    hostname = hostname.lower()

    if not checkIfIP(mapping, "IPv4"):
        raise Exception(f"{mapping} is not an IPv4 address as it should be")

    mapping = mapping.lower()

    record = {'record': hostname, "mapping": mapping,
              "ttl": ttl, "setAt": stampToISO(now)}

    return record


def createAAAARecord(hostname, mapping, ttl=3600, now=time.time()):
    if not isinstance(ttl, int):
        raise Exception('"ttl" filed must be of type int')

    if not checkHostname(hostname):
        raise Exception(f"{hostname} is not a valid hostname")

    hostname = hostname.lower()

    if not checkIfIP(mapping, "IPv6"):
        raise Exception(f"{mapping} is not an IPv6 address as it should be")

    mapping = mapping.lower()

    record = {'record': hostname, "mapping": mapping,
              "ttl": ttl, "setAt": stampToISO(now)}

    return record


def createTXTRecord(hostname, value, ttl=3600, now=time.time()):
    if not isinstance(ttl, int):
        raise Exception('"ttl" filed must be of type int')

    if not checkHostname(hostname):
        raise Exception(f"{hostname} is not a valid hostname")

    hostname = hostname.lower()

    record = {'record': hostname, "value": value,
              "ttl": ttl, "setAt": stampToISO(now)}

    return record

###################################
# IMPORTABLE FUNCTIONS AND VALUES #
###################################


recordMappings = {'A': createARecord,
                  'AAAA': createAAAARecord, 'TXT': createTXTRecord}

supportedRecords = list(recordMappings.keys())


def validateRecord(recordType, records):
    now = time.time()
    recordFunction = recordMappings[recordType]

    transformedRecords = []
    try:
        for record in records:
            print(record)
            record = recordFunction(**record, now=now)
            transformedRecords.append(record)
    except TypeError as e:
        e = str(e)
        if 'required positional argument' in e:
            e = e.split(":")[-1][1:] + " fields missing in request body"
        if 'got an unexpected keyword argument' in e:
            e = "Unexpected " + \
                e.split(" ")[-1] + " field included in request body"
        raise Exception(e)

    return transformedRecords
