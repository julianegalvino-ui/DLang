import tkinter as tk
import sys

# Função que a GUI vai sobrescrever para escrever no editor
def dlang_inserir_codigo(texto):
    pass  # Por padrão não faz nada, a GUI vai mudar isso

# Função que a GUI vai sobrescrever para executar o código
def dlang_executar_tudo():
    pass  # Por padrão não faz nada, a GUI vai mudar isso

memoria = {}
funcoes = {}
__retorno__ = None
trava_execucao = False  # ⚠️ ADICIONE ISSO

def dlang_print(texto):
    sys.stdout.write(str(texto) + "\n")


def interpolar_string(texto):
    """
    Substitui {expressão} pelo valor avaliado da expressão.
    Exemplo: "Meu numero é: {num1 * num2}" → "Meu numero é: 42"
    """
    resultado = texto
    while "{" in resultado and "}" in resultado:
        inicio = resultado.index("{")
        fim = resultado.index("}", inicio)
        expressao = resultado[inicio + 1:fim].strip()

        # Avalia a expressão
        valor, tipo = avaliar_expressao_completa(expressao)
        if tipo == "error":
            return f"Err; {valor}"

        # Substitui na string
        resultado = resultado[:inicio] + str(valor) + resultado[fim + 1:]

    return resultado

def executar_com_pybt(bloco_codigo):
    """Executa código com <pybt> trazendo os comandos de volta ao nível principal"""
    for linha in bloco_codigo:
        linha = linha.strip()
        if linha.startswith("<pybt>"):
            comando = linha[6:].strip()
            executar(comando)
        else:
            executar(linha)


# ==================================================
# JANELAS (GUI)
# ==================================================

def processar_window(linha, bloco_codigo):
    conteudo = linha[7:-1].strip()
    titulo = conteudo
    largura = 500
    altura = 300
    widgets_pendentes = []

    i = 0
    while i < len(bloco_codigo):
        item = bloco_codigo[i].strip()

        if item.startswith("title ="):
            valor = item[7:].strip()
            if (valor.startswith('"') and valor.endswith('"')):
                titulo = valor[1:-1]
            else:
                titulo = valor
        elif item.startswith("size ="):
            partes = item[6:].strip().split(",")
            if len(partes) == 2:
                try:
                    largura = int(partes[0].strip())
                    altura = int(partes[1].strip())
                except ValueError:
                    pass
        elif item.startswith("label "):
            nome_label = item[6:-1].strip()
            props = {"type": "label", "name": nome_label, "text": "", "x": 10, "y": 10, "color": "black"}
            i += 1
            while i < len(bloco_codigo) and bloco_codigo[i].strip().startswith("--"):
                prop = bloco_codigo[i].strip()[2:]
                if prop.startswith("text ="):
                    val = prop[6:].strip()
                    if val.startswith('"') and val.endswith('"'):
                        val = val[1:-1]
                    props["text"] = val
                elif prop.startswith("position ="):
                    coords = prop[10:].strip().split(",")
                    props["x"] = int(coords[0].strip())
                    props["y"] = int(coords[1].strip())
                elif prop.startswith("color ="):
                    props["color"] = prop[7:].strip()
                i += 1
            widgets_pendentes.append(props)
            continue
        elif item.startswith("button "):
            nome_btn = item[7:-1].strip()
            props = {"type": "button", "name": nome_btn, "text": "Button", "x": 10, "y": 10, "command_block": []}
            i += 1
            while i < len(bloco_codigo) and bloco_codigo[i].strip().startswith("--"):
                prop = bloco_codigo[i].strip()[2:]
                if prop.startswith("text ="):
                    val = prop[6:].strip()
                    if val.startswith('"') and val.endswith('"'):
                        val = val[1:-1]
                    props["text"] = val
                elif prop.startswith("position ="):
                    coords = prop[10:].strip().split(",")
                    props["x"] = int(coords[0].strip())
                    props["y"] = int(coords[1].strip())
                elif prop.startswith("command:"):
                    i += 1
                    while i < len(bloco_codigo) and bloco_codigo[i].strip().startswith("--"):
                        cmd = bloco_codigo[i].strip()
                        while cmd.startswith("--"):
                            cmd = cmd[2:]
                        props["command_block"].append(cmd)
                        i += 1
                    continue
                i += 1
            widgets_pendentes.append(props)
            continue
        i += 1

    janela = tk.Toplevel()
    janela.title(titulo)
    janela.geometry(f"{largura}x{altura}")

    for w in widgets_pendentes:
        if w["type"] == "label":
            lbl = tk.Label(janela, text=w["text"], fg=w["color"], font=("Arial", 10))
            lbl.place(x=w["x"], y=w["y"])
        elif w["type"] == "button":
            bloco_cmd = w["command_block"]
            def acao(b=bloco_cmd):
                # ⚠️ AQUI ESTÁ A MÁGICA: Para cada linha do botão, chama dlang_inserir_codigo
                for linha in b:
                    dlang_inserir_codigo(linha + "\n")
            btn = tk.Button(janela, text=w["text"], command=acao, font=("Arial", 10))
            btn.place(x=w["x"], y=w["y"])


