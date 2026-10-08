"""
tests/test_catalogo.py
Etapa 2: navegacion y verificacion del catalogo de productos.
"""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import TIEMPO_ESPERA

logger = logging.getLogger(__name__)

def test_titulo_inventario(driver_logueado):
    """La pagina del inventario muestra el titulo correcto"""
    #1. Validar titulo del inventario
    assert driver_logueado.title == "Swag Labs", f"Titulo obtenido: {driver_logueado.title}"

    #2. Validar el encabezado de la pagina
    encabezado = driver_logueado.find_element(By.CLASS_NAME, "title").text
    assert encabezado == "Products", f"Encabezado obtenido: {encabezado}"


def test_productos_visibles(driver_logueado):
    """Hay productos visibles, el primero con nombre y precio"""
    #1. Crear espera
    espera = WebDriverWait(driver_logueado, TIEMPO_ESPERA)
    productos = espera.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "inventory_item")))

    #2. Validamos que al menos exista un producto
    assert len(productos) > 0, f"Cantid de productos: {len(productos)}"

    #3. Datos del primer producto
    primer_producto = productos[0]
    nombre = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text

    #4. Muestra de contenido de productos
    logger.info(f"Primer producto: {nombre} - Precio: {precio}")

    #5. Validaciones
    assert nombre != "", f"Nombre Primer Producto Obtenido: {nombre}"
    assert precio.startswith("$"), f"Precio Primer Producto Obtenido: {precio}"


def test_elementos_interfaz(driver_logueado):
    """Elementos princiapales son visibles en la interfaz"""
    #1. El menu Hamburguesa esta visible
    menu = driver_logueado.find_element(By.ID, "react-burger-menu-btn")
    assert menu.is_displayed(), "El menu hamburguesa NO esta visible"

    #2. Filtro ordenado de productos es visible
    filtro = driver_logueado.find_element(By.CLASS_NAME, "product_sort_container")
    assert filtro.is_displayed(), "Los filtros NO estan visibles"

    #3. Icono del carrito esta visible
    carrito = driver_logueado.find_element(By.CLASS_NAME, "shopping_cart_link")
    assert carrito.is_displayed(), "Icono del carrito NO esta visible"