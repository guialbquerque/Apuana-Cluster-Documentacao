## **Documentação do Cluster Apuana**
## **Link para o site**: <https://www.cin.ufpe.br/~jgbal/docs/build/html/>

### A página da web do cluster foi gerada utilizando Sphinx, ferramenta de documentação de código aberto amplamente usada para criar documentação técnica, incluindo documentação de código-fonte, manuais de usuário e documentação de API.. Recomenda-se uma leitura nos primeiros passos para melhor entendimento de como a ferramenta funciona. Esta documentação seguiu rigorosamente os passos descritos no site oficial. Segue link : <https://www.sphinx-doc.org/en/master/usage/quickstart.html>

## Edição do arquivo de configuração
###  O arquivo de configuração principal é chamado de conf.py e está localizado na pasta raiz do projeto. Você pode editá-lo para configurar várias opções de documentação, como temas, extensões, entre outros.

### Comandos necessários para gerar a renderização na web utilizando a ferramenta Sphinx do Python

## Criação de arquivos de documentação
### Você pode começar a criar sua documentação adicionando arquivos de documentação no formato reStructuredText (ou RST) na pasta source do seu projeto. O RST é uma linguagem de marcação usada pelo Sphinx para criar a documentação. Você pode criar arquivos RST para cada seção da sua documentação, como páginas de introdução, tutoriais, referências, etc.

### Considera-se que um ambiente virtual foi criado para comportar todos os pacotes necessários.Exemplo: python3 -m venv .cluster

### 1.  pip install -U sphinx
## Instalação de alguns pacotes e temas utilizados na renderização

### 2. pip install wheel, groundwork-sphinx-theme


### Tema principal utilizado: Groundwork

### 3. Adicionar em conf.py a seguinte linha:

### html_theme = 'groundwork'

### As seguintes linhas em conf.py precisarao ser atualizadas:

### html_static_path = ['/home/barad-dur/Apuana-Cluster-Documentacao/docs/build/_static']
### html_logo = '/home/barad-dur/Apuana-Cluster-Documentacao/docs/source/cin-logo.png'
### Considerando que toda a construcao foi feita num sistema linux e na home do sistema, basta alterar /home/USUARIO/Apuana-Cluster-Documentacao/docs/build/_static

### Após procedimentos acima, caso alguma alteração tenha sido feita, aplicar o seguinte comando para gerar renderização na web:


### sphinx-build -b html docs/source/ docs/build/html
 
## Publicação da documentação na web
### Após a compilação da documentação, você pode publicá-la na web copiando os arquivos gerados na pasta _build/html para um servidor web ou plataforma de hospedagem de sua escolha. O processo de hospedagem no site do CIn pode ser verificado no link abaixo dependendo do sistema operacional utilizando: <https://helpdesk.cin.ufpe.br/servicos/dados-e-hospedagem>
### Toda a página foi baseada no projeto já consolidado do Milla Cluster-Canadá
<https://github.com/mila-iqia/mila-docs>
