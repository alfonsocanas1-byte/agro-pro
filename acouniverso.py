import streamlit as st

def render_catalogo():
    st.title("🎨 Ilustraciones ACOuniverso")
    st.write("Dibujos de Alfonso Cañas Orduz, únicos y originales.")
    st.write("**Precio:** $15.000 (en papel fotográfico)")

    # Botón de retorno al núcleo
    if st.button("⬅️ Regresar al menú principal"):
        st.session_state.pagina_actual = "principal"
        st.rerun()

    st.markdown("---")

    # Definición técnica de los archivos en el repositorio
    ilustraciones = [
        {"ref": "acouniverso1.jpg", "nombre": "Dibujo único 1"},
        {"ref": "acouniverso2.jpg", "nombre": "Dibujo único 2"},
        {"ref": "acouniverso3.jpg", "nombre": "Dibujo único 3"},
        {"ref": "acouniverso4.jpg", "nombre": "Dibujo único 4"}
    ]

    # Renderizado vertical con imágenes reducidas
    for item in ilustraciones:
        with st.container():
            try:
                # Ajuste técnico: width=300 reduce el tamaño visual en pantalla
                st.image(item['ref'], caption=f"Referencia: {item['ref']}", width=300)
            except:
                st.error(f"Archivo {item['ref']} no encontrado.")
            
            # Controles de pedido
            cant = st.number_input(
                f"Cantidad para {item['ref']}", 
                min_value=0, 
                step=1, 
                key=f"input_{item['ref']}"
            )
            
            if st.button(f"Confirmar {item['ref']}", key=f"btn_{item['ref']}"):
                if cant > 0:
                    st.session_state.carrito.append({
                        "producto": f"Dibujo: {item['ref']}",
                        "cantidad": cant,
                        "subtotal": cant * 15000
                    })
                    st.success(f"Añadido: {cant} unidad(es) de {item['ref']}")
            
            st.markdown("---") 

    st.info(f"Items actuales en memoria: {len(st.session_state.carrito)}")