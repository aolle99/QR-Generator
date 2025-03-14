import qrcode
from PIL import Image

def invertir_color(color_hex):
    """Invierte un color en formato hexadecimal"""
    color_hex = color_hex.lstrip("#")  # Eliminar "#" si está presente
    r, g, b = int(color_hex[0:2], 16), int(color_hex[2:4], 16), int(color_hex[4:6], 16)
    return f"#{255 - r:02X}{255 - g:02X}{255 - b:02X}"

def generar_qr(url, fill_color="#000000", nombre_archivo="qr.png", logotipo=None):
    # Calcular el color inverso
    back_color = invertir_color(fill_color)

    # Crear el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Crear la imagen QR con colores personalizados
    img_qr = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

    # Convertir el fondo blanco en transparente
    datos = img_qr.getdata()
    nuevo_datos = []

    back_rgb = Image.new("RGB", (1, 1), back_color).getpixel((0, 0))  # Convertir HEX a RGB
    for item in datos:
        # Si el pixel coincide con el color de fondo, lo hacemos transparente
        if item[:3] == back_rgb:
            nuevo_datos.append((255, 255, 255, 0))  # Transparente
        else:
            nuevo_datos.append(item)  # Mantener el color del QR

    img_qr.putdata(nuevo_datos)

    # Si se proporciona un logotipo, agregarlo al centro
    if logotipo:
        try:
            logo = Image.open(logotipo).convert("RGBA")

            # Redimensionar el logotipo para que encaje en el QR
            qr_width, qr_height = img_qr.size
            factor = 4  # Ajustar el tamaño del logo
            logo_size = qr_width // factor

            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

            # Posición para centrar el logotipo
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

            # Pegar el logotipo en la imagen QR con transparencia
            img_qr.paste(logo, pos, mask=logo)

        except Exception as e:
            print(f"Error al cargar el logotipo: {e}")

    # Guardar el código QR en PNG
    img_qr.save(nombre_archivo)
    print(f"✅ Código QR guardado como {nombre_archivo} (Fondo: {back_color})")

# Ejemplo de uso
generar_qr("https://es.linkedin.com/in/alexolle", fill_color="#FFFFFF", nombre_archivo="qr.png")