# ==================================================
# ENTRADA E VALIDAÇÃO
# ==================================================

def executar_tck(pergunta_str):
    pergunta = pergunta_str.strip()
    if ((pergunta.startswith('"') and pergunta.endswith('"')) or
            (pergunta.startswith("'") and pergunta.endswith("'"))):
        pergunta = pergunta[1:-1]
    return input(pergunta)


def validar_e_converter(valor_str, tipo):
    valor_str = valor_str.strip()
    if valor_str == "vaco":
        return "vaco", None
    if valor_str == "":
        return "hollow", None

    if tipo == "nde":
        if "." in valor_str:
            return None, f'Err; "{valor_str}" is not an nde. my friend'
        try:
            return int(valor_str), None
        except ValueError:
            return None, f'Err; "{valor_str}" is not an nde. my friend'
    elif tipo == "dec":
        try:
            return float(valor_str), None
        except ValueError:
            return None, f'Err; "{valor_str}" is not a dec. my friend'
    elif tipo == "chr":
        try:
            float(valor_str)
            return None, f'Err; "{valor_str}" is not a chr. my friend'
        except ValueError:
            pass
        if ((valor_str.startswith('"') and valor_str.endswith('"')) or
                (valor_str.startswith("'") and valor_str.endswith("'"))):
            valor_str = valor_str[1:-1]
        return valor_str, None
    else:
        try:
            if "." in valor_str:
                return float(valor_str), None
            return int(valor_str), None
        except ValueError:
            if ((valor_str.startswith('"') and valor_str.endswith('"')) or
                    (valor_str.startswith("'") and valor_str.endswith("'"))):
                valor_str = valor_str[1:-1]
            return valor_str, None


def eh_comando(valor_str):
    valor_str = valor_str.strip()
    comandos_conhecidos = ["show(", "pin "]
    for cmd in comandos_conhecidos:
        if valor_str.startswith(cmd):
            return True
    return False


# ==================================================
# PARSER DE EXPRESSÕES
# ==================================================

def tokenizar_expressao_completa(expr):
    tokens = []
    atual = ""
    dentro_aspas = False
    aspas_char = None

    for char in expr:
        if char in ('"', "'") and not dentro_aspas:
            dentro_aspas = True
            aspas_char = char
            atual += char
        elif char == aspas_char and dentro_aspas:
            dentro_aspas = False
            aspas_char = None
            atual += char
        elif char in ("+", "-", "*", "/", "(", ")") and not dentro_aspas:
            if atual.strip():
                tokens.append(atual.strip())
            tokens.append(char)
            atual = ""
        else:
            atual += char

    if atual.strip():
        tokens.append(atual.strip())
    return tokens


