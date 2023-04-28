Compartilhando dados com ACLs
=============================

Os bits de permissão regulares são ferramentas extremamente limitadas: eles controlam
o acesso por meio de apenas três conjuntos de bits - usuário proprietário, grupo
proprietário e todos os outros. Portanto, o acesso é ou muito restrito 
(0700 permite acesso apenas ao usuário proprietário) ou muito amplo 
(770 dá todas as permissões para todos no mesmo grupo, e 777 para literalmente todos).

As ACLs (Listas de Controle de Acesso) são uma expansão dos bits de permissão que permitem
um controle mais granular de acessos a um arquivo. Elas podem ser usadas para permitir 
que usuários específicos acessem arquivos e pastas, mesmo que as permissões padrão 
conservadoras os tenham negado esse acesso.

Como exemplo ilustrativo, para usar as ACLs para permitir que $USER (a si mesmo) compartilhe 
com $USER2 (outra pessoa) uma hierarquia de pastas "playground" no sistema de arquivos de 
rascunho do Apuana em um local

    ``/network/scratch/${USER:0:1}/$USER/X/Y/Z/...``

de maneira segura e que permita que ambos os usuários leiam, escrevam, executem, pesquisem e excluam
os arquivos um do outro:



----


| **1.** Grant **oneself** permissions to access any **future** files/folders created
  by the other *(or oneself)*
| (``-d`` renders this permission a "default" / inheritable one)

.. code-block:: console

    setfacl -Rdm user:${USER}:rwx  /network/scratch/${USER:0:1}/$USER/X/Y/Z/

----

.. note::
    A importância de fazer este passo aparentemente redundante primeiro é que arquivos e
    pastas são sempre de propriedade de apenas uma pessoa, quase sempre o seu criador 
    (o UID será do criador, o GID geralmente também). Se esse usuário não for você,
    você não terá acesso a esses arquivos a menos que a outra pessoa especificamente os dê
    a você - ou esses arquivos herdem uma ACL padrão que permita acesso total.

   **This** Esta é a ACL padrão herdada que serve esse propósito.

| **2.** Grant **the other** permission to access any **future** files/folders created
  by the other *(or oneself)*
| (``-d`` renders this permission a "default" / inheritable one)

.. code-block:: console

    setfacl -Rdm user:${USER2}:rwx /network/scratch/${USER:0:1}/$USER/X/Y/Z/

----

| **3.** Grant **the other** permission to access any **existing** files/folders created
  by *oneself*.
| Esses arquivos e pastas foram criados antes das novas ACLs padrão serem adicionadas acima e,
    portanto, não as herdaram de sua pasta pai no momento de sua criação.
.. code-block:: console

    setfacl -Rm  user:${USER2}:rwx /network/scratch/${USER:0:1}/$USER/X/Y/Z/

.. note::
   O objetivo de conceder permissões primeiro para arquivos *futuros* e depois para arquivos
    existentes é evitar uma condição de corrida em que, após o primeiro comando ``setfacl``, a
    outra pessoa possa criar arquivos aos quais o segundo comando ``setfacl`` não se aplica.


----

| **4.** Grant **another** permission to search through one's hierarchy down to the
    shared location in question.

* **Non**-recursive (!!!!)
* May also grant ``:rx`` in unlikely event others listing your folders on the
    path is not troublesome or desirable.

.. code-block:: console

    setfacl -m   user:${USER2}:x   /network/scratch/${USER:0:1}/$USER/X/Y/
    setfacl -m   user:${USER2}:x   /network/scratch/${USER:0:1}/$USER/X/
    setfacl -m   user:${USER2}:x   /network/scratch/${USER:0:1}/$USER/

.. note::
    Para acessar um arquivo, todas as pastas desde o diretório raiz (``/``) até a pasta pai
    em questão devem ser pesquisáveis (+x) pelo usuário em questão. Isso já é o caso 
    para todos os usuários em pastas como ``/``, ``/network`` e ``/network/scratch``, mas os usuários
    devem conceder acesso explicitamente a alguns ou a todos os usuários, seja por meio de
    permissões básicas ou adicionando ACLs, para pelo menos ``/network/scratch/${USER:0:1}/$USER``, ``$HOME`` e subpastas.

    Para permitir bruscamente que todos os usuários pesquisem uma pasta (**pense duas vezes!**), o seguinte comando pode ser usado:





    .. code-block:: console

        chmod a+x /network/scratch/${USER:0:1}/$USER/


.. note::
    Para obter mais informações sobre ``setfacl`` e resolução de caminho/verificação
    de acesso, considere os seguintes comandos de visualização de documentação:

  * ``man setfacl``
  * ``man path_resolution``

Visualizando e Verificando ACLs
-------------------------------

.. code-block:: console

    getfacl /path/to/folder/or/file
                1:  # file: somedir/
                2:  # owner: lisa
                3:  # group: staff
                4:  # flags: -s-
                5:  user::rwx
                6:  user:joe:rwx               #effective:r-x
                7:  group::rwx                 #effective:r-x
                8:  group:cool:r-x
                9:  mask::r-x
                10:  other::r-x
                11:  default:user::rwx
                12:  default:user:joe:rwx       #effective:r-x
                13:  default:group::r-x
                14:  default:mask::r-x
                15:  default:other::---

.. note::
  * ``man getfacl``