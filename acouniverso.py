import streamlit as st

def render_catalogo():
    st.title("🎨 Ilustraciones ACOuniverso")
    st.write("Dibujos de Alfonso Cañas Orduz, únicos y originales.")
    st.write("**Precio:** $15.000 (Papel Fotográfico)")

    # Botón de retorno al Hub
    if st.button("⬅️ Regresar al menú principal"):
        st.session_state.pagina_actual = "principal"
        st.rerun()

    st.markdown("---")

    # Listado con las extensiones específicas (jpg y jgep)
    ilustraciones = [
        {"ref": "acouniverso1.jpg", "nombre": "Dibujo 1"},
        {"ref": "acouniverso2.jpg", "nombre": "Dibujo 2"},
        {"ref": "acouniverso3.jgep", "nombre": "Dibujo 3"},
        {"ref": "acouniverso.jgep", "nombre": "Dibujo 4"}
    ]

    # Renderizado VERTICAL (Sin columnas para evitar desconfiguración)
    for item in ilustraciones:
        with st.container():
            try:
                # Imagen pequeña (width=300) y centrada por flujo vertical
                st.image(item['ref'], caption=f"Ref: {item['ref']}", width=300)
            except:
                st.error(f"Archivo {item['ref']} no encontrado.")
            
            # Control de cantidad justo debajo de la imagen
            cant = st.number_input(
                f"Cantidad para {item['ref']}", 
                min_value=0, 
                step=1, 
                key=f"in_{item['ref']}"
            )
            
            if st.button(f"Añadir {item['ref']}", key=f"btn_{item['ref']}"):
                if cant > 0:
                    st.session_state.carrito.append({
                        "producto": f"Dibujo: {item['ref']}",
                        "cantidad": cant,
                        "subtotal": cant * 15000
                    })
                    st.success(f"¡{item['ref']} añadido!")
            
            st.markdown("---") # Separador entre cada dibujo

    st.info(f"Items en carrito: {len(st.session_state.carrito)}")