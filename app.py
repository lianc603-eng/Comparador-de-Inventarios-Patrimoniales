import streamlit as st
import pandas as pd
import io

# Catálogo Maestro del Personal y sus Departamentos
PERSONAL_DEPTOS = {
    "SANCHEZ PREVE ROSENDO": "OFICINA DE LA DIRECCION DE DESARROLLO URBANO Y MEDIO AMBIENTE",
    "ARGUELLES CASTRO VERONICA BERENICE": "OFICINA DE LA DIRECCION DE DESARROLLO URBANO Y MEDIO AMBIENTE",
    "MAY MASS REYNA ANTONIA": "OFICINA DE LA DIRECCION DE DESARROLLO URBANO Y MEDIO AMBIENTE",
    "PAREDES MISS RUBEN HILARIO": "OFICINA DE LA DIRECCION DE DESARROLLO URBANO Y MEDIO AMBIENTE",
    "R DE LA GALA CHABLE JORGE MARTIN": "OFICINA DE LA DIRECCION DE DESARROLLO URBANO Y MEDIO AMBIENTE",
    "BROWN OCAÑA CITLALLI ESTEFANIA": "DEPARTAMENTO ADMINISTRATIVO",
    "CRUZ PAT LIAN VADHIR": "DEPARTAMENTO ADMINISTRATIVO",
    "ALONZO HERRERA FRANCISCO JAVIER": "DEPARTAMENTO ADMINISTRATIVO",
    "EUAN CHABLE MARCO ANTONIO": "DEPARTAMENTO ADMINISTRATIVO",
    "NAVARRO PACHECO LEIDY CONSUELO": "DEPARTAMENTO ADMINISTRATIVO",
    "CETINA ARGUELLES RENAN DE ATOCHA": "DEPARTAMENTO JURIDICO",
    "BRITO AKE GABRIELA BEATRIZ": "DEPARTAMENTO JURIDICO",
    "VALLE QUEVEDO KARINA DEL CARMEN": "DEPARTAMENTO JURIDICO",
    "QUEN UC ZOILA REINA DE LOS ANGELES": "DEPARTAMENTO JURIDICO",
    "PEREZ ANGULO SAMANTHA FERNANDA": "SUBDIRECCION TECNICA DE DESARROLLO URBANO Y MEDIO AMBIENTE",
    "SEGOVIA KOYOC IRMA GUADALUPE": "SUBDIRECCION TECNICA DE DESARROLLO URBANO Y MEDIO AMBIENTE",
    "REJON CETINA JESSICA": "SUBDIRECCION TECNICA DE DESARROLLO URBANO Y MEDIO AMBIENTE",
    "HERNANDEZ FERNANDEZ SUSUKI ENID": "DEPARTAMENTO DE INSPECCION",
    "CANUL MISS BRENDA ELENA": "DEPARTAMENTO DE INSPECCION",
    "CHAN MIAN JUAN NOEL": "DEPARTAMENTO DE INSPECCION",
    "DZUL QUE ROMAN JESUS": "DEPARTAMENTO DE INSPECCION",
    "CAHUICH MANRRERO LUIS ALBERTO": "DEPARTAMENTO DE INSPECCION",
    "SARAVIA PACHECO AXEL ALONSO": "DEPARTAMENTO DE INSPECCION",
    "CONTRERAS SALAZAR FRANCISCO XAVIER": "DEPARTAMENTO DE INSPECCION",
    "COBOS ZAPATA DELTA PATRICIA": "DEPARTAMENTO DE INSPECCION",
    "CAHUICH CHE DIANA BEATRIZ": "DEPARTAMENTO OPERATIVO",
    "BURAD SANCHEZ KARIME DEL CARMEN": "DEPARTAMENTO DE VIABILIDAD Y CULTURA AMBIENTAL",
    "FUENTES RIVERO VICTORIA GUADALUPE": "SUBDIRECCION DE DESARROLLO URBANO",
    "TE MORENO MARTINA DEL CARMEN": "SUBDIRECCION DE DESARROLLO URBANO",
    "ABREU ARTEAGA PAULA ESTELA": "DEPARTAMENTO DE NOMENCLATURA Y SEÑALIZACION",
    "BOLIVAR RODRIGUEZ DANIEL ENRIQUE": "DEPARTAMENTO DE NOMENCLATURA Y SEÑALIZACION",
    "ESPINOSA UC JUAN GABRIEL": "DEPARTAMENTO DE NOMENCLATURA Y SEÑALIZACION",
    "HERRERA CHI AGUSTIN HIGINIO": "DEPARTAMENTO DE NOMENCLATURA Y SEÑALIZACION",
    "CAMARA LARA JOSE ADRIAN": "DEPARTAMENTO DE NOMENCLATURA Y SEÑALIZACION",
    "UC MAY JOSE MARTIN": "DEPARTAMENTO DE NOMENCLATURA Y SEÑALIZACION",
    "AGUILAR BALAM ADRIANA MARGARITA": "DEPARTAMENTO DE NOMENCLATURA Y SEÑALIZACION",
    "CUANDON ALONZO ZOILA FARIDE": "DEPARTAMENTO DE NOMENCLATURA Y SEÑALIZACION",
    "ZETINA BARRIENTOS JORGE PABLO": "DEPARTAMENTO DE URBANISMO",
    "PECH MUT FRANCISCO ALBERTO": "DEPARTAMENTO DE URBANISMO",
    "SULU CABALLERO PEDRO DAVID": "DEPARTAMENTO DE URBANISMO",
    "PEREZ MACIAS HECTOR LEONEL": "DEPARTAMENTO DE URBANISMO",
    "ZAZUETA HERNANDEZ MASILEMA DEL ROCIO": "DEPARTAMENTO DE URBANISMO",
    "UICAB CORTEZ SALVADOR": "DEPARTAMENTO DE URBANISMO",
    "GALLARDO PINO ALEJANDRA": "DEPARTAMENTO DE URBANISMO",
    "MAY ACOSTA GREGORIO ALAN": "COORDINACION DE IMAGEN URBANA Y LICENCIAS",
    "CHAVEZ GARDUZA TATIANA ISABEL": "COORDINACION DE IMAGEN URBANA Y LICENCIAS",
    "CU TUZ CARLOS GUADALUPE": "DEPARTAMENTO DE MOVILIDAD URBANA Y ZONA HISTORICA",
    "ALCOCER PAVON FARID ADAN": "DEPARTAMENTO DE MOVILIDAD URBANA Y ZONA HISTORICA",
    "PACHECO MARTINEZ HELDER DE JESUS": "COORDINACION DE INSPECCION URBANA",
    "FLORES VERGAR MARIO EDIBERTO": "DEPARTAMENTO DE INSPECCION URBANA Y NOTIFICACION",
    "PEREZ MAZIN CARLOS EDUARDO": "DEPARTAMENTO DE INSPECCION URBANA Y NOTIFICACION",
    "ARROYO AVILEZ IRAID EDEY": "DEPARTAMENTO DE INSPECCION URBANA Y NOTIFICACION",
    "COB CHAVEZ NARCISO DEL JESUS": "DEPARTAMENTO DE INSPECCION URBANA Y NOTIFICACION",
    "ORTEGA VILLACIS LUIS ALBERTO": "DEPARTAMENTO DE INSPECCION URBANA Y NOTIFICACION",
    "MEDINA PEREZ SANDRA BEATRIZ": "DEPARTAMENTO DE INSPECCION URBANA Y NOTIFICACION",
    "RIVERO TUN GLORIA GEOVANA": "DEPARTAMENTO DE INSPECCION URBANA Y NOTIFICACION",
    "DE LA CRUZ PEREZ WILLIAN ARLEY": "DEPARTAMENTO DE INSPECCION URBANA Y NOTIFICACION",
    "GONZALEZ MARIN ANA ALEXANDRA": "SUBDIRECCION DE MEDIO AMBIENTE",
    "HAU LEON OMAR IVAN": "SUBDIRECCION DE MEDIO AMBIENTE",
    "RODRIGUEZ MADRIGAL JOSUE": "SUBDIRECCION DE MEDIO AMBIENTE",
    "GONZALEZ CASTILLO ANGEL SANTIAGO": "SUBDIRECCION DE MEDIO AMBIENTE",
    "SALAZAR BADILLO JESUS ESTEBAN": "COORDINACION DE GESTION Y CONTROL OPERATIVO AMBIENTAL",
    "ESCALANTE NOH EMIGDIO ELIAS": "COORDINACION DE GESTION Y CONTROL OPERATIVO AMBIENTAL",
    "CABALLERO LOPEZ JOSE JUAN": "COORDINACION DE GESTION Y CONTROL OPERATIVO AMBIENTAL",
    "QUEVEDO CONTRERAS JOSE LUIS": "COORDINACION DE GESTION Y CONTROL OPERATIVO AMBIENTAL",
    "BARRIENTOS JIMENEZ JORGE LUIS": "COORDINACION DE GESTION Y CONTROL OPERATIVO AMBIENTAL",
    "MEDINA QUIJANO CARLOS ENRIQUE": "COORDINACION DE GESTION Y CONTROL OPERATIVO AMBIENTAL",
    "RAMIREZ KU MARTIN FEDERICO": "COORDINACION DE GESTION Y CONTROL OPERATIVO AMBIENTAL",
    "VAZQUEZ ESTRELLA JUAN ESTEBAN": "COORDINACION DE GESTION Y CONTROL OPERATIVO AMBIENTAL",
    "CAMARA MARTINEZ JORGE MELIK": "COORDINACION DE GESTION Y CONTROL OPERATIVO AMBIENTAL",
    "MANZANILLA GONZALEZ ROBERTO FRANCISCO": "DEPARTAMENTO DE BIENESTAR ANIMAL",
    "OROPEZA CHAVEZ OMAR": "DEPARTAMENTO DE BIENESTAR ANIMAL",
    "DEL ANGEL TAFOYA FAUSTO ROLANDO": "DEPARTAMENTO DE BIENESTAR ANIMAL",
    "CORDOVA GARCIA FLORISEL": "DEPARTAMENTO DE BIENESTAR ANIMAL",
    "KANTUN CHABLE ERNESTO WILIAN": "DEPARTAMENTO DE BIENESTAR ANIMAL",
    "SAGUNDO GONZALEZ VALDEMAR": "DEPARTAMENTO DE BIENESTAR ANIMAL",
    "CALDERON COLLI FERNANDO MARTIN": "DEPARTAMENTO DE BIENESTAR ANIMAL",
    "PEREZ GOMEZ MANUEL ALEJANDRO": "DEPARTAMENTO DE BIENESTAR ANIMAL",
    "BUSTAMANTE CU MIGUEL ANTONIO": "DEPARTAMENTO DE BIENESTAR ANIMAL",
    "HERRERA RIVERO MIGUEL ANGEL": "DEPARTAMENTO DE BIENESTAR ANIMAL",
    "MARTINEZ CELIS EDITH CONCEPCION": "DEPARTAMENTO DE BIENESTAR ANIMAL",
    "LIC. SANCHEZ PREVE ROSENDO": "BODEGA DE LA OFICINA",
    "PECH MUT FRANCISCO ALBERTO 2": "BODEGA DE DESARROLLO URBANO",
    "CAIM": "SUBDIRECCION DE MEDIO AMBIENTE"
}

def normalizar_nombre(val):
    if pd.isna(val):
        return ""
    return str(val).strip().upper()

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

    st.markdown("---")
    # Opción toggle para incluir el departamento
    incluir_depto = st.toggle("🏢 Incluir Departamento asignado a los Resguardantes", value=False)

    if st.button("🔍 Comparar Inventarios", type="primary"):
        # Normalizar claves
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

                if incluir_depto:
                    resumen_loc["Depto. Resguardante Anterior"] = resumen_loc["Resguardante Anterior"].apply(normalizar_nombre).map(PERSONAL_DEPTOS).fillna("")
                    resumen_loc["Depto. Resguardante Actual"] = resumen_loc["Resguardante Actual"].apply(normalizar_nombre).map(PERSONAL_DEPTOS).fillna("")

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

                if incluir_depto:
                    resumen_falt["Departamento"] = resumen_falt["Último Resguardante Conocido"].apply(normalizar_nombre).map(PERSONAL_DEPTOS).fillna("")

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

                if incluir_depto:
                    resumen_nuev["Departamento"] = resumen_nuev["Resguardante Actual"].apply(normalizar_nombre).map(PERSONAL_DEPTOS).fillna("")

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
