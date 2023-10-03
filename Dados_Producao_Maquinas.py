from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import tkinter as tk

#Verficar se é um numero sendo digitado e limitar a 5 caracteres
def validar_entrada(event, entry):
    entry_text = entry.get()
    if entry_text.isdigit() and len(entry_text) <= 5:
        return True
    else:
        return False
    
def limitar_entrada(event):
    if not validar_entrada(event, entry1):
        entry1.delete(0, 'end')  # Limpe o conteúdo se não for um número válido
    if not validar_entrada(event, entry2):
        entry2.delete(0, 'end')
    if not validar_entrada(event, quantidade_entry):
        quantidade_entry.delete(0, 'end')    
        
#Dicionário que mapeia pn de acordo com o cliente
cliente_pn = {'WSS FIAT': ['31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49', 
'50','51','52','53','54','55','56','57','58'],
             'WSS RNT': ['16','17','18','19','20','21','26','27','28'],
             'GEM': ['8042','8043','8045','8047','8048'],
             'GSE': ['CPDD GSE','ACAM GSE'],
             'EA211': ['ACPS EA211','CPDD EA211','ACAM EA211'],
             'GV4': ['ACAM GV4','ACPS GV4']
}

def atualizar_opcoes_pn(event):
    cliente_selecionado = combo2.get()
    if cliente_selecionado in cliente_pn:
        pn = cliente_pn[cliente_selecionado]
    else:
        pn = []
     
    # Atualize as opções do combobox de PNs
    combo3['values'] = pn
    combo3.set('')  # Limpe a seleção atual
        
#Dicionário que mapeia máquinas às suas falhas
maquinas_e_falhas = {
    'ENGEL 1': ['Falha A', 'Falha B', 'Falha C'],
    'ENGEL 2': ['Falha D', 'Falha E', 'Falha F'],
    'ENGEL 3': ['Falha W', 'Falha Y', 'Falha Z'],
    'ENGEL 4': ['Falha G', 'Falha H', 'Falha I'],
    'ENGEL 5': ['Falha J', 'Falha K', 'Falha L'],
    'ENGEL 6': ['Falha M', 'Falha N', 'Falha O'],
    'ENGEL 7': ['Falha P', 'Falha Q', 'Falha R'],
    'ENGEL 8': ['Falha S', 'Falha T', 'Falha U'],
    'ENGEL 9': ['Falha V', 'Falha X', 'Falha X1'],
    'ARBURG 1': ['Falha A2', 'Falha A3', 'Falha A4'],
    'ARBURG 2': ['Falha B2', 'Falha B3', 'Falha B4'],
    'ARBURG 3': ['Falha C2', 'Falha C3', 'Falha C4'],
}

#Função para atualizar as opções do ComboBox de falhas com base na máquina selecionada
def atualizar_falhas(event):
    maquina_selecionada = combo1.get()
    if maquina_selecionada in maquinas_e_falhas:
        falhas = maquinas_e_falhas[maquina_selecionada]
    else:
        falhas = []
    
    # Atualize as opções do combobox de falhas
    combo_falhas['values'] = falhas
    combo_falhas.set('')  #Limpe a seleção atual
    
#Função para adicionar a falha selecionada com a quantidade especificada
quantidades_falhas = []
def adicionar_falha():
    falha_selecionada = combo_falhas.get()
    quantidade = quantidade_entry.get()    
    
    if falha_selecionada and quantidade:
        falha_com_quantidade = f"{falha_selecionada} - Qtde: {quantidade}"
        lista_falhas.insert(END, falha_com_quantidade)
        quantidade_entry.delete(0, END)
        global quantidades_falhas
        quantidades_falhas.append(int(quantidade))
        atualizar_total_falhas()
                
#Função para atualizar o total de falhas com base na lista de falhas selecionadas
total_falhas = 0  
def atualizar_total_falhas():
    global total_falhas
    if quantidades_falhas:
        total_falhas = sum(quantidades_falhas)
    else:
        total_falhas = 0    
    lbl_total_falhas.config(text=f'TOTAL FALHAS: {total_falhas}')
    return total_falhas

#Função para remover o modo de falha selecionado da lista
def remover_falha_selecionada():
    selecao = lista_falhas.curselection()  # Obtém o índice do item selecionado
    if selecao:
        indice = selecao[0]  # Pega o primeiro índice selecionado
        lista_falhas.delete(indice)  # Remove o item da lista
        global quantidades_falhas
        quantidades_falhas.pop(indice)  # Remove o item da lista de quantidades
        atualizar_total_falhas()

# Função para verificar se todos os campos da aba de produção estão preenchidos
def campos_producao_preenchidos():
    data = entry0.get()
    re = entry1.get()
    maquina = combo.get()
    total_produzido = entry2.get()
    cliente = combo2.get()
    pn = combo3.get()
    
    # Verificar se algum campo obrigatório está vazio
    if not (data and re and maquina and total_produzido and cliente and pn):
        return False
    return True
        
