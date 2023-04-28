Software no cluster
*******************

Esta seção tem como objetivo conscientizar sobre os problemas que se pode encontrar
ao tentar executar um software em diferentes computadores e como isso é tratado em
clusters de computação típicos.

Em relação ao desenvolvimento em Python, recomendamos o uso de ambientes virtuais para
instalar pacotes Python em isolamento.



Módulos de software do cluster
==============================

Os módulos são pequenos arquivos que modificam suas variáveis de ambiente para 
apontar para versões específicas de vários softwares e bibliotecas. Por exemplo, 
um módulo pode fornecer o comando "python" para apontar para o Python 3.7, outro 
pode ativar a versão 11.0 do CUDA, outro pode fornecer o pacote "torch" e assim por diante.

Para obter mais informações, consulte :ref:`O comando module`.


Contêineres
===========

Os contêineres são uma forma especial de isolamento de software e suas dependências.
Um contêiner é essencialmente uma máquina virtual leve: ele encapsula um sistema de arquivos
virtual para uma instalação completa do sistema operacional, bem como uma rede e ambiente de
execução separados.

Por exemplo, você pode criar um contêiner Ubuntu no qual instala vários pacotes usando "apt", 
modifica configurações como faria como usuário root, e assim por diante, mas sem interferir na
sua instalação principal. Uma vez construído, um contêiner pode ser executado em qualquer sistema
compatível.

Para obter mais informações, consulte :ref:`Usando contêineres`.


Ambientes virtuais Python
=========================

Um ambiente virtual em Python é um ambiente local e isolado no qual você pode instalar
ou desinstalar pacotes Python sem interferir no ambiente global (ou em outros ambientes virtuais).
Para usar um ambiente virtual, primeiro você deve ativá-lo.

Para obter mais informações, consulte :ref:`Ambientes virtuais`.
