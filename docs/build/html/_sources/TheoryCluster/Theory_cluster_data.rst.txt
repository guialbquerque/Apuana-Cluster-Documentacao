Processamento de dados
**********************

Para processar grandes quantidades de dados comuns para o aprendizado profundo,
seja para pré-processamento de conjuntos de dados ou treinamento, existem várias técnicas.
Cada uma tem usos e limitações típicas

Paralelismo de dados
====================

A primeira técnica é chamada de **paralelismo de dados** (também conhecida
como paralelismo de tarefas na ciência da computação formal). Você simplesmente
executa muitos processos, cada um lidando com uma parte dos dados que você deseja processar.
Isso é de longe a técnica mais fácil de usar e deve ser favorecida sempre que possível. Um exemplo
comum disso é a otimização de hiperparâmetros.

Para cálculos realmente pequenos, o tempo para configurar vários processos pode
ser maior do que o tempo de processamento e levar a desperdício. Isso pode ser 
resolvido agrupando alguns dos processos juntos, fazendo o processamento sequencial
de subpartições dos dados.

Para os sistemas de cluster, também não é recomendável lançar milhares de trabalhos
e mesmo que cada trabalho fosse executado por um período razoável de tempo
(vários minutos no mínimo), seria melhor formar grupos maiores até que a 
quantidade de trabalhos seja no máximo algumas centenas.

Finalmente, outra coisa a ter em mente é que a largura de banda de transferência
é limitada entre os sistemas de arquivos (consulte :ref:`Preocupações com o sistema
de arquivos``) e os nós de computação e se você executar muitos trabalhos usando muitos
dados de uma só vez, eles podem não ser mais rápidos porque passarão seu tempo esperando 
pelos dados chegarem.


Paralelismo de modelo
=====================

A segunda técnica é chamada de **paralelismo de modelo** (que não tem um 
único equivalente na ciência da computação formal). É usada principalmente
quando uma única instância de um modelo não cabe em um recurso de computaçã
o (como a memória da GPU sendo muito pequena para todos os parâmetros).

Nesse caso, o modelo é dividido em suas partes constituintes, cada uma processada
independentemente e seus resultados intermediários comunicados entre si para chegar
a um resultado final.

Isso é geralmente mais difícil, mas necessário para trabalhar com modelos maiores e mais poderosos como o GPT.

Preocupações com a comunicação
==============================

A principal diferença dessas duas abordagens é a necessidade de comunicação
entre os múltiplos processos. Alguns métodos comuns de treinamento, como o
descida de gradiente estocástica, ficam em algum lugar entre os dois, pois
requerem alguma comunicação, mas não muita. A maioria das pessoas classifica-o
como paralelismo de dados, já que fica mais próximo desse fim.

Em geral, para tarefas de paralelismo de dados ou tarefas que se comunicam com
pouca frequência, não faz muita diferença onde os processos estão, porque a largura
de banda e a latência de comunicação não terão muito impacto no tempo necessário
para concluir o trabalho. As tarefas individuais podem geralmente ser agendadas independentemente.

Por outro lado, para o paralelismo de modelo, você precisa prestar mais atenção
a onde estão suas tarefas. Nesse caso, geralmente é necessário usar as instalações
do gerenciador de carga de trabalho para agrupar as tarefas de modo que estejam
na mesma máquina ou em máquinas que estejam intimamente ligadas para garantir 
uma comunicação ideal. A melhor alocação depende da arquitetura específica do 
cluster disponível e das tecnologias que ele suporta (como InfiniBand, RDMA, NVLink ou outras).


Preocupações com o sistema de arquivos
======================================

Ao trabalhar em um cluster, você geralmente encontrará vários sistemas
de arquivos diferentes. Normalmente, haverá nomes como "home", "scratch", "datasets", "projects", "tmp".

A razão de ter diferentes sistemas de arquivos disponíveis em vez de um
único gigante é fornecer para diferentes casos de uso. Por exemplo, o
sistema de arquivos "datasets" seria otimizado para leituras rápidas,
mas teria desempenho lento de escrita. Isso ocorre porque os conjuntos
de dados geralmente são escritos uma vez e, em seguida, lidos com muita frequência para treinamento.

O conjunto de sistemas de arquivos fornecido pelo cluster que você está
usando deve ser detalhado na documentação desse cluster e os nomes 
podem diferir dos acima. Você deve prestar atenção ao caso de uso 
recomendado na documentação e usar o sistema de arquivos apropriado
para o trabalho apropriado. Existem casos em que um trabalho rodou 
centenas de vezes mais devagar porque tentou usar um sistema de arquivos que não era adequado para o trabalho.

Uma última coisa a prestar atenção é a política de retenção de dados
para os sistemas de arquivos. Isso tem dois subpontos: por quanto tempo
os dados são mantidos e se há backups.

Alguns sistemas de arquivos terão um limite de tempo para manter seus arquivos.
Tipicamente, o limite é algum número de dias (como 90 dias), mas pode ser "enquanto
o trabalho estiver sendo executado" para alguns.

Quanto aos backups, alguns sistemas de arquivos não terão um limite para os dados,
mas também não terão backups. Para estes, é importante manter uma cópia de quaisquer
dados cruciais em outro lugar. Os dados não serão excluídos intencionalmente, mas o
sistema de arquivos pode falhar e perder todos ou parte de seus dados. Se você tiver
algum dado que é crucial para um artigo ou para a sua tese, mantenha uma cópia adicional em outro lugar.