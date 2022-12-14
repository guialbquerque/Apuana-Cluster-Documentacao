## **Documentação do Cluster Apuana**
## **Link para o site**: <https://www.cin.ufpe.br/~jgbal/docs/build/html/>

A página da web do cluster foi gerada utilizando a ferramenta Sphinx, que utiliza a linguagem Python para gerar páginas na web. Recomenda-se uma leitura nos primeiros passos para melhor entendimento de como a ferramenta funciona. Esta documentação seguiu rigorosamente os passos descritos no site oficial. Segue link : <https://www.sphinx-doc.org/en/master/usage/quickstart.html>
### Comandos necessários para gerar a redenrização na web utilizando a ferramenta Sphinx do Python

### Considera-se que um ambiente virtual foi criado para comportar todos os pacotes necessários

### 1.  pip install -U --pre sphinx
## Instalação de alguns pacotes e temas utilizados na renderização

### 2. pip install sphinx_rtd_theme

### Após instalação, adicionar no arquivo conf.py

### import sphinx_rtd_theme

#### extensions = [
    ...
    'sphinx_rtd_theme',
]

### Tema principal utilizado: Groundwork

### 3. pip install groundwork-sphinx-theme

### Adicionar em conf.py a seguinte linha:

### html_theme = 'groundwork'

### Caso o editor de texto reclame de algum outro pacote faltando, apenas verificar e utilizar pip para instalar conforme os passos anteriores.

### Após procedimentos acima, caso alguma alteração tenha sido feita, aplicar o seguinte comando para gerar renderização na web:


### sphinx-build -b html docs/source/ docs/build/html

Considerando, obviamente que a hierarquia de diretórios se mantém conforme este repositório.

### Toda a página foi baseada no projeto já consolidado do Milla Cluster-Canadá
<https://github.com/mila-iqia/mila-docs>
