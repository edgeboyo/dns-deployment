

import threading
import time
import traceback

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from metrics.loggers import checkMetrics, consumeAccessLog, disableMetrics

bucket = "p3-bucket"

client = None


def setUpInfluxDBClient(idb_port, idb_user, idb_passwd):
    global client

    if not checkMetrics():
        return
    try:
        print(f"Logging in: P:{idb_port}, U:{idb_user}, P:{idb_passwd}")

        client = InfluxDBClient(url="localhost",
                                port=idb_port, username=idb_user, password=idb_passwd, org="p3", token='secret-auth-token', bucket=bucket)

        write_api = client.write_api(write_options=SYNCHRONOUS)
        query_api = client.query_api()

        client = (write_api, query_api, client)
    except:
        print("Error connecting to Influx DB")
        traceback.print_exc()
        print("\nAwaiting user termination...")
        print("Progressing without metrics will commence in 5 seconds")
        time.sleep(5)
        client = None
        disableMetrics()
        print("Processing...")
        return

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
