# FaaSFlow

## Introduction

FaaSFlow is a serverless workflow engine that enables efficient workflow execution in 2 ways: a worker-side workflow schedule pattern to reduce scheduling overhead, and a adaptive storage library to use local memory to transfer data between functions on the same node.

## Installation and Software Dependencies

1. In our experiment setup, we use aliyun ecs instance installed with Ubuntu 18.04 (ecs.c6e.2xlarge, cores: 8, DRAM: 16GB) for each worker node, and a ecs.g6e.4xlarge(cores: 16, DRAM: 64GB) instance for database node installed with Ubuntu 18.04 and CouchDB.

2. Clone our code: `https://github.com/lzjzx1122/FaaSFlow.git`

On database node:

3. Reset configuration on `src/grouping/node_info.yaml`. This specify your worker address and scale_limit.

4. Run: `scripts/db_setup.bash`. This install docker, couchdb, some python packages, and build grouping results from 8 benchmarks.

On each worker node:

5. Reset COUCHDB_URL in `src/container/config.py`, `src/workflow_manager/config.py`, `test/asplos/config.py` to the corresponding db you build previously.

6. Run `scripts/worker_setup.bash`. This install docker, redis, some python packages, and build docker images from 8 benchmarks.

## Start-up

1. Enter `src/workflow_manager`, `config.py` includes serveral config that you should pay attention to: `DATA_MODE=raw/optimized`, `CONTROL_MODE=MasterSP/WorkerSP`. If you run under MasterSP, MASTER_HOST is where you start your master node.

2. Start a proxy on each worker node: `python3 proxy.py <worker_ip> <worker_port> `

3. For MasterSP, start another proxy at any node as master node, using corresponding ip and port in MASTER_HOST.

4. Start a gateway also at any node you like. The gateway opens an api for benchmark quick-startup. Choose workflow(fileprocessing, wordcount, video, illgal_recognizer, cycles, epigenomics, genome, soykb) and request_id. You can view the results in 'results' database in CouchDB. 

- ` python3 gateway.py <gateway_ip> <gateway_port> `
- ` POST /run {"workflow": "...", "request_id": "1"} `

## Run Experiment

We provide some test scripts under `test/asplos`.

### Component Overhead: overhead of one workflow engine

1. Start a proxy and record its pid.

2. Run: `python3 component_overhead.py --pid=<pid>`

3. Result is in: `component_overhead.txt`

### Data Overhead: total time spend on data transmission

1. On each node, reset DATA_MODE in `src/workflow_manager/config.py` to `raw`(cache unabled) or `optimized`(cache enabled), and start a proxy. Start a gateway also.

2. Run: `python3 component_overhead.py --datamode=<DATA_MODE>`

3. Result is in: `optimized.csv` and `raw.csv`

### End-to-End Latency: run one-by-one and run all-at-once

1. Start a proxy on each node. Start a gateway also.

2. Run: `python3 e2e_latency.py --datamode=<DATA_MODE> --mode=<MODE>` DATA_MODE = `raw` or `optimized`, MODE = `single` or `corun`

### Scheduler Scalability: the overhead of graph scheduler when scale-up total nodes of one workflow

1. Run: `python3 scheduler_scalability.py`

### Schedule Overhead: time spend on scheduling tasks

1. On each node, reset CONTROL_MODE in `src/workflow_manager/config.py` to `MasterSP` or `WorkerSP`, and start a proxy. Start a gateway also.

2. Run: `python3 schedule_overhead.py --controlmode=<CONTROL_MODE>`