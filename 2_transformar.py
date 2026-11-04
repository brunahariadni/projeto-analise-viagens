
from datetime import datetime
from decimal import Decimal, InvalidOperation

from banco import conectar
from config import TAMANHO_BLOCO


def limpar_texto(valor):
    """Transforma textos vazios em None e remove espaços externos."""
    if valor is None:
        return None

    valor = valor.strip()

    return valor if valor else None


def converter_decimal(valor):
    """Converte números no formato brasileiro para Decimal."""
    valor = limpar_texto(valor)

    if valor is None:
        return None

    valor = valor.replace("R$", "").replace(" ", "")

    if "," in valor:
        valor = valor.replace(".", "").replace(",", ".")

    try:
        return Decimal(valor).quantize(Decimal("0.01"))
    except InvalidOperation:
        return None


def converter_data(valor):
    """Converte datas DD/MM/AAAA para o formato DATE."""
    valor = limpar_texto(valor)

    if valor is None:
        return None

    try:
        return datetime.strptime(valor, "%d/%m/%Y").date()
    except ValueError:
        return None


def converter_inteiro(valor):
    """Converte textos numéricos para inteiro."""
    valor = limpar_texto(valor)

    if valor is None:
        return None

    try:
        return int(Decimal(valor))
    except InvalidOperation:
        return None


def limpar_tabelas_silver(conexao):
    """Limpa as tabelas Silver respeitando as chaves estrangeiras."""
    cursor = conexao.cursor()

    tabelas = [
        "silver_trecho",
        "silver_passagem",
        "silver_pagamento",
        "silver_viagem",
    ]

    for tabela in tabelas:
        cursor.execute(f"DELETE FROM {tabela}")
        print(f"Tabela {tabela} limpa.")

    conexao.commit()
    cursor.close()


def transformar_viagem(linha):
    """Prepara os dados da tabela de viagens."""

    (
        id_viagem,
        num_proposta,
        situacao,
        viagem_urgente,
        cod_orgao_superior,
        nome_orgao_superior,
        nome_viajante,
        cargo,
        data_inicio,
        data_fim,
        destinos,
        motivo,
        valor_diarias,
        valor_passagens,
        valor_devolucao,
        valor_outros_gastos,
    ) = linha

    id_viagem = limpar_texto(id_viagem)
    nome_orgao_superior = limpar_texto(nome_orgao_superior)

    if not id_viagem or not nome_orgao_superior:
        return None

    data_inicio = converter_data(data_inicio)
    data_fim = converter_data(data_fim)

    valor_diarias = converter_decimal(valor_diarias)
    valor_passagens = converter_decimal(valor_passagens)
    valor_devolucao = converter_decimal(valor_devolucao)
    valor_outros_gastos = converter_decimal(valor_outros_gastos)

    valor_total = (
        (valor_diarias or Decimal("0.00"))
        + (valor_passagens or Decimal("0.00"))
        + (valor_outros_gastos or Decimal("0.00"))
        - (valor_devolucao or Decimal("0.00"))
    )

    duracao_dias = None

    if data_inicio and data_fim:
        duracao_dias = (data_fim - data_inicio).days

    return (
        id_viagem,
        limpar_texto(num_proposta),
        limpar_texto(situacao),
        limpar_texto(viagem_urgente),
        limpar_texto(cod_orgao_superior),
        nome_orgao_superior,
        limpar_texto(nome_viajante),
        limpar_texto(cargo),
        data_inicio,
        data_fim,
        limpar_texto(destinos),
        limpar_texto(motivo),
        valor_diarias,
        valor_passagens,
        valor_devolucao,
        valor_outros_gastos,
        valor_total,
        duracao_dias,
    )


def transformar_pagamento(linha):
    """Prepara os dados da tabela de pagamentos."""

    (
        id_viagem,
        num_proposta,
        nome_orgao_pagador,
        nome_ug_pagadora,
        tipo_pagamento,
        valor,
    ) = linha

    id_viagem = limpar_texto(id_viagem)
    tipo_pagamento = limpar_texto(tipo_pagamento)

    if not id_viagem or not tipo_pagamento:
        return None

    return (
        id_viagem,
        limpar_texto(num_proposta),
        limpar_texto(nome_orgao_pagador),
        limpar_texto(nome_ug_pagadora),
        tipo_pagamento,
        converter_decimal(valor),
    )


