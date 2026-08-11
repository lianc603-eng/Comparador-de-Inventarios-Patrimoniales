import streamlit as st
from pdf2docx import Converter
import tempfile
import os

st.set_page_config(page_title="PDF a Word", page_icon="📄")
st.title("Convertidor de PDF a Word Editable")
st.write("Sube tu archivo PDF para convertirlo a Word conservando la estructura original.")

uploaded_file = st.file_uploader("Elige un archivo PDF", type=["pdf"])

if uploaded_file is not None:
    if st.button("Convertir a Word"):
        with st.spinner("Procesando y convirtiendo documento..."):
            # Guardar el PDF subido temporalmente
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(uploaded_file.read())
                tmp_pdf_path = tmp_pdf.name

            output_docx_path = tmp_pdf_path.replace(".pdf", ".docx")

            try:
                # Conversión manteniendo estructura
                cv = Converter(tmp_pdf_path)
                cv.convert(output_docx_path, start=0, end=None)
                cv.close()

                # Leer el archivo convertido para la descarga
                with open(output_docx_path, "rb") as file:
                    st.success("¡Conversión completada con éxito!")
                    st.download_button(
                        label="Descargar archivo Word (.docx)",
                        data=file,
                        file_name=uploaded_file.name.replace(".pdf", ".docx"),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            except Exception as e:
                st.error(f"Ocurrió un error en la conversión: {e}")
            finally:
                # Limpiar archivos temporales
                if os.path.exists(tmp_pdf_path):
                    os.remove(tmp_pdf_path)
                if os.path.exists(output_docx_path):
                    os.remove(output_docx_path)
