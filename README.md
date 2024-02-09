# Software_Dados_Producao_Maquinas

## HR X HR
Criação de um software para coleta de dados de produção diária hora x hora das máquinas.

## TECNOLOGIAS USADAS:
- Pycharm 2023.3.2
- Python 3.12
  - tkinter==8.6
  - tkcalendar==1.6.1
  - pandas==2.1.4
  - datetime==3.12
  - tinydb==4.8.0
  - Babel==2.14.0
  - pillow==10.2.0
  - pyinstaller==6.0.0
 
## Instalação das bibliotecas
```bash
pip install tkcalendar
pip install pandas
pip install tinydb
pip install Pillow
pip install pyinstaller==6.0.0
pip install babel
```
 
## ARTIGOS
[Parte 1](https://www.linkedin.com/pulse/fluxo-de-dados-da-interface-gr%2525C3%2525A1fica-at%2525C3%2525A9-visualiza%2525C3%2525A7%2525C3%2525A3o-yara-psehf%3FtrackingId=oxkh279SSeeQE88wBUmWZA%253D%253D/?trackingId=oxkh279SSeeQE88wBUmWZA%3D%3D) | 
[Parte 2]()

## DESENVOLVIMENTO
- Este software tem como objetivo simplificar as anotações HR x HR;
  - Usando uma interface gráfica onde já é gerado a data atual e o dia da semana, caso o usuário queira trocar data, o dia da semana é atualizado simultaneamente;
  - Há 2 listas onde o usuário deve escolher o turno e a máquina, essas 2 opções não podem ficar vazias se não o botão Gerar Hr x Hr irá te alertar dos campos vazios;
  - Ao clilcar no botão Gerar Hr x Hr abrirá uma nova janela de acordo com as horas do turno selecionado;
  - Nessa janela haverá as colunas "HR x HR", "MAT", "COD", "QTDE REAL", "Parada(em Min)", "Justificativa" e os campos vazios para o usuário digitar de acordo com a folha impressa;
  - Para facilitar o preenchimento dos dados o botão "REPETIR COD" copia a primeira linha da coluna COD para as demais, assim como o botão "REPETIR MAT" para sua respectiva coluna;
  - Os campos da colunas "MAT", "QTDE REAL" não podem ficar vazios se não o botão GRAVAR DADOS mostrará um alerta sobre isso;
  - Os campos da coluna "Parada(Min)" não podem ser maiores que 60 minutos se não o botão GRAVAR DADOS mostrará um alerta sobre isso;
  - Todos os dados inseridos vão passar por um processo no pandas que adiciona automaticamente cada linha que é preenchida a um DataFrame, converte a coluna Parada(em Min) em número inteiro, reordena e acrescenta as colunas de acordo os critérios estabelecidos e formata a data para o padrão brasileiro.
  - Os dados serão salvos ao clicar no botão GRAVAR em um documento chamado bd_hrxhr.json;
  - Após isso a nova janela se fechará.

## Documentação
[Tinydb](https://tinydb.readthedocs.io/en/latest/) | [Pandas](https://pandas.pydata.org/docs/) | [Tkinter](https://docs.python.org/pt-br/dev/library/tkinter.html) | [tkcalendar](https://tkcalendar.readthedocs.io/en/stable/index.html)

