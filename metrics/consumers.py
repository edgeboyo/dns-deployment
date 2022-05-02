

import threading
import time
import traceback

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from metrics.loggers import checkMetrics, consumeAccessLog, disableMetrics

bucket = "p3-bucket"

client: InfluxDBClient = None


def setUpInfluxDBClient(idb_port, idb_user, idb_passwd):
    global client

    if not checkMetrics():
        return
    try:
        client = InfluxDBClient(url="localhost",
                                port=idb_port, org="part3", token='secret-auth-token', bucket=bucket)

        query_api = client.query_api()
        tables = query_api.query(
            f'from(bucket:"{bucket}") |> range(start: -10m)')
        print(tables)
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

    for i in range(amount):
        thread = threading.Thread(target=consume, args=(i+1,))
        thread.daemon = True
        thread.start()


def consume(threadId):

    print(f"[MetricConsumer #{threadId}] starting...")

    while True:
        try:
            log = consumeAccessLog()
            print(f"[MetricConsumer #{threadId}] {log}")

            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=bucket, record=log.toPoint())
        except:
            print("Metric collector error: ")
            traceback.print_exc()
            print("Continueing thread")
            continue