def resolver_operando(token):
    if ((token.startswith('"') and token.endswith('"')) or
            (token.startswith("'") and token.endswith("'"))):
        return token[1:-1], "chr"
    if token == "vaco":
        return "vaco", "vaco"

    if "(" in token and token.endswith(")"):
        idx = token.index("(")
        nome_func = token[:idx].strip()
        args_str = token[idx + 1:-1].strip()
        if nome_func in funcoes:
            args = [] if args_str == "" else [a.strip() for a in args_str.split(",")]
            resultado = executar_funcao(nome_func, args)
            if resultado is None:
                return None, "unknown"
            return resultado, inferir_tipo(resultado)

    try:
        if "." in token:
            return float(token), "dec"
        return int(token), "nde"
    except ValueError:
        pass

    if token in memoria:
        var = memoria[token]
        if var["valor"] == "hollow":
            return None, "hollow"
        return var["valor"], var["tipo"]
    return None, "unknown"


def inferir_tipo(valor):
    if isinstance(valor, int):
        return "nde"
    elif isinstance(valor, float):
        return "dec"
    elif isinstance(valor, str):
        return "chr"
    return "unknown"


def avaliar_expressao_completa(expr):
    tokens = tokenizar_expressao_completa(expr)
    if not tokens:
        return "", None
    pos = [0]

    def parse_expression():
        left = parse_term()
        if left[1] == "error":
            return left
        while pos[0] < len(tokens) and tokens[pos[0]] in ("+", "-"):
            op = tokens[pos[0]]
            pos[0] += 1
            right = parse_term()
            if right[1] == "error":
                return right
            if op == "+":
                if isinstance(left[0], str) or isinstance(right[0], str):
                    left = (str(left[0]) + str(right[0]), "chr")
                else:
                    result = left[0] + right[0]
                    left = (result, "dec" if isinstance(result, float) else "nde")
            else:
                result = left[0] - right[0]
                left = (result, "dec" if isinstance(result, float) else "nde")
        return left

    def parse_term():
        left = parse_factor()
        if left[1] == "error":
            return left
        while pos[0] < len(tokens) and tokens[pos[0]] in ("*", "/"):
            op = tokens[pos[0]]
            pos[0] += 1
            right = parse_factor()
            if right[1] == "error":
                return right
            if op == "*":
                result = left[0] * right[0]
                left = (result, "dec" if isinstance(result, float) else "nde")
            else:
                if right[0] == 0:
                    return "Err; Division by zero.", "error"
                result = left[0] / right[0]
                left = (result, "dec")
        return left

    def parse_factor():
        if pos[0] >= len(tokens):
            return "Err; Unexpected end of expression.", "error"
        token = tokens[pos[0]]

        if pos[0] + 1 < len(tokens) and tokens[pos[0] + 1] == "(":
            profundidade = 0
            inicio = pos[0]
            for j in range(pos[0], len(tokens)):
                if tokens[j] == "(":
                    profundidade += 1
                elif tokens[j] == ")":
                    profundidade -= 1
                    if profundidade == 0:
                        token = "".join(tokens[inicio:j + 1])
                        pos[0] = j + 1
                        valor, tipo = resolver_operando(token)
                        if tipo == "hollow":
                            return "Err; Variable is hollow.", "error"
                        if valor is None and tipo == "unknown":
                            return "Err; Unknown variable or function.", "error"
                        return valor, tipo

        if token == "(":
            pos[0] += 1
            result = parse_expression()
            if pos[0] < len(tokens) and tokens[pos[0]] == ")":
                pos[0] += 1
            else:
                return "Err; Missing closing parenthesis.", "error"
            return result

        pos[0] += 1
        valor, tipo = resolver_operando(token)
        if tipo == "hollow":
            return f'Err; The variable "{token}" is hollow.', "error"
        if valor is None and tipo == "unknown":
            return f'Err; The variable "{token}" does not exist.', "error"
        return valor, tipo

    return parse_expression()


