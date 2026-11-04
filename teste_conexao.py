
from banco import conectar

try:
    conexao = conectar()

    if conexao.is_connected():
        print("Conexão com MySQL realizada com sucesso!")

        cursor = conexao.cursor()
        cursor.execute("SELECT DATABASE()")

        banco = cursor.fetchone()
        print(f"Banco conectado: {banco[0]}")

        cursor.close()

except Exception as erro:
    print(f"Erro na conexão: {erro}")

finally:
    if "conexao" in locals() and conexao.is_connected():
        conexao.close()
        print("Conexão encerrada.")
