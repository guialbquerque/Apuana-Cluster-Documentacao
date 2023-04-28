Construindo os containers
-------------------------

Construir um container é como criar um novo ambiente, exceto que os containers são
muito mais poderosos, pois são sistemas autocontidos. Com o Singularity, existem 
duas maneiras de construir containers.

A primeira é fazê-lo você mesmo, é como quando você compra um novo laptop Linux e
não sabe muito bem o que precisa, se perceber que algo está faltando, você o instala.
Aqui, você pode obter um container vanilla com o Ubuntu chamado sandbox, você faz o 
login e instala cada pacote por si mesmo. Esse procedimento pode levar tempo, mas permitirá
que você entenda como as coisas funcionam e o que precisa ser feito. Isso é recomendado se
você precisa descobrir como as coisas serão compiladas ou se deseja instalar pacotes na hora
Nos referiremos a este procedimento como singularity sandboxes.

A segunda maneira é mais como se você soubesse o que quer, então você escreve uma lista de tudo o
que precisa, envia para o Singularity e ele instalará tudo para você. Essas listas são chamadas de
singularity recipes.


Primeira maneira: construir e usar um sandbox
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Você pode se perguntar: *Em qual máquina devo construir um container?*

Antes de tudo, você precisa escolher onde construirá o seu container. Essa
operação requer muita **memória e alto uso da CPU**.

.. warning:: NÃO construa containers em nenhum nó de login!

* (Recomendado para iniciantes) Se você precisar usar o apt-get, você deve construir
    o container em seu laptop com privilégios de superusuário. Você só precisará
    instalar o Singularity em seu laptop. Usuários de Windows/Mac podem ver `there`_
    e usuários de Ubuntu/Debian podem usar diretamente:

        .. _there: https://www.sylabs.io/guides/3.0/user-guide/installation.html#install-on-windows-or-mac

        .. code-block:: console

            sudo apt-get install singularity-container


Nesse caso, para evitar muita entrada/saída (I/O) na rede, você deve definir o cache do
Singularity localmente:

        .. code-block:: console

            export SINGULARITY_CACHEDIR=$SLURM_TMPDIR

* Se você **não pode instalar o Singularity** em seu laptop e **deseja usar o apt-get**,
    você pode usar o `singularity-hub`_ para construir seus containers e ler a seção
    Recipe_section_.

.. _singularity-hub: https://www.singularity-hub.org/