# ==================================================
# FUNÇÕES DO USUÁRIO
# ==================================================

def executar_funcao(nome, args_valores):
    global __retorno__
    func = funcoes[nome]
    params = func["params"]
    bloco = func["bloco"]

    if len(args_valores) != len(params):
        print(f'Err; Function "{nome}" expects {len(params)} arguments, got {len(args_valores)}.')
        return None

    backup = {}
    for p in params:
        if p in memoria:
            backup[p] = memoria[p]

    for i, p in enumerate(params):
        arg = args_valores[i].strip()
        valor, tipo = resolver_operando(arg)
        if valor is None and tipo not in ("vaco",):
            resultado, tipo_expr = avaliar_expressao_completa(arg)
            if tipo_expr == "error":
                print(resultado)
                return None
            memoria[p] = {"tipo": tipo_expr, "valor": resultado}
        else:
            memoria[p] = {"tipo": tipo if tipo else "unknown", "valor": valor}

    __retorno__ = None
    executar_bloco(bloco)
    resultado = __retorno__

    for p in params:
        if p in backup:
            memoria[p] = backup[p]
        elif p in memoria:
            del memoria[p]
    return resultado


# ==================================================
# PIN E ATRIBUIÇÃO
# ==================================================

def processar_pin(linha):
    if "=" not in linha:
        print("Err; Invalid pin.")
        return

    partes = linha.split("=", 1)
    lado_esq = partes[0].strip()
    lado_dir = partes[1].strip()

    if "." in lado_esq:
        partes_nome = lado_esq.split(".", 1)
        tipo = partes_nome[0].strip()
        nome = partes_nome[1].strip()
        if not tipo or not nome:
            print("Err; Invalid pin.")
            return
    else:
        tipo = None
        nome = lado_esq

    if nome == "":
        print("Err; Invalid pin.")
        return

    if lado_dir.startswith("tck(") and lado_dir.endswith(")"):
        pergunta = lado_dir[4:-1]
        resposta = executar_tck(pergunta)
        try:
            if "." in resposta:
                valor_final = float(resposta)
                tipo_inferido = "dec"
            else:
                valor_final = int(resposta)
                tipo_inferido = "nde"
        except ValueError:
            valor_final = resposta
            tipo_inferido = "chr"
        memoria[nome] = {"tipo": tipo_inferido, "valor": valor_final}
        return

    if eh_comando(lado_dir):
        memoria[nome] = {"tipo": "command", "valor": lado_dir}
        return

    if lado_dir == "":
        memoria[nome] = {"tipo": tipo if tipo else "unknown", "valor": "hollow"}
        return

    tem_operador = any(op in lado_dir for op in ("+", "-", "*", "/"))
    tem_parenteses = "(" in lado_dir or ")" in lado_dir
    tem_funcao = any(f + "(" in lado_dir for f in funcoes)

    if tem_operador or tem_parenteses or tem_funcao:
        resultado, tipo_resultado = avaliar_expressao_completa(lado_dir)
        if tipo_resultado == "error":
            print(resultado)
            return
        if tipo:
            valor_convertido, erro = validar_e_converter(str(resultado), tipo)
            if erro:
                print(erro)
                return
            memoria[nome] = {"tipo": tipo, "valor": valor_convertido}
        else:
            memoria[nome] = {"tipo": tipo_resultado, "valor": resultado}
        return

    valor_convertido, erro = validar_e_converter(lado_dir, tipo)
    if erro:
        print(erro)
        return
    memoria[nome] = {"tipo": tipo if tipo else "unknown", "valor": valor_convertido}


def processar_atribuicao_direta(linha):
    partes = linha.split("=", 1)
    nome = partes[0].strip()
    valor = partes[1].strip()

    if not (valor.startswith("tck(") and valor.endswith(")")):
        print("Err; Unknown command.")
        return

    pergunta = valor[4:-1]
    resposta = executar_tck(pergunta)
    try:
        if "." in resposta:
            valor_final = float(resposta)
            tipo_inferido = "dec"
        else:
            valor_final = int(resposta)
            tipo_inferido = "nde"
    except ValueError:
        valor_final = resposta
        tipo_inferido = "chr"
    memoria[nome] = {"tipo": tipo_inferido, "valor": valor_final}


