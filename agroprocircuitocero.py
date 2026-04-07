import streamlit as st
import pandas as pd
import json
import os
import urllib.parse
from datetime import datetime
# Importación técnica del módulo solicitado
from acouniverso import render_catalogo

class AgroProApp:
    def __init__(self):
        self.DATA_FILE = "pedidos_agropro.json"
        self.WHATSAPP_NUM = "573122204688"
        self.PRECIOS = {
            "Huevos Panal x30": 16000,
            "Fotografía Universo": 25000,
            "Ilustración ACOuniverso": 25000
        }
        self.inicializar_sesion()

    def inicializar_sesion(self):
        if 'carrito' not in st.session_state:
            st.session_state.carrito = []
        # Estado de navegación entre módulos
        if 'pagina_actual' not in st.session_state:
            st.session_state.pagina_actual = "principal"

    def enviar_whatsapp(self, cliente, total):
        mensaje = f"🚀 *Nuevo Pedido Agro-pro*\n\n"
        mensaje += f"👤 *Cliente:* {cliente}\n"
        mensaje += f"📅 *Fecha:* {datetime.now().strftime('%d/%m/%Y')}\n\n"
        mensaje += "📦 *Detalle:*\n"
        
        for item in st.session_state.carrito:
            mensaje += f"- {item['cantidad']} x {item['producto']} (${item['subtotal']:,})\n"
        
        mensaje += f"\n💰 *TOTAL A PAGAR: ${total:,}*"
        
        texto_url = urllib.parse.quote(mensaje)
        url_ws = f"https://wa.me/{self.WHATSAPP_NUM}?text={texto_url}"
        return url_ws

    def render_ui(self):
        # Lógica de enrutamiento técnico
        if st.session_state.pagina_actual == "acouniverso":
            render_catalogo()
            return

        st.set_page_config(page_title="Agro-pro Logistics", layout="wide")
        st.title("🚀 Agro-pro: Miércoles de Surtido Alacena")
        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🛒 Catálogo de Productos")
            cliente = st.text_input("Nombre del Cliente", placeholder="Ej: Alfonso")

            # Sección Huevos
            cant_h = st.number_input("Huevos Panal x30 ($16,000)", min_value=0, step=1)
            if st.button("Añadir Huevos"):
                if cant_h > 0:
                    st.session_state.carrito.append({"producto": "Huevos Panal x30", "cantidad": cant_h, "subtotal": cant_h * 16000})
                    st.success("Huevos añadidos")

            # Sección Fotografía
            st.markdown("---")
            st.write("📷 **Fotografías del Universo**")
            if st.button("Ingresar a fotografiasuniverso.py"):
                st.info("Módulo en desarrollo...")
            
            cant_f = st.number_input("Cantidad de Fotografías ($25,000)", min_value=0, step=1, key="cant_foto")
            if st.button("Añadir Fotografías"):
                if cant_f > 0:
                    st.session_state.carrito.append({"producto": "Fotografía Universo", "cantidad": cant_f, "subtotal": cant_f * 25000})

            # Sección ACOuniverso - Navegación inyectada
            st.markdown("---")
            st.write("🎨 **Ilustraciones ACOuniverso**")
            if st.button("Ingresar a acouniverso.py"):
                st.session_state.pagina_actual = "acouniverso"
                st.rerun()

            cant_a = st.number_input("Cantidad de Ilustraciones ($25,000)", min_value=0, step=1, key="cant_ilustra")
            if st.button("Añadir Ilustraciones"):
                if cant_a > 0:
                    st.session_state.carrito.append({"producto": "Ilustración ACOuniverso", "cantidad": cant_a, "subtotal": cant_a * 25000})

        with col2:
            st.subheader("📋 Carrito Conciliado")
            if st.session_state.carrito:
                df = pd.DataFrame(st.session_state.carrito)
                st.table(df)
                total = df['subtotal'].sum()
                st.metric("Total", f"${total:,}")

                if st.button("✅ Terminar y enviar a WhatsApp"):
                    if cliente:
                        url = self.enviar_whatsapp(cliente, total)
                        st.markdown(f'''
                            <a href="{url}" target="_blank">
                                <button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">
                                    Abrir WhatsApp para enviar pedido
                                </button>
                            </a>
                            ''', unsafe_allow_html=True)
                    else:
                        st.error("Por favor, ingresa el nombre del cliente.")
            
            if st.button("Vaciar Carrito"):
                st.session_state.carrito = []
                st.rerun()

if __name__ == "__main__":
    app = AgroProApp()
    app.render_ui()