# 🎤 J.A.R.V.I.S Transcript - Transcrição de Áudio e Vídeo

Este projeto é uma aplicação feita com **Python** e **Streamlit** que utiliza o modelo **Whisper API** da **OpenAI** para transcrever áudios de três fontes diferentes:

✅ Microfone (captura de voz em tempo real)  
✅ Arquivo de vídeo (.mp4)  
✅ Arquivo de áudio (.mp3)

---

## 🚀 Funcionalidades

- 🎙️ Transcrição automática da sua fala pelo microfone
- 📼 Transcrição de áudio extraído de vídeos (.mp4)
- 🎵 Transcrição de arquivos de áudio (.mp3)
- 🎯 Possibilidade de adicionar um **prompt de contexto** para melhorar a precisão
- 🔐 Configuração rápida da API Key pela interface
- 🌐 Funciona diretamente no navegador (via Streamlit)

---

## 🎯 Como usar

### 1. Clone o repositório

bash
git clone https://github.com/seu-usuario/jarvis-transcript.git
cd jarvis-transcript

# 2. Crie e ative um ambiente virtual (opcional, mas recomendado)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instale as dependências
bash
Copy
Edit
pip install -r requirements.txt

# 4. Execute o projeto
bash
Copy
Edit
streamlit run app.py

# 🧩 Estrutura do projeto
bash
Copy
Edit
├── app.py                      # Código principal da aplicação
├── temp/                       # Pasta para arquivos temporários (áudio e vídeo)
├── requirements.txt            # Dependências do projeto
└── README.md                   # Informações do projeto
# 🎥 Funcionalidades Principais
✅ Transcrição em tempo real via microfone (WebRTC)
✅ Upload de vídeos (.mp4) com extração e transcrição do áudio
✅ Upload de áudios (.mp3) para transcrição
✅ Campo para prompt opcional para melhorar a transcrição
✅ Armazenamento temporário dos arquivos para processamento
✅ Gerenciamento da API Key da OpenAI diretamente na aba Configurações

# 👨‍💻 Tecnologias
Python

Streamlit

Streamlit WebRTC

MoviePy

Pydub

OpenAI Whisper API

# 🔐 Requisitos
Para utilizar o projeto, você precisa:

Ter uma conta na OpenAI

Gerar uma API Key válida

Internet estável para captura de áudio via WebRTC

# 📌 Observação
Os arquivos de áudio e vídeo são armazenados temporariamente na pasta temp/ para realizar o processamento. Após a transcrição, os arquivos podem ser apagados manualmente, se desejar.

# 🧑‍🏫 Desenvolvido por
Leandro Souza

# ⭐️ Licença
Uso livre para fins acadêmicos, pessoais ou estudos.
Contribuições são bem-vindas!
