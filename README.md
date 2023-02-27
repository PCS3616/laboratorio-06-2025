# PCS3616 - Laboratório 6 - MVN 3

Hoje é a última aula com linguagem de máquina, portanto vai ser a mais
interessante delas, vamos implementar um dumper e um loader.

```bash
# Instalação do programa "bless" (editor de arquivos binários)
sudo apt-get update
sudo apt-get install -y bless
```

Nesta aula, você deverá trabalhar **em dupla** para desenvolver dois
programas escritos na linguagem de máquina da MVN: um dumper e um
loader.

Um dos membros da dupla será o responsável pelo desenvolvimento do
dumper e o outro membro será responsável pelo desenvolvimento do loader.
Ao final do desenvolvimento, estes dois programas deverão funcionar
corretamente em conjunto.

A especificação completa do funcionamento do loader e dumper está
disponível nos slides da Aula 12, disponíveis no Moodle.

**Observações:**

-   Vamos usar a seguinte convenção: os dois programas (dumper e loader)
devem ler/escrever do dispositivo `300`. Ou seja, no seu arquivo
disp.lst, use a seguinte linha:

    -   `3 0 dump.dat e/l` (`e` para escrita e `l` para leitura)

-   É obrigatório iniciar o loader no endereço 0xB00 (endereço máximo: `0xCFF`).

-   É obrigatório iniciar o dumper no endereço 0x700 (endereço máximo: `0xAFF`).

    -   `0x704`: Parâmetro "endereço inicial"

    -   `0x706`: Parâmetro "qtd. de palavras"

-   Quantidade de **bytes de dados** por bloco: 256 (128 palavras).

    - Em caso

-   Ambas as funções devem ser codificadas como subrotinas.

## Entrega:
- Arquivo `dumper.mvn` com o dumper
- Arquivo `loader.mvn` com o loader
