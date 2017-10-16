# Metrics [![Build Status](https://travis-ci.org/comtihon/metrics.svg?branch=master)](https://travis-ci.org/comtihon/metrics)
Set of services for IOT monitoring.  
Can receive metrics from sensors, generate events if metric value is above configured, save metrics and events to database, generate sensor's statistics.
## Architecture
Metrics service contains 4 microservices and 3 third-party services:
1. [Receiver](https://github.com/comtihon/metric_receiver) - receives metrics and put them to `Kafka`.
2. [Processor](https://github.com/comtihon/metric_processor) - reads metric values in `Kafka`, if detects temperature above configured - creates warning in redis. If detects number of warnings more than configured - 
creates event in `Kafka`. Resets warning counters every time it gets normal metric.
3. [Saver](https://github.com/comtihon/metric_saver) - saves events and metrics from `Kafka` to `PostgreSQL`
4. [Assessor](https://github.com/comtihon/metric_assessor) - an http api for getting events and metric's statistics. Reads from `PostgreSQL`.
5. [PostgreSQL](https://www.postgresql.org) for storing all metrics and events.
6. [Kafka](https://kafka.apache.org/) for streaming metrics and events.
7. [Redis](https://redis.io/) for warning counters.

```
                                 Metrics And Events
Metrics ---> Receiver ---> Kafka --------> Saver ------> Postres
                            || /\                           ||
                   Metrics  || ||                           || Metrics 
                            || || Events                    || and Events
                            \/ ||                           \/
                            Processor <-------> Redis      Assessor -------------> Events
                                       Warning                      -------------> Sensor Statistics
                                       counters
```

## Waiting for a high load

* `Kafka`: use different topics for different sets of sensors
* `Kafka`: switch to [avro](https://avro.apache.org/) or [msgpack](http://msgpack.org/index.html)
* `Kafka`: more partitions for topic
* `Redis`: switch to cluster
* `Kafka`: use cluster
* `Kafka`: switch `Processor` to kafka-streams
* `Postgres` : `Assessor`s should read from slaves.

## Run

    make run
Will clone and build Docker images of services (if not built) and start all services via docker-compose.   
__Important__: Avoid port conflicts with your running services.  
See `docker-compose.yml` for details.  
__Requirements__:  
* [docker](https://www.docker.com/)
* [docker-compose](https://docs.docker.com/compose/)

    make stop
will stop all the services

## Integration testing
Run integrations tests for metric microservises.
### Full test
1. send metrics to `Receiver`
2. check them in `Kafka`
3. check events in `Kafka` (should produce 2)
4. check `Redis` counters for last warnings (should be 3)
5. check `Postres` for saved events and metrics
6. check statistics and events from `Assessor`

### Run

    make test_build && make test_install && metric_tester
or simple:

    make test_run
__Important__: Services should be accessible for tests. 
Running `make run && ./travis/sleep_if_needed.sh && make test_run` will do the job.   
__Requirements__:
* [python3.6](https://www.python.org/downloads/release/python-360/). Service is not compatible with python2.7. 
Compatibility with 3.0-3.5 versions was not tested. _(python should be linked to python3 in your os)_
* [pip](https://pypi.python.org/pypi/pip). If your os provide `pip3` instead - you should modify Makefile to use pip3.
* [wheel](https://pypi.python.org/pypi/wheel)
All other dependencies should be resolved automatically by wheel. 
If not - see them in `setup.py` `install_requires` section and use `sudo pip install <require>`.

__Configuration__:
System configuration is available in `tester/resources/services.yml`

### Adding your test
Add your test in two steps:
 * create module in `tester.test` package implementing `Test` module or any of its children.
 * and... that's all. Now second step  

System configuration is passed to your `init` method as dict.
