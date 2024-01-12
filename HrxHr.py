#Bibliotecas
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
import pandas as pd
import tinydb
from babel import numbers

#Mapear os dias da semana para pt-Br
def converter_dia_semana(dia_semana_ingles):
    dias_semana = {'Monday': 'Segunda-feira',
                   'Tuesday': 'Terça-feira',
                   'Wednesday': 'Quarta-feira',
                   'Thursday': 'Quinta-feira',
                   'Friday': 'Sexta-feira',
                   'Saturday': 'Sábado',
                   'Sunday': 'Domingo'}
    return dias_semana.get(dia_semana_ingles, 'Dia não encontrado')


# Atualizar dia da semana de acordo com a data selecionada
def atualizar_dia_da_semana(event):
    data_inserida = entry0.get()
    data_formatada = datetime.strptime(data_inserida, '%d/%m/%Y')
    dia_da_semana_ingles = data_formatada.strftime('%A')
    dia_da_semana_portugues = converter_dia_semana(dia_da_semana_ingles)
    lbl2.config(text=f'{dia_da_semana_portugues}'.upper())


# Verificação se os campos de turno e máquina estão preenchidos
def verificar_campos_preenchidos():
    if entry0.get() == "" or combo.get() == "" or combo1.get() == "":
        tk.messagebox.showwarning("Aviso!", "Preencha todos os campos obrigatórios.")
        return False
    else:
        return True


