import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
import acouniverso as aco
import santiagoarango as santi

# Configuración única
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
        mensaje += "📦 *Detalle:*\n"
        for item in st.session_state.carrito:
            mensaje += f"- {item['cantidad']} x {item['producto']} (${item['subtotal']:,})\n"
        mensaje += f"\n💰 *TOTAL A PAGAR: ${total:,}*"
        return f"https://wa.me/{self.WHATSAPP_NUM}?text={urllib.parse.quote(mensaje)}"

    def render_ui(self):
        # Enrutamiento de Módulos
        if st.session_state.pagina_actual == "acouniverso":
            aco.render_catalogo()
            return
        if st.session_state.pagina_actual == "mugs_santiago":
            santi.render_galeria_santiago()
            return

        # PÁGINA PRINCIPAL - RESTAURACIÓN DE TEXTOS
        st.markdown("""<style>
            [data-testid="stColumn"]:nth-child(2) { position: sticky; top: 2rem; }
            .disponible-no { opacity: 0.4; filter: grayscale(1); pointer-events: none; }
        </style>""", unsafe_allow_html=True)

        # Advertencia de navegación
        st.warning("⚠️ **No refresques la página ni te devuelvas con la flecha <-** debido a que puede perder la memoria temporal del carrito, usa los botones de **'regresar al menú principal'**.")
        
        st.title("🚀 Agro-pro: Miércoles de Surtido Alacena")
        
        # Registro
        st.header("👤 Registro")
        st.session_state.cliente = st.text_input("Nombre del Cliente", value=st.session_state.cliente, placeholder="Escriba su nombre...")
        st.markdown("---")

        col_izq, col_der = st.columns([0.6, 0.4])

        with col_izq:
            # ALIMENTOS
            st.header("🥚 Alimentos")
            cant_h = st.number_input("Huevos Panal x30 (Huevos Oro) - $16,000", min_value=0, step=1)
            if st.button("Añadir Huevos"):
                if cant_h > 0:
                    st.session_state.carrito.append({"producto": "Huevos Panal x30", "cantidad": cant_h, "subtotal": cant_h * 16000})
                    st.success("Huevos añadidos")

            # ELECTRÓNICA
            st.markdown("---")
            st.header("⚡ Electrónica")
            st.subheader("Primer sistema básico para iluminar luz LED desde cero")
            st.write("Costo: $100.000 (Incluye instrucciones y explicación para personas entre 8 y 99 años)")
            c1, c2 = st.columns(2)
            c1.image("acoelectronica1.jpeg", width=200, caption="Componentes (Desarmado)")
            c2.image("acoelectronica2.jpeg", width=200, caption="Sistema Armado")
            
            if st.button("Añadir Kit Electrónica ($100.000)"):
                st.session_state.carrito.append({"producto": "Kit Electrónica Básico", "cantidad": 1, "subtotal": 100000})

            # ARTE
            st.markdown("---")
            st.header("🎨 Arte y Accesorios")
            st.write("- Dibujos o fotografías en papel fotográfico: **$15.000**.")
            st.write("- Dibujos de Alfonso Cañas Orduz, únicos y originales a **$2.000** en papel normal.")
            
            if st.button("🖼️ Ingresar para ver la galería de acouniverso"):
                st.session_state.pagina_actual = "acouniverso"
                st.rerun()
            
            if st.button("☕ Ingresar a Pocillos Mug (Santiago Arango)"):
                st.session_state.pagina_actual = "mugs_santiago"
                st.rerun()

        with col_der:
            st.subheader("📋 Carrito Conciliado")
            if st.session_state.carrito:
                df = pd.DataFrame(st.session_state.carrito)
                st.table(df[['producto', 'cantidad', 'subtotal']])
                total = df['subtotal'].sum()
                st.metric("Total a pagar", f"${total:,}")
                if st.button("✅ ENVIAR PEDIDO"):
                    if st.session_state.cliente:
                        st.markdown(f'<a href="{self.enviar_whatsapp(total)}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">ABRIR WHATSAPP</button></a>', unsafe_allow_html=True)
                if st.button("Vaciar Carrito"):
                    st.session_state.carrito = []
                    st.rerun()
            else:
                st.info("Carrito vacío.")

if __name__ == "__main__":
    app = AgroProApp()
    app.render_ui()