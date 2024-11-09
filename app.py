import gradio as gr
import os
from gtts import gTTS
from datetime import datetime


def text_to_speech(file, text_input, lang_input):
    # Kullanıcı dosya yüklediyse, dosyadan metin oku
    if file is not None:
        try:
            with open(file.name, 'r', encoding='utf-8') as f:
                metin = f.read()
        except Exception as e:
            return f"Dosya okunamadı: {e}"
    # Dosya yoksa ve kullanıcı doğrudan metin girdiyse, metni kullan
    elif text_input:
        metin = text_input
    else:
        return "Lütfen bir dosya yükleyin veya metin girin."

    try:
        # gTTS nesnesini oluştur
        kayit = gTTS(text=metin, lang=lang_input, slow=False)
        dosya_adi = f"ses_{lang_input}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        kayit.save(dosya_adi)

        # Ses dosyasının yolunu döndür
        if os.path.exists(dosya_adi):
            return dosya_adi  # Bu dosyayı indirme linki olarak döndüreceğiz
        else:
            return "Ses kaydedilemedi."
    except Exception as e:
        return f"Bir hata oluştu: {e}"


# Gradio arayüzü
with gr.Blocks() as demo:
    gr.Markdown("# Metni veya Dosyayı Seslendirme Uygulaması")

    with gr.Row():
        file_input = gr.File(label="Metin Dosyasını Yükle (.txt)")
        text_input = gr.Textbox(label="Metin Girin", placeholder="Seslendirmek istediğiniz metni buraya yazın.")

    lang_input = gr.Radio(["tr", "en", "fr"], label="Dil Seçimi", value="tr")
    output = gr.Audio(label="Ses Dosyası", interactive=True)

    submit_button = gr.Button("Seslendir")
    submit_button.click(
        fn=text_to_speech,
        inputs=[file_input, text_input, lang_input],
        outputs=output
    )

# Uygulamayı çalıştır
demo.launch(share=True)
