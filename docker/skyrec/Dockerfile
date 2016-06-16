FROM metno/opencv
RUN git clone --depth 1 https://github.com/metno/skyrec.git /skyrec && cd /skyrec && pip3 install setuptools && python3 setup.py install
WORKDIR /skyrec
