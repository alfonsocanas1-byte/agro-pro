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

    # Renderizado vertical (uno por uno)
    for item in ilustraciones:
        # Contenedor individual para cada imagen y su control
        with st.container():
            try:
                st.image(item['ref'], caption=f"Referencia: {item['ref']}", use_container_width=True)
            except:
                st.error(f"Archivo {item['ref']} no encontrado en el repositorio.")
            
            # Selector de cantidad y botón de confirmación debajo de cada imagen
            cant = st.number_input(
                f"Cantidad para {item['ref']}", 
                min_value=0, 
                step=1, 
                key=f"input_{item['ref']}"
            )
            
            if st.button(f"Confirmar {item['ref']}", key=f"btn_{item['ref']}"):
                if cant > 0:
                    # Inyección de datos en el carrito global con precio de $15.000
                    st.session_state.carrito.append({
                        "producto": f"Dibujo: {item['ref']}",
                        "cantidad": cant,
                        "subtotal": cant * 15000
                    })
                    st.success(f"Añadido: {cant} unidad(es) de {item['ref']}")
                else:
                    st.warning("Seleccione una cantidad mayor a 0")
            
            st.markdown("---") # Separador visual entre items

    st.info(f"Items actuales en memoria: {len(st.session_state.carrito)}")