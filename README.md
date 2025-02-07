# PCS3616 - Laboratório 6 - MVN 4

Hoje vamos implementar um dumper e/ou um loader.

Nesta aula, você deverá trabalhar **em dupla** para desenvolver um dos
seguintes programas: dumper ou loader (basta fazer um apenas).

O corretor automático do github sempre testará o dumper e o loader, com isso
caso a dupla faça apenas um dos programas, o github indicará que algum teste falhou.
Mas não se preocupe, caso a sua dupla resolva um deles de forma completa, a
nota da dupla será 10.

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
com 2 bytes por linha usando a seguinte função em Python 3
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

Um exemplo de arquivo binário `.dat` - seguindo os padrões de dump da MVN - foi disponibilizado nesse repositório com o nome `ex.dat`. Este arquivo serve tanto como exemplo de output do dumper, como de input para o loader.

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

-   Ambas as funções devem ser codificadas como subrotinas.

## Entrega
- Arquivo `dumper.asm` com o dumper
- Arquivo `loader.asm` com o loader
