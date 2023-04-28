.. _python:

Ambientes virtuais
------------------

Um ambiente virtual em Python é um ambiente local e isolado no qual você pode instalar
ou desinstalar pacotes do Python sem interferir no ambiente global (ou em outros ambientes virtuais).
Ele geralmente fica em um diretório (a localização varia dependendo se você usa venv, conda ou poetry).
Para usar um ambiente virtual, você precisa ativá-lo. Ativar um ambiente define essencialmente variáveis
de ambiente em seu shell para que:

* ``python`` aponta para a versão correta do Python para aquele ambiente (diferentes ambientes virtuais podem usar
 diferentes versões do Python!)
* ``python`` procura pacotes no ambiente virtual
* ``pip install`` instala pacotes no ambiente virtual
* Quaisquer comandos de shell instalados via ``pip install`` estão disponíveis

Para executar experimentos dentro de um ambiente virtual, você pode simplesmente ativá-lo no script fornecido para ``sbatch``.


Pip/Virtualenv
^^^^^^^^^^^^^^

O Pip é o gerenciador de pacotes preferido para Python e cada cluster fornece
diversas versões do Python por meio do módulo associado, que vem com o pip.
Para instalar novos pacotes, você primeiro precisará criar um espaço pessoal 
para que eles possam ser armazenados. A solução preferida (assim como é nos 
clusters da Digital Research Alliance do Canadá) é usar ambientes virtuais.
 `<https://virtualenv.pypa.io/en/stable/>`_.

Primeiro, carregue o módulo Python que você deseja usar:
.. code-block:: console

    module load python/3.8

Então, crie um ambiente virtual no seu diretório ``home``:

.. code-block:: console

    python -m venv $HOME/<env>

onde ``<env>`` é o nome do seu ambiente. Finalmente, ative o ambiente:

.. code-block:: console

    source $HOME/<env>/bin/activate

Agora você pode instalar qualquer pacote Python que desejar usando o comando ``pip``, por exemplo:
`pytorch <https://pytorch.org/get-started/locally>`_:

.. code-block:: console

    pip install torch torchvision

Or `Tensorflow <https://www.tensorflow.org/install/gpu>`_:

.. code-block:: console

    pip install tensorflow-gpu


Conda
^^^^^


Outra solução para Python é usar o miniconda.
`<https://docs.conda.io/en/latest/miniconda.html>`_ ou anaconda
`<https://docs.anaconda.com>`_ 