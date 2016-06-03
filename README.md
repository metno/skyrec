# skyrec
Hackathon project for sky recognition using web camera input.

## Developing

You need to install Docker according to https://docs.docker.com/engine/installation/.

To build the Docker containers with OpenCV and Skyrec, run:

```
make opencv skyrec
```

When the process completes, you may run the container. You must start one process for each module you want to run.

```
docker run --interactive --tty --volume `pwd`:/skyrec skyrec
```

A new shell appears. Your source code is available at `/skyrec`. To run the programs:

```
python3 setup.py develop
# run proxy (proxies client requests to server backend):
python3 -m skyrec.proxy
# run camproc (the actual image processing software):
python3 -m skyrec.camproc tcp://127.0.0.1:22222
# run verification:
python3 -m skyrec.verification tcp://127.0.0.1:29999 contrib/data.csv --path /path/to/images/
```

Replace `127.0.0.1` with the interface address of the `proxy` server.
