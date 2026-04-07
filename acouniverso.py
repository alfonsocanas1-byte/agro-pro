import streamlit as st

def render_catalogo():
    st.title("🎨 Ilustraciones ACOuniverso")
    st.write("Arte original - $25.000/unidad")

    # Botón para retornar al núcleo logístico
    if st.button("⬅️ Volver a Menú Principal"):
        st.session_state.pagina_actual = "principal"
        st.rerun()

    st.markdown("---")

    # Definición técnica de los archivos en el repositorio
    ilustraciones = [
        {"ref": "acouniverso1.jpg", "nombre": "Ilustración Esencia 1"},
        {"ref": "acouniverso2.jpg", "nombre": "Ilustración Esencia 2"}
    ]

    cols = st.columns(2)

    for i, item in enumerate(ilustraciones):
        with cols[i]:
            # Visualización del archivo .jpg
            st.image(item['ref'], caption=f"Referencia: {item['ref']}", use_container_width=True)
            
            # Selector de cantidad con clave única por referencia
            cant = st.number_input(
                f"Cantidad para {item['ref']}", 
                min_value=0, 
                step=1, 
                key=f"input_{item['ref']}"
            )
            
            if st.button(f"Confirmar {item['ref']}", key=f"btn_{item['ref']}"):
                if cant > 0:
                    # Inyección de datos en el carrito global
                    st.session_state.carrito.append({
                        "producto": f"Dibujo: {item['ref']}",
                        "cantidad": cant,
                        "subtotal": cant * 25000
                    })
                    st.success(f"Añadido: {cant} unidad(es) de {item['ref']}")
                else:
                    st.warning("Seleccione una cantidad mayor a 0")

    st.markdown("---")
    # Indicador de estado para el cliente
    st.info(f"Items actuales en memoria: {len(st.session_state.carrito)}")