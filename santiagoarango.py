import streamlit as st

def render_galeria_santiago():
    st.title("📷 Galería de Santiago Arango")
    st.markdown("### *Arte aplicado a tu vida cotidiana*")
    
    if st.button("⬅️ Regresar al menú principal"):
        st.session_state.pagina_actual = "principal"
        st.rerun()

    st.divider()

    productos = [
        {
            "id": 1,
            "nombre": "Pocillo Tucán Andino",
            "imagen": "fotopocillo1.jpeg",
            "precio": 38000,
            "descripcion": "Diseño vibrante del tucán andino."
        },
        {
            "id": 2,
            "nombre": "Pocillo Ave Turquesa",
            "imagen": "fotopocillo2.jpeg",
            "precio": 38000,
            "descripcion": "Serenidad de los bosques andinos."
        }
    ]

    for prod in productos:
        col_img, col_info = st.columns([1, 1.2])
        with col_img:
            try:
                st.image(prod["imagen"], use_container_width=True)
            except:
                st.warning(f"Imagen {prod['imagen']} no encontrada.")
        
        with col_info:
            st.subheader(prod["nombre"])
            st.write(f"**Precio:** ${prod['precio']:,} COP")
            
            cant = st.number_input(f"Cantidad {prod['nombre']}", min_value=0, step=1, key=f"santi_{prod['id']}")
            if st.button(f"Añadir {prod['nombre']}", key=f"btn_s_{prod['id']}"):
                if cant > 0:
                    st.session_state.carrito.append({
                        "producto": f"Mug: {prod['nombre']}",
                        "cantidad": cant,
                        "subtotal": cant * prod['precio']
                    })
                    st.success("Agregado al carrito global")
        st.divider()