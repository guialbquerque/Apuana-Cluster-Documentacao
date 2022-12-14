Primeiros Passos
================

Conectando a Maquina de Acesso
------------------------------

O envio de tarefas para o cluster precisa ser feito a partir de uma maquina de acesso, a entrada na maquina de acesso é realizado através do SSH

**ssh <login>@slurm-client1.cin.ufpe.br**

Uma vez conectado na máquina de acesso é possível alocar e editar seus jobs a partir de comandos **slurm**. Primeiramente, você precisará preparar seu ambiente de 
trabalho no servidor que você utilizará. Jobs que utilizam máquinas virtuais (**Docker e afins**) não serão aprovados, pois abrem brechas de segurança. Qualquer 
biblioteca que necessite de instalação, por favor, nos contate e faremos a instalação o mais rápido possível. Para acessar o servidor que realizará o processamento, 
utilize o comando “**salloc**”, como no exemplo abaixo:

**salloc**

Nossos servidores já tem o gerenciador de pacotes **conda** para qualquer projeto que for realizado em Python. Os comandos de git também estão disponíveis e prontos 
para uso. Após a preparação do seu ambiente, volte para o nodo de login com o comando “**exit**” e rode o seu job com o comando **srun**. Exemplo:

**srun --gpus=N_GPUS --cpus-per-task=N_CPUS nvidia-smi**

Bibliotecas disponíveis
-----------------------
- Pytorch = 1.10.2 com Python = 3.9.15
- Tensorflow = 2.10.0 com Python  = 3.10.8

Exemplo com repositório do público do GitHub
--------------------------------------------

**Primeiro é necessário clonar o repositório. Obs.: o diretório home do usuário é sincronizado entre todas as máquinas.**

1. git clone https://github.com/username/repoName.git

Depois de clonar o repositório, é criado um script .sh. Uma das alternativas é utilizando nano:

.. code-block:: console

    nano test_slurm.sh

Em seguida, o usuário preenche o script com as diretivas do SBATCH que ele acha necessário e depois com os comandos que devem ser executados no node.

test_slurm.sh

.. code-block:: console

    #!/bin/sh
    #SBATCH -o slurm-%j.out  # Write the log here
    #SBATCH --gres=gpu:1    # Ask for 1 GPU
    #SBATCH --output=job_output.txt
    #SBATCH --error=job_error.txt

    . "/usr/local/anaconda3/etc/profile.d/conda.sh"
    conda create –-name myenv
    conda activate myenv
    conda install python=3.9
    conda install pytorch
    conda install pandas
    conda install matplotlib
    conda install seaborn
    conda install IPython
    python repoName/thisScript.py

Perceba a criação de um novo ambiente e em seguida sua ativação. Aqui foi realizado o dowgrade da versão do Python de 3.10 para 3.9. Isto foi feito porque 
ainda existem bugs da classe DataLoader do PyTorch ao utilizar o python 3.10. O conda é bastante versátil neste aspecto, pois pode-se escolher a versão do 
python e das dependencias mais adequadas para o funcionamento do seu código.

Um exemplo de script que faz uso de tensorflow é apresentado abaixo:

.. code-block:: console
    
    #!/bin/sh
    #SBATCH -o slurm-%j.out  # Write the log here
    #SBATCH --gres=gpu:1    # Ask for 1 GPU
    #SBATCH --output=job_output.txt
    #SBATCH --error=job_error.txt

    . "/usr/local/anaconda3/etc/profile.d/conda.sh"
    conda create -n myenv
    conda activate myenv
    conda install  tensorflow
    python repoName/thisScript.py

Para agendar o job faça:

.. code-block:: console

    sbatch test_slurm.sh

Para verificar a posição do job na fila faça:

.. code-block:: console

    squeue

Para cancelar o job faça:

.. code-block:: console

    scancel job_id

Exemplo com repositório privado do GitHub
-----------------------------------------

**Clonando um repositório privado**

1. Foto do perfil -> Settings -> Developer settings -> Personal access tokens -> Tokens (classic) -> Generate new token (classic) -> configurar da forma que desejar -> gerar token (salvar em um local seguro para reutilizar)

2. Copie o token e clone o repositório substituindo o nome do usuário e o token no comando


3. git clone https://username:token@github.com/username/repoName.git

Em seguida, basta repetir os outros passos do exemplo com repositório público do GitHub.