# Botão para abir nova janela com HR x HR de acordo com o turno selecionado
def gerar_hr_hr():
    if verificar_campos_preenchidos():

        turno = combo.get()
        data = entry0.get_date()
        data_formatada = data.strftime('%d/%m/%Y')
        dia_semana = lbl2.cget("text").strip()

        # Abrir uma nova janela
        nova_janela = tk.Toplevel(janela)
        nova_janela.title(f"HR x HR MÁQUINA {combo1.get()} - {turno} - {data_formatada} - {dia_semana}")
        nova_janela.resizable(False, False)

        # Criar uma lista vazia para armazenar as horas correspondentes ao turno selecionado
        hr_x_hr = []

        # Mapeia o dia da semana e o turno para as horas correspondentes
        horas_por_turno = {
            '1T': ['06:00 - 07:00', '07:00 - 08:00', '08:00 - 09:00', '09:00 - 10:00', '10:00 - 11:00',
                   '11:00 - 12:00', '12:00 - 13:00', '13:00 - 14:00'],
            '2T': ['14:00 - 15:00', '15:00 - 16:00', '16:00 - 17:00', '17:00 - 18:00', '18:00 - 19:00',
                   '19:00 - 20:00', '20:00 - 21:00', '21:00 - 22:00'],
            '3T': ['22:00 - 23:00', '23:00 - 00:00', '00:00 - 01:00', '01:00 - 02:00', '02:00 - 03:00',
                   '03:00 - 04:00', '04:00 - 05:00', '05:00 - 06:00']
        }

        min_por_turno = {
            '1T': [60, 60, 60, 60, 60, 60, 60, 60],
            '2T': [60, 60, 60, 60, 60, 60, 60, 60],
            '3T': [60, 60, 60, 60, 60, 60, 60, 60],
        }

        # Obter as horas correspondentes ao turno selecionado
        hr_x_hr = horas_por_turno.get(turno, [])
        min_disponiveis = min_por_turno.get(turno, [])

        # Definir o número de linhas e colunas da tabela
        linhas = len(hr_x_hr)
        colunas = 6
        labels = ["HR x HR", "MAT", "COD", "QTDE REAL", "Parada(em Min)", "Motivo"]  # Criar os rotulos das colunas

        # Definir larguras personalizadas para as colunas
        largura_coluna_mat = 10
        largura_coluna_cod = 6
        largura_coluna_qtde = 5
        largura_coluna_parada = 5
        largura_coluna_observacao = 100

        # Combobox para o campo "COD"
        opcoes_cod = ['X1234', 'X4567', 'X8901', 'Y2345', 'Y6789']

        # Cria os campos de entrada
        combo_cod_values = [tk.StringVar() for i in range(linhas)]
        campos = []
        for i in range(linhas):
            campos.append([])
            for j in range(colunas):
                entrada = None
                if j == 0:
                    label = tk.Label(nova_janela, text=hr_x_hr[i])
                    label.grid(row=i + 7, column=j, padx=5, pady=5)
                elif j == 2:  # Apenas para a coluna "COD"
                    combo_cod = ttk.Combobox(nova_janela, values=opcoes_cod, textvariable=combo_cod_values[i])
                    combo_cod.grid(row=i + 7, column=j, padx=5, pady=5)
                    combo_cod.config(width=largura_coluna_cod)
                else:
                    entrada = tk.Entry(nova_janela)
                    entrada.grid(row=i + 7, column=j, padx=5, pady=5)
                    # Aplicar a largura personalizada com base na coluna
                    if j == 1:
                        entrada.config(width=largura_coluna_mat)
                    elif j == 3:
                        entrada.config(width=largura_coluna_qtde)
                    elif j == 4:
                        entrada.config(width=largura_coluna_parada)
                    elif j == 5:
                        entrada.config(width=largura_coluna_observacao)

                campos[i].append(entrada)

        # Insirir os labels das colunas na primeira linha
        for j, label_text in enumerate(labels):
            label = tk.Label(nova_janela, text=label_text)
            label.grid(row=6, column=j)

        def funcao_de_gravacao():
            # Recupere os dados dos campos de entrada e processe-os
            dados = []

            # Recupere os valores do COD para cada linha separadamente
            cod_values = [combo_cod.get() for combo_cod in combo_cod_values]

            # Preencher a lista 'dados' com os dados inseridos pelo usuário
            for i in range(linhas):
                linha_dados = [hr_x_hr[i]]  # Adicione hr_x_hr na primeira coluna
                for j in range(1, colunas):
                    entrada = campos[i][j]
                    if entrada:
                        valor = entrada.get()
                    else:
                        valor = ""
                    linha_dados.append(valor)
                dados.append(linha_dados)

            #Fazer alterações com o pandas antes de salvar
            df = pd.DataFrame(dados, columns=["HR x HR"] + labels[1:])
            df["COD"] = cod_values
            #print(df)

            #Converter em numeros
            df['QTDE REAL'] = pd.to_numeric(df['QTDE REAL'], errors='coerce')

            #Colocar em ordem as colunas
            colunas_df = ['DATA', 'HR x HR', 'MAQ', 'MAT', 'COD', 'TURNO', 'QTDE REAL', 'Parada(em Min)', 'Motivo']
            df_atualizado = pd.DataFrame(columns=colunas_df)

            # Lista vazia para os dados da data
            datas_formatadas = []

            for i in range(linhas):
                data = entry0.get_date()
                data_formatada = data.strftime('%d/%m/%Y')
                datas_formatadas.append(data_formatada)

            #Acrescentar colunas
            df_atualizado['DATA'] = datas_formatadas
            df_atualizado['HR x HR'] = df['HR x HR']
            df_atualizado['MAQ'] = combo1.get()
            df_atualizado['MAT'] = df['MAT']
            df_atualizado['COD'] = df['COD']
            df_atualizado['TURNO'] = turno
            df_atualizado['QTDE REAL'] = df['QTDE REAL']
            df_atualizado['Parada(em Min)'] = df['Parada(em Min)']
            df_atualizado['Motivo'] = df['Motivo']

            #print(df_atualizado)

            #Verificar se os campos "COD" e "QTDE REAL" estão vazios
            empty_cod = any(value.get() == "" for value in combo_cod_values)
            empty_qtde_real = any(campos[i][3].get() == "" for i in range(linhas))

            #Verificar se os min digitado pelo usuario não são maiores que os min disponiveis
            def validar_minutos_parada(turno, minutos_disponiveis, minutos):
                if turno not in min_por_turno:
                    return True
                minutos = int(
                    minutos) if minutos.isdigit() else 0  # Convertendo a string para inteiro antes de comparar
                return minutos > minutos_disponiveis

            validacao_minutos = any(
                validar_minutos_parada(combo.get(), min_por_turno[combo.get()][i], campos[i][4].get()) for i in
                range(linhas))

            if empty_cod or empty_qtde_real:
                messagebox.showerror("Erro!","Os campos 'COD' e 'QTDE REAL' não podem estar vazios.")
            elif validacao_minutos:
                messagebox.showerror("Erro!","O campo 'Parada(em Min)' não pode ser maior que o de minutos disponíveis.")
            else:
                #Exibir uma caixa de diálogo de confirmação
                resposta = messagebox.askquestion("CONFIRMAÇÃO DE DADOS", "Deseja confirmar os dados?", icon="warning")
                if resposta == "yes":
                    #Converte o DataFrame para um dicionário
                    dados_dict = df_atualizado.to_dict(orient='index')

                    #Caminho do arquivo e salvar de acordo com a aba
                    caminho = r'C:\Users\Usuário\Documents\DataScience\Projetos\Continental\Proeff_Software\AutoWerk\Banco_de_dados\bd_hrxhr.json'

                    #Cria um banco de dados
                    db = tinydb.TinyDB(caminho)

                    #Cria uma tabela chamada "dados"
                    tabela = db.table("dados")

                    #Insere o documento no banco de dados
                    tabela.insert_multiple(dados_dict.values())

                    messagebox.showinfo("Sucesso!", "Dados salvos com sucesso!")
                    nova_janela.destroy()  # Fechar a janela se a resposta for "Sim"
                else:
                    messagebox.showinfo("Cancelado!", "Dados não foram salvos.")

        # Função para somar a qtde real
        def atualizar_soma():
            soma_qtde_real = 0
            for i in range(linhas):
                qtde_real = campos[i][3].get()
                if qtde_real:
                    soma_qtde_real += int(qtde_real)

            # Atualizar a label com a soma
            soma_label.config(text=f"TOTAL PRODUZIDO: {soma_qtde_real}")

        soma_label = tk.Label(nova_janela, text="TOTAL PRODUZIDO: 0")
        soma_label.grid(row=7 + linhas, column=0, columnspan=1, padx=5, pady=5)

        # Adicionar um evento para atualizar a soma quando os valores forem modificados
        for i in range(linhas):
            campos[i][3].bind('<KeyRelease>', lambda event, i=i: atualizar_soma())

        # Função para copiar o MAT da primeira linha para as demais linhas
        def copiar_mat():
            mat_primeira_linha = campos[0][1].get()
            for i in range(1, linhas):
                campos[i][1].delete(0, tk.END)  # Limpar o campo de entrada, caso já haja um valor
                campos[i][1].insert(0, mat_primeira_linha)

        # BOTAO REPETIR MAT
        botao_copiar_mat = tk.Button(nova_janela, text="Repetir MAT", command=copiar_mat)
        botao_copiar_mat.config(width=15, height=1)
        botao_copiar_mat.grid(row=7 + linhas, column=1, columnspan=1, padx=5, pady=5)

        # Função para copiar o COD da primeira linha para as demais linhas
        def copiar_cod():
            cod_primeira_linha = combo_cod_values[0].get()
            for i in range(1, linhas):
                combo_cod_values[i].set(cod_primeira_linha)

        # BOTAO REPETIR PN
        botao_copiar_pn = tk.Button(nova_janela, text="Repetir COD", command=copiar_cod)
        botao_copiar_pn.config(width=15, height=1)
        botao_copiar_pn.grid(row=7 + linhas, column=2, columnspan=2, padx=5, pady=5)

        # BOTAO GRAVAR DADOS
        botao_gravar = tk.Button(nova_janela, text="GRAVAR DADOS", command=funcao_de_gravacao)
        botao_gravar.config(width=15, height=1)
        botao_gravar.grid(row=7 + linhas, column=3, columnspan=colunas, padx=5, pady=5)


