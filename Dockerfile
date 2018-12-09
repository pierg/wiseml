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
RUN python get-pip.py
RUN python3 get-pip.py
RUN rm get-pip.py


RUN mkdir -p $HOME
WORKDIR $HOME

# Cloning the repositories
RUN git clone https://github.com/pierg/wiseml.git
RUN git clone https://github.com/pierg/baselines.git
RUN cd wiseml


RUN pip3 install --upgrade pip

RUN \
    pip install --upgrade pip && \
    pip install codacy-coverage && \
    pip install scipy && \
    pip install tqdm && \
    pip install joblib && \
    pip install zmq && \
    pip install dill && \
    pip install progressbar2 && \
    pip install mpi4py && \
    pip install cloudpickle && \
    pip install tensorflow==1.5.0 && \
    pip install click && \
    pip install opencv-python && \
    pip install numpy && \
    pip install pandas && \
    pip install pytest==3.5.1 && \
    pip install pytest-cov && \
    pip install matplotlib && \
    pip install seaborn && \
    pip install glob2 && \
    pip install gym[atari,classic_control]>=0.10.9

RUN \
    pip install PyQt5 && \
    pip install transitions


ENV PYTHONPATH $PYTHONPATH:$HOME/baselines

WORKDIR $HOME/wiseml

ENTRYPOINT ["./entrypoint.sh"]
CMD [""]
