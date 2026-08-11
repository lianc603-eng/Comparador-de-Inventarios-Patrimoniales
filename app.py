import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Comparador de Inventarios", page_icon="📦", layout="wide")

st.title("📦 Comparador de Inventarios Patrimoniales")
st.write("Sube el inventario **Anterior** y el **Nuevo** para comparar resguardos, ubicaciones y bienes faltantes.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Inventario Anterior / Base")
    file_ant = st.file_uploader("Sube el archivo anterior (Excel/CSV)", type=["xlsx", "xls", "csv"], key="ant")

with col2:
    st.subheader("2. Inventario Nuevo / Reciente")
    file_nue = st.file_uploader("Sube el archivo nuevo (Excel/CSV)", type=["xlsx", "xls", "csv"], key="nue")

if file_ant and file_nue:
    def cargar_datos(file):
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)

    df_ant = cargar_datos(file_ant)
    df_nue = cargar_datos(file_nue)

    st.success("¡Archivos cargados correctamente!")
    st.markdown("---")
    
    st.subheader("⚙️ Configuración de Columnas")
    st.write("Selecciona las columnas correspondientes en cada archivo para realizar la comparación:")

    c1, c2, c3 = st.columns(3)
    
    with c1:
        col_id_ant = st.selectbox("Clave / No. Inventario (Anterior)", df_ant.columns, index=0 if "sub_clave" in df_ant.columns else 0)
        col_id_nue = st.selectbox("Clave / No. Inventario (Nuevo)", df_nue.columns, index=0 if "sub_clave" in df_nue.columns else 0)
        
    with c2:
        col_resp_ant = st.selectbox("Resguardante / Responsable (Anterior)", df_ant.columns, index=1 if "Nombre" in df_ant.columns else 0)
        col_resp_nue = st.selectbox("Resguardante / Responsable (Nuevo)", df_nue.columns, index=1 if "Nombre" in df_nue.columns else 0)

    with c3:
        col_desc_ant = st.selectbox("Descripción del Bien (Anterior)", df_ant.columns, index=2 if "Descripción del Bien" in df_ant.columns else 0)
        col_desc_nue = st.selectbox("Descripción del Bien (Nuevo)", df_nue.columns, index=2 if "Descripción del Bien" in df_nue.columns else 0)

    if st.button("🔍 Comparar Inventarios", type="primary"):
        # Limpieza de claves para asegurar coincidencias correctas
        df_ant[col_id_ant] = df_ant[col_id_ant].astype(str).str.strip().str.upper()
        df_nue[col_id_nue] = df_nue[col_id_nue].astype(str).str.strip().str.upper()

        # Nombres asignados tras el merge
        col_resp_ant_renamed = f"{col_resp_ant}_ANTERIOR"
        col_resp_nue_renamed = f"{col_resp_nue}_NUEVO"

        # Cruce de datos
        merged = pd.merge(
            df_ant, 
            df_nue, 
            left_on=col_id_ant, 
            right_on=col_id_nue, 
            how="outer", 
            suffixes=("_ANTERIOR", "_NUEVO")
        )

        # Manejar nombres si las columnas tenían títulos distintos
        if col_resp_ant_renamed not in merged.columns:
            col_resp_ant_renamed = col_resp_ant
        if col_resp_nue_renamed not in merged.columns:
            col_resp_nue_renamed = col_resp_nue

        col_id_ant_m = f"{col_id_ant}_ANTERIOR" if f"{col_id_ant}_ANTERIOR" in merged.columns else col_id_ant
        col_id_nue_m = f"{col_id_nue}_NUEVO" if f"{col_id_nue}_NUEVO" in merged.columns else col_id_nue

        col_desc_ant_m = f"{col_desc_ant}_ANTERIOR" if f"{col_desc_ant}_ANTERIOR" in merged.columns else col_desc_ant
        col_desc_nue_m = f"{col_desc_nue}_NUEVO" if f"{col_desc_nue}_NUEVO" in merged.columns else col_desc_nue

        # 1. Bienes localizados en ambos
        encontrados = merged[merged[col_id_ant_m].notna() & merged[col_id_nue_m].notna()].copy()
        
        if not encontrados.empty:
            def detectar_cambio(row):
                r_ant = str(row[col_resp_ant_renamed]).strip() if pd.notna(row[col_resp_ant_renamed]) else ""
                r_nue = str(row[col_resp_nue_renamed]).strip() if pd.notna(row[col_resp_nue_renamed]) else ""
                if r_ant == r_nue:
                    return "Sin cambio de resguardo"
                return "⚠️ Cambio de resguardante"

            encontrados["Estado_Resguardo"] = encontrados.apply(detectar_cambio, axis=1)

        # 2. Pendientes de localizar (Estaban en anterior, no en nuevo)
        faltantes = merged[merged[col_id_ant_m].notna() & merged[col_id_nue_m].isna()].copy()

        # 3. Nuevos ingresos (Están en nuevo, no en anterior)
        nuevos = merged[merged[col_id_ant_m].isna() & merged[col_id_nue_m].notna()].copy()

        # Métricas
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Inventario Anterior", len(df_ant))
        m2.metric("Total Inventario Nuevo", len(df_nue))
        m3.metric("Bienes Localizados", len(encontrados))
        m4.metric("🚨 Pendientes de Localizar", len(faltantes))

        # Pestañas de resultados
        tab1, tab2, tab3 = st.tabs(["📊 Bienes Localizados y Cambios", "🚨 Pendientes de Localizar (Faltantes)", "🆕 Nuevos Registros"])

        with tab1:
            st.markdown("### Resumen de Bienes Localizados")
            if not encontrados.empty:
                resumen_loc = pd.DataFrame({
                    "Clave Inventario": encontrados[col_id_nue_m],
                    "Descripción": encontrados[col_desc_nue_m],
                    "Resguardante Anterior": encontrados[col_resp_ant_renamed],
                    "Resguardante Actual": encontrados[col_resp_nue_renamed],
                    "Estatus": encontrados["Estado_Resguardo"]
                })
                st.dataframe(resumen_loc, use_container_width=True)
            else:
                st.info("No se encontraron coincidencias entre ambos inventarios.")

        with tab2:
            st.markdown("### Bienes en el Inventario Anterior NO encontrados en el Nuevo")
            if not faltantes.empty:
                resumen_falt = pd.DataFrame({
                    "Clave Inventario": faltantes[col_id_ant_m],
                    "Descripción": faltantes[col_desc_ant_m],
                    "Último Resguardante Conocido": faltantes[col_resp_ant_renamed]
                })
                st.dataframe(resumen_falt, use_container_width=True)
            else:
                st.success("¡Excelente! Todos los bienes del inventario anterior fueron localizados.")

        with tab3:
            st.markdown("### Bienes Nuevos (No estaban en el registro anterior)")
            if not nuevos.empty:
                resumen_nuev = pd.DataFrame({
                    "Clave Inventario": nuevos[col_id_nue_m],
                    "Descripción": nuevos[col_desc_nue_m],
                    "Resguardante Actual": nuevos[col_resp_nue_renamed]
                })
                st.dataframe(resumen_nuev, use_container_width=True)
            else:
                st.info("No hay registros nuevos en el último inventario.")

        # Descarga Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if not encontrados.empty:
                resumen_loc.to_excel(writer, sheet_name='Localizados', index=False)
            if not faltantes.empty:
                resumen_falt.to_excel(writer, sheet_name='Pendientes_Localizar', index=False)
            if not nuevos.empty:
                resumen_nuev.to_excel(writer, sheet_name='Bienes_Nuevos', index=False)
        
        output.seek(0)

        st.markdown("---")
        st.download_button(
            label="📥 Descargar Reporte Comparativo en Excel",
            data=output,
            file_name="Reporte_Comparativo_Inventario.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
