
# rpi-monitor-api

<p align="center">
    <img alt="GitHub Tag" src="https://img.shields.io/github/v/tag/alvmarrod/rpi-monitor-api">
    <img alt="Python Version" src="https://img.shields.io/badge/python-3.11-blue">
</p>

## Table of Contents

- [Description](#description)
- [How to run](#how-to-run)
  - [Execution](#execution)
  - [Containers](#containers)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Description

This is a Python API for monitoring `Raspberry Pi` devices. It allows to query real-time data about the system's status, including CPU usage, memory usage, disk usage, and network statistics.

## How to run

### Execution

As this project is implemented using FastAPI, you can run it with a server like uvicorn (which is assumed in [requirements.txt](requirements.txt)) as:

```bash
uvicorn app.main:rpi_mon_api --host 0.0.0.0 --port 80
```

As alternative, you can run it as a Docker container, for what [Dockerfile](Dockerfile) is provided and there are targets on [Makefile](Makefile). Notice that in this case, docker requires an option `--security-opt systempaths=unconfined` to allow access from the container to the system files like belonging to `/proc/` from where the information is retrieved.

### Containers

In order to enable faster deployment by building in your computer instead of directly in your rpi device, [Makefile](Makefile) provides a target `build-linux-arm` which will allow you to build the docker image for `linux/arm64` platform.

This image can later be saved by using the target `arm-image-export`, which will generate a `.tar.gz` file with the image that you can later just `scp` to your rpi and use it.

Right now those images are not publicly available at any image registry to pull from there, so you need to build them if what to use containers.

## Endpoints

To review the available endpoints, their interfaces and responses, you can access `Swagger` or `ReDoc` interfaces. Please check testing section below.

## Testing

As this project is implemented with FastAPI, you can review and test the endpoints by using [Swagger](http://127.0.0.1:8000/docs#/) while running the server, and access [ReDoc](http://127.0.0.1:8000/redoc).

Easiest way to access them is using [Makefile](Makefile) `test` target.

## Dependencies

You can check the current depencies and their versions in the [requirements](requirements.txt) file.

## Contributing

If you want to contribute to this project, please submit a pull request or issue following the available templates

## License

This project is licensed under the MIT License
