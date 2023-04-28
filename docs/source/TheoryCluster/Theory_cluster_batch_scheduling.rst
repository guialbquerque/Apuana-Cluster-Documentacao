O gerenciador de carga de trabalho
**********************************

Em um cluster, os usuários não têm acesso direto aos nós de computação,
mas se conectam a um nó de login e adicionam trabalhos à fila do gerenciador
de carga de trabalho. Sempre que houver recursos disponíveis para executar
esses trabalhos, eles serão alocados para um nó de computação e executados,
o que pode acontecer imediatamente ou após uma espera de vários dias.


Anatomia de um trabalho
-----------------------

Um trabalho consiste em uma série de etapas que serão executadas uma após a outra.
Isso é feito para que você possa agendar uma sequência de processos que podem usar
os resultados das etapas anteriores sem ter que interagir manualmente com o escalonador.

Cada etapa pode ter qualquer número de tarefas, que são grupos de processos que podem 
ser agendados independentemente no cluster, mas podem ser executados em paralelo se houver
recursos disponíveis. A distinção entre etapas e tarefas é que várias tarefas, se fizerem
parte da mesma etapa, não podem depender dos resultados de outras tarefas porque não há
garantias sobre a ordem em que serão executadas.

Finalmente, cada grupo de processos é a unidade básica agendada no cluster.
Ele consiste em um conjunto de processos (ou threads) que podem ser executados
em vários recursos (CPU, GPU, RAM, ...) e são agendados juntos como uma unidade
em uma ou mais máquinas.

Cada um desses conceitos é adequado para um uso específico. Para treinamento com
várias GPUs em cargas de trabalho de inteligência artificial, você usaria uma tarefa
por GPU para paralelismo de dados ou um grupo de processos se estiver fazendo paralelismo de modelo.
A otimização de hiperparâmetros pode ser feita usando uma combinação de tarefas e etapas, mas
provavelmente é melhor deixá-la para um framework fora do escopo do gerenciador de carga de trabalho.

Se tudo isso parece complicado, você deve saber que todas essas coisas não precisam ser usadas sempre.
É perfeitamente aceitável enviar trabalhos com uma única etapa, uma única tarefa e um único processo.

Compreendendo a fila
--------------------

Os recursos disponíveis no cluster não são infinitos e é o trabalho do
gerenciador de carga alocá-los. Sempre que uma solicitação de trabalho é feita
e não há recursos suficientes disponíveis para iniciar imediatamente, ele
será colocado na fila.

Uma vez que um trabalho está na fila, ele permanecerá lá até que outro trabalho
termine e, em seguida, o gerenciador de carga tentará usar os recursos liberados
com trabalhos da fila. A ordem exata em que os trabalhos serão iniciados não é
fixa, pois depende das políticas locais que podem levar em conta a prioridade do
usuário, o tempo desde que o trabalho foi solicitado, a quantidade de recursos
solicitados e possivelmente outras coisas. Deve haver uma ferramenta que acompanha
o gerenciador em que você pode ver o status dos trabalhos em fila e por que eles
permanecem na fila.

Sobre partições
----------------

O gerenciador de carga irá dividir o cluster em partições de acordo com
a configuração definida pelos administradores. Uma partição é um conjunto de
máquinas geralmente reservadas para um propósito específico. Um exemplo pode
ser máquinas somente com CPU para pré-processamento configuradas como uma partição
separada. É possível que várias partições compartilhem recursos.

Sempre haverá pelo menos uma partição que é a partição padrão na qual os trabalhos
sem solicitação específica serão executados. Outras partições podem ser solicitadas,
mas podem ser restritas a um grupo de usuários, dependendo da política.

As partições são úteis do ponto de vista de política para garantir o uso eficiente
dos recursos do cluster e evitar o uso excessivo de um tipo de recurso que possa
bloquear o uso de outro. Elas também são úteis para clusters heterogêneos, onde
diferentes hardwares são misturados e nem todos os softwares são compatíveis com
todos eles (por exemplo, CPUs x86 e POWER).


Ultrapassando limites (preempção e períodos de graça)
-----------------------------------------------------

Para garantir uma distribuição justa dos recursos de computação para todos,
o gerenciador de carga estabelece limites na quantidade de recursos que um
único usuário pode usar de uma só vez. Esses limites podem ser limites rígidos
que impedem a execução de trabalhos quando você ultrapassa ou limites flexíveis
que permitirão que você execute trabalhos, mas apenas até que outro trabalho precise dos recursos.

A política do administrador determinará quais são os limites exatos para um cluster
ou usuário específico e se eles são limites rígidos ou flexíveis.

A forma como os limites flexíveis são aplicados é por meio de preempção, o que
significa que quando outro trabalho com prioridade mais alta precisa dos recursos
que seu trabalho está usando, seu trabalho receberá um sinal de que precisa salvar
seu estado e sair. Será dado um certo tempo para isso (o período de graça, que pode ser de 0s)
e depois ele será encerrado à força se ainda estiver em execução.

Dependendo do gerenciador de carga em uso e da configuração do cluster, um trabalho
que seja preemptionado dessa forma pode ser automaticamente reagendado para ter a
chance de terminar ou pode caber ao trabalho reagendar-se.

O outro limite que pode ser encontrado é com um trabalho que ultrapassa seus limites declarados.
Ao agendar um trabalho, você declara quanto de recursos ele precisará (RAM, CPUs, GPUs, ...).
Alguns desses recursos podem ter valores padrão e não serem definidos explicitamente. Para
determinados tipos de dispositivos, como GPUs, o acesso a unidades acima do limite do seu
trabalho fica indisponível. Para outros, como RAM, o uso é monitorado e seu trabalho será
encerrado se exceder o limite. Isso torna importante garantir que você estime com precisão o uso de recursos.



Informações sobre Apuana
------------------------

Comandos de cliente **Slurm** estão disponíveis nos nós de login para que você possa enviar
trabalhos para o controlador principal e adicioná-los à fila. Existem dois tipos de trabalhos:
trabalhos em *lote* (batch) e trabalhos *interativos* (interactive).

