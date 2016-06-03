FROM ubuntu:16.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -y --no-install-recommends install \
        build-essential \
        cmake \
        gfortran \
        git \
        libatlas-base-dev \
        libavcodec-dev \
        libavformat-dev \
        libgtk2.0-dev \
        libjasper-dev \
        libjpeg8-dev \
        libpng12-dev \
        libswscale-dev \
        libtiff5-dev \
        libv4l-dev \
        libzmq3-dev \
        pkg-config \
        python3-dev \
        python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install numpy
RUN git clone --depth 1 --branch 3.1.0 https://github.com/Itseez/opencv.git /opencv
RUN git clone --depth 1 --branch 3.1.0 https://github.com/Itseez/opencv_contrib.git /opencv_contrib
RUN mkdir /opencv/build \
    && cd /opencv/build \
    && cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr \
        -D INSTALL_C_EXAMPLES=OFF \
        -D INSTALL_PYTHON_EXAMPLES=ON \
        -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules \
        -D BUILD_EXAMPLES=OFF \
        /opencv \
    && make -j4 \
    && make install \
    && ldconfig \
    && cd / \
    && rm -rf /opencv \
    && rm -rf /opencv_contrib
RUN git clone --depth 1 https://github.com/metno/skyrec.git /skyrec && cd /skyrec && pip3 install setuptools && python3 setup.py install
