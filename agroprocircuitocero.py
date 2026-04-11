import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
import acouniverso as aco
import santiagoarango as santi
import acopadmouse as pad  # Importación del módulo de Padmouses

# 1. Configuración única de la aplicación
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
        # --- NAVEGACIÓN ENTRE MÓDULOS ---
        if st.session_state.pagina_actual == "acouniverso":
            aco.render_catalogo()
            return
        if st.session_state.pagina_actual == "acopadmouse":
            pad.render_padmouse()
            return
        if st.session_state.pagina_actual == "mugs_santiago":
            santi.render_galeria_santiago()
            return

        # --- INTERFAZ DEL HUB (MENÚ PRINCIPAL) ---
        st.markdown("""<style>
            [data-testid="stColumn"]:nth-child(2) { position: -webkit-sticky; position: sticky; top: 2rem; height: max-content; }
            .no-disponible { opacity: 0.5; filter: grayscale(1); pointer-events: none; padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px; background-color: #f9f9f9; }
        </style>""", unsafe_allow_html=True)

        st.warning("⚠️ **No refresques la página ni te devuelvas con la flecha <-** usa los botones de 'regresar al menú principal'.")
        st.title("🚀 Agro-pro Hub: Surtido Alacena")
        
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

            st.markdown('<div class="no-disponible">🚫 Azúcar Incauca - No disponible</div>', unsafe_allow_html=True)
            st.markdown('<div class="no-disponible">🚫 Café Sello Rojo - No disponible</div>', unsafe_allow_html=True)

            # ELECTRÓNICA
            st.markdown("---")
            st.header("⚡ Electrónica")
            st.subheader("Primer sistema básico para iluminar luz LED")
            c1, c2 = st.columns(2)
            c1.image("acoelectronica1.jpeg", width=200, caption="Componentes")
            c2.image("acoelectronica2.jpeg", width=200, caption="Sistema Armado")
            if st.button("Añadir Kit Electrónica ($100.000)"):
                st.session_state.carrito.append({"producto": "Kit Electrónica Básico", "cantidad": 1, "subtotal": 100000})

            # SECCIÓN DE ARTE ORGANIZADA POR MÓDULOS
            st.markdown("---")
            st.header("🎨 Módulos de Arte")
            
            # Bloque Alfonso Cañas
            st.subheader("🖼️ Alfonso Cañas (ACOuniverso)")
            st.write("Fotos, imágenes y padmouses únicos.")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Ingresar a Fotos e Imágenes"):
                    st.session_state.pagina_actual = "acouniverso"
                    st.rerun()
            with col_b2:
                if st.button("Ingresar a Padmouses"):
                    st.session_state.pagina_actual = "acopadmouse"
                    st.rerun()
            
            st.divider()

            # Bloque Santiago Arango
            st.subheader("☕ Santiago Arango")
            st.write("Arte aplicado en pocillos (Mugs) de colección.")
            if st.button("Ingresar a galería de Mugs"):
                st.session_state.pagina_actual = "mugs_santiago"
                st.rerun()

        with col_der:
            # CARRITO STICKY
            st.subheader("📋 Carrito Conciliado")
            if st.session_state.carrito:
                df = pd.DataFrame(st.session_state.carrito)
                st.table(df[['producto', 'cantidad', 'subtotal']])
                total = df['subtotal'].sum()
                st.metric("Total a pagar", f"${total:,}")
                
                if st.button("✅ ENVIAR PEDIDO POR WHATSAPP"):
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