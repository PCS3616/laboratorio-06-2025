# PCS3616 - Laboratório 6 - MVN 3

Hoje é a última aula com linguagem de máquina, portanto vai ser a mais
interessante delas, vamos implementar um dumper e um loader.

Nesta aula, você deverá trabalhar **em dupla** para desenvolver dois
programas escritos na linguagem de máquina da MVN: um dumper e um
loader.

Um dos membros da dupla será o responsável pelo desenvolvimento do
dumper e o outro membro será responsável pelo desenvolvimento do loader.
Ao final do desenvolvimento, estes dois programas deverão funcionar
corretamente em conjunto.

A especificação completa do funcionamento do loader e dumper está
disponível nos slides de aula por meio
[deste link](https://drive.google.com/file/d/1oCtP5S192MhYEdF5Xw-bLgyUAXzcrRaN/view?usp=share_link)
com acesso liberado somente para emails USP.

## Ferramentas recomendadas

Um editor de texto normal (como `vim`) não foi desenvolvido para a edição
de arquivos não-texto. Assim, é recomendado utilizar outro editor, como
o `bless`, que pode ser instalado executando
```bash
sudo apt-get update
sudo apt-get install -y bless
```

O `bless` é um programa com interface gráfica, então pode não funcionar
em versões antigas do WSL ou em outros ambientes sem interface gráfica. 
Caso não consiga executar, é possível codificar textos em hexadecimal 
com 2 btytes por linha usando a seguinte função em Python 3
```python
def string_to_two_byte_hex(string: str):
    string_bytes = string.encode('ascii')
    string_hex = string_bytes.hex('\n', 2)  # \n every 2 bytes
    print(string_hex)
```
e é possível visualizar um arquivo em binário usando o utilirário do Linux
`hexdump`, executando
```bash
hexdump -C ARQUIVO
```

## Instruções

-   Vamos usar a seguinte convenção: os dois programas (dumper e loader)
devem ler/escrever do dispositivo `300`. Ou seja, no seu arquivo
disp.lst, use a seguinte linha:

    -   `3 0 dump.dat e/l` (`e` para escrita e `l` para leitura)

-   É obrigatório iniciar o loader no endereço 0xB00 (endereço máximo: `0xCFF`).

-   É obrigatório iniciar o dumper no endereço 0x700 (endereço máximo: `0xAFF`).

    -   `0x704`: Parâmetro "endereço inicial"

    -   `0x706`: Parâmetro "qtd. de palavras"

-   Quantidade máxima de **bytes de dados** por bloco: 256 (128 palavras).

    - Os slides anteriormente mencionavam 64 palavras por bloco, mas
    sua implementação deve usar 128.

-   Ambas as funções devem ser codificadas como subrotinas.

## Entrega
- Arquivo `dumper.mvn` com o dumper
- Arquivo `loader.mvn` com o loader
