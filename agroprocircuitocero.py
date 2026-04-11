import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
import acouniverso as aco
import santiagoarango as santi

# CONFIGURACIÓN ÚNICA (Solo aquí)
st.set_page_config(page_title="Agro-pro Logistics", layout="wide")

class AgroProApp:
    def __init__(self):
        self.WHATSAPP_NUM = "573122204688"
        self.inicializar_sesion()

    def inicializar_sesion(self):
        if 'carrito' not in st.session_state: st.session_state.carrito = []
        if 'pagina_actual' not in st.session_state: st.session_state.pagina_actual = "principal"
        if 'cliente' not in st.session_state: st.session_state.cliente = ""

    def enviar_whatsapp(self, total):
        mensaje = f"🚀 *Nuevo Pedido Agro-pro*\n\n👤 *Cliente:* {st.session_state.cliente}\n\n📦 *Detalle:*\n"
        for item in st.session_state.carrito:
            mensaje += f"- {item['cantidad']} x {item['producto']} (${item['subtotal']:,})\n"
        mensaje += f"\n💰 *TOTAL: ${total:,}*"
        return f"https://wa.me/{self.WHATSAPP_NUM}?text={urllib.parse.quote(mensaje)}"

    def render_ui(self):
        # NAVEGACIÓN
        if st.session_state.pagina_actual == "acouniverso":
            aco.render_catalogo()
            return
        if st.session_state.pagina_actual == "mugs_santiago":
            santi.render_galeria_santiago()
            return

        # PÁGINA PRINCIPAL
        st.markdown("""<style>
            [data-testid="stColumn"]:nth-child(2) { position: sticky; top: 2rem; }
            .disponible-no { opacity: 0.4; filter: grayscale(1); pointer-events: none; }
        </style>""", unsafe_allow_html=True)

        st.warning("⚠️ No refresques la página. Usa los botones de 'regresar'.")
        st.title("🚀 Agro-pro: Miércoles de Surtido")
        
        st.session_state.cliente = st.text_input("Nombre del Cliente", value=st.session_state.cliente)
        
        col_izq, col_der = st.columns([0.6, 0.4])

        with col_izq:
            st.header("🥚 Alimentos")
            cant_h = st.number_input("Huevos Panal x30 ($16,000)", min_value=0, step=1)
            if st.button("Añadir Huevos"):
                if cant_h > 0:
                    st.session_state.carrito.append({"producto": "Huevos Panal x30", "cantidad": cant_h, "subtotal": cant_h * 16000})
                    st.success("Huevos añadidos")

            st.header("⚡ Electrónica")
            st.image("acoelectronica2.jpeg", width=250)
            if st.button("Añadir Kit LED ($100.000)"):
                st.session_state.carrito.append({"producto": "Kit LED", "cantidad": 1, "subtotal": 100000})

            st.header("🎨 Arte y Accesorios")
            if st.button("🖼️ Ver Dibujos/Fotos"):
                st.session_state.pagina_actual = "acouniverso"; st.rerun()
            if st.button("☕ Ver Mugs (Santiago)"):
                st.session_state.pagina_actual = "mugs_santiago"; st.rerun()

        with col_der:
            st.subheader("📋 Carrito")
            if st.session_state.carrito:
                df = pd.DataFrame(st.session_state.carrito)
                st.table(df[['producto', 'cantidad', 'subtotal']])
                total = df['subtotal'].sum()
                st.metric("Total", f"${total:,}")
                if st.button("✅ ENVIAR PEDIDO"):
                    if st.session_state.cliente:
                        st.markdown(f'<a href="{self.enviar_whatsapp(total)}" target="_blank"><button style="background-color:#25D366; color:white; padding:10px; border-radius:5px;">ABRIR WHATSAPP</button></a>', unsafe_allow_html=True)
                if st.button("Vaciar"):
                    st.session_state.carrito = []; st.rerun()
            else: st.info("Carrito vacío.")

if __name__ == "__main__":
    app = AgroProApp(); app.render_ui()