# ==== INTERFACE ===
janela = Tk()
janela.title("HR X HR")
janela.geometry('300x200')
janela.resizable(False, False)  # Impede a redimensionamento horizontal e vertical

#DATA
lbl0 = Label(janela, text='DATA')
lbl0.grid(column=0, row=1, padx=5, pady=5, sticky='NSEW')
entry0 = DateEntry(janela, date_pattern='dd/mm/yyyy', locale='pt_BR')
entry0.grid(column=1, row=1, padx=5, pady=5, sticky='NSEW')

#DIA DA SEMANA
lbl1 = Label(janela, text='DIA DA SEMANA')
lbl1.grid(column=0, row=2, padx=5, pady=5, sticky='NSEW')
lbl2 = Label(janela, text='', relief='solid')
lbl2.grid(column=1, row=2, padx=5, pady=5, sticky='NSEW')
atualizar_dia_da_semana(None)
entry0.bind("<<DateEntrySelected>>", atualizar_dia_da_semana)

#TURNO
lbl3 = Label(janela, text='TURNO')
lbl3.grid(column=0, row=3, padx=5, pady=5, sticky='NSEW')
combo = ttk.Combobox(janela, values=('1T', '2T', '3T'), state="readonly")
combo.grid(column=1, row=3, padx=5, pady=5, sticky='NSEW')

#MÁQUINA
lbl4 = Label(janela, text='MÁQUINA')
lbl4.grid(column=0, row=4, padx=5, pady=5, sticky='NSEW')
combo1 = ttk.Combobox(janela, values=('1', '2', '3'), state="readonly")
combo1.grid(column=1, row=4, padx=5, pady=5, sticky='NSEW')

#BOTAO GERAR HR X HR
botao_hrxhr = Button(janela, text="GERAR HR X HR", command=gerar_hr_hr)
botao_hrxhr.config(width=15, height=1)
botao_hrxhr.grid(column=0, row=5, columnspan=2, padx=5, pady=5)

#Crédito
credit_label = tk.Label(janela, text='Desenvolvido por Yara de Oliveira Rufino', font=('Arial', 10), fg='gray')
credit_label.grid(column=0, row=6, sticky='NSEW', padx=5, pady=5, columnspan=2)

janela.mainloop()
