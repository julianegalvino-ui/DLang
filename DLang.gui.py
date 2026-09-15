import tkinter as tk
from tkinter import simpledialog
import io
import sys

import DLang


# ==================================================
# JANELA
# ==================================================

janela = tk.Tk()
janela.title("DLang")
janela.geometry("900x650")


# ==================================================
# TÍTULO DO CÓDIGO
# ==================================================

label_codigo = tk.Label(
    janela,
    text="DLang Code",
    font=("Arial", 11)
)

label_codigo.pack(
    anchor="w",
    padx=10,
    pady=(8, 0)
)


# ==================================================
# ÁREA DO CÓDIGO
# ==================================================

texto_codigo = tk.Text(
    janela,
    font=("Consolas", 12),
    height=18
)

texto_codigo.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=5
)


# ==================================================
# BOTÃO EXECUTE()
# ==================================================

botao_execute = tk.Button(
    janela,
    text="Execute()",
    font=("Consolas", 11),
    height=1,
    command=lambda: executar_codigo()
)

botao_execute.pack(
    fill="x",
    padx=10,
    pady=5
)


# ==================================================
# TERMINAL
# ==================================================

terminal = tk.Text(
    janela,
    bg="black",
    fg="white",
    insertbackground="white",
    font=("Consolas", 11),
    height=10
)

terminal.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=(0, 10)
)


# ==================================================
# TCK
# ==================================================

def executar_tck_gui(pergunta):

    pergunta = pergunta.strip()

    if (
        pergunta.startswith('"')
        and pergunta.endswith('"')
    ) or (
        pergunta.startswith("'")
        and pergunta.endswith("'")
    ):
        pergunta = pergunta[1:-1]

    resposta = simpledialog.askstring(
        "DLang - tck()",
        pergunta,
        parent=janela
    )

    if resposta is None:
        return ""

    return resposta


DLang.executar_tck = executar_tck_gui

def dlang_print_gui(texto):
    terminal.insert("end", str(texto) + "\n")
    terminal.see("end")

DLang.dlang_print = dlang_print_gui


# Hackeando o DLang para escrever no editor de código
def dlang_inserir_codigo_gui(texto):
    texto_codigo.insert("end", texto)
    texto_codigo.see("end")  # Rola para baixo automaticamente

    # ⚠️ A MÁGICA: Se a linha escrita for o <exctDLang>, executa o código sozinho!
    if texto.strip() == "<exctDLang>":
        if not DLang.trava_execucao:
            # Usa um pequeno delay (100ms) para dar tempo do texto aparecer na tela
            janela.after(100, executar_codigo)


DLang.dlang_inserir_codigo = dlang_inserir_codigo_gui

# ==================================================
# ESCREVER NO TERMINAL
# ==================================================

def escrever_terminal(texto):

    terminal.insert(
        "end",
        texto
    )

    terminal.see("end")


# ==================================================
# EXECUTAR DLANG
# ==================================================



def executar_codigo():

    codigo = texto_codigo.get(
        "1.0",
        "end-1c"
    )

    if not codigo.strip():
        escrever_terminal(
            "Err; No DLang code.\n"
        )
        return

    linhas = codigo.splitlines()

    codigo_fonte = []

    # Verifica se existe o comando especial
    limpar_terminal = False

    for linha in linhas:

        # Comando especial da GUI
        if linha.strip() == "<demolish DLang>":
            limpar_terminal = True
            continue

        # execute() continua sendo ignorado pela GUI
        if linha.strip() == "execute()":
            break

        codigo_fonte.append(linha)

    # Se encontrou <demolish DLang>,
    # limpa completamente o terminal
    if limpar_terminal:
        terminal.delete(
            "1.0",
            "end"
        )

    # Limpa memória anterior
    DLang.memoria.clear()
    DLang.funcoes.clear()
    DLang.__retorno__ = None

    # Captura os prints do DLang
    captura = io.StringIO()

    stdout_original = sys.stdout

    try:

        sys.stdout = captura

        DLang.executar_programa(
            codigo_fonte
        )

    except Exception as erro:

        print(
            f"Err; Python exception: {erro}"
        )

    finally:

        sys.stdout = stdout_original

    resultado = captura.getvalue()

    if resultado:
        escrever_terminal(resultado)



# ==================================================
# CTRL + ENTER
# ==================================================

def atalho_execute(event):

    executar_codigo()

    return "break"


texto_codigo.bind(
    "<Control-Return>",
    atalho_execute
)


# ==================================================
# CÓDIGO DE EXEMPLO
# ==================================================

texto_codigo.insert(
    "1.0",
    'pin nde.x = 10\n'
    'show(x)'
)


# ==================================================
# INICIAR
# ==================================================

janela.mainloop()