# ==================================================
# SHOW E CONDIÇÕES
# ==================================================

def avaliar_expressao_show(expr):
    resultado, tipo = avaliar_expressao_completa(expr)
    if tipo == "error":
        return resultado
    return str(resultado)


def processar_show(linha):
    conteudo = linha.strip()
    if conteudo.startswith("tck(") and conteudo.endswith(")"):
        pergunta = conteudo[4:-1]
        resposta = executar_tck(pergunta)
        print(resposta)
        return
    saida = avaliar_expressao_show(conteudo)
    if saida.startswith("Err;"):
        print(saida)
    else:
        print(saida)


def avaliar_condicao_if(condicao):
    condicao = condicao.strip()
    operadores = [">=", "<=", "=/", "==", ">", "<"]
    operador_encontrado = None

    for op in operadores:
        if op in condicao:
            operador_encontrado = op
            partes = condicao.split(op, 1)
            break

    if not operador_encontrado:
        print("Err; Invalid if condition.")
        return False

    lado_esq = partes[0].strip()
    lado_dir = partes[1].strip()

    if lado_esq not in memoria:
        print(f'Err; The variable "{lado_esq}" does not exist.')
        return False

    var_esq = memoria[lado_esq]
    valor_esq = var_esq["valor"]
    tipo_esq = var_esq["tipo"]

    if valor_esq == "hollow":
        print(f'Err; The variable "{lado_esq}" is hollow.')
        return False

    if lado_dir in ("nde", "dec", "chr"):
        if operador_encontrado == "==":
            return tipo_esq == lado_dir
        elif operador_encontrado == "=/":
            return tipo_esq != lado_dir
        else:
            print(f"Err; Cannot use {operador_encontrado} with types.")
            return False

    if lado_dir in memoria:
        var_dir = memoria[lado_dir]
        valor_dir = var_dir["valor"]
        if valor_dir == "hollow":
            print(f'Err; The variable "{lado_dir}" is hollow.')
            return False
    else:
        try:
            if "." in lado_dir:
                valor_dir = float(lado_dir)
            else:
                valor_dir = int(lado_dir)
        except ValueError:
            if ((lado_dir.startswith('"') and lado_dir.endswith('"')) or
                    (lado_dir.startswith("'") and lado_dir.endswith("'"))):
                valor_dir = lado_dir[1:-1]
            else:
                valor_dir = lado_dir

    try:
        if operador_encontrado == "==":
            return valor_esq == valor_dir
        elif operador_encontrado == "=/":
            return valor_esq != valor_dir
        elif operador_encontrado == ">":
            return valor_esq > valor_dir
        elif operador_encontrado == "<":
            return valor_esq < valor_dir
        elif operador_encontrado == ">=":
            return valor_esq >= valor_dir
        elif operador_encontrado == "<=":
            return valor_esq <= valor_dir
    except TypeError:
        print(f'Err; Cannot compare {tipo_esq} with {type(valor_dir).__name__}.')
        return False
    return False


# ==================================================
# TRANSFORMADOR, REPEAT, RUN, RET
# ==================================================

