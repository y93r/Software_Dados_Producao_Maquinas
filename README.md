# Software_Dados_Producao_Maquinas
Criação de um software para coleta de dados de produção diário

## TECNOLOGIAS USADAS:
- Python 3.10.9
  - tkinter: 8.6 
  - tkcalendar: 1.5.0
  - ttkthemes: 3.2.2
 
  ## Instalação das bibliotecas
```bash
pip install tkcalendar
pip install ttkthemes
```
 
## AUTORA
- [Yara De Oliveira Rufino](https://www.linkedin.com/in/yara-de-oliveira-rufino/)

## DESENVOLVIMENTO
- Esta janela intergráfica tem como objetivo agilizar a anotação de dados de produção
  - Na aba de produção o usuário deve colocar a data, matrícula, turno, máquina, cliente, código e o total produzido
  - Na aba de falhas deverá colocar o modo de falha e a quantidade, a soma do total de falhas é feita automaticamente
  - Há os botões de adicionar e remover falha, ao clicar no primeiro será acrescentado em uma lista o modo de falha e a quantidade. Ao clicar no segundo, a falha selecionada será retirada da lista
  - Voltando a aba produção há o botão de gravar, sendo clicado abrirá outra janela para conferir os dados: data, matrícula, turno, máquina, cliente, código, total produzido, falhas, total falhas e fpy
  - Caso algo não esteja correto o usuário tem a opção de apertar o botão de cancelar e corrigir o que está errado ou faltando. Se tudo estiver certo, ele pode apertar o botão OK, a janela se encerrará e todos os dados serão apagados.
