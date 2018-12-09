FROM consol/ubuntu-xfce-vnc:1.1.0

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 USER=$USER HOME=$HOME

RUN echo "The working directory is: $HOME"
RUN echo "The user is: $USER"

USER 0

EXPOSE 5901
EXPOSE 6901
EXPOSE 8097

RUN apt-get update && apt-get install -y \
        sudo \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# install dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    apt-utils \
    curl \
    nano \
    vim \
    git \
    zlib1g-dev \
    cmake \
    python-software-properties \
    software-properties-common \
    graphviz \
    libgraphviz-dev \
    graphviz-dev \
    pkg-config \
    ffmpeg \
    zlib1g-dev cmake \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libfontconfig1 \
    libxrender1


# Install python
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python-numpy \
    python-dev

# Installing python3.6
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3.6 \
    python3.6-dev \
    python3.6-venv


RUN ln -s /usr/bin/python3.6 /usr/local/bin/python3

# Installing pip and pip3
RUN apt-get remove python-pip python3-pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py --trusted-host pypi.python.org
RUN python3 get-pip.py --trusted-host pypi.python.org
RUN rm get-pip.py


RUN mkdir -p $HOME
WORKDIR $HOME

# Cloning the repositories
RUN git clone https://github.com/pierg/wiseml.git
RUN git clone https://github.com/pierg/baselines.git
RUN cd wiseml


RUN pip3 install --upgrade pip

RUN \
    pip3 install codacy-coverage && \
    pip3 install scipy && \
    pip3 install tqdm && \
    pip3 install joblib && \
    pip3 install zmq && \
    pip3 install dill && \
    pip3 install progressbar2 && \
    pip3 install mpi4py && \
    pip3 install cloudpickle && \
    pip3 install tensorflow==1.5.0 && \
    pip3 install click && \
    pip3 install opencv-python && \
    pip3 install numpy && \
    pip3 install pandas && \
    pip3 install pytest==3.5.1 && \
    pip3 install pytest-cov && \
    pip3 install matplotlib && \
    pip3 install seaborn && \
    pip3 install glob2 && \
    pip3 install gym[atari,classic_control]>=0.10.9

RUN \
    pip3 install PyQt5 && \
    pip3 install transitions


ENV PYTHONPATH $PYTHONPATH:$HOME/baselines

WORKDIR $HOME/wiseml

ENTRYPOINT ["./entrypoint.sh"]
CMD [""]
