"""
tests/test_carrito.py
Etapa 3: interaccion con productos y carrito de compras
"""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import TIEMPO_ESPERA

logger = logging.getLogger(__name__)

def test_agregar_primer_producto_al_carrito(driver_logueado):
    """Agregar el primer incrementa el valor del contador y el producto aparece en el carrito"""
    #1. Crear espera
    espera = WebDriverWait(driver_logueado, TIEMPO_ESPERA)

    #2. Validamos que el carrito arranque vacio (sin contador)
    contador_inicial = driver_logueado.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(contador_inicial) == 0, f"El carrito no arranco vacio: {len(contador_inicial)}"

    #3. Obtener el primer producto y guardar su valor
    productos = espera.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "inventory_item")))
    primer_producto = productos[0]
    nombre_esperado = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text

    #4. Agregar producto al carrito
    primer_producto.find_element(By.TAG_NAME, "button").click()
    logger.info(f"Producto agregado al carrito: {nombre_esperado}")

    #5. Esperar a que aparezca el contador y validar contenido "1"
    contador = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))).text
    assert contador == "1", f"Contador obtenido: {contador}"

    #6. Navegar al carrito
    driver_logueado.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    espera.until(EC.url_contains("/cart.html"))
    logger.info("Navegación al carrito exitosa")

    #7 Validar que el item se haya agregado al carrito "1" y que sea el producto correcto
    items_carrito = espera.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "cart_item")))
    assert len(items_carrito) == 1, f"Cantidad de items en el carrito: {len(items_carrito)}"

    nombre_en_carrito = items_carrito[0].find_element(By.CLASS_NAME, "inventory_item_name").text
    logger.info(f"Agregado: {nombre_esperado} | En carrito: {nombre_en_carrito}")
    assert nombre_en_carrito == nombre_esperado, f"Se esperaba '{nombre_esperado}', se obtuvo '{nombre_en_carrito}'"