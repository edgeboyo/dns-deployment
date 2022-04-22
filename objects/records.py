import time

from objects.utils import stampToISO

##################
# UTIL FUNCTIONS #
##################


def checkIfIPv4(address):
    prohibited = ['0.0.0.0']

    if address in prohibited:
        return False

    try:
        sections = address.split('.')
        if len(sections) != 4:
            return False

        for num in sections:
            num = int(num)

            if num < 0 or num >= 256:
                return False
    except:
        return False  # if errors assume record does not comply

    return True

#####################
# RECORD GENERATORS #
#####################


def createARecord(record, mapping, ttl=3600):
    if not isinstance(ttl, int):
        raise Exception('"ttl" filed must be of type int')

    if not checkIfIPv4(mapping):
        raise Exception(f"{mapping} is not an IPv4 address as it should be")

    now = time.time()
    record = {'record': record, "mapping": mapping,
              "ttl": ttl, "setAt": stampToISO(now)}

    return record

###################################
# IMPORTABLE FUNCTIONS AND VALUES #
###################################


recordMappings = {'A': createARecord}

supportedRecords = list(recordMappings.keys())


def validateRecord(recordType, records):
    now = time.time()
    recordFunction = recordMappings[recordType]

    transformedRecords = []
    try:
        for record in records:
            print(record)
            record = recordFunction(**record)
            transformedRecords.append(record)
    except TypeError as e:
        e = str(e)
        if 'required positional argument' in e:
            e = e.split(":")[-1][1:] + " fields missing in a record"
        raise Exception(e)

    return transformedRecords
