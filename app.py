import os
import streamlit as st
import yt_dlp
import numpy as np
import openai
import moviepy as mp
from transformers import pipeline
import wave
import whisper


# Configuração da API OpenAI
openai.api_key = "APIKEY"  # Substitua pela sua chave da API OpenAI

# Função para baixar vídeo do YouTube
def download_video(youtube_url, output_path="video.mp4"):
    ydl_opts = {
        "format": "mp4",
        "outtmpl": output_path,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return output_path

# Função para extrair áudio do vídeo
def extract_audio_from_video(video_path, audio_path="audio.wav"):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')  # Salva o áudio em WAV
    return audio_path

def load_wav_file(filename):
    with wave.open(filename, 'rb') as wf:
        # Verifica se o áudio é mono e qual é o sample rate
        channels = wf.getnchannels()
        sample_rate = wf.getframerate()
        n_frames = wf.getnframes()
        audio_data = wf.readframes(n_frames)
        # Converter os dados para um array numpy
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
        # Se o áudio tiver mais de um canal, faça a média para obter mono
        if channels > 1:
            audio_np = audio_np.reshape(-1, channels).mean(axis=1)
        # Normalizar para o intervalo [-1, 1]
        audio_np /= np.max(np.abs(audio_np))
    return audio_np, sample_rate

# Função para transcrever o áudio usando Whisper
def transcribe_audio(audio_path):
    # Carega o áudio e verifica o sample rate
    audio_np, sr = load_wav_file(audio_path)
    print(f"Sample rate: {sr}")

    # Se necessário, você pode fazer o reamostramento para 16000 Hz usando, por exemplo, a biblioteca librosa:
    if sr != 16000:
        import librosa
        audio_np = librosa.resample(audio_np, orig_sr=sr, target_sr=16000)
        sr = 16000

    # Carregar o modelo Whisper
    model = whisper.load_model("base")

    # Transcrever passando o array NumPy
    result = model.transcribe(audio_np)
    print(result["text"])
    return result["text"]

# Função para gerar tags SEO com a API OpenAI
def generate_seo_tags(transcription):
    prompt = f"Com base na seguinte transcrição de vídeo, gere tags SEO relevantes:\n\n{transcription}"

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # ou "gpt-4" se quiser usar o modelo mais avançado
    messages=[{"role": "system", "content": "Você é um assistente de IA."},
              {"role": "user", "content": "Gere tags SEO para este texto..."}],
    temperature=0.7
    )


    seo_tags = response.choices[0].text.strip()
    return seo_tags

# Interface no Streamlit
st.title("Gerador de SEO para Vídeos do YouTube")

# Input do vídeo do YouTube
video_url = st.text_input("Cole o link do vídeo do YouTube")

if st.button("Baixar, Processar e Gerar Tags SEO"):
    if video_url:
        with st.spinner('Baixando e processando o vídeo...'):
            # Baixar o vídeo
            video_path = download_video(video_url, "youtube_video.mp4")
            st.success(f"Vídeo {video_url} baixado com sucesso!")

            # Extrair o áudio do vídeo
            audio_path = extract_audio_from_video(video_path, "audio.wav")
            st.success(f"Áudio extraído com sucesso do vídeo!")

            # Transcrever o áudio
            audio_path = r"C:\Users\JPA\Desktop\Projetos\IA\gerador_seo\audio.wav"

            transcription = transcribe_audio(audio_path)
            st.success("Transcrição do áudio concluída!")

            # Gerar tags SEO
            seo_tags = generate_seo_tags(transcription)

            st.write("### Tags SEO Geradas:")
            st.write(seo_tags)

# Enviar vídeo próprio
uploaded_file = st.file_uploader("Ou envie seu próprio vídeo de gameplay", type=["mp4", "avi", "mov"])

if uploaded_file:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner('Processando seu vídeo...'):
        # Extrair áudio do vídeo
        audio_path = extract_audio_from_video("temp_video.mp4", "audio.wav")
        st.success("Áudio extraído do vídeo!")

        # Transcrever áudio
        transcription = transcribe_audio(audio_path)
        st.success("Transcrição do áudio concluída!")

        # Gerar tags SEO
        seo_tags = generate_seo_tags(transcription)

        st.write("### Tags SEO Geradas:")
        st.write(seo_tags)
