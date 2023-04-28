Preocupações e soluções de portabilidade
========================================

Ao trabalhar em um projeto de software, é importante estar ciente
de todo o software e bibliotecas nos quais o projeto depende e 
listá-los explicitamente e sob um sistema de controle de versão
de tal forma que possam ser facilmente instalados e disponibilizados
em diferentes sistemas. As vantagens são significativas:

* Facilidade de instalação e execução no cluster
* Facilidade de colaboração
* Melhor reprodutibilidade


Para alcançar isso, tente sempre manter em mente os seguintes aspectos:

* Versões: Para cada dependência, certifique-se de ter algum registro da versão 
    específica que está usando durante o desenvolvimento. Dessa forma, no futuro, você
    poderá reproduzir o ambiente original que sabe ser compatível. De fato, quanto mais
    tempo passa, mais provável é que novas versões de alguma dependência tenham alterações
    quebradas. O comando pip freeze pode criar tal registro para dependências do Python.
* Isolamento: Idealmente, cada um de seus projetos de software deve estar isolado dos outros.
    O que isso significa é que atualizar o ambiente do projeto A não deve atualizar o ambiente do
    projeto B. Dessa forma, você pode instalar e atualizar software e bibliotecas livremente para
    o primeiro, sem se preocupar em quebrar o segundo (o que você pode não perceber até semanas 
    depois, na próxima vez em que trabalhar no projeto B!) O isolamento pode ser alcançado usando
    :ref:`Python Virtual environments` and :ref:`containers`.

.. Creating a list of your software's dependencies
.. -----------------------------------------------
.. TODO


Gerenciando seus ambientes
--------------------------

.. include:: Userguide_python.rst


Usando módulos
--------------

Muito software, como Python e Conda, já está compilado e disponível no cluster por
meio do comando ``module`` e seus subcomandos. Em particular, se você deseja usar 
o ``Python 3.7``, basta fazer:

.. code-block:: console

    module load python/3.7


No uso de contêineres
---------------------

Outra opção para criar código portátil é: :ref:`Using containers`.

Containers são uma abordagem popular para implantar aplicativos, empacotando juntos muitas das dependências necessárias.
 A ferramenta mais popular para isso é o `Docker <https://www.docker.com/>`_.