Baixando containers da web.
"""""""""""""""""""""""""""
Felizmente, você pode não precisar criar containers do zero, pois muitos já foram
construídos para os softwares de deep learning mais comuns. Você pode encontrá-los
na maioria em `dockerhub`_.

.. _dockerhub: https://hub.docker.com/


Acesse `dockerhub`_ e selecione o container que você deseja baixar

.. _dockerhub: https://hub.docker.com/

Por exemplo, se você deseja obter a última versão do PyTorch com suporte para GPU
(Substitua *runtime* por *devel* se precisar do conjunto completo de ferramentas do Cuda):

.. code-block:: console

    singularity pull docker://pytorch/pytorch:1.0.1-cuda10.0-cudnn7-runtime

Ou a última versão do TensorFlow:

.. code-block:: console

    singularity pull docker://tensorflow/tensorflow:latest-gpu-py3

Atualmente, a imagem baixada ``pytorch.simg`` ou ``tensorflow.simg`` é somente leitura,
o que significa que você não poderá instalar nada nela. A partir de agora, o PyTorch
será usado como exemplo. Se você estiver usando o TensorFlow, simplesmente substitua
todas as ocorrências de **pytorch** por **tensorflow**.

Como adicionar ou instalar coisas em um container
"""""""""""""""""""""""""""""""""""""""""""""""""

O primeiro passo é transformar o seu container somente leitura
``pytorch-1.0.1-cuda10.0-cudnn7-runtime.simg`` em uma versão gravável que
permitirá que você adicione pacotes.

.. warning:: Dependendo da versão do singularity que você está usando, o singularity criará um container
    com a extensão .simg ou .sif. Se você estiver usando arquivos .sif, substitua todas as ocorrências
    de .simg por .sif.

.. tip:: Se você quiser usar o apt-get, deve colocar sudo antes dos comandos a seguir

Este comando criará uma imagem gravável na pasta ``pytorch``.


.. code-block:: console

    singularity build --sandbox pytorch pytorch-1.0.1-cuda10.0-cudnn7-runtime.simg

Então você precisará do seguinte comando para fazer login dentro do container.

.. code-block:: console

    singularity shell --writable -H $HOME:/home pytorch


Assim que você entrar no container, pode usar o pip e instalar tudo o que precisar
(ou usar ``apt-get`` se você construiu o container com sudo).

.. warning:: O Singularity monta sua pasta pessoal, então se você instalar coisas no
    diretório ``$HOME`` do seu container, elas serão instaladas no seu ``$HOME`` real!


Você deve instalar seus pacotes em /usr/local.
 

Criando diretórios úteis
""""""""""""""""""""""""

Um dos benefícios dos containers é que você poderá usá-los em diferentes clusters.
No entanto, para cada cluster, a localização das pastas de datasets e experimentos
pode ser diferente. Para ser invariante em relação a essas localizações, criaremos
alguns pontos de montagem úteis dentro do container:

.. code-block:: console

    mkdir /dataset
    mkdir /tmp_log
    mkdir /final_log

A partir de agora, você não precisará mais se preocupar em especificar onde buscar
seu conjunto de dados ao escrever seu código. Seu conjunto de dados estará sempre
em ``/dataset``, independentemente do cluster que você estiver usando.

Testes
""""""

Se você tem algum código que deseja testar antes de finalizar o seu contêiner, 
você tem duas opções. Você pode entrar no seu contêiner e executar o código
Python dentro dele com:

.. code-block:: console

    singularity shell --nv pytorch

Ou você pode executar seu comando diretamente com:

.. code-block:: console

    singularity exec --nv pytorch Python YOUR_CODE.py

.. tip:: ---nv permite que o container use GPUs. Você não precisa disso se não planeja usar uma GPU.

.. warning:: Não se esqueça de limpar o cache dos pacotes que você instalou nos containers.


Criando uma nova imagem a partir do sandbox
"""""""""""""""""""""""""""""""""""""""""""

Depois que tudo o que você precisa estiver instalado dentro do contêiner,
você precisa convertê-lo de volta em uma imagem singularity somente leitura com:

.. code-block:: console

    singularity build pytorch_final.simg pytorch

.. _Recipe_section:

Segunda opção: Use receitas
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Uma receita do Singularity é um arquivo que inclui especificações sobre a instalação
de software, variáveis de ambiente, arquivos a serem adicionados e metadados do contêiner.
É um ponto de partida para projetar qualquer contêiner personalizado. Em vez de baixar um
contêiner e instalar seus pacotes manualmente, você pode especificar neste arquivo os pacotes
que deseja e, em seguida, construir seu contêiner a partir deste arquivo.

Aqui está um exemplo simples de uma receita do Singularity que instala alguns pacotes:

.. code-block:: console

    ################# Header: Define the base system you want to use ################
    # Reference of the kind of base you want to use (e.g., docker, debootstrap, shub).
    Bootstrap: docker
    # Select the docker image you want to use (Here we choose tensorflow)
    From: tensorflow/tensorflow:latest-gpu-py3

    ################# Section: Defining the system #################################
    # Commands in the %post section are executed within the container.
    %post
            echo "Installing Tools with apt-get"
            apt-get update
            apt-get install -y cmake libcupti-dev libyaml-dev wget unzip
            apt-get clean
            echo "Installing things with pip"
            pip install tqdm
            echo "Creating mount points"
            mkdir /dataset
            mkdir /tmp_log
            mkdir /final_log


    # Environment variables that should be sourced at runtime.
    %environment
            # use bash as default shell
            SHELL=/bin/bash
            export SHELL

Um arquivo de receita contém duas partes: o "cabeçalho" (header) e "seções" (sections).
No "cabeçalho", você especifica qual sistema base deseja usar, pode ser qualquer contêiner
do Docker ou do Singularity. Em "seções", você pode listar as coisas que deseja instalar 
na subseção "post" ou listar as variáveis de ambiente que precisa carregar em cada execução
na subseção "environment". Para uma descrição mais detalhada, consulte `singularity documentation`_.

.. _singularity documentation: https://www.sylabs.io/guides/2.6/user-guide/container_recipes.html#container-recipes

Para construir um container singularity a partir de um arquivo de receita, você deve usar:

.. code-block:: console

    sudo singularity build <NAME_CONTAINER> <YOUR_RECIPE_FILES>

.. warning:: Você sempre precisa usar o sudo ao construir um contêiner a partir de uma receita.
    Como não há acesso ao sudo no cluster, é necessário um computador pessoal ou o uso do singularity
    hub para construir um contêiner.


Construir receita no Singularity Hub
"""""""""""""""""""""""""""""""""""""

O Singularity Hub permite que os usuários criem contêineres a partir de receitas
diretamente na nuvem do Singularity Hub, o que significa que você não precisa criar
contêineres sozinho. Você precisa se registrar no `singularity-hub`_ e vincular sua conta
do Singularity Hub à sua conta do GitHub, e então:

.. _singularity-hub: https://www.singularity-hub.org/

    #. Crie um novo repositório no Github.
    #. Adicione uma coleção no `singularity-hub`_ e selecione o repositório do Github que você criou.
    #. Clone o repositório do Github em seu computador.
 
    ::

        $ git clone <url>

   #. Write the singularity recipe and save it as a file named **Singularity**.
   #. Git add **Singularity**, commit and push on the master branch

    ::

        $ git add Singularity
        $ git commit
        $ git push origin master

Neste ponto, os robôs do singularity-hub irão construir o contêiner para você,
e você poderá baixá-lo do site ou diretamente usando:

.. code-block:: console

    singularity pull shub://<github_username>/<repository_name>


Exemplo: Receita com OpenAI gym, MuJoCo e Miniworld
"""""""""""""""""""""""""""""""""""""""""""""""""""

