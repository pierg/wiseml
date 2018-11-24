FROM ubuntu:16.04

RUN apt-get -y update && apt-get -y install git wget python-dev python3-dev libopenmpi-dev zlib1g-dev cmake libglib2.0-0 libsm6 libxext6 libfontconfig1 libxrender1 git
ENV CODE_DIR /root/code
ENV VENV /root/venv


RUN apt-get remove python-pip python3-pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN python3 get-pip.py

RUN \
    pip install virtualenv && \
    virtualenv $VENV --python=python3 && \
    . $VENV/bin/activate && \
    mkdir $CODE_DIR && \
    cd $CODE_DIR && \
    git clone https://github.com/pierg/wiseml.git && \
    git clone https://github.com/pierg/baselines.git && \
    cd wiseml && \
    pip install -r requirements.txt && \
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

ENV PATH=$VENV/bin:$PATH
ENV PYTHONPATH $PYTHONPATH:$CODE_DIR/baselines

WORKDIR $HOME/wiseml

#ENTRYPOINT ["./entrypoint.sh"]
#CMD [""]
