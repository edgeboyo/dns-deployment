

import threading
import traceback

from influxdb import InfluxDBClient

from metrics.loggers import checkMetrics, consumeAccessLog

influxdb = None


def setUpInfluxDBClient(idb_port):
    global influxdb

    if not checkMetrics():
        return

    influxdb = InfluxDBClient(port=idb_port)

    return


def startMetricConsumers(amount):

    if not checkMetrics():
        print("Metric collection disabled. No threads started")
        return

    for i in range(amount):
        thread = threading.Thread(target=consume, args=(i+1,))
        thread.daemon = True
        thread.start()


def consume(threadId):

    print(f"Metric thread #{threadId} starting...")

    while True:
        try:
            log = consumeAccessLog()
            # Do more stuff
        except:
            print("Metric collector error: ")
            traceback.print_exc()
            print("Continueing thread")
            continue
