.. _python:

Virtual environments
--------------------

A virtual environment in Python is a local, isolated environment in which you
can install or uninstall Python packages without interfering with the global
environment (or other virtual environments). It usually lives in a directory
(location varies depending on whether you use venv, conda or poetry). In order
to use a virtual environment, you have to **activate** it. Activating an
environment essentially sets environment variables in your shell so that:

* ``python`` points to the right Python version for that environment (different
    virtual environments can use different versions of Python!)
* ``python`` looks for packages in the virtual environment
* ``pip install`` installs packages into the virtual environment
* Any shell commands installed via ``pip install`` are made available

To run experiments within a virtual environment, you can simply activate it
in the script given to ``sbatch``.


Pip/Virtualenv
^^^^^^^^^^^^^^

Pip is the preferred package manager for Python and each cluster provides
several Python versions through the associated module which comes with pip. In
order to install new packages, you will first have to create a personal space
for them to be stored.  The preferred solution (as it is the preferred solution
on Digital Research Alliance of Canada clusters) is to use `virtual
environments <https://virtualenv.pypa.io/en/stable/>`_.

First, load the Python module you want to use:

.. code-block:: console

    module load python/3.8

Then, create a virtual environment in your ``home`` directory:

.. code-block:: console

    python -m venv $HOME/<env>

Where ``<env>`` is the name of your environment. Finally, activate the environment:

.. code-block:: console

    source $HOME/<env>/bin/activate

You can now install any Python package you wish using the ``pip`` command, e.g.
`pytorch <https://pytorch.org/get-started/locally>`_:

.. code-block:: console

    pip install torch torchvision

Or `Tensorflow <https://www.tensorflow.org/install/gpu>`_:

.. code-block:: console

    pip install tensorflow-gpu


Conda
^^^^^

Another solution for Python is to use `miniconda
<https://docs.conda.io/en/latest/miniconda.html>`_ or `anaconda
<https://docs.anaconda.com>`_ which are also available through the ``module``
command: (the use of Conda is not recommended for Digital Research Alliance of
Canada clusters due to the availability of custom-built packages for pip)

.. code-block:: console

    $ module load miniconda/3
    [=== Module miniconda/3 loaded ===]
    To enable conda environment functions, first use:

To create an environment (see `here
<https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_
for details) using a specific Python version, you may write:

.. code-block:: console

    conda create -n <env> python=3.9

Where ``<env>`` is the name of your environment. You can now activate it by doing:

.. code-block:: console

    conda activate <env>

You are now ready to install any Python package you want in this environment.
For instance, to install PyTorch, you can find the Conda command of any version
you want on `pytorch's website <https://pytorch.org/get-started/locally>`_, e.g:

.. code-block:: console

    conda install pytorch torchvision cudatoolkit=10.0 -c pytorch

If you make a lot of environments and install/uninstall a lot of packages, it
can be good to periodically clean up Conda's cache:

.. code-block:: console

    conda clean --all