def transformar_passagem(linha):
    """Prepara os dados da tabela de passagens."""

    (
        id_viagem,
        meio_transporte,
        pais_origem_ida,
        uf_origem_ida,
        cidade_origem_ida,
        pais_destino_ida,
        uf_destino_ida,
        cidade_destino_ida,
        valor_passagem,
        taxa_servico,
        data_emissao,
    ) = linha

    id_viagem = limpar_texto(id_viagem)

    if not id_viagem:
        return None

    return (
        id_viagem,
        limpar_texto(meio_transporte),
        limpar_texto(pais_origem_ida),
        limpar_texto(uf_origem_ida),
        limpar_texto(cidade_origem_ida),
        limpar_texto(pais_destino_ida),
        limpar_texto(uf_destino_ida),
        limpar_texto(cidade_destino_ida),
        converter_decimal(valor_passagem),
        converter_decimal(taxa_servico),
        converter_data(data_emissao),
    )


def transformar_trecho(linha):
    """Prepara os dados da tabela de trechos."""

    (
        id_viagem,
        sequencia_trecho,
        origem_data,
        origem_uf,
        origem_cidade,
        destino_data,
        destino_uf,
        destino_cidade,
        meio_transporte,
        numero_diarias,
    ) = linha

    id_viagem = limpar_texto(id_viagem)

    if not id_viagem:
        return None

    return (
        id_viagem,
        converter_inteiro(sequencia_trecho),
        converter_data(origem_data),
        limpar_texto(origem_uf),
        limpar_texto(origem_cidade),
        converter_data(destino_data),
        limpar_texto(destino_uf),
        limpar_texto(destino_cidade),
        limpar_texto(meio_transporte),
        converter_decimal(numero_diarias),
    )


def carregar_tabela(
    conexao_origem,
    conexao_destino,
    consulta,
    sql_insert,
    funcao_transformacao,
    nome_tabela,
):
    """Lê os dados em blocos, transforma e insere no Silver."""

    cursor_origem = conexao_origem.cursor()
    cursor_destino = conexao_destino.cursor()

    cursor_origem.execute(consulta)

    total_lido = 0
    total_preparado = 0
    total_inserido = 0

    print(f"\nIniciando transformação: {nome_tabela}")

    while True:
        bloco = cursor_origem.fetchmany(TAMANHO_BLOCO)

        if not bloco:
            break

        dados = []

        for linha in bloco:
            resultado = funcao_transformacao(linha)

            if resultado is not None:
                dados.append(resultado)

        if dados:
            cursor_destino.executemany(sql_insert, dados)
            conexao_destino.commit()

            total_preparado += len(dados)
            total_inserido += cursor_destino.rowcount

        total_lido += len(bloco)

        print(
            f"Registros lidos: {total_lido} | "
            f"Preparados: {total_preparado} | "
            f"Inseridos: {total_inserido}"
        )

    cursor_origem.close()
    cursor_destino.close()

    print(f"Transformação concluída: {nome_tabela}")
    print(f"Total lido: {total_lido}")
    print(f"Total inserido: {total_inserido}")


