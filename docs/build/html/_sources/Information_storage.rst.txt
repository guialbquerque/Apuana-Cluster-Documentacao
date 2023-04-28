
Armazenamnto
============


====================================================== =========== ====================================== =================== ====== ============
Path                                                   Performance Usage                                  Quota (Space/Files) Backup Auto-cleanup
====================================================== =========== ====================================== =================== ====== ============
``/network/datasets/``                                 High        * Curated raw datasets (read only)
``$HOME`` or ``/home/apuana/<u>/<username>/``            Low       * Personal user space                  100GB/1000K         Daily  no
                                                                   * Specific libraries, code, binaries
``$SCRATCH`` or ``/network/scratch/<u>/<username>/``   High        * Temporary job results                no                  no     90 days
                                                                   * Processed datasets
                                                                   * Optimized for small Files
``$SLURM_TMPDIR``                                      Highest     * High speed disk for temporary job    4TB/-               no     at job end
                                                                     results
``/network/projects/<groupname>/``                     Fair        * Shared space to facilitate           200GB/1000K         Daily  no
                                                                     collaboration between researchers
                                                                   * Long-term project storage
``$ARCHIVE`` or ``/network/archive/<u>/<username>/``   Low         * Long-term personal storage           500GB               no     no
====================================================== =========== ====================================== =================== ====== ============

.. note:: O sistema de arquivos ``$HOME`` é copiado uma vez por dia. Para solicitar a restauração de um arquivo,
faça uma solicitação ao `suporte de TI do Apuana` com o caminho do arquivo ou diretório a ser restaurado
e a data necessária.

$HOME
-----

As quotas estão habilitadas em ``$HOME`` tanto para capacidade de disco (blocos)
quanto para o número de arquivos (inodes). Os limites para blocos e inodes
são, respectivamente, 100GiB e 1 milhão por usuário. O comando para verificar
o uso da quota a partir de um nó de login é:

.. code-block:: console

   beegfs-ctl --cfgFile=/etc/beegfs/home.d/beegfs-client.conf --getquota --uid $USER

$SCRATCH
--------

``$SCRATCH`` pode ser usado para armazenar conjuntos de dados processados, conjuntos
de dados em andamento ou resultados temporários de trabalho. Seu tamanho de bloco
é otimizado para arquivos pequenos, o que minimiza o impacto no desempenho ao
trabalhar em conjuntos de dados extraídos.

.. note:: **Auto-limpeza**: este sistema de arquivos é limpo semanalmente,
    arquivos que não são usados há mais de 90 dias serão excluídos.

$SLURM_TMPDIR
-------------

``$SLURM_TMPDIR`` aponta para o disco local do nó em que um trabalho está sendo executado.
Ele deve ser usado para copiar os dados no nó no início do trabalho e gravar pontos
de verificação intermediários. Esta pasta é limpa após cada trabalho.

Projetos
--------

Os ``projetos`` podem ser usados para projetos colaborativos. Tem como objetivo
facilitar o compartilhamento de dados entre usuários que trabalham em um projeto
de longo prazo.

As cotas estão habilitadas em "projetos" tanto para a capacidade do disco (blocos)
quanto para o número de arquivos (inodes). Os limites para blocos e inodes são,
respectivamente, de 200 GiB e 1 milhão por usuário e por grupo.

$ARCHIVE
--------

O objetivo do ``$ARCHIVE`` é armazenar dados que não sejam de conjuntos de dados e 
que precisam ser mantidos a longo prazo (por exemplo, amostras geradas, logs,
dados relevantes para a submissão de artigos).

``$ARCHIVE`` está disponível apenas nos nós de login. Como esse sistema de arquivos
é ajustado para arquivos grandes, é recomendável arquivar seus diretórios.
Por exemplo, para arquivar os resultados de um experimento em ``$SCRATCH/my_experiment_results/``,
execute os comandos abaixo a partir de um nó de login:

.. code-block:: console

   cd $SCRATCH
   tar cJf $ARCHIVE/my_experiment_results.tar.xz --xattrs my_experiment_results

As cotas de capacidade de disco estão habilitadas no ``$ARCHIVE``. O limite
suave por usuário é de 500 GB e o limite rígido é de 550 GB. O período
de graça é de 7 dias, o que significa que pode-se usar mais de 500 GB
por 7 dias antes que o sistema de arquivos execute a cota. No entanto,
não é possível usar mais de 550 GB. O comando para verificar o uso da
cota a partir de um nó de login é `df``:

.. code-block:: console

   df -h $ARCHIVE

.. note:: **NÃO** HÁ backup deste sistema de arquivos.


