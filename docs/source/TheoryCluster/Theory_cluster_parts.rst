Partes de um cluster de computação
**********************************

Para fornecer capacidades de computação de alto desempenho, clusters podem combinar
centenas a milhares de computadores, chamados de nós, que são todos interconectados por
uma rede de comunicação de alto desempenho. A maioria dos nós são projetados para cálculos
de alto desempenho, mas clusters também podem usar nós especializados para oferecer sistemas
de arquivos paralelos, bancos de dados, nós de login e até mesmo a funcionalidade de agendamento
do cluster, conforme ilustrado na imagem abaixo.

.. image:: cluster_overview2.png

Vamos revisar os diferentes tipos de nós que você pode encontrar em um cluster típico.


Os nós de login
===============


Para executar processos de computação em um cluster, você primeiro deve se conectar
a um cluster e isso é feito através de um *nó de login*. Esses chamados nós de login
são o ponto de entrada para a maioria dos clusters.

Outro ponto de entrada para alguns clusters, como o cluster Mila, é a interface web JupyterHub,
mas leremos sobre isso mais tarde. Por enquanto, voltemos ao assunto desta seção: os nós de login.
Para se conectar a eles, você normalmente usaria uma conexão de shell remoto. A ferramenta mais comum
para fazer isso é o SSH. Você ouvirá e lerá muito sobre essa ferramenta. Imagine-a como um cabo de extensão
muito longo (e um pouco mágico) que conecta o computador que você está usando agora, como seu laptop, ao terminal
shell de um computador remoto. Você pode já saber o que é um terminal shell se já usou a linha de comando.


Os nós de computação
====================

No campo da inteligência artificial, geralmente você estará à procura de GPUs.
Na maioria dos clusters, os nós de computação são aqueles com capacidade de GPU.

Embora haja um paradigma geral de tendência para uma configuração homogênea para nós,
isso nem sempre é possível no campo da inteligência artificial, já que o hardware evolui
rapidamente e é complementado por novos hardware, e assim por diante. Portanto, você frequentemente
lerá sobre classes de nós computacionais. Alguns deles podem ter modelos de GPU diferentes ou até
mesmo nenhuma GPU. 

Os nós de armazenamento
=======================

Alguns computadores em um cluster funcionam apenas para armazenar e servir arquivos.
Embora o nome desses computadores possa ser importante para alguns, como usuário,
você só se preocupa com o caminho dos dados. Mais sobre isso na seção :ref:`Processamento de dados`.


Nós diferentes para usos diferentes
===================================

É importante notar aqui a diferença nos usos pretendidos entre os nós de computação
e os nós de login. Enquanto os nós de computação são destinados a computação pesada,
os nós de login não são.

Os nós de login, no entanto, são usados por todos que usam o cluster e deve-se tomar cuidado
para não sobrecarregá-los. Consequentemente, apenas processos muito curtos e leves devem ser
executados nesses nós, caso contrário, o cluster pode se tornar inacessível. Em outras palavras,
por favor, abstenha-se de executar processos longos ou de computação intensiva em nós de login,
pois isso afeta todos os outros usuários. Em alguns casos, você também descobrirá que fazer isso
pode lhe causar problemas.