def main():
    conexao_origem = None
    conexao_destino = None

    try:
        print("Conectando ao banco de dados...")

        conexao_origem = conectar()
        conexao_destino = conectar()

        print("Conexões realizadas com sucesso!")

        limpar_tabelas_silver(conexao_destino)

        consulta_viagem = """
            SELECT
                `Identificador do processo de viagem`,
                `Número da Proposta (PCDP)`,
                `Situação`,
                `Viagem Urgente`,
                `Código do órgão superior`,
                `Nome do órgão superior`,
                `Nome`,
                `Cargo`,
                `Período - Data de início`,
                `Período - Data de fim`,
                `Destinos`,
                `Motivo`,
                `Valor diárias`,
                `Valor passagens`,
                `Valor devolução`,
                `Valor outros gastos`
            FROM raw_viagem
        """

        sql_viagem = """
            INSERT IGNORE INTO silver_viagem (
                id_viagem, num_proposta, situacao,
                viagem_urgente, cod_orgao_superior,
                nome_orgao_superior, nome_viajante, cargo,
                data_inicio, data_fim, destinos, motivo,
                valor_diarias, valor_passagens,
                valor_devolucao, valor_outros_gastos,
                valor_total, duracao_dias
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s
            )
        """

        carregar_tabela(
            conexao_origem,
            conexao_destino,
            consulta_viagem,
            sql_viagem,
            transformar_viagem,
            "silver_viagem",
        )

        conexao_origem.commit()

        consulta_pagamento = """
            SELECT
                r.`Identificador do processo de viagem`,
                r.`Número da Proposta (PCDP)`,
                r.`Nome do órgao pagador`,
                r.`Nome da unidade gestora pagadora`,
                r.`Tipo de pagamento`,
                r.`Valor`
            FROM raw_pagamento r
            INNER JOIN silver_viagem v
                ON TRIM(r.`Identificador do processo de viagem`)
                = v.id_viagem
        """

        sql_pagamento = """
            INSERT IGNORE INTO silver_pagamento (
                id_viagem, num_proposta, nome_orgao_pagador,
                nome_ug_pagadora, tipo_pagamento, valor
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        carregar_tabela(
            conexao_origem,
            conexao_destino,
            consulta_pagamento,
            sql_pagamento,
            transformar_pagamento,
            "silver_pagamento",
        )

        consulta_passagem = """
            SELECT
                r.`Identificador do processo de viagem`,
                r.`Meio de transporte`,
                r.`País - Origem ida`,
                r.`UF - Origem ida`,
                r.`Cidade - Origem ida`,
                r.`País - Destino ida`,
                r.`UF - Destino ida`,
                r.`Cidade - Destino ida`,
                r.`Valor da passagem`,
                r.`Taxa de serviço`,
                r.`Data da emissão/compra`
            FROM raw_passagem r
            INNER JOIN silver_viagem v
                ON TRIM(r.`Identificador do processo de viagem`)
                = v.id_viagem
        """

        sql_passagem = """
            INSERT IGNORE INTO silver_passagem (
                id_viagem, meio_transporte,
                pais_origem_ida, uf_origem_ida,
                cidade_origem_ida, pais_destino_ida,
                uf_destino_ida, cidade_destino_ida,
                valor_passagem, taxa_servico, data_emissao
            )
            VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """

        carregar_tabela(
            conexao_origem,
            conexao_destino,
            consulta_passagem,
            sql_passagem,
            transformar_passagem,
            "silver_passagem",
        )

        consulta_trecho = """
            SELECT
                r.`Identificador do processo de viagem`,
                r.`Sequência Trecho`,
                r.`Origem - Data`,
                r.`Origem - UF`,
                r.`Origem - Cidade`,
                r.`Destino - Data`,
                r.`Destino - UF`,
                r.`Destino - Cidade`,
                r.`Meio de transporte`,
                r.`Número Diárias`
            FROM raw_trecho r
            INNER JOIN silver_viagem v
                ON TRIM(r.`Identificador do processo de viagem`)
                = v.id_viagem
        """

        sql_trecho = """
            INSERT IGNORE INTO silver_trecho (
                id_viagem, sequencia_trecho,
                origem_data, origem_uf, origem_cidade,
                destino_data, destino_uf, destino_cidade,
                meio_transporte, numero_diarias
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """

        carregar_tabela(
            conexao_origem,
            conexao_destino,
            consulta_trecho,
            sql_trecho,
            transformar_trecho,
            "silver_trecho",
        )

        print("\nTodas as transformações foram concluídas!")

    except Exception as erro:
        print(f"\nERRO durante a transformação: {erro}")
        raise

    finally:
        if conexao_origem is not None and conexao_origem.is_connected():
            conexao_origem.close()

        if conexao_destino is not None and conexao_destino.is_connected():
            conexao_destino.close()

        print("Conexões com o banco encerradas.")


if __name__ == "__main__":
    main()
