import smtplib
import os
import mimetypes
from email.message import EmailMessage
from typing import List, Optional

def enviar(
    destinatarios: List[str],
    assunto: str,
    corpo_texto: str,
    corpo_html: Optional[str] = None,
    anexos: Optional[List[str]] = None,
    smtp_server: str = 'smtp.gmail.com',
    smtp_port: int = 465,
    smtp_user: Optional[str] = None,
    smtp_password: Optional[str] = None,
):
    """
    Função para enviar um e-mail para uma lista de destinatários.

    Args:
        destinatarios (List[str]): Lista de e-mails dos destinatários.
        assunto (str): O assunto do e-mail.
        corpo_texto (str): O corpo do e-mail em texto puro.
        corpo_html (Optional[str], optional): O corpo do e-mail em HTML. Defaults to None.
        anexos (Optional[List[str]], optional): Lista com os caminhos dos arquivos a serem anexados. Defaults to None.
        smtp_server (str): Endereço do servidor SMTP. Padrão é 'smtp.gmail.com'.
        smtp_port (int): Porta do servidor SMTP. Padrão é 465 (SSL).
        smtp_user (str): E-mail do remetente (usuário de login).
        smtp_password (str): Senha do e-mail (preferencialmente senha de app).

    Returns:
        bool: True se o e-mail foi enviado com sucesso, False caso contrário.
    """
    # Se o usuário e a senha não forem passados, tenta pegar das variáveis de ambiente
    smtp_user = smtp_user or os.getenv("EMAIL_ADDRESS")
    smtp_password = smtp_password or os.getenv("EMAIL_PASSWORD")
    
    if not smtp_user or not smtp_password:
        print("Erro: Credenciais de e-mail (usuário e senha) não foram fornecidas ou encontradas nas variáveis de ambiente.")
        return False

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = smtp_user
    msg['To'] = ", ".join(destinatarios)
    msg.set_content(corpo_texto)

    if corpo_html:
        msg.add_alternative(corpo_html, subtype='html')

    if anexos:
        for caminho_anexo in anexos:
            if not os.path.exists(caminho_anexo):
                print(f"Aviso: Anexo não encontrado em '{caminho_anexo}'. Pulando.")
                continue
            
            mime_type, _ = mimetypes.guess_type(caminho_anexo)
            mime_type, mime_subtype = (mime_type or 'application/octet-stream').split('/', 1)
            
            with open(caminho_anexo, 'rb') as f:
                msg.add_attachment(f.read(),
                                   maintype=mime_type,
                                   subtype=mime_subtype,
                                   filename=os.path.basename(caminho_anexo))

    server = None
    try:
        # Lógica de conexão dinâmica baseada na porta
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:  # Conexão TLS explícita (Outlook, outros)
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

        server.login(smtp_user, smtp_password)
        server.send_message(msg)

        return True
    except smtplib.SMTPAuthenticationError:
        print("Erro de autenticação. Verifique seu e-mail, senha de app e as configurações de segurança.")
        return False
    except Exception as e:
        print(f"Ocorreu um erro ao enviar o e-mail: {e}")
        return False
    finally:
        if server:
            server.quit()

