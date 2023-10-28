# Software_Dados_Producao_Maquinas

## HR X HR
Criação de um software para coleta de dados de produção diária hora x hora das máquinas.

## TECNOLOGIAS USADAS:
- Python 3.10.9
  - tkinter==8.6 
  - tkcalendar==1.6.1
  - pandas==2.1.1
  - datetime==3.10.9
  - openpyxl==3.1.2
  - Babel==2.13.1
  - Pillow==10.1.0
- Excel versão Microsoft 365
 
## Instalação das bibliotecas
```bash
pip install tkcalendar
pip install pyinstaller
pip install Pillow

```
 
## AUTORA
- [Yara De Oliveira Rufino](https://www.linkedin.com/in/yara-de-oliveira-rufino/)

## DESENVOLVIMENTO
- Este software tem como objetivo simplificar as anotações HR x HR;
  - Usando uma interface gráfica onde já é gerado a data atual e o dia da semana, caso o usuário queira trocar data, o dia da semana é atualizado simultaneamente;
  - Há 2 listas onde o usuário deve escolher o turno e a máquina, essas 2 opções não podem ficar vazias se não o botão Gerar Hr x Hr irá te alertar dos campos vazios;
  - Ao clilcar no botão Gerar Hr x Hr abrirá uma nova janela de acordo com as horas do turno selecionado;
  - Nessa janela haverá as colunas "HR x HR", "MAT", "COD", "QTDE REAL", "Parada(em Min)", "Justificativa" e os campos vazios para o usuário digitar de acordo com a folha impressa;
  - Para facilitar o preenchimento dos dados o botão "REPETIR COD" copia a primeira linha da coluna COD para as demais, assim como o botão "REPETIR MAT" para sua respectiva coluna;
  - Os campos da colunas "MAT", "QTDE REAL" não podem ficar vazios se não o botão GRAVAR DADOS mostrará um alerta sobre isso;
  - Todos os dados inseridos passaram por um processo no pandas para antes de salvar na planilha original ter as mesmas colunas e na mesma ordem;
  - Os dados serão salvos na aba de acordo com a máquina selecionada ao clicar no botão GRAVAR;
  - Após isso a nova janela se fechará.

