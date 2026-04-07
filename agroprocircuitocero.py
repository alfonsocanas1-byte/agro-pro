import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

class AgroProApp:
    def __init__(self):
        self.DATA_FILE = "pedidos_agropro.json"
        self.PRECIOS = {
            "Huevos Panal x30": 16000,
            "Fotografía Universo": 25000,
            "Ilustración ACOuniverso": 25000
        }
        self.inicializar_sesion()

    def inicializar_sesion(self):
        if 'carrito' not in st.session_state:
            st.session_state.carrito = []

    def guardar_pedido_json(self, cliente):
        pedido = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cliente": cliente,
            "items": st.session_state.carrito,
            "total": sum(i['subtotal'] for i in st.session_state.carrito)
        }
        
        datos = []
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r") as f:
                datos = json.load(f)
        
        datos.append(pedido)
        with open(self.DATA_FILE, "w") as f:
            json.dump(datos, f, indent=4)

    def render_ui(self):
        st.set_page_config(page_title="Agro-pro Logistics", layout="wide")
        
        st.title("🚀 Agro-pro: Miércoles de Surtido Alacena")
        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🛒 Catálogo de Productos")
            cliente = st.text_input("Nombre del Cliente", placeholder="Ej: Residencia Cali")
            
            for producto, precio in self.PRECIOS.items():
                cant = st.number_input(f"{producto} (${precio})", min_value=0, step=1, key=producto)
                if st.button(f"Añadir {producto.split()[0]}", key=f"btn_{producto}"):
                    if cant > 0:
                        st.session_state.carrito.append({
                            "producto": producto,
                            "cantidad": cant,
                            "precio_unitario": precio,
                            "subtotal": cant * precio
                        })
                        st.success(f"Añadido: {producto}")

        with col2:
            st.subheader("📋 Resumen del Pedido")
            if st.session_state.carrito:
                df = pd.DataFrame(st.session_state.carrito)
                st.table(df[['producto', 'cantidad', 'subtotal']])
                
                total = df['subtotal'].sum()
                st.metric("Total a Cobrar", f"${total:,}")

                if st.button("Confirmar Pedido y Registrar en Ruta"):
                    if cliente:
                        self.guardar_pedido_json(cliente)
                        st.balloons()
                        st.info(f"Logística: Carga en Huevos Oro para {cliente} confirmada.")
                        st.session_state.carrito = []
                    else:
                        st.error("Error: Ingrese el nombre del cliente.")
            else:
                st.write("El carrito está vacío.")

        # Histórico de Pedidos con Pandas
        if os.path.exists(self.DATA_FILE):
            st.markdown("---")
            st.subheader("🚛 Hoja de Ruta (Historial)")
            with open(self.DATA_FILE, "r") as f:
                historico = json.load(f)
            st.dataframe(pd.DataFrame(historico))

if __name__ == "__main__":
    app = AgroProApp()
    app.render_ui()