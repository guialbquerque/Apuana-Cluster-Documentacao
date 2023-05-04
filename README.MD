## **Documentação do Cluster Apuana**

### A página da web do cluster foi gerada utilizando Sphinx, ferramenta de documentação de código aberto amplamente usada para criar documentação técnica, incluindo documentação de código-fonte, manuais de usuário e documentação de API.. Recomenda-se uma leitura nos primeiros passos para melhor entendimento de como a ferramenta funciona. Esta documentação seguiu rigorosamente os passos descritos no site oficial. Segue link : <https://www.sphinx-doc.org/en/master/usage/quickstart.html>

## Edição do arquivo de configuração
###  O arquivo de configuração principal é chamado de conf.py e está localizado na pasta raiz do projeto. Você pode editá-lo para configurar várias opções de documentação, como temas, extensões, entre outros.

## Criação de arquivos de documentação
### Você pode começar a criar sua documentação adicionando arquivos de documentação no formato reStructuredText (ou RST) na pasta source do seu projeto. O RST é uma linguagem de marcação usada pelo Sphinx para criar a documentação. Você pode criar arquivos RST para cada seção da sua documentação, como páginas de introdução, tutoriais, referências, etc.

## Organizacao de documentos

### É possível criar diretórios dentro da pasta source do seu projeto Sphinx para organizar os arquivos RST. Na verdade, essa é uma prática comum para manter a organização e estrutura da documentação. Você pode criar quantos diretórios quiser dentro da pasta source e colocar os arquivos RST neles, seguindo a estrutura que melhor se adeque às suas necessidades. Após criar os diretórios e colocar os arquivos RST neles, você pode referenciar os arquivos RST em outros arquivos RST ou no arquivo de índice (normalmente chamado de index.rst) para criar a estrutura da documentação e estabelecer os links entre os diferentes tópicos

## Primeiros passos
### Considera-se que um sistema linux esteja sendo utilizado, caso esteja num windows, utilizar o wsl2 para uso do linux. Também considera-se que tenha o visual studio code instalado. 
 1. <https://learn.microsoft.com/en-us/windows/wsl/install> 
 2. <https://code.visualstudio.com/download>
### 1. Abrir terminal e digitar: git clone https://github.com/guialbquerque/Apuana-Cluster-Documentacao.git

### 2. No terminal, mudar para o diretorio clonado com o comando: 'cd Apuana-Cluster-Documentacao'. Após isso, digitar 'code .' 
### 3.  Dentro do vscode, abrir terminal e criar um ambiente virtual: python3 -m venv .cluster, e ativar: source .cluster/bin/activate
### 4. Instalar: pip install -U sphinx
## Instalação de alguns pacotes e temas utilizados na renderização

### 5. pip install groundwork-sphinx-theme


### Tema principal utilizado: Groundwork'

### As seguintes linhas em conf.py precisarao ser atualizadas:

### html_static_path = ['/home/USUARIO/Apuana-Cluster-Documentacao/docs/build/_static']
### html_logo = '/home/USUARIO/Apuana-Cluster-Documentacao/docs/source/cin-logo.png'
### Considerando que toda a construcao foi feita num sistema linux e na home do sistema, substituir USUARIO pelo nome de usuario da máquina.
### Caso tenha clonado em outro local, substituir pelo caminho correto.


### Após procedimentos acima, aplicar o seguinte comando para gerar renderização na web:

### sphinx-build -b html docs/source/ docs/build/html

## Publicação da documentação na web
### Após a compilação da documentação, você pode publicá-la na web copiando os arquivos gerados na pasta _build/html para um servidor web ou plataforma de hospedagem de sua escolha. O processo de hospedagem no site do CIn pode ser verificado no link abaixo dependendo do sistema operacional utilizando: <https://helpdesk.cin.ufpe.br/servicos/dados-e-hospedagem>
### Toda a página foi baseada no projeto já consolidado do Milla Cluster-Canadá
<https://github.com/mila-iqia/mila-docs>
