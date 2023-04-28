.. _Using containers:

Usando Conteiners no cluster
----------------------------


Como usar conteiners no cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Em todo cluster com Slurm, os conjuntos de dados e resultados intermediários
devem ser armazenados em ``$SLURM_TMPDIR``, enquanto os resultados finais do
experimento devem ser salvos em ``$SCRATCH``. Para usar o contêiner que você criou,
é necessário copiá-lo para o cluster que deseja usar.

.. warning:: Você sempre deve armazenar o seu contêiner em $SCRATCH!

Em seguida, reserve um nó com srun/sbatch, copie o contêiner e o seu conjunto de
dados para o nó fornecido pelo SLURM (ou seja, em ``$SLURM_TMPDIR``) e execute o
código ``<YOUR_CODE>`` dentro do contêiner ``<YOUR_CONTAINER>`` com:

.. code-block:: console

    singularity exec --nv -H $HOME:/home -B $SLURM_TMPDIR:/dataset/ -B $SLURM_TMPDIR:/tmp_log/ -B $SCRATCH:/final_log/ $SLURM_TMPDIR/<YOUR_CONTAINER> python <YOUR_CODE>


Remember that ``/dataset``, ``/tmp_log`` and ``/final_log`` were created in the
previous section. Now each time, we'll use singularity, we are explicitly
telling it to mount ``$SLURM_TMPDIR`` on the cluster's node in the folder
``/dataset`` inside the container with the option ``-B`` such that each dataset
downloaded by PyTorch in ``/dataset`` will be available in ``$SLURM_TMPDIR``.

This will allow us to have code and scripts that are invariant to the cluster
environment. The option ``-H`` specify what will be the container's home. For
example, if you have your code in ``$HOME/Project12345/Version35/`` you can
specify ``-H $HOME/Project12345/Version35:/home``, thus the container will only
have access to the code inside ``Version35``.

If you want to run multiple commands inside the container you can use:

Lembre-se de que ``/dataset``, ``/tmp_log`` e ``/final_log`` foram criados na seção anterior. 
Agora, cada vez que usarmos o singularity, estamos explicitamente dizendo a ele
para montar ``$SLURM_TMPDIR`` no nó do cluster na pasta ``/dataset`` dentro do container
com a opção ``-B``, de modo que cada conjunto de dados baixado pelo PyTorch em ``/dataset``
estará disponível em ``$SLURM_TMPDIR``.

Isso nos permitirá ter código e scripts que são invariantes ao ambiente do cluster.
A opção ``-H`` especifica qual será o diretório raiz do container. Por exemplo, se você
tem seu código em ``$HOME/Projeto12345/Versao35/``, você pode especificar
``-H $HOME/Projeto12345/Versao35:/home``, assim o container terá acesso apenas ao código dentro de ``Versao35``.

Se você quiser executar vários comandos dentro do container, pode usar:

.. code-block:: console

    singularity exec --nv -H $HOME:/home -B $SLURM_TMPDIR:/dataset/ \
        -B $SLURM_TMPDIR:/tmp_log/ -B $SCRATCH:/final_log/ \
        $SLURM_TMPDIR/<YOUR_CONTAINER> bash -c 'pwd && ls && python <YOUR_CODE>'


Exemplo: Caso interativo (srun/salloc)
""""""""""""""""""""""""""""""""""""""

Depois de obter uma sessão interativa com o SLURM, copie ``<YOUR_CONTAINER>`` e
``<YOUR_DATASET>`` para ``$SLURM_TMPDIR``.

.. code-block:: console

    # 0. Get an interactive session
    $ srun --gres=gpu:1
    # 1. Copy your container on the compute node
    $ rsync -avz $SCRATCH/<YOUR_CONTAINER> $SLURM_TMPDIR
    # 2. Copy your dataset on the compute node
    $ rsync -avz $SCRATCH/<YOUR_DATASET> $SLURM_TMPDIR

Então, use o comando ``singularity shell`` para obter um shell dentro do contêiner.

.. code-block:: console

    # 3. Get a shell in your environment
    $ singularity shell --nv \
            -H $HOME:/home \
            -B $SLURM_TMPDIR:/dataset/ \
            -B $SLURM_TMPDIR:/tmp_log/ \
            -B $SCRATCH:/final_log/ \
            $SLURM_TMPDIR/<YOUR_CONTAINER>

