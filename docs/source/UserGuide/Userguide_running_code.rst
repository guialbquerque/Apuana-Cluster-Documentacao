Executando o seu código
=======================

Guia de comandos SLURM
----------------------

Uso básico
^^^^^^^^^^

A documentação do SLURM `<https://slurm.schedmd.com/documentation.html>`_
fornece informações extensas sobre os comandos disponíveis para consultar o 
status do cluster ou enviar trabalhos.

A seguir, são apresentados alguns exemplos básicos de como usar o SLURM.

Enviando trabalhos
^^^^^^^^^^^^^^^^^^

Trabalho em lote
"""""""""""""""

Para enviar um trabalho em lote, você precisa criar um script contendo o(s) comando(s) principal(is)
que deseja executar nos recursos/nós alocados.

.. code-block:: console

    #!/bin/bash
    #SBATCH --job-name=test
    #SBATCH --output=job_output.txt
    #SBATCH --error=job_error.txt
    #SBATCH --ntasks=1
    #SBATCH --time=10:00
    #SBATCH --mem=100Gb

    module load python/3.5
    python my_script.py


Seu script de trabalho é então enviado para o SLURM com ``sbatch`` (`ref.
<https://slurm.schedmd.com/sbatch.html>`__)

.. code-block:: console

    $ sbatch job_script
    sbatch: Submitted batch job 4323674

O diretório de trabalho do trabalho será aquele onde você executou o comando ``sbatch``.


.. tip::
    As diretivas do Slurm podem ser especificadas na linha de comando juntamente 
    com ``sbatch`` ou dentro do script de trabalho com uma linha iniciada por ``#SBATCH``.


Job interativo
"""""""""""""""

Os gerenciadores de carga geralmente executam trabalhos em lote para evitar ter que monitorar
sua progressão e deixar o agendador executá-lo assim que os recursos estiverem disponíveis.
Se você quiser acessar um shell enquanto utiliza recursos do cluster, pode enviar um trabalho
interativo onde o executável principal é um shell com o comando ``srun/salloc``.
 (`srun <https://slurm.schedmd.com/srun.html>`_/`salloc <https://slurm.schedmd.com/salloc.html>`_) comandos:

.. code-block:: console

    salloc

Iniciar um trabalho interativo no primeiro nó disponível com os recursos padrão 
definidos no SLURM (1 tarefa/1 CPU). O comando  ``srun`` aceita os mesmos argumentos
que ``sbatch``, com exceção do ambiente que não é passado.

.. tip::

    Para passar seu ambiente atual para um trabalho interativo, adicione  ``--preserve-env`` ao ``srun``.

``salloc`` também pode ser usado e é principalmente um invólucro em torno de ``srun`` se 
fornecido sem mais informações, mas fornece mais flexibilidade se, por exemplo, 
você quiser obter uma alocação em vários nós.


Argumentos de submissão de tarefas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Para selecionar com precisão os recursos para sua tarefa, vários argumentos estão disponíveis. Os mais importantes são:

=========================== ============================================================================

Argumento                   Descrição
=========================== ============================================================================
-n, --ntasks=<number>       O número de tarefas no seu script, geralmente é 1.
-c, --cpus-per-task=<ncpus> O número de núcleos para cada tarefa.
-t, --time=<time>           Tempo solicitado para o seu trabalho.
--mem=<size[units]>         Memória solicitada para todas as tarefas do seu trabalho.
--gres=<list>               Selecione recursos genéricos, como GPUs, para o seu trabalho: ``--gres=gpu:GPU_MODEL``
=========================== ============================================================================

.. tip::
    Sempre considere solicitar a quantidade adequada de recursos para melhorar o 
    agendamento do seu trabalho (trabalhos pequenos sempre são executados primeiro).


verificando job status
^^^^^^^^^^^^^^^^^^^^^^

Para exibir os *jobs* atualmente na fila, use ``squeue`` e para obter apenas seus trabalhos digite squeue -u $USER

.. code-block:: console

    $ squeue -u $USER
    JOBID   USER          NAME    ST  START_TIME         TIME NODES CPUS TRES_PER_NMIN_MEM NODELIST (REASON) COMMENT
    133     my_username   myjob   R   2019-03-28T18:33   0:50     1    2        N/A  7000M node1 (None) (null)

.. note::
    
    O número máximo de trabalhos que podem ser enviados ao sistema por usuário é 1000 (MaxSubmitJobs=1000)
    em qualquer momento da associação dada. Se este limite for atingido, novas solicitações de envio serão
    negadas até que os trabalhos existentes nesta associação sejam concluídos.


Removendo um job
^^^^^^^^^^^^^^^^

Para cancelar o seu trabalho, simplesmente use ``scancel``.

.. code-block:: console

    scancel 4323674



Particionamento
---------------

Como não temos muitas GPUs no cluster, os recursos devem ser compartilhados de forma justa.
A opção ``--partition=/-p`` do SLURM permite que você defina a prioridade necessária para um trabalho. 
Cada trabalho atribuído com uma prioridade pode interromper trabalhos com prioridade mais baixa:
``unkillable > main > long``. Uma vez interrompido, seu trabalho é morto sem aviso prévio e é automaticamente
reenfileirado na mesma partição até que os recursos estejam disponíveis. (Para aproveitar um mecanismo de
interrupção diferente, consulte a documentação do SLURM).
:ref:`Handling preemption <advanced_preemption>`)

============================= ========================== ============ ====================
Flag                          Max Resource Usage         Max Time     Note
============================= ========================== ============ ====================
\--partition=unkillable       6  CPUs, mem=32G,  1 GPU   2 days
\--partition=unkillable-cpu   2  CPUs, mem=16G           2 days       CPU-only jobs
\--partition=short-unkillable 24 CPUs, mem=128G, 4 GPUs  3 hours (!)  Large but short jobs
\--partition=main             8  CPUs, mem=48G,  2 GPUs  5 days
\--partition=main-cpu         8  CPUs, mem=64G           5 days       CPU-only jobs
\--partition=long             no limit of resources      7 days
\--partition=long-cpu         no limit of resources      7 days       CPU-only jobs
============================= ========================== ============ ====================

.. warning::

    Historicamente, antes da introdução em 2022 de nós exclusivos para CPU 
    (por exemplo, a série "cn-f"), trabalhos apenas com CPU eram executados lado
    a lado com trabalhos com GPU em nós de GPU. Para evitar que esses trabalhos 
    obstruíssem qualquer trabalho com GPU, eles sempre tinham a menor prioridade 
    e eram preemptíveis. Isso foi implementado automaticamente atribuindo-os a uma
    das partições agora obsoletas ``cpu_jobs``, ``cpu_jobs_low`` ou ``cpu_jobs_low-grace``.
    Não use mais esses nomes de partição. Prefira os nomes de partição ``*-cpu`` definidos acima.

    Para fins de compatibilidade com versões anteriores, os nomes das partições legadas são traduzidos 
    para seu equivalente efetivo ``long-cpu``, mas eventualmente serão removidos completamente.

.. note ::
    Como conveniência, se você solicitar a partição ``unkillable``, ``main`` ou ``long`` para um trabalho
    apenas com CPU, a partição será traduzida automaticamente para seu equivalente ``-cpu``.