Aqui está um exemplo de como você pode usar uma receita do Singularity
para instalar um ambiente complexo como o OpenAI gym, MuJoCo e Miniworld
em um contêiner baseado em PyTorch. 

.. code-block:: console

    #This is a dockerfile that sets up a full Gym install with test dependencies
    Bootstrap: docker

    # Here we ll build our container upon the pytorch container
    From: pytorch/pytorch:1.0-cuda10.0-cudnn7-runtime

    # Now we'll copy the mjkey file located in the current directory inside the container's root
    # directory
    %files
            mjkey.txt

    # Then we put everything we need to install
    %post
            export PATH=$PATH:/opt/conda/bin
            apt -y update && \
            apt install -y keyboard-configuration && \
            apt install -y \
            python3-dev \
            python-pyglet \
            python3-opengl \
            libhdf5-dev \
            libjpeg-dev \
            libboost-all-dev \
            libsdl2-dev \
            libosmesa6-dev \
            patchelf \
            ffmpeg \
            xvfb \
            libhdf5-dev \
            openjdk-8-jdk \
            wget \
            git \
            unzip && \
            apt clean && \
            rm -rf /var/lib/apt/lists/*
            pip install h5py

            # Download Gym and MuJoCo
            mkdir /Gym && cd /Gym
            git clone https://github.com/openai/gym.git || true && \
            mkdir /Gym/.mujoco && cd /Gym/.mujoco
            wget https://www.roboti.us/download/mjpro150_linux.zip  && \
            unzip mjpro150_linux.zip && \
            wget https://www.roboti.us/download/mujoco200_linux.zip && \
            unzip mujoco200_linux.zip && \
            mv mujoco200_linux mujoco200

            # Export global environment variables
            export MUJOCO_PY_MJKEY_PATH=/Gym/.mujoco/mjkey.txt
            export MUJOCO_PY_MUJOCO_PATH=/Gym/.mujoco/mujoco150/
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/Gym/.mujoco/mjpro150/bin
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/Gym/.mujoco/mujoco200/bin
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/bin
            cp /mjkey.txt /Gym/.mujoco/mjkey.txt
            # Install Python dependencies
            wget https://raw.githubusercontent.com/openai/mujoco-py/master/requirements.txt
            pip install -r requirements.txt
            # Install Gym and MuJoCo
            cd /Gym/gym
            pip install -e '.[all]'
            # Change permission to use mujoco_py as non sudoer user
            chmod -R 777 /opt/conda/lib/python3.6/site-packages/mujoco_py/
            pip install --upgrade minerl

    # Export global environment variables
    %environment
            export SHELL=/bin/sh
            export MUJOCO_PY_MJKEY_PATH=/Gym/.mujoco/mjkey.txt
            export MUJOCO_PY_MUJOCO_PATH=/Gym/.mujoco/mujoco150/
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/Gym/.mujoco/mjpro150/bin
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/Gym/.mujoco/mujoco200/bin
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/bin
            export PATH=/Gym/gym/.tox/py3/bin:$PATH

    %runscript
            exec /bin/sh "$@"


Here is the same recipe but written for TensorFlow:

.. code-block:: console

    #This is a dockerfile that sets up a full Gym install with test dependencies
    Bootstrap: docker

    # Here we ll build our container upon the tensorflow container
    From: tensorflow/tensorflow:latest-gpu-py3

    # Now we'll copy the mjkey file located in the current directory inside the container's root
    # directory
    %files
            mjkey.txt

    # Then we put everything we need to install
    %post
            apt -y update && \
            apt install -y keyboard-configuration && \
            apt install -y \
            python3-setuptools \
            python3-dev \
            python-pyglet \
            python3-opengl \
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

            # Download Gym and MuJoCo
            mkdir /Gym && cd /Gym
            git clone https://github.com/openai/gym.git || true && \
            mkdir /Gym/.mujoco && cd /Gym/.mujoco
            wget https://www.roboti.us/download/mjpro150_linux.zip  && \
            unzip mjpro150_linux.zip && \
            wget https://www.roboti.us/download/mujoco200_linux.zip && \
            unzip mujoco200_linux.zip && \
            mv mujoco200_linux mujoco200

            # Export global environment variables
            export MUJOCO_PY_MJKEY_PATH=/Gym/.mujoco/mjkey.txt
            export MUJOCO_PY_MUJOCO_PATH=/Gym/.mujoco/mujoco150/
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/Gym/.mujoco/mjpro150/bin
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/Gym/.mujoco/mujoco200/bin
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/bin
            cp /mjkey.txt /Gym/.mujoco/mjkey.txt

            # Install Python dependencies
            wget https://raw.githubusercontent.com/openai/mujoco-py/master/requirements.txt
            pip install -r requirements.txt
            # Install Gym and MuJoCo
            cd /Gym/gym
            pip install -e '.[all]'
            # Change permission to use mujoco_py as non sudoer user
            chmod -R 777 /usr/local/lib/python3.5/dist-packages/mujoco_py/

            # Then install miniworld
            cd /usr/local/
            git clone https://github.com/maximecb/gym-miniworld.git
            cd gym-miniworld
            pip install -e .

    # Export global environment variables
    %environment
            export SHELL=/bin/bash
            export MUJOCO_PY_MJKEY_PATH=/Gym/.mujoco/mjkey.txt
            export MUJOCO_PY_MUJOCO_PATH=/Gym/.mujoco/mujoco150/
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/Gym/.mujoco/mjpro150/bin
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/Gym/.mujoco/mujoco200/bin
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/bin
            export PATH=/Gym/gym/.tox/py3/bin:$PATH

    %runscript
            exec /bin/bash "$@"
