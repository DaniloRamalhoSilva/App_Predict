## Introdução
Este projeto é um aplicativo web interativo desenvolvido em **Streamlit 1.45.0**, destinado a simular o cadastro de clientes e prever se eles são propensos (1) ou não (0) a comprar um produto de campanha, usando um modelo de Machine Learning treinado com PyCaret. Além da entrada via CSV (“Offline”), o app oferece:
- **Modo Online**: formulário para inserir manualmente cada _feature_ e gerar predição em tempo real;
- **Threshold Dinâmico**: ajuste do limite de decisão (entre 0.0 e 1.0) por slider e por prompt de texto;
- **Analytics**: comparação interativa (boxplots, histogramas) das distribuições de _features_ para clientes preditos como 0×1, recalculadas sempre que o threshold mudar;
- **Deploy**: pronto para publicação no Streamlit Cloud, com repositório GitHub integrado.


## Integrantes do Grupo
   -  Nome: Danilo Ramalho Silva | RM: 555183
   -  Nome: Israel Dalcin Alves Diniz | RM: 554668
   -  Nome: João Vitor Pires da Silva | RM: 556213
   -  Nome: Pablo Menezes Barreto | RM: 556389
   -  Nome: Tiago Toshio Kumagai Gibo | RM: 556984

   Acesso ao [app](https://share.streamlit.io/) no Streamlit Cloud.  
   Acesso ao [repositório](https://github.com/DaniloRamalhoSilva/App_Predict) do GitHub  
   Acesso a [apresentação]() (09/05/2025, até 15 minutos)  


## Funcionalidades Detalhadas
1. **Menu Lateral**
   - Navegação entre as abas: “Home”, “Offline (CSV)”, “Online”, “Analytics” e “Sobre”.
   - Arquivo responsável: `menu_lateral.py`.

2. **Offline (CSV)**
   - Upload de arquivo CSV com dados de múltiplos clientes;
   - Geração de predições em lote;
   - Exibição de tabela com scores e classes preditas.
   - Código em: `simulador_csv.py`.

3. **Online**
   - Formulário para cada _feature_ usada no treinamento;
   - Criação dinâmica de um `DataFrame` pandas;
   - Envio ao modelo e exibição do score + classe (0/1) em destaque, usando caixas coloridas (`st.info`, `st.success`, etc.).
   - Lógica em: `simulador_online.py`.

4. **Threshold**
   - **Slider**: `st.slider("Threshold", 0.0, 1.0, 0.5, step=0.01)`;
   - **Prompt de Texto**: campo `st.text_input` onde o usuário digita “0.65” por exemplo, que atualiza o slider e a lógica de decisão.

5. **Analytics**
   - Aba em `st.tabs(["Dados", "Gráficos"])`;
   - **Boxplots** e **Histogramas** para cada _feature_, comparando classes 0×1;
   - Gráficos re-renderizados sempre que o threshold for alterado, refletindo o novo particionamento das classes.


## Estrutura de Pastas
```plaintext
├── app_aula.py            # Arquivo principal (Home + integração de módulos)
├── menu_lateral.py        # Layout do menu lateral
├── simulador_csv.py       # Lógica de predição via CSV
├── simulador_online.py    # Formulário e predição online
├── requirements.txt       # Lista de dependências
├── README.md              # Este arquivo
```


## Pré-requisitos
- **Python 3.10
- **Git**
- Conta gratuita no **Streamlit Cloud** (para deploy)


## Instalação e Setup Local
1. **Clone o repositório**
   ```bash
   git clone https://github.com/SEU-ORG/SEU-REPO.git
   cd SEU-REPO
   ```
2. **Ambiente Virtual**
   ```bash
   python -m venv .venv
   source .venv/bin/activate       # Linux/macOS
   .venv\Scripts\activate          # Windows
   ```
3. **Instale as dependências**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   > *Exemplo de `requirements.txt`:*
   > ```
   > streamlit==1.45.0
   > pandas==1.5.3
   > numpy
   > scikit-learn==1.2.2
   > joblib==1.3.2
   > scipy==1.11.4
   > pycaret[classification]==3.0.1
   > openai==1.77.0
   > python-dotenv

## Como Rodar o Projeto
No diretório do projeto ativo no virtualenv, execute:
```bash
streamlit run app_aula.py
```
- O navegador abrirá automaticamente em `http://localhost:8501`.
- Navegue pelo menu lateral para testar as abas **Offline**, **Online**, **Analytics** e **Sobre**.


## Deploy no Streamlit Cloud
1. **Crie um repositório** no GitHub e faça push de todo o código.
2. Acesse [streamlit.io/cloud](https://streamlit.io/cloud) e conecte sua conta GitHub.
3. Selecione o repositório e configure:
   - **Branch**: `main` (ou outra que preferir)
   - **File path**: `app_aula.py`
   - **Python version**: `3.10`
4. Clique em **Deploy**.
5. Copie a URL gerada e compartilhe com o grupo.



## Licença
Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).


