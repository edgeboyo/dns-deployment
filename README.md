# dns-deployment
DNS Deployment for the Part 3 individual project

Initial deployment makes use of [this gist by pklaus](https://gist.github.com/pklaus/b5a7876d4d2cf7271873)

## Deployment in docker

In order to initialize the project an image needs to be generated. This can be done in two ways:

* By building the image with `./docker.sh -b`
* Or downloading it from the registry with `./docker.sh -d`

After that a network needs to be created with `./docker.sh -n`.

Initialization of all containers in the correct order can be made with `./docker.sh -u`. 

The build script has more functionally as outlined by it's help message:

```
./docker.sh -b/--build -c/--create -d/--deploy -h/--help
---------------------------------------------------------------
-b/--build - Build docker image from source
-c/--create - Create new docker container
-p/--publish - Publish this image to a docker repository (required login to repo)
-d/--download - Download the image from the docker repository (required login to repo)
-n/--network - Set up internal network for the containers
-u/--up - Set up both required containers and remove previous versions
-h/--help - Show this message
---------------------------------------------------------------
```

These options can be used in sequence for for instance in first startup the user might use `./docker.sh -b -n -u` to build, create a network and set up containers.

## Individual use of deployment

A base deployment of the program can be started with `py main --udp` with a UDP server and `py main --tcp` with a TCP server. Both options can be enabled in one time.

The deployment relies on `InfluxDB` and the `semantic similarity analyzer`. However these can be disabled by starting the project with 
```py
echo "echo 0" > blank
chmod +x blank

py main.py --udp --no-metrics --ssga-path blank
```

This will create a blank script to run as ssga and disable metric collection.

Additional functions can be accessed in main's help section as seen here:
```
usage: main.py [-h] [-d] [--dns-port DNS_PORT] [--http-port HTTP_PORT] [--tld TLD] [--data-folder DATA_FOLDER] [--ssga-path SSGA_PATH] [--tcp] [--udp] [--dry-run] [--fallback-dns FALLBACK_DNS]
               [--no-metrics] [--influx-port INFLUX_PORT] [--influx-token INFLUX_TOKEN] [--influx-org INFLUX_ORG] [--metrics-consumers METRICS_CONSUMERS]

Start a DNS implemented in Python. Usually DNSs use UDP on port 53.

options:
  -h, --help            show this help message and exit
  -d                    Set this flag to use internal docker addresses (for docker deployment)
  --dns-port DNS_PORT   The port to listen on for the DNS server.
  --http-port HTTP_PORT
                        The port to listen on for the HTTP API and GUI.
  --tld TLD             The top level domain of this DNS deployment (default ".tld")
  --data-folder DATA_FOLDER
                        Location of DNS files being stored (default "./data")
  --ssga-path SSGA_PATH
                        Location of the semantic similarity analyzer [SSGA] (default "ssga" for Linux and "ssga.exe" for Windows)
  --tcp                 Prepare a TCP DNS server
  --udp                 Prepare a UDP DNS server
  --dry-run             Initialize the program, check arguments and exit immediately
  --fallback-dns FALLBACK_DNS
                        Address to a DNS used as authority when the domain requested is not under this server
  --no-metrics          Allow for the deployment to not collect metrics
  --influx-port INFLUX_PORT
                        Set a custom port for InfluxDB
  --influx-token INFLUX_TOKEN
                        Set a custom auth token for InfluxDB (default "secret-auth-token")
  --influx-org INFLUX_ORG
                        Set a custom org for InfluxDB (default "part3")
  --metrics-consumers METRICS_CONSUMERS
                        Set custom amount of metrics consumer threads (default 5)
```