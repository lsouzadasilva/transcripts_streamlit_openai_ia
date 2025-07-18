from pathlib import Path
import queue
import time

import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

import openai
import pydub
from moviepy.editor import VideoFileClip

PASTA_TEMP = Path(__file__).parent / 'temp'
PASTA_TEMP.mkdir(exist_ok=True)
ARQUIVO_AUDIO_TEMP = PASTA_TEMP / 'audio.mp3'
ARQUIVO_VIDEO_TEMP = PASTA_TEMP / 'video.mp4'
ARQUIVO_MIC_TEMP = PASTA_TEMP / 'mic.mp3'

if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''
    

# --- Ocult menus ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


def transcreve_audio(caminho_audio, prompt):
    if not st.session_state['api_key']:
        st.error("Por favor, configure a chave da API na aba Configurações.")
        return

    client = openai.OpenAI(api_key=st.session_state['api_key'])
    
    with open(caminho_audio, 'rb') as arquivo_audio:
        transcricao = client.audio.transcriptions.create(
            model='whisper-1',
            language='pt',
            response_format='text',
            file=arquivo_audio,
            prompt=prompt,
        )
        return transcricao

if not 'transcricao_mic' in st.session_state:
    st.session_state['transcricao_mic'] = ''

@st.cache_data
def get_ice_servers():
    return [{'urls': ['stun:stun.l.google.com:19302']}]


def adiciona_chunck_de_audio(frames_de_audio, chunck_audio):
    for frame in frames_de_audio:
        sound = pydub.AudioSegment(
            data=frame.to_ndarray().tobytes(),
            sample_width=frame.format.bytes,
            frame_rate=frame.sample_rate,
            channels=len(frame.layout.channels)
        )
        chunck_audio += sound
    return chunck_audio

def transcreve_tab_mic():
    prompt_mic = st.text_input('(opcional) Digite o seu prompt', key='input_mic')
    webrtx_ctx = webrtc_streamer(
        key='recebe_audio',
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={'video': False, 'audio':True}
    )

    if not webrtx_ctx.state.playing:
        st.write(st.session_state['transcricao_mic'])
        return
    
    container = st.empty()
    container.markdown('Comece a falar...')
    chunck_audio = pydub.AudioSegment.empty()
    tempo_ultima_transcricao = time.time()
    st.session_state['transcricao_mic'] = ''
    while True:
        if webrtx_ctx.audio_receiver:
            try:
                frames_de_audio = webrtx_ctx.audio_receiver.get_frames(timeout=1)
            except queue.Empty:
                time.sleep(0.1)
                continue
            chunck_audio = adiciona_chunck_de_audio(frames_de_audio, chunck_audio)

            agora = time.time()
            if len(chunck_audio) > 0 and agora - tempo_ultima_transcricao > 10:
                tempo_ultima_transcricao = agora
                chunck_audio.export(ARQUIVO_MIC_TEMP)
                transcricao = transcreve_audio(ARQUIVO_MIC_TEMP, prompt_mic)
                st.session_state['transcricao_mic'] += transcricao
                container.write(st.session_state['transcricao_mic'])
                chunck_audio = pydub.AudioSegment.empty()
        else:
            break


# TRANSCREVE VIDEO =====================================
def _salva_audio_do_video(video_bytes):
    with open(ARQUIVO_VIDEO_TEMP, mode='wb') as video_f:
        video_f.write(video_bytes.read())
    moviepy_video = VideoFileClip(str(ARQUIVO_VIDEO_TEMP))
    moviepy_video.audio.write_audiofile(str(ARQUIVO_AUDIO_TEMP))

def transcreve_tab_video():
    prompt_input = st.text_input('(opcional) Digite o seu prompt', key='input_video')
    arquivo_video = st.file_uploader('Adicione um arquivo de vídeo .mp4', type=['mp4'])
    if not arquivo_video is None:
        _salva_audio_do_video(arquivo_video)
        transcricao = transcreve_audio(ARQUIVO_AUDIO_TEMP, prompt_input)
        st.write(transcricao)

# TRANSCREVE AUDIO =====================================
def transcreve_tab_audio():
    prompt_input = st.text_input('(opcional) Digite o seu prompt', key='input_audio')
    arquivo_audio = st.file_uploader('Adicione um arquivo de áudio .mp3', type=['mp3'])
    if arquivo_audio is not None:
        with open(ARQUIVO_AUDIO_TEMP, 'wb') as f:
            f.write(arquivo_audio.read())
        transcricao = transcreve_audio(ARQUIVO_AUDIO_TEMP, prompt_input)
        st.write(transcricao)

# API_KEY ===================================================

def api_key():
    st.text_input('Digite sua chave da API OpenAI:', key='api_key', type='password')
    if st.session_state['api_key']:
        st.success('Chave salva com sucesso')

# MAIN =====================================
def main():
    st.header('Bem-vindo ao J.A.R.V.I.S Transcript🎤', divider=True)
    st.markdown("""
    **Desenvolvido por Leandro Souza**  
    [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/leandro-souza-dados/)
    [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/lsouzadasilva/transcripts_streamlit_openai)
    """)
    st.markdown('#### Transcreva áudio do microfone, de vídeos e de arquivos de áudio')
    tab_mic, tab_video, tab_audio, tab_key = st.tabs(['Microfone', 'Vídeo', 'Áudio', 'Configurações'])
    with tab_mic:
        transcreve_tab_mic()
    with tab_video:
        transcreve_tab_video()
    with tab_audio:
        transcreve_tab_audio()
    with tab_key:
        api_key()
        

if __name__ == '__main__':
    main()
