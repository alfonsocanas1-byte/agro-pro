import streamlit as st

# Configuración de la interfaz
st.set_page_config(
    page_title="Fotografía de Santiago Arango",
    page_icon="📷",
    layout="centered"
)

# Estilos personalizados (CSS)
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .price-tag {
        font-size: 24px;
        color: #1e8449;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .product-card {
        padding: 1.5rem;
        border-radius: 15px;
        background-color: #f8f9f9;
        border: 1px solid #eaecee;
        margin-bottom: 25px;
    }
    .wa-button {
        display: block;
        text-align: center;
        background-color: #25D366;
        color: white !important;
        padding: 12px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 15px;
    }
    .wa-button:hover {
        background-color: #128C7E;
    }
    </style>
    """, unsafe_allow_html=True)

# Encabezado principal
st.title("📷 Bienvenido a fotografía de Santiago Arango")
st.markdown("### *Arte aplicado a tu vida cotidiana*")
st.write("Implementamos fotografías en diferentes accesorios o instrumentos como pocillos, transformando objetos comunes en piezas de colección.")

st.divider()

# Lista de productos (Ajustada a .jpeg)
productos = [
    {
        "id": 1,
        "nombre": "Pocillo Tucán Andino",
        "imagen": "fotopocillo1.jpeg",
        "precio": "38.000",
        "descripcion": "Un diseño vibrante que captura la elegancia del tucán andino en todo su esplendor. Colores intensos y mirada imponente en una pieza única que conecta con la biodiversidad de los Andes."
    },
    {
        "id": 2,
        "nombre": "Pocillo Ave Turquesa",
        "imagen": "fotopocillo2.jpeg",
        "precio": "38.000",
        "descripcion": "La serenidad de los bosques andinos en un mug. Este ave de tonos turquesa transmite frescura y armonía, ideal para acompañar tus momentos de calma."
    }
]

# Datos de contacto de Santiago
TEL_WHATSAPP = "573104448243"

# Generación de la galería
for prod in productos:
    # Creamos un contenedor por producto
    with st.container():
        col_img, col_info = st.columns([1, 1.2])
        
        with col_img:
            try:
                # Se cargan las imágenes con extensión .jpeg
                st.image(prod["imagen"], use_container_width=True)
            except:
                st.warning(f"Archivo {prod['imagen']} no encontrado en la carpeta.")
        
        with col_info:
            st.subheader(prod["nombre"])
            st.markdown(f"<p class='price-tag'>${prod['precio']} COP</p>", unsafe_allow_html=True)
            st.write(prod["descripcion"])
            
            # Link personalizado para WhatsApp
            mensaje = f"¡Hola Santiago! Quiero agregar al carrito el '{prod['nombre']}' (${prod['precio']}). ¿Me das información para el pago?"
            link_wa = f"https://wa.me/{TEL_WHATSAPP}?text={mensaje.replace(' ', '%20')}"
            
            st.markdown(f'<a href="{link_wa}" target="_blank" class="wa-button">🛒 Agregar al carrito y enviar WhatsApp</a>', unsafe_allow_html=True)
        
        st.write("") # Espaciado
        st.divider()

# Pie de página
st.caption("© 2026 Fotografía de Santiago Arango - Santiago Arango Fotógrafo")