.. code-block:: console

    # 4. Execute your code
    <Singularity_container>$ python <YOUR_CODE>

**or** use ``singularity exec`` to execute ``<YOUR_CODE>``.

.. code-block:: console

    # 3. Execute your code
    $ singularity exec --nv \
            -H $HOME:/home \
            -B $SLURM_TMPDIR:/dataset/ \
            -B $SLURM_TMPDIR:/tmp_log/ \
            -B $SCRATCH:/final_log/ \
            $SLURM_TMPDIR/<YOUR_CONTAINER> \
            python <YOUR_CODE>

Você também pode criar o seguinte alias para facilitar sua vida:

.. code-block:: console

    alias my_env='singularity exec --nv \
            -H $HOME:/home \
            -B $SLURM_TMPDIR:/dataset/ \
            -B $SLURM_TMPDIR:/tmp_log/ \
            -B $SCRATCH:/final_log/ \
            $SLURM_TMPDIR/<YOUR_CONTAINER>'

Isso permitirá que você execute qualquer código com:

.. code-block:: console

    my_env python <YOUR_CODE>


Exemplo: caso sbatch
""""""""""""""""""""

Você também pode criar um script ``sbatch``:

.. code-block:: console

    #!/bin/bash
    #SBATCH --cpus-per-task=6         # Ask for 6 CPUs
    #SBATCH --gres=gpu:1              # Ask for 1 GPU
    #SBATCH --mem=10G                 # Ask for 10 GB of RAM
    #SBATCH --time=0:10:00            # The job will run for 10 minutes

    # 1. Copy your container on the compute node
    rsync -avz $SCRATCH/<YOUR_CONTAINER> $SLURM_TMPDIR
    # 2. Copy your dataset on the compute node
    rsync -avz $SCRATCH/<YOUR_DATASET> $SLURM_TMPDIR
    # 3. Executing your code with singularity
    singularity exec --nv \
            -H $HOME:/home \
            -B $SLURM_TMPDIR:/dataset/ \
            -B $SLURM_TMPDIR:/tmp_log/ \
            -B $SCRATCH:/final_log/ \
            $SLURM_TMPDIR/<YOUR_CONTAINER> \
            python "<YOUR_CODE>"
    # 4. Copy whatever you want to save on $SCRATCH
    rsync -avz $SLURM_TMPDIR/<to_save> $SCRATCH


Problema com as bibliotecas PyBullet e OpenGL
""""""""""""""""""""""""""""""""""""""""""""

Se você estiver executando certos ambientes do gym que requerem o ``pyglet``,
você pode encontrar um problema ao executar sua instância do singularity
com os drivers Nvidia usando a flag ``--nv``. Isso acontece porque a flag ``--nv``
também fornece as bibliotecas do OpenGL:

.. code-block:: console

    libGL.so.1 => /.singularity.d/libs/libGL.so.1
    libGLX.so.0 => /.singularity.d/libs/libGLX.so.0

Se você não está tendo esses problemas com ``pyglet``, provavelmente não precisa se
preocupar com isso. Caso contrário, você pode resolver esses problemas com ``apt-get install -y 
libosmesa6-dev mesa-utils mesa-utils-extra libgl1-mesa-glx`` e, em seguida, certificar-se de que
seu ``LD_LIBRARY_PATH`` aponte para essas bibliotecas antes das que estão em ``/ .singularity.d / libs``.

.. code-block:: console

    %environment
            # ...
            export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/mesa:$LD_LIBRARY_PATH


Apuana cluster
""""""""""""""

No cluster Apuana, ``$SCRATCH`` ainda não está definido, você deve adicionar os
resultados do experimento que deseja manter em ``/network/scratch/<u>/<username>/``.
Para usar o script sbatch acima e para corresponder a outros nomes de ambiente de
cluster, você pode definir ``$SCRATCH`` como um alias para ``/network/scratch/<u>/<username>`` com:

.. code-block:: console

    echo "export SCRATCH=/network/scratch/${USER:0:1}/$USER" >> ~/.bashrc

Então, você pode seguir o procedimento geral explicado acima.
