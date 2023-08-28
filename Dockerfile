# docker container running pyBBarolo & BBarolo

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt -y update && apt install -y apt-utils && \
    apt install -y --no-install-recommends \
    build-essential \
    make \
    gcc \
    git \
    wget \
    curl \
    swig \
    libfftw3-dev \
    libfftw3-doc \
    netpbm \
    wcslib-dev \
    wcslib-tools \
    zlib1g-dev \
    libbz2-dev \
    libcairo2-dev \
    libcfitsio-dev \
    libcfitsio-bin \
    libgsl-dev \
    libjpeg-dev \
    libnetpbm10-dev \
    libpng-dev \
    python3 \
    python3-dev \
    python3-pip \
    python3-tk \
    python3-setuptools \
    python3-wheel \
    python3-numpy \
    python3-scipy \
    python3-matplotlib \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# create a Bbarolo dir
RUN mkdir /3dbarolo

# and make it the work dir
WORKDIR /3dbarolo

COPY cluster_dilated_cubelets /3dbarolo


# trial for cfitsio ?
RUN wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio_latest.tar.gz \
    && tar -xvf cfitsio_latest.tar.gz \
    && cd cfitsio-4.3.0 \
    && ./configure \
    && make \
    && make install \
    && make clean && echo cfitsio installed successfully

# now install 3dBBarolo
RUN git clone -b master --single-branch https://github.com/editeodoro/Bbarolo \
    && cd Bbarolo \
    && ./configure \
    && make \
    && make install \
    && make clean && echo 3dB has been installed

#pip installs

RUN for x in \
    fitsio \
    astropy \
    pyBBarolo \
    ; do pip3 install --no-cache-dir $x; done

#set python to 3

RUN ln -s /usr/bin/python3 /usr/bin/python
ENV PYTHONPATH=/usr/local/lib/python

CMD ['python', 'pyBBarolo_new_model.py']