def processar_transformador(linha):
    partes = linha.split(">>")
    if len(partes) != 2:
        print("Err; Invalid transformador.")
        return
    nome_var = partes[0].strip()
    lado_dir = partes[1].strip()

    if nome_var not in memoria:
        print(f'Err; The variable "{nome_var}" does not exist.')
        return

    var = memoria[nome_var]
    valor_atual = var["valor"]
    tipo_atual = var["tipo"]

    if lado_dir in ("nde", "dec", "chr"):
        if valor_atual == "hollow":
            print(f'Err; The variable "{nome_var}" is hollow.')
            return
        if valor_atual == "vaco":
            memoria[nome_var] = {"tipo": lado_dir, "valor": "vaco"}
            return
        try:
            if lado_dir == "nde":
                if isinstance(valor_atual, str):
                    if "." in valor_atual:
                        print(f'Err; Cannot convert "{valor_atual}" to nde.')
                        return
                    novo_valor = int(valor_atual)
                else:
                    novo_valor = int(valor_atual)
            elif lado_dir == "dec":
                novo_valor = float(valor_atual)
            else:
                novo_valor = str(valor_atual)
            memoria[nome_var] = {"tipo": lado_dir, "valor": novo_valor}
        except (ValueError, TypeError):
            print(f'Err; Cannot convert "{valor_atual}" to {lado_dir}.')
        return

    novo_valor, novo_tipo = resolver_operando(lado_dir)
    if novo_valor is None and novo_tipo == "unknown":
        novo_valor, novo_tipo = avaliar_expressao_completa(lado_dir)
        if novo_tipo == "error":
            print(novo_valor)
            return
    if novo_valor is None and novo_tipo == "unknown":
        novo_valor = lado_dir
        novo_tipo = "chr"

    if tipo_atual != "unknown":
        valor_str = str(novo_valor)
        valor_convertido, erro = validar_e_converter(valor_str, tipo_atual)
        if erro:
            print(erro)
            return
        memoria[nome_var] = {"tipo": tipo_atual, "valor": valor_convertido}
    else:
        memoria[nome_var] = {"tipo": novo_tipo, "valor": novo_valor}


def processar_repeat(linha, bloco_codigo=None):
    conteudo = linha[7:].strip()
    if conteudo.startswith("while "):
        condicao = conteudo[6:].strip()
        if not condicao.endswith(":"):
            print("Err; Invalid repeat while syntax.")
            return
        condicao = condicao[:-1].strip()
        max_iteracoes = 10000
        iteracao = 0
        while avaliar_condicao_if(condicao):
            if bloco_codigo:
                executar_bloco(bloco_codigo)
            iteracao += 1
            if iteracao >= max_iteracoes:
                print("Err; Maximum iterations reached.")
                break
        return

    if "(" in conteudo and ")" in conteudo:
        partes = conteudo.split("(")
        nome_var = partes[0].strip()
        vezes_str = partes[1].replace(")", "").strip()
        try:
            vezes = int(vezes_str)
        except ValueError:
            print(f'Err; "{vezes_str}" is not a valid number.')
            return
    else:
        nome_var = conteudo.strip()
        vezes = -1

    if nome_var not in memoria:
        print(f'Err; The variable "{nome_var}" does not exist.')
        return
    var = memoria[nome_var]
    if var["valor"] == "hollow":
        print(f'Err; The variable "{nome_var}" is hollow.')
        return

    if var["tipo"] == "command":
        comando = var["valor"]
        if vezes == -1:
            try:
                while True:
                    executar(comando)
            except KeyboardInterrupt:
                print("\n[Repeat interrompido]")
        else:
            for _ in range(vezes):
                executar(comando)
    else:
        valor = str(var["valor"])
        if vezes == -1:
            try:
                while True:
                    print(valor)
            except KeyboardInterrupt:
                print("\n[Repeat interrompido]")
        else:
            for _ in range(vezes):
                print(valor)


def processar_run(linha):
    nome_var = linha[4:].strip()
    if nome_var not in memoria:
        print(f'Err; The variable "{nome_var}" does not exist.')
        return
    var = memoria[nome_var]
    if var["tipo"] != "command":
        print(f'Err; The variable "{nome_var}" is not a command.')
        return
    executar(var["valor"])


def processar_ret(linha):
    global __retorno__
    valor_str = linha[4:].strip()
    resultado, tipo = avaliar_expressao_completa(valor_str)
    if tipo == "error":
        print(resultado)
        return
    __retorno__ = resultado


