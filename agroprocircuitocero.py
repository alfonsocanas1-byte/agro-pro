import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
import acouniverso as aco
import santiagoarango as santi

# 1. CONFIGURACIÓN DE PÁGINA (Única para toda la app)
st.set_page_config(page_title="Agro-pro Logistics", layout="wide")

class AgroProApp:
    def __init__(self):
        self.WHATSAPP_NUM = "573122204688"
        self.inicializar_sesion()

    def inicializar_sesion(self):
        if 'carrito' not in st.session_state:
            st.session_state.carrito = []
        if 'pagina_actual' not in st.session_state:
            st.session_state.pagina_actual = "principal"
        if 'cliente' not in st.session_state:
            st.session_state.cliente = ""

    def enviar_whatsapp(self, total):
        mensaje = f"🚀 *Nuevo Pedido Agro-pro*\n\n"
        mensaje += f"👤 *Cliente:* {st.session_state.cliente}\n"
        mensaje += f"📅 *Fecha:* {datetime.now().strftime('%d/%m/%Y')}\n\n"
        mensaje += "📦 *Detalle:*\n"
        for item in st.session_state.carrito:
            mensaje += f"- {item['cantidad']} x {item['producto']} (${item['subtotal']:,})\n"
        mensaje += f"\n💰 *TOTAL A PAGAR: ${total:,}*"
        return f"https://wa.me/{self.WHATSAPP_NUM}?text={urllib.parse.quote(mensaje)}"

    def render_ui(self):
        # LÓGICA DE NAVEGACIÓN (Esto controla qué se ve)
        if st.session_state.pagina_actual == "acouniverso":
            aco.render_catalogo()
            return
        
        if st.session_state.pagina_actual == "mugs_santiago":
            santi.render_galeria_santiago()
            return

        # --- PÁGINA PRINCIPAL (TODO LO QUE DICES QUE SE PERDIÓ) ---
        st.markdown("""<style>
            [data-testid="stColumn"]:nth-child(2) { position: sticky; top: 2rem; }
            .disponible-no { opacity: 0.4; filter: grayscale(1); pointer-events: none; }
        </style>""", unsafe_allow_html=True)

        st.title("🚀 Agro-pro: Miércoles de Surtido Alacena")
        
        # Registro de cliente
        st.session_state.cliente = st.text_input("Nombre del Cliente", value=st.session_state.cliente)
        st.markdown("---")

        col_izq, col_der = st.columns([0.6, 0.4])

        with col_izq:
            # SECCIÓN HUEVOS
            st.header("🥚 Alimentos")
            cant_h = st.number_input("Huevos Panal x30 (Oro) - $16,000", min_value=0, step=1)
            if st.button("Añadir Huevos"):
                if cant_h > 0:
                    st.session_state.carrito.append({"producto": "Huevos Panal x30", "cantidad": cant_h, "subtotal": cant_h * 16000})
                    st.success("Añadido")

            # SECCIÓN ELECTRÓNICA (RESTURADA)
            st.markdown("---")
            st.header("⚡ Electrónica")
            st.subheader("Sistema básico luz LED")
            c1, c2 = st.columns(2)
            c1.image("acoelectronica1.jpeg", width=200, caption="Componentes")
            c2.image("acoelectronica2.jpeg", width=200, caption="Sistema")
            if st.button("Añadir Kit Electrónica ($100.000)"):
                st.session_state.carrito.append({"producto": "Kit Electrónica Básico", "cantidad": 1, "subtotal": 100000})

            # SECCIÓN ARTE (LOS ACCESOS)
            st.markdown("---")
            st.header("🎨 Arte y Accesorios")
            if st.button("🖼️ Ver Dibujos o Fotos"):
                st.session_state.pagina_actual = "acouniverso"
                st.rerun()
            
            if st.button("☕ Ver Pocillos Mug (Santiago Arango)"):
                st.session_state.pagina_actual = "mugs_santiago"
                st.rerun()

        with col_der:
            # EL CARRITO STICKY
            st.subheader("📋 Carrito Conciliado")
            if st.session_state.carrito:
                df = pd.DataFrame(st.session_state.carrito)
                st.table(df[['producto', 'cantidad', 'subtotal']])
                total = df['subtotal'].sum()
                st.metric("Total", f"${total:,}")
                if st.button("✅ ENVIAR POR WHATSAPP"):
                    if st.session_state.cliente:
                        st.markdown(f'<a href="{self.enviar_whatsapp(total)}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer; font-weight:bold;">ABRIR WHATSAPP</button></a>', unsafe_allow_html=True)
                if st.button("Vaciar Carrito"):
                    st.session_state.carrito = []
                    st.rerun()
            else:
                st.info("Carrito vacío.")

if __name__ == "__main__":
    app = AgroProApp()
    app.render_ui()