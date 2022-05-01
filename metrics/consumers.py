

import threading
import traceback

from metrics.loggers import checkMetrics, consumeAccessLog


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
            return


def startMetricConsumers(amount):

    if not checkMetrics():
        print("Metric collection disabled. No threads started")
        return

    for i in range(amount):
        thread = threading.Thread(target=consume, args=(i+1,))
        thread.daemon = True
        thread.start()
