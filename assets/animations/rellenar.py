from PIL import Image, ImageChops
import os

# Configuración
carpeta_raiz = r"C:\Users\Lauta\Desktop\Italian Brainrots Arena\assets\animations"
TAMANO_REQUERIDO = (1008, 504)

def reparar_huecos_con_fondo_blanco(ruta_imagen):
    try:
        original = Image.open(ruta_imagen).convert("RGBA")

        if original.size != TAMANO_REQUERIDO:
            print(f"⚠️ Tamaño incorrecto: {ruta_imagen} ({original.size[0]}×{original.size[1]})")
            return

        # Extraer canal alfa para obtener la silueta del personaje
        alpha = original.getchannel("A")

        # Crear una imagen blanca solo en la silueta
        silueta_blanca = Image.new("RGBA", original.size, (255, 255, 255, 255))
        silueta_blanca.putalpha(alpha)

        # Componer: la silueta blanca va detrás, el sprite encima
        resultado = Image.alpha_composite(silueta_blanca, original)

        # Guardar sobrescribiendo el archivo original
        resultado.save(ruta_imagen)
        print(f"✅ Corregido: {ruta_imagen}")

    except Exception as e:
        print(f"❌ Error en {ruta_imagen}: {e}")

# Recorrido por todos los PNG
for carpeta_actual, _, archivos in os.walk(carpeta_raiz):
    for archivo in archivos:
        if archivo.lower().endswith(".png"):
            ruta = os.path.join(carpeta_actual, archivo)
            reparar_huecos_con_fondo_blanco(ruta)

print("\n🏁 Proceso completado correctamente. Todos los sprites fueron reparados.")