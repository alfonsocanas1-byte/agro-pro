import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
import acouniverso as aco
import santiagoarango as santi

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
        texto_url = urllib.parse.quote(mensaje)
        return f"https://wa.me/{self.WHATSAPP_NUM}?text={texto_url}"

    def render_ui(self):
        # Enrutamiento modular para evitar errores de carga
        if st.session_state.pagina_actual == "acouniverso":
            aco.render_catalogo()
            return
        if st.session_state.pagina_actual == "mugs_santiago":
            santi.render_galeria_santiago()
            return

        st.set_page_config(page_title="Agro-pro Logistics", layout="wide")
        
        # CSS para Sticky Sidebar y efectos visuales
        st.markdown("""
            <style>
            [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] > [data-testid="stColumn"]:nth-child(2) {
                position: -webkit-sticky; position: sticky; top: 2rem; height: max-content; z-index: 999;
            }
            .disponible-no { opacity: 0.4; filter: grayscale(1); pointer-events: none; }
            </style>
        """, unsafe_allow_html=True)

        st.warning("⚠️ **No refresques la página ni te devuelvas con la flecha <-** usa los botones de **'regresar al menú principal'**.")
        st.title("🚀 Agro-pro: Miércoles de Surtido Alacena")
        
        # SECCIÓN SUPERIOR: REGISTRO
        with st.container():
            st.header("👤 Registro")
            st.session_state.cliente = st.text_input("Nombre del Cliente", value=st.session_state.cliente, placeholder="Escriba su nombre...")
        st.markdown("---")

        col_izq, col_der = st.columns([0.6, 0.4])

        with col_izq:
            # SECCIÓN ALIMENTOS
            st.header("🥚 Alimentos")
            cant_h = st.number_input("Huevos Panal x30 (Huevos Oro) - $16,000", min_value=0, step=1)
            if st.button("Añadir Huevos"):
                if cant_h > 0:
                    st.session_state.carrito.append({"producto": "Huevos Panal x30", "cantidad": cant_h, "subtotal": cant_h * 16000})
                    st.success("Huevos añadidos")

            # SECCIÓN ELECTRÓNICA
            st.markdown("---")
            st.header("⚡ Electrónica")
            st.subheader("Primer sistema básico para iluminar luz LED desde cero")
            st.write("Costo: $100.000")
            c1, c2 = st.columns(2)
            c1.image("acoelectronica1.jpeg", width=200, caption="Componentes")
            c2.image("acoelectronica2.jpeg", width=200, caption="Sistema Armado")
            
            cant_e = st.number_input("Cantidad Kit Básico LED", min_value=0, step=1)
            if st.button("Añadir Kit Electrónica"):
                if cant_e > 0:
                    st.session_state.carrito.append({"producto": "Kit Electrónica Básico", "cantidad": cant_e, "subtotal": cant_e * 100000})

            # SECCIÓN ARTE Y ACCESORIOS
            st.markdown("---")
            st.header("🎨 Arte y Accesorios")
            
            if st.button("🖼️ Ingresar a Dibujos o Fotos ($15.000 / $2.000)"):
                st.session_state.pagina_actual = "acouniverso"
                st.rerun()
            
            if st.button("☕ Ingresar a Pocillos Mug (Santiago Arango)"):
                st.session_state.pagina_actual = "mugs_santiago"
                st.rerun()

            st.markdown('<div class="disponible-no">', unsafe_allow_html=True)
            st.button("🖱️ Padmouse - No disponible")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_der:
            # CARRITO FIJO (STICKY)
            st.subheader("📋 Carrito Conciliado")
            if st.session_state.carrito:
                df = pd.DataFrame(st.session_state.carrito)
                st.dataframe(df[['producto', 'cantidad', 'subtotal']], use_container_width=True, hide_index=True)
                total = df['subtotal'].sum()
                st.metric("Total a pagar", f"${total:,}")

                if st.button("✅ Terminar y enviar a WhatsApp"):
                    if st.session_state.cliente:
                        url = self.enviar_whatsapp(total)
                        st.markdown(f'<a href="{url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer; font-weight:bold;">ABRIR WHATSAPP</button></a>', unsafe_allow_html=True)
                    else:
                        st.error("Error: Ingrese el Nombre del Cliente.")
                
                if st.button("Vaciar Carrito"):
                    st.session_state.carrito = []
                    st.rerun()
            else:
                st.info("El carrito está vacío.")

if __name__ == "__main__":
    app = AgroProApp()
    app.render_ui()