#Função para coletar todos os dados da aba de produção e falhas
def coletar_dados():

    #Coletar dados da aba de produção
    data = entry0.get()
    re = entry1.get()
    turno = combo.get()
    maquina = combo1.get()
    total_produzido = entry2.get()
    cliente = combo2.get()
    pn = combo3.get()

    #Coletar dados da aba de falhas
    #total_falhas = total_falhas
    lista_falhas_selecionadas = lista_falhas.get(0, END)

    #Calcular FPY (First Pass Yield)
    def calcular_fpy():
        try:
            total_produzido_int = int(total_produzido)
            total_falhas_int = int(total_falhas)
            fpy_value = ((total_produzido_int - total_falhas_int) / total_produzido_int) * 100
            return round(fpy_value, 2)
        except (ValueError, ZeroDivisionError):
            return "N/A"

    fpy = calcular_fpy()

    #Calcular peças boas
    def calcular_pecas_boas():
        try:
            total_produzido_int = int(total_produzido)
            total_falhas_int = int(total_falhas)
            total_pecas_boas = total_produzido_int - total_falhas_int
            return total_pecas_boas
        except (ValueError):
            return "N/A"

    total_pecas_boas = calcular_pecas_boas()

    #Retornar todos os dados coletados
    falhas_texto = "\n".join(lista_falhas_selecionadas) # Crie uma string para as falhas, onde cada falha está em uma nova linha

    return f'''DATA: {data}\nRE: {re}\nMÁQUINA: {maquina}\nTURNO: {turno}
    \nCLIENTE: {cliente}\nPN: {pn}
    \nTOTAL PRODUZIDO: {total_produzido}\nTOTAL PEÇAS BOAS: {total_pecas_boas}\nTOTAL FALHAS: {total_falhas}\nFPY: {fpy}%
    \nFALHAS: {falhas_texto}
    '''

# Função para exibir a janela de confirmação com os dados coletados
janela_confirmacao = None  # Inicialize a variável global

def exibir_janela_confirmacao():
    global janela_confirmacao  # Declare a variável como global
    
    if campos_producao_preenchidos():
        dados = coletar_dados()

        # Criar uma nova janela de confirmação
        janela_confirmacao = Toplevel()
        janela_confirmacao.title("Conferir Dados")
        
        # Exibir os dados coletados na janela de confirmação
        label_dados = Label(janela_confirmacao, text=dados, padx=10, pady=10)
        label_dados.pack()

        # Botão "OK" para apagar os dados
        botao_ok = Button(janela_confirmacao, text="OK", command=apagar_dados)
        botao_ok.pack(side=LEFT, padx=10, pady=10)

        # Botão "Cancelar" para manter os dados
        botao_cancelar = Button(janela_confirmacao, text="Cancelar", command=janela_confirmacao.destroy)
        botao_cancelar.pack(side=RIGHT, padx=10, pady=10)
        
    else:
        messagebox.showerror("Erro!", "Todos os campos de produção devem ser preenchidos.") 

# Função para zerar o contador de total de falhas
def zerar_total_falhas():
    lbl_total_falhas.config(text='TOTAL FALHAS: 0')
    
# Função para apagar os dados
def apagar_dados():
    entry1.delete(0, END)
    entry2.delete(0, END)
    lista_falhas.delete(0, END)
    combo.set("")  #Limpar o ComboBox de turno
    combo1.set("")  #Limpar o ComboBox de MÁQUINA
    combo2.set("")  #Limpar o ComboBox de cliente
    combo3.set("")  #Limpar o ComboBox de PN
    zerar_total_falhas()  # Zerar o contador de total de falhas
    combo_falhas.set("")  #Limpar o ComboBox de falhas
    janela_confirmacao.destroy()  # Fechar a janela de confirmação
        
# =========== INTERFACE ==========        
# Criar janela
janela = Tk()
janela.title("FPY Injetoras PSS")
janela.geometry('400x400')

# Criar abas
tab_control = ttk.Notebook(janela)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

tab_control.add(tab1, text='PRODUÇÃO')
tab_control.add(tab2, text='FALHAS')
tab_control.add(tab3, text='CHECKLIST')

#primeira aba a ser exibida
tab_control.select(tab3) 
# ======== Aba PRODUÇÃO ====================
#DATA
lbl0 = Label(tab1, text='DATA')  # Use tab1 para colocar o rótulo na aba 'Produção'
lbl0.grid(column=0, row=1, padx=5, pady=5)
entry0 = DateEntry(tab1, date_pattern='dd/mm/yyyy', locale='pt_BR')  # Use tab1 para o DateEntry
entry0.grid(column=1, row=1, padx=5, pady=5)

