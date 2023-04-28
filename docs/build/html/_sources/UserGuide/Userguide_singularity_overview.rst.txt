Visão Geral
-----------

O que é singularidade
^^^^^^^^^^^^^^^^^^^^^

Executar o Docker no SLURM é um problema de segurança (por exemplo, executando como root,
tendo a capacidade de montar qualquer diretório). A alternativa é usar o Singularity,
que é uma solução popular no mundo de HPC.

Existe um bom nível de compatibilidade entre Docker e Singularity, e podemos encontrar
muitas alegações exageradas sobre a capacidade de converter contêineres do Docker para
Singularity sem qualquer atrito. Muitas vezes, imagens do DockerHub são 100% compatíveis
com o Singularity e podem ser usadas sem atrito, mas as coisas ficam complicadas quando
tentamos converter nossos próprios arquivos de construção do Docker em receitas do Singularity.

Links para documentação oficial
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* official `Singularity user guide <https://singularity-docs.readthedocs.io/en/latest/>`_ 

* official `Singularity admin guide <https://sylabs.io/guides/latest/admin-guide/>`_

Visão gerald dos passos usados na prática
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Na maioria das vezes, o processo para criar e usar um contêiner Singularity é:

* No seu computador Linux (em casa ou no trabalho)

  * selecione uma imagem Docker do DockerHub (por exemplo, *pytorch/pytorch*)
  * crie um arquivo de receita para o Singularity que comece com essa imagem do DockerHub
  * construa o arquivo de receita, criando assim o arquivo de imagem (por exemplo, ``my-pytorch-image.sif``)
  * teste seu contêiner Singularity antes de enviá-lo para o cluster
  * ``rsync -av my-pytorch-image.sif <login-node>:Documents/my-singularity-images``

* No nó de login desse cluster

  * enfileire seus trabalhos com ``sbatch ...``
  * (observe que seus trabalhos copiarão o arquivo ``my-pytorch-image.sif`` para $SLURM_TMPDIR e então iniciarão o Singularity com essa imagem)
    faça outra coisa enquanto espera que eles terminem
  * enfileire mais trabalhos com o mesmo ``my-pytorch-image.sif``, reutilizando-o várias vezes

Nas próximas seções, você encontrará exemplos específicos ou dicas para realizar na prática as etapas destacadas acima.

Não, não no MacOS
^^^^^^^^^^^^^^^^^

Singularity não funciona no MacOS, até a data desta escrita em 2021.
Docker realmente não roda no MacOS, mas o Docker instala silenciosamente uma
máquina virtual executando Linux, o que torna a experiência agradável,
e o usuário não precisa se preocupar com os detalhes de como o Docker faz isso.

Dado sua origem em HPC, o Singularity não fornece esse tipo de experiência sem problemas no MacOS,
embora tecnicamente seja possível executá-lo dentro de uma máquina virtual Linux no MacOS.

Onde construir imagens
^^^^^^^^^^^^^^^^^^^^^^

Construir imagens do Singularity é uma tarefa bastante pesada, que pode levar 20 minutos
se você tiver muitas etapas na sua receita. Isso torna uma tarefa ruim para rodar em
os nós de login de nossos clusters, especialmente se precisar ser executado regularmente.

No cluster Mila, temos a sorte de ter acesso irrestrito à internet nos nós de computação,
o que significa que qualquer pessoa pode solicitar um nó de CPU interativo (sem necessidade de GPU)
e construir suas imagens lá sem problemas.

.. warning:: Não construa imagens do Singularity do zero toda vez que executar um
    trabalho em um grande lote. Isso será um desperdício colossal de tempo de GPU e também de
    largura de banda da internet. Se você configurar seu fluxo de trabalho corretamente
    (por exemplo, usando caminhos de ligação para o seu código e dados), você pode passar meses reutilizando a mesma
    imagem do Singularity ``my-pytorch-image.sif``.

