

import threading
import time
import traceback

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from metrics.loggers import checkMetrics, consumeAccessLog, disableMetrics

bucket = "p3-bucket"
org = None
client: InfluxDBClient = None


def setUpInfluxDBClient(idb_url, idb_port, idb_org, idb_token):
    global client

    if not checkMetrics():
        return
    try:
        print(f"Connecting to {idb_url} on port {idb_port}")
        client = InfluxDBClient(url=f"http://{idb_url}:{idb_port}",
                                org=idb_org, token=idb_token, bucket=bucket)

        query_api = client.query_api()
        query_api.query(
            f'from(bucket:"{bucket}") |> range(start: -10m)')
        org = idb_org
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

    print("Starting InfluxDB connection...")

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


def deleteDomainMetrics(domainName):
    delete_api = client.delete_api()

    from objects.utils import epoch, stampToISO

    start = epoch
    stop = stampToISO(time.time())

    delete_api.delete(
        start, stop, f'secondLevelDomain="{domainName}"', org=org,  bucket=bucket)
