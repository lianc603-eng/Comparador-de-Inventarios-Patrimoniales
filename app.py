import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Comparador de Inventarios", page_icon="📦", layout="wide")

st.title("📦 Comparador de Inventarios Patrimoniales")
st.write("Sube el inventario **Anterior** y el **Nuevo** para comparar resguardos, ubicaciones, bienes faltantes y nuevas altas.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Inventario Anterior / Base")
    file_ant = st.file_uploader("Sube el archivo anterior (Excel/CSV)", type=["xlsx", "xls", "csv"], key="ant")

with col2:
    st.subheader("2. Inventario Nuevo / Reciente")
    file_nue = st.file_uploader("Sube el archivo nuevo (Excel/CSV)", type=["xlsx", "xls", "csv"], key="nue")

if file_ant and file_nue:
    @st.cache_data
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
        # Normalizar claves: eliminar decimales flotantes como .0, espacios y pasar a texto
        def limpiar_clave(val):
            if pd.isna(val):
                return ""
            val_str = str(val).strip()
            if val_str.endswith(".0"):
                val_str = val_str[:-2]
            return val_str.upper()

        df_ant_clean = df_ant.copy()
        df_nue_clean = df_nue.copy()

        df_ant_clean["CLAVE_NORM"] = df_ant_clean[col_id_ant].apply(limpiar_clave)
        df_nue_clean["CLAVE_NORM"] = df_nue_clean[col_id_nue].apply(limpiar_clave)

        # Filtrar vacíos
        df_ant_clean = df_ant_clean[df_ant_clean["CLAVE_NORM"] != ""]
        df_nue_clean = df_nue_clean[df_nue_clean["CLAVE_NORM"] != ""]

        # Eliminar duplicados exactos dentro del mismo archivo
        df_ant_unique = df_ant_clean.drop_duplicates(subset=["CLAVE_NORM"]).copy()
        df_nue_unique = df_nue_clean.drop_duplicates(subset=["CLAVE_NORM"]).copy()

        # Cruce por clave normalizada
        merged = pd.merge(
            df_ant_unique, 
            df_nue_unique, 
            on="CLAVE_NORM", 
            how="outer", 
            suffixes=("_ANTERIOR", "_NUEVO")
        )

        col_resp_ant_renamed = f"{col_resp_ant}_ANTERIOR" if f"{col_resp_ant}_ANTERIOR" in merged.columns else col_resp_ant
        col_resp_nue_renamed = f"{col_resp_nue}_NUEVO" if f"{col_resp_nue}_NUEVO" in merged.columns else col_resp_nue
        col_desc_ant_renamed = f"{col_desc_ant}_ANTERIOR" if f"{col_desc_ant}_ANTERIOR" in merged.columns else col_desc_ant
        col_desc_nue_renamed = f"{col_desc_nue}_NUEVO" if f"{col_desc_nue}_NUEVO" in merged.columns else col_desc_nue

        # Clasificación estricta
        encontrados = merged[merged[f"{col_id_ant}_ANTERIOR"].notna() & merged[f"{col_id_nue}_NUEVO"].notna()].copy() if f"{col_id_ant}_ANTERIOR" in merged.columns else merged[merged[col_id_ant].notna() & merged[col_id_nue].notna()].copy()
        
        faltantes = merged[merged["CLAVE_NORM"].isin(df_ant_unique["CLAVE_NORM"]) & ~merged["CLAVE_NORM"].isin(df_nue_unique["CLAVE_NORM"])].copy()
        nuevos = merged[~merged["CLAVE_NORM"].isin(df_ant_unique["CLAVE_NORM"]) & merged["CLAVE_NORM"].isin(df_nue_unique["CLAVE_NORM"])].copy()

        if not encontrados.empty:
            def detectar_cambio(row):
                r_ant = str(row[col_resp_ant_renamed]).strip() if pd.notna(row[col_resp_ant_renamed]) else ""
                r_nue = str(row[col_resp_nue_renamed]).strip() if pd.notna(row[col_resp_nue_renamed]) else ""
                return "Sin cambio de resguardo" if r_ant == r_nue else "⚠️ Cambio de resguardante"

            encontrados["Estado_Resguardo"] = encontrados.apply(detectar_cambio, axis=1)

        # Métricas principales
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Anterior (Válidos)", len(df_ant_unique))
        m2.metric("Nuevo (Válidos)", len(df_nue_unique))
        m3.metric("Bienes Coincidentes", len(encontrados))
        m4.metric("🚨 Faltantes", len(faltantes))
        m5.metric("➕ Sobrantes / Nuevos", len(nuevos))

        # Pestañas
        tab1, tab2, tab3 = st.tabs([
            "📊 Bienes Coincidentes y Cambios", 
            "🚨 Faltantes (En Anterior, NO en Nuevo)", 
            "➕ Sobrantes / Nuevas Altas (En Nuevo, NO en Anterior)"
        ])

        with tab1:
            st.markdown("### Resumen de Bienes Localizados")
            if not encontrados.empty:
                resumen_loc = pd.DataFrame({
                    "Clave Inventario": encontrados["CLAVE_NORM"],
                    "Descripción": encontrados[col_desc_nue_renamed],
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
                    "Clave Inventario": faltantes["CLAVE_NORM"],
                    "Descripción": faltantes[col_desc_ant_renamed],
                    "Último Resguardante Conocido": faltantes[col_resp_ant_renamed]
                })
                st.dataframe(resumen_falt, use_container_width=True)
            else:
                st.success("¡Excelente! Todos los bienes del inventario anterior fueron localizados.")

        with tab3:
            st.markdown("### Bienes Sobrantes / Nuevas Altas (No estaban en el registro anterior)")
            if not nuevos.empty:
                resumen_nuev = pd.DataFrame({
                    "Clave Inventario": nuevos["CLAVE_NORM"],
                    "Descripción": nuevos[col_desc_nue_renamed],
                    "Resguardante Actual": nuevos[col_resp_nue_renamed]
                })
                st.dataframe(resumen_nuev, use_container_width=True)
            else:
                st.info("No hay registros nuevos en el último inventario.")

        # Exportación
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if not encontrados.empty:
                resumen_loc.to_excel(writer, sheet_name='Coincidentes', index=False)
            if not faltantes.empty:
                resumen_falt.to_excel(writer, sheet_name='Faltantes', index=False)
            if not nuevos.empty:
                resumen_nuev.to_excel(writer, sheet_name='Sobrantes_Nuevas_Altas', index=False)
        output.seek(0)

        st.markdown("---")
        st.download_button(
            label="📥 Descargar Reporte Comparativo en Excel",
            data=output,
            file_name="Reporte_Comparativo_Inventario.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
