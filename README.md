# skyrec
Hackathon project for sky recognition using web camera input.

## Developing

You need to install Docker according to https://docs.docker.com/engine/installation/.

To build the Docker container with OpenCV, run:

```
docker build --tag=opencv .
```

When the process completes, you may run the container:

```
docker run --interactive --tty --volume `pwd`:/skyrec opencv
```

A new shell appears. Your source code is available at `/skyrec`. To run the programs:

```
cd /skyrec
python3 setup.py develop
# run camproc:
python3 -m skyrec.camproc tcp://192.168.x.y:29292
# run verification:
python3 -m skyrec.verification
```