#RE
lbl1 = Label(tab1, text='RE')
lbl1.grid(column=0, row=2, padx=5, pady=5)
entry1 = Entry(tab1)  
entry1.grid(column=1, row=2, padx=5, pady=5)
entry1.bind('<KeyRelease>', limitar_entrada)

#TURNO
lbl3 = Label(tab1, text='TURNO')
lbl3.grid(column=0, row=3, padx=5, pady=5)
combo = ttk.Combobox(tab1)  
combo['values'] = ('1T', '2T', '3T')
combo.grid(column=1, row=3, padx=5, pady=5)

#MÁQUINA
lbl2 = Label(tab1, text='MÁQUINA')
lbl2.grid(column=0, row=4, padx=5, pady=5)
combo1 = ttk.Combobox(tab1)  
combo1['values'] = ('ENGEL 1', 'ENGEL 2', 'ENGEL 3','ENGEL 4','ENGEL 5','ENGEL 6','ENGEL 7','ENGEL 8','ENGEL 9',
                    'ARBURG 1','ARBURG 2','ARBURG 3')
combo1.grid(column=1, row=4, padx=5, pady=5)
combo1.bind("<<ComboboxSelected>>", atualizar_falhas)

#CLIENTE
lbl4 = Label(tab1, text='CLIENTE')
lbl4.grid(column=0, row=5, padx=5, pady=5)
combo2 = ttk.Combobox(tab1) 
combo2['values'] = ('WSS FIAT', 'WSS RNT', 'GEM','GSE','EA211','GV4')
#combo.current(0)  # Define o item selecionado
combo2.grid(column=1, row=5, padx=5, pady=5)
combo2.bind("<<ComboboxSelected>>", atualizar_opcoes_pn)

#PN
lbl5 = Label(tab1, text='PN')
lbl5.grid(column=0, row=6, padx=5, pady=5)
combo3 = ttk.Combobox(tab1)  
combo3.grid(column=1, row=6, padx=5, pady=5)

#TOTAL PRODUZIDO
lbl6 = Label(tab1, text='TOTAL PRODUZIDO')
lbl6.grid(column=0, row=7, padx=5, pady=5)
entry2 = Entry(tab1)  
entry2.grid(column=1, row=7, padx=5, pady=5)
entry2.bind('<KeyRelease>', limitar_entrada)

# Botão para gravar os dados
botao_gravar = Button(tab1, text="GRAVAR", command=exibir_janela_confirmacao)
botao_gravar.grid(column=0, row=8, columnspan=2, padx=5, pady=5)

#========= Aba FALHAS ===========================
#QTDE
lbl_total_falhas = Label(tab2,text='TOTAL FALHAS: 0')
lbl_total_falhas.grid(column=0, row=1, padx=5, pady=5)

# Falhas na aba Modo de falhas
lbl_falhas = Label(tab2, text='MODO DE FALHA')
lbl_falhas.grid(column=0, row=2, padx=5, pady=5)
combo_falhas = ttk.Combobox(tab2)
combo_falhas.grid(column=1, row=2, padx=5, pady=5)

#QTDE de falhas no Modo de falhas
lbl_quantidade = Label(tab2, text='QUANTIDADE')
lbl_quantidade.grid(column=0, row=3, padx=5, pady=5)
quantidade_entry = Entry(tab2)
quantidade_entry.bind('<KeyRelease>', limitar_entrada)
quantidade_entry.grid(column=1, row=3, padx=5, pady=5)

#Botão para add falhas
adicionar_button = Button(tab2, text='ADICIONAR FALHA', command=adicionar_falha)
adicionar_button.grid(column=1, row=4, padx=5, pady=5)

#Botão para remover o modo de falha selecionado
remover_button = Button(tab2, text='REMOVER FALHA', command=remover_falha_selecionada)
remover_button.grid(column=0, row=4, padx=5, pady=5)

#lista de falhas
lista_falhas = Listbox(tab2, width=30, height=10)
lista_falhas.grid(column=0, row=5, columnspan=3, padx=5, pady=5)

#Barra de rolagem vertical
scrollbar = Scrollbar(janela, orient=VERTICAL, command=lista_falhas.yview)
scrollbar.grid(column=1, row=0,sticky='ns')
lista_falhas.config(yscrollcommand=scrollbar.set) # Conecte a Listbox à barra de rolagem

#=========== Aba CHECKLSIT ==============
#Botão para abrir checklist
checklist_button = Button(tab3, text='ABRIR CHECKLIST')
checklist_button.pack(side='top', padx=5, pady=5)
#checklist_button.grid(column=2, row=4, columnspan=3, padx=5, pady=5)
#=========== INTERFACE ==========
# Usar grid para o tab_control
tab_control.grid(column=0, row=0, sticky='NSEW')

# Crédito
credit_label = tk.Label(janela, text='Desenvolvido por Yara de Oliveira Rufino', font=('Arial', 10), fg='gray')
credit_label.grid(column=0, row=1, sticky='SE', padx=5, pady=5)

janela.mainloop()