# ==================================================
# MEMÓRIA (DEMOLISH E COLLAPSE)
# ==================================================

def processar_demolish(linha):
    conteudo = linha[9:].strip()
    if conteudo == "":
        print("Err; Nothing to demolish.")
        return
    nome_var = conteudo
    if nome_var not in memoria:
        print(f'Err; The variable "{nome_var}" does not exist.')
        return
    memoria[nome_var]["valor"] = "vaco"


def processar_collapse(linha):
    conteudo = linha[9:].strip()
    if conteudo == "":
        print("Err; Nothing to collapse.")
        return
    nome_var = conteudo
    if nome_var not in memoria:
        print(f'Err; The variable "{nome_var}" does not exist.')
        return
    del memoria[nome_var]


# ==================================================
# ROTEADOR PRINCIPAL
# ==================================================

def executar(linha, bloco_codigo=None):
    linha = linha.strip()
    if not linha:
        return

    # ⚠️ Se a linha começa com <pybt>, processa interpolação primeiro
    if linha.startswith("<pybt>"):
        linha = linha[6:].strip()  # Remove o <pybt>

        # Interpola todas as strings na linha
        # Procura por strings entre aspas e interpola elas
        nova_linha = ""
        dentro_aspas = False
        aspas_char = None
        string_atual = ""

        for char in linha:
            if char in ('"', "'") and not dentro_aspas:
                dentro_aspas = True
                aspas_char = char
                string_atual = char
            elif char == aspas_char and dentro_aspas:
                dentro_aspas = False
                string_atual += char
                # Interpola a string
                if "{" in string_atual:
                    string_interpolada = interpolar_string(string_atual[1:-1])
                    if string_interpolada.startswith("Err;"):
                        dlang_print(string_interpolada)
                        return
                    nova_linha += '"' + string_interpolada + '"'
                else:
                    nova_linha += string_atual
                string_atual = ""
                aspas_char = None
            elif dentro_aspas:
                string_atual += char
            else:
                nova_linha += char

        linha = nova_linha

    # Agora processa a linha normalmente
    if linha == "pin":
        dlang_print("Err; Nothing to pin. It's vaco.")
    elif linha.startswith("pin "):
        processar_pin(linha[4:])
    elif linha.startswith("show(") and linha.endswith(")"):
        processar_show(linha[5:-1])
    elif linha.startswith("repeat:"):
        processar_repeat(linha, bloco_codigo)
    elif linha.startswith("run "):
        processar_run(linha)
    elif linha.startswith("ret "):
        processar_ret(linha)
    elif linha.startswith("demolish:"):
        processar_demolish(linha)
    elif linha.startswith("collapse:"):
        processar_collapse(linha)
    elif ">>" in linha:
        processar_transformador(linha)
    elif "=" in linha and not linha.startswith("pin ") and not linha.startswith("show("):
        processar_atribuicao_direta(linha)
    else:
        dlang_print("Err; Unknown command.")

# ==================================================
# BLOCOS E INDENTAÇÃO
# ==================================================

def remover_um_nivel_indentacao(linha):
    linha_stripped = linha.strip()
    if linha_stripped.startswith("--"):
        return linha_stripped[2:]
    return linha_stripped


def coletar_bloco_indentado(codigo_fonte, i):
    bloco = []
    while i < len(codigo_fonte):
        proxima_linha = codigo_fonte[i].strip()
        if proxima_linha.startswith("--"):
            bloco.append(remover_um_nivel_indentacao(proxima_linha))
            i += 1
        else:
            break
    return bloco, i


def processar_fn(linha, codigo_fonte, i):
    conteudo = linha[3:-1].strip()
    if "(" not in conteudo or ")" not in conteudo:
        print("Err; Invalid function definition.")
        return i
    idx_abre = conteudo.index("(")
    idx_fecha = conteudo.index(")")
    nome = conteudo[:idx_abre].strip()
    params_str = conteudo[idx_abre + 1:idx_fecha].strip()
    params = [] if params_str == "" else [p.strip() for p in params_str.split(",")]
    i += 1
    bloco, i = coletar_bloco_indentado(codigo_fonte, i)
    funcoes[nome] = {"params": params, "bloco": bloco}
    return i


