FROM ubuntu:18.04

# Install keyboard-configuration separately to avoid travis hanging waiting for keyboard selection
RUN \
    apt -y update && \
    apt install -y keyboard-configuration && \

    apt install -y \ 
        python3-pip \
        python3-dev \
        python-pyglet \
        python3-opengl \
        python3-setuptools \
        libjpeg-dev \
        libboost-all-dev \
        libsdl2-dev \
        libosmesa6-dev \
        patchelf \
        ffmpeg \
        xvfb \
        wget \
        git \
        unzip && \

    apt clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /home

# Cloning the repositories
RUN git clone https://github.com/pierg/wiseml.git
RUN git clone https://github.com/pierg/baselines.git
RUN git clone https://github.com/pierg/gym-minigrid.git
RUN git clone https://github.com/pierg/pytorch-a2c-ppo.git

RUN python3 -m pip install --user --upgrade pip==9.0.3

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
    pip3 install imageio && \
    pip3 install gym[atari,classic_control]>=0.10.9 && \
    pip3 install tensorboardX && \
    pip3 install transitions


# Installing pytorch
RUN pip3 install https://download.pytorch.org/whl/cpu/torch-1.0.0-cp36-cp36m-linux_x86_64.whl
RUN pip3 install torchvision


WORKDIR /home/wiseml

ENV PYTHONPATH "${PYTHONPATH}:/home/wiseml:/home/baselines:/home/pytorch-a2c-ppo:/home/pytorch-a2c-ppo/torch_rl:/home/gym-minigrid/:/home/gym-minigrid/gym_minigrid:/home/gym-minigrid/gym_minigrid/envs"

ENTRYPOINT ["./entrypoint.sh"]
CMD [""]