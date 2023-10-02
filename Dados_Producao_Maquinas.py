from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox

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

#Dicionário que mapeia cod de acordo com o cliente
cliente_cod = {'CLIENTE 1': ['1234','4567','8901','2345','6789'],
             'CLIENTE 2': ['1111','2222'],
             'CLIENTE 3': ['2110','2111','2112'],
             'CLIENTE 4': ['9994','8884']
}

def atualizar_opcoes_cod(event):
    cliente_selecionado = combo2.get()
    if cliente_selecionado in cliente_cod:
        cod = cliente_cod[cliente_selecionado]
    else:
        cod = []
     
    # Atualize as opções do combobox de cod
    combo3['values'] = cod
    combo3.set('')  # Limpe a seleção atual
        
#Dicionário que mapeia máquinas às suas falhas
maquinas_e_falhas = {
    'MAQUINA 1': ['Falha A', 'Falha B', 'Falha C'],
    'MAQUINA 2': ['Falha D', 'Falha E', 'Falha F'],
    'MAQUINA 3': ['Falha W', 'Falha Y', 'Falha Z'],
    'MAQUINA 4': ['Falha G', 'Falha H', 'Falha I'],
    'MAQUINA 5': ['Falha J', 'Falha K', 'Falha L'],
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
    combo_falhas.set('')  # Limpe a seleção atual
    
#Função para adicionar a falha selecionada com a quantidade especificada
quantidades_falhas = []
def adicionar_falha():
    falha_selecionada = combo_falhas.get()
    quantidade = quantidade_entry.get()    
    
    if falha_selecionada and quantidade:
        falha_com_quantidade = f"{falha_selecionada} (Qtde: {quantidade})"
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
    mat = entry1.get()
    maquina = combo.get()
    total_produzido = entry2.get()
    cliente = combo2.get()
    cod = combo3.get()
    
    # Verificar se algum campo obrigatório está vazio
    if not (data and mat and maquina and total_produzido and cliente and cod):
        return False
    return True
        
#Função para coletar todos os dados da aba de produção e falhas
def coletar_dados():
    if campos_producao_preenchidos():
        #Coletar dados da aba de produção
        data = entry0.get()
        mat = entry1.get()
        maquina = combo.get()
        total_produzido = entry2.get()
        cliente = combo2.get()
        cod = combo3.get()

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

        return f'''DATA: {data}\nMATRICULA: {mat}\nMÁQUINA: {maquina}\nCLIENTE: {cliente}\nCODIGO: {cod}
        \nTOTAL PRODUZIDO: {total_produzido}\nTOTAL PEÇAS BOAS: {total_pecas_boas}\nFALHAS: {falhas_texto}\nTOTAL FALHAS: {total_falhas}
        \nFPY: {fpy}%'''
            
    else:
        messagebox.showerror("Erro", "Todos os campos de produção devem ser preenchidos.") 

# Função para exibir a janela de confirmação com os dados coletados
janela_confirmacao = None  # Inicialize a variável global

def exibir_janela_confirmacao():
    global janela_confirmacao  # Declare a variável como global
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

# Função para apagar os dados
def apagar_dados():
    entry1.delete(0, END)
    entry2.delete(0, END)
    lista_falhas.delete(0, END)
    combo.set("")  #Limpar o ComboBox de turno
    combo1.set("")  #Limpar o ComboBox de MÁQUINA
    combo2.set("")  #Limpar o ComboBox de cliente
    combo3.set("")  #Limpar o ComboBox de cod
    combo_falhas.set("")  #Limpar o ComboBox de falhas
    janela_confirmacao.destroy()  # Fechar a janela de confirmação
        
# =========== INTERFACE ==========        
# Criar janela
janela = Tk()
janela.title("PRODUÇÃO MAQUINAS")
janela.geometry('400x400')

# Criar abas
tab_control = ttk.Notebook(janela)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text='PRODUÇÃO')
tab_control.add(tab2, text='FALHAS')

# ======== Aba PRODUÇÃO ====================
#DATA
lbl0 = Label(tab1, text='DATA')  # Use tab1 para colocar o rótulo na aba 'Produção'
lbl0.grid(column=0, row=1, padx=5, pady=5)
entry0 = DateEntry(tab1, date_pattern='dd/mm/yyyy', locale='pt_BR')  # Use tab1 para o DateEntry
entry0.grid(column=1, row=1, padx=5, pady=5)

#Matricula
lbl1 = Label(tab1, text='MATRICULA')
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
combo1['values'] = ('MAQUINA 1', 'MAQUINA 2', 'MAQUINA 3','MAQUINA 4','MAQUINA 5')
combo1.grid(column=1, row=4, padx=5, pady=5)
combo1.bind("<<ComboboxSelected>>", atualizar_falhas)

#CLIENTE
lbl4 = Label(tab1, text='CLIENTE')
lbl4.grid(column=0, row=5, padx=5, pady=5)
combo2 = ttk.Combobox(tab1) 
combo2['values'] = ('CLIENTE 1', 'CLIENTE 2', 'CLIENTE 3','CLIENTE 4')
#combo.current(0)  # Define o item selecionado
combo2.grid(column=1, row=5, padx=5, pady=5)
combo2.bind("<<ComboboxSelected>>", atualizar_opcoes_cod)

#cod
lbl5 = Label(tab1, text='CODIGO')
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
quantidade_entry.grid(column=1, row=3, padx=5, pady=5)

#Botão para add falhas
adicionar_button = Button(tab2, text='ADICIONAR FALHA', command=adicionar_falha)
adicionar_button.grid(column=1, row=4, padx=5, pady=5)

# Botão para remover o modo de falha selecionado
remover_button = Button(tab2, text='REMOVER FALHA', command=remover_falha_selecionada)
remover_button.grid(column=0, row=4, padx=5, pady=5)

#lista de falhas
lista_falhas = Listbox(tab2)
lista_falhas.grid(column=0, row=5, columnspan=3, padx=5, pady=5)

# Usar grid para o tab_control
tab_control.grid(column=0, row=0, sticky='NSEW')

janela.mainloop()
