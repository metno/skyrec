FROM ubuntu:16.04

WORKDIR /
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
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
    python3-pip
RUN pip3 install numpy
RUN git clone --depth 1 --branch 3.1.0 https://github.com/Itseez/opencv.git /opencv
RUN git clone --depth 1 --branch 3.1.0 https://github.com/Itseez/opencv_contrib.git /opencv_contrib
RUN mkdir /opencv/build
WORKDIR /opencv/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules \
    -D BUILD_EXAMPLES=OFF \
    /opencv
RUN make -j4
RUN make install && ldconfig
WORKDIR /
