import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from enviar_email import enviar

# Carrega as variáveis de ambiente do arquivo
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Configurações do Relatório Semanal ---

destinatario = os.getenv("EMAIL_ADDRESS")
dia_da_semana_envio = 6

# Pasta onde os relatórios de estudo são salvos.

pasta_relatorios = os.path.join(script_dir, 'Relatórios')

assunto_email = "Relatório Semanal"

corpo = """

    Bom dia!
    Segue Relatório semanal em anexo.
    Este e-mail foi enviado automaticamente.
   
    Atenciosamente,
    
    Sistema de Automação Python
    """

#Encontra arquivos criados/modificados nos últimos 7 dias

def encontrar_relatorios(pasta_relatorios:str)-> list[str]:
    

    arquivos_encontrados = []
    hoje = datetime.now()
    uma_semana_atras = hoje - timedelta(days=7)

    if not os.path.isdir(pasta_relatorios):
        print(f"Aviso: A pasta de relatórios não existe, Criando agora... ")
        os.makedirs(pasta_relatorios)
        return []
    
    print(f"Procurando relatórios semanais... desde {uma_semana_atras.strftime('%d/%m/%y')}")

    for nome_arquivo in os.listdir(pasta_relatorios):
        caminho_arquivo = os.path.join(pasta_relatorios, nome_arquivo)
        if os.path.isfile(caminho_arquivo):
            data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_arquivo))
            if data_modificacao >= uma_semana_atras:
                arquivos_encontrados.append(caminho_arquivo)
                print(f"- Encontrado: {caminho_arquivo}")
    return arquivos_encontrados

#Função para enviar os relatórios
#Verificar se é Domingo, e verifica também se é o Domingo da semana que estamos

def enviar_relatorios():
    """
    Loop principal que verifica o dia da semana e envia o e-mail com os relatórios.
    """
    semana_ultimo_envio = -1

    print("Serviço de relatório semanal iniciado.")
    print(f"Destinatário: {destinatario}")
    print(f"Dia de envio: {dia_da_semana_envio}")
    print(f"Pasta de relatorios: {pasta_relatorios}")
    print("Pressione Ctrl+C para sair.")

    while True:
        hoje = datetime.now()
        dia_da_semana_atual = hoje.weekday()
        semana_do_ano = hoje.isocalendar().week

        if(dia_da_semana_atual == dia_da_semana_envio) and (semana_ultimo_envio != semana_do_ano):
            relatorios_para_enviar = encontrar_relatorios(pasta_relatorios)

            if not relatorios_para_enviar:
                print("Nenhum relatório encontrado para enviar.")
                semana_ultimo_envio = semana_do_ano
            else:
                print(f"Encontrado(s) {len(relatorios_para_enviar)} relatório(s). Preparando e-mail...")
                fim_semana = hoje
                inicio_semana = fim_semana - timedelta(days=6)
                assunto = assunto_email.format(inicio_semana=inicio_semana.strftime('%d/%m'), fim_semana=fim_semana.strftime('%d/%m/%Y'))
                sucesso = enviar(destinatarios=[destinatario], assunto=assunto, corpo_texto=corpo, anexos=relatorios_para_enviar)
                if sucesso:
                    print("e-mail enviado com sucesso!")
                    semana_ultimo_envio = semana_do_ano
                else:
                    print("Falha no envio do e-mail")

        print(f"[{hoje.strftime('%Y-%m-%d %H:%M:%S')}] Próxima verificação em 12 horas...")
        time.sleep(12 * 3600)



# Ponto de entrada do script. Antes de executar a função (enviar)
# Verifica as variáveis de ambientes no meu arquivo .env

if __name__ == "__main__":
    if not os.getenv("EMAIL_ADDRESS") or not os.getenv("EMAIL_PASSWORD"):
        print("\nERRO: As variáveis de ambiente 'EMAIL_ADDRESS' e 'EMAIL_PASSWORD' não estão configuradas.")
    else:
        try:
            enviar_relatorios()
        except KeyboardInterrupt:
            print("\n\nServiço interrompido pelo usuário. Encerrando.")
        except Exception as e:
            print(f"\nOcorreu um erro crítico e inesperado: {e}")
    