def validar_comentario(codigo_fonte, i):
    linha = codigo_fonte[i].strip()
    if not linha.startswith("#"):
        return True
    if i > 0 and codigo_fonte[i - 1].strip() != "":
        print(f'Err; Comment at line {i + 1} needs an empty line before it.')
        return False
    if i < len(codigo_fonte) - 1 and codigo_fonte[i + 1].strip() != "":
        print(f'Err; Comment at line {i + 1} needs an empty line after it.')
        return False
    return True


# ==================================================
# EXECUÇÃO DE BLOCOS (COM IF, IFAT E ELSE)
# ==================================================

def executar_bloco(bloco_linhas):
    i = 0
    while i < len(bloco_linhas):
        linha = bloco_linhas[i].strip()

        if not linha:
            i += 1
            continue

        if linha.startswith("#"):
            if not validar_comentario(bloco_linhas, i):
                return
            i += 1
            continue

        # LÓGICA DE IF, IFAT E ELSE (Refatorada e à prova de falhas)
        if linha.startswith("if ") and linha.endswith(":"):
            cadeias = []
            condicao_atual = linha[3:-1]
            i += 1
            bloco_atual, i = coletar_bloco_indentado(bloco_linhas, i)
            cadeias.append((condicao_atual, bloco_atual))

            # Coleta todos os ifat e else que vierem em seguida
            while i < len(bloco_linhas):
                proxima = bloco_linhas[i].strip()
                if proxima.startswith("ifat ") and proxima.endswith(":"):
                    cond_ifat = proxima[5:-1]
                    i += 1
                    bloco_ifat, i = coletar_bloco_indentado(bloco_linhas, i)
                    cadeias.append((cond_ifat, bloco_ifat))
                elif proxima == "else:":
                    i += 1
                    bloco_else, i = coletar_bloco_indentado(bloco_linhas, i)
                    cadeias.append((None, bloco_else))
                else:
                    break

            # Avalia a cadeia e executa apenas o bloco correto
            for cond, bloco in cadeias:
                if cond is None:
                    executar_bloco(bloco)
                    break
                else:
                    if avaliar_condicao_if(cond):
                        executar_bloco(bloco)
                        break

        elif linha.startswith("fn ") and linha.endswith(":"):
            i = processar_fn(linha, bloco_linhas, i)

        elif linha.startswith("window ") and linha.endswith(":"):
            i += 1
            bloco_window, i = coletar_bloco_indentado(bloco_linhas, i)
            processar_window(linha, bloco_window)

        elif linha.startswith("repeat while ") and linha.endswith(":"):
            condicao = linha[13:-1].strip()
            i += 1
            bloco_repeat, i = coletar_bloco_indentado(bloco_linhas, i)
            max_iteracoes = 10000
            iteracao = 0
            while avaliar_condicao_if(condicao):
                executar_bloco(bloco_repeat)
                iteracao += 1
                if iteracao >= max_iteracoes:
                    print("Err; Maximum iterations reached.")
                    break
        else:
            executar(linha)
            i += 1


# ==================================================
# PROGRAMA E MAIN
# ==================================================

def executar_programa(codigo_fonte):
    global trava_execucao

    # ⚠️ Se já estiver executando, não faz nada (evita o vírus)
    if trava_execucao:
        return

    trava_execucao = True  # Trava a execução

    try:
        while codigo_fonte and codigo_fonte[-1].strip() == "":
            codigo_fonte.pop()
        executar_bloco(codigo_fonte)
    except Exception as e:
        dlang_print(f"Err; Python exception: {e}")
    finally:
        trava_execucao = False  # Destrava quando terminar

