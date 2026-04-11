import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# --- IMPORTACIÓN SEGURA ---
try:
    import acouniverso as aco
except ImportError:
    aco = None

try:
    import santiagoarango as santi
except ImportError:
    santi = None

try:
    import acopadmouse as pad
except ImportError:
    pad = None

# 1. Configuración única
st.set_page_config(page_title="Agro-pro Hub", layout="wide")

class AgroProApp:
    def __init__(self):
        self.WHATSAPP_NUM = "573122204688"
        self.inicializar_sesion()

    def inicializar_sesion(self):
        if 'carrito' not in st.session_state: st.session_state.carrito = []
        if 'pagina_actual' not in st.session_state: st.session_state.pagina_actual = "principal"
        if 'cliente' not in st.session_state: st.session_state.cliente = ""

    def enviar_whatsapp(self, total):
        mensaje = f"🚀 *Nuevo Pedido Agro-pro*\n\n👤 *Cliente:* {st.session_state.cliente}\n📦 *Detalle:*\n"
        for item in st.session_state.carrito:
            mensaje += f"- {item['cantidad']} x {item['producto']} (${item['subtotal']:,})\n"
        mensaje += f"\n💰 *TOTAL: ${total:,}*"
        return f"https://wa.me/{self.WHATSAPP_NUM}?text={urllib.parse.quote(mensaje)}"

    def render_ui(self):
        if st.session_state.pagina_actual == "acouniverso" and aco:
            aco.render_catalogo(); return
        if st.session_state.pagina_actual == "mugs_santiago" and santi:
            santi.render_galeria_santiago(); return
        if st.session_state.pagina_actual == "acopadmouse" and pad:
            pad.render_padmouse(); return

        # --- MENÚ PRINCIPAL ---
        st.markdown("""<style>
            [data-testid="stColumn"]:nth-child(2) { position: sticky; top: 2rem; }
            .no-disponible { opacity: 0.5; filter: grayscale(1); pointer-events: none; padding: 8px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9; margin-bottom: 5px; }
        </style>""", unsafe_allow_html=True)

        st.title("🚀 Agro-pro Hub")
        st.write("Bienvenido a tienda móvil Agro-pro, encontrarás diferentes productos de alimentos, electrónica y arte")
        st.warning("⚠️ No refresques la página, regresa al menú anterior con el botón 'regresar al menú principal'")
        
        st.session_state.cliente = st.text_input("Nombre del Cliente", value=st.session_state.cliente)
        
        col_izq, col_der = st.columns([0.6, 0.4])

        with col_izq:
            st.header("🥚 Alimentos")
            # Huevos Oro
            cant_h = st.number_input("Huevos oro Panal x30 - $16,000", min_value=0, step=1)
            if st.button("Añadir Huevos"):
                if cant_h > 0:
                    st.session_state.carrito.append({"producto": "Huevos oro Panal x30", "cantidad": cant_h, "subtotal": cant_h * 16000})

            st.markdown('<div class="no-disponible">🚫 Azúcar Incauca - No disponible</div>', unsafe_allow_html=True)
            st.markdown('<div class="no-disponible">🚫 Café Sello Rojo - No disponible</div>', unsafe_allow_html=True)

            st.header("⚡ Electrónica")
            st.subheader("Experimento básico de luz LED")
            st.write("Para personas de 8 y 99 años, entretenido y para descubrir el mundo de la electrónica.")
            st.image("acoelectronica2.jpeg", width=250)
            if st.button("Añadir Kit LED ($100.000)"):
                st.session_state.carrito.append({"producto": "Kit LED", "cantidad": 1, "subtotal": 100000})

            # --- HUB DE ARTE ---
            st.header("🎨 Módulos de Arte")
            
            # Alfonso
            st.subheader("🖼️ Alfonso Cañas")
            st.write("Precios: $2.000 papel normal | $15.000 papel fotográfico")
            if aco:
                if st.button("Ver Fotos e Imágenes"):
                    st.session_state.pagina_actual = "acouniverso"; st.rerun()
            else: st.error("Módulo acouniverso.py no encontrado")
            
            # Santiago
            st.divider()
            st.subheader("☕ Santiago Arango")
            st.write("Mugs de colección: $38.000")
            if santi:
                if st.button("Ver Mugs Colección"):
                    st.session_state.pagina_actual = "mugs_santiago"; st.rerun()
            else: st.error("Módulo santiagoarango.py no encontrado")

        with col_der:
            st.subheader("📋 Carrito")
            if st.session_state.carrito:
                df = pd.DataFrame(st.session_state.carrito)
                st.table(df[['producto', 'cantidad', 'subtotal']])
                total = df['subtotal'].sum()
                st.metric("Total", f"${total:,}")
                if st.button("✅ ENVIAR PEDIDO"):
                    if st.session_state.cliente:
                        st.markdown(f'<a href="{self.enviar_whatsapp(total)}" target="_blank">Abrir WhatsApp</a>', unsafe_allow_html=True)
                if st.button("Vaciar"):
                    st.session_state.carrito = []; st.rerun()
            else: st.info("Carrito vacío.")

if __name__ == "__main__":
    app = AgroProApp(); app.render_ui()