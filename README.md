# Enviador de Relatório Semanal

Este é um script Python que automatiza o processo de encontrar relatórios de estudo criados na última semana e enviá-los por e-mail.

## Funcionalidades

-   **Busca Automática:** Varre uma pasta designada em busca de arquivos modificados nos últimos 7 dias.
-   **Envio Agendado:** O script roda em um loop, verificando se é o dia correto da semana (domingo) para realizar o envio.
-   **Segurança:** Utiliza um arquivo `credenciais.env` para armazenar as credenciais de e-mail de forma segura, que não é enviado para o repositório graças ao `.gitignore`.
-   **Configurável:** O destinatário e o dia de envio podem ser facilmente alterados no código.

## Como Usar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/guicost3/Relatorio_Semanal.git
    cd Relatorio_Semanal
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure suas credenciais:**
    Crie um arquivo chamado `credenciais.env` na raiz do projeto com o seguinte conteúdo, substituindo com seus dados:
    ```
    EMAIL_ADDRESS="seu_email@exemplo.com"
    EMAIL_PASSWORD="sua_senha_de_app_do_email"
    ```

4.  **Execute o script:**
    ```bash
    python relatorio_semanal.py
    ```

