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

# Configuración de la aplicación
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
        st.title("🚀 Agro-pro Hub")
        st.write("Bienvenido a tienda móvil Agro-pro, encontrarás diferentes productos de alimentos, electrónica y arte")
        st.warning("⚠️ No refresques la página, regresa al menú anterior con el botón 'regresar al menú principal'")
        
        st.session_state.cliente = st.text_input("Nombre del Cliente", value=st.session_state.cliente)
        
        col_izq, col_der = st.columns([0.6, 0.4])

        with col_izq:
            st.header("🥚 Alimentos")
            cant_h = st.number_input("Huevos oro Panal x30 - $16,000", min_value=0, step=1)
            if st.button("Añadir Huevos"):
                if cant_h > 0:
                    st.session_state.carrito.append({"producto": "Huevos oro Panal x30", "cantidad": cant_h, "subtotal": cant_h * 16000})

            st.header("⚡ Electrónica")
            st.subheader("Experimento básico de luz LED")
            st.write("Para personas de 8 y 99 años, entretenido y para descubrir el mundo de la electrónica.")
            
            # Imágenes de electrónica cargadas verticalmente
            try:
                st.image("acoelectronica1.jpeg", caption="Componentes del Kit", width=300)
                st.image("acoelectronica2.jpeg", caption="Sistema Funcionando", width=300)
            except:
                st.error("Archivos de imagen de electrónica no encontrados (.jpeg)")

            if st.button("Añadir Kit LED ($100.000)"):
                st.session_state.carrito.append({"producto": "Kit LED", "cantidad": 1, "subtotal": 100000})

            st.header("🎨 Módulos de Arte")
            st.subheader("🖼️ Alfonso Cañas")
            st.write("• Papel normal: **$2.000** | • Papel fotográfico: **$15.000**")
            if aco:
                if st.button("Ver Fotos e Imágenes"):
                    st.session_state.pagina_actual = "acouniverso"; st.rerun()
            
            st.divider()
            st.subheader("☕ Santiago Arango")
            st.write("• Mugs de colección: **$38.000**")
            if santi:
                if st.button("Ver Mugs Colección"):
                    st.session_state.pagina_actual = "mugs_santiago"; st.rerun()

        with col_der:
            st.subheader("📋 Carrito")
            if st.session_state.carrito:
                df = pd.DataFrame(st.session_state.carrito)
                st.table(df[['producto', 'cantidad', 'subtotal']])
                total = df['subtotal'].sum()
                st.metric("Total", f"${total:,}")
                if st.button("✅ ENVIAR PEDIDO POR WHATSAPP"):
                    if st.session_state.cliente:
                        st.markdown(f'<a href="{self.enviar_whatsapp(total)}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">ABRIR WHATSAPP</button></a>', unsafe_allow_html=True)
                    else:
                        st.error("Por favor, ingresa el nombre del cliente.")
                if st.button("Vaciar"):
                    st.session_state.carrito = []; st.rerun()
            else: st.info("Carrito vacío.")

if __name__ == "__main__":
    app = AgroProApp(); app.render_ui()