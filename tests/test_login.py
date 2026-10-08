"""
tests/test_login.py
Etapa 1: casos de prueba del login de saucedemo.com.
"""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import login, cargar_usuario, TIEMPO_ESPERA

logger = logging.getLogger(__name__)


def test_login_exitoso(driver):
    """Un usuario válido inicia sesión y es redirigido a la página de inventario."""
    #1. Carga de credenciales "valido" desde el JSON
    usuario, password = cargar_usuario("valido")

    #2. Hacer login con el helper
    login(driver, usuario, password)

    #3. Espera explicita para carga de inventario
    espera = WebDriverWait(driver, TIEMPO_ESPERA)
    espera.until(EC.url_contains("/inventory.html"))

    #4. Validar URL
    assert "/inventory.html" in driver.current_url, f"URL inesperada: {driver.current_url}"

    #5. Validar titulo de la pestaña
    assert driver.title == "Swag Labs", f"Titulo inesperado: {driver.title}"

    #6. Validar encabezado
    encabezado = driver.find_element(By.CLASS_NAME, "title").text
    assert encabezado == "Products", f"Encabezado inesperado: {encabezado}"

    logger.info(f"Login exitoso. URL actual: {driver.current_url}")

def test_login_usuario_bloqueado(driver):
    """Usuario con credenciales bloqueadas no puede iniciar sesion"""
    #1. Carga de credenciales "bloqueado" desde el JSON
    usuario, password = cargar_usuario("bloqueado")

    #2. Hacer login con el helper
    login(driver, usuario, password)

    #3. Espera por mensaje de error
    espera = WebDriverWait(driver, TIEMPO_ESPERA)
    mensaje_error = espera.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))).text

    #4. Validar contenido de mensaje "locked out"
    assert "locked out" in mensaje_error, f"Mensaje inesperado: {mensaje_error}"

    #5. Validar que la URL no contenga "/inventory.html" (resultado esperado, no deberia entrar el usuario)
    assert "/inventory.html" not in driver.current_url

    logger.info(f"Mensaje de error mostrado: {mensaje_error}")


def test_login_password_incorrecta(driver):
    """Usuario con credenciales incorrectas"""
    #1. Carga de credenciales "password_incorrecta" desde el JSON
    usuario, password = cargar_usuario("password_incorrecta")

    #2. Hacer login con el helper
    login(driver, usuario, password)

    #3. Espera por mensaje de error
    espera = WebDriverWait(driver, TIEMPO_ESPERA)
    mensaje_error = espera.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))).text

    #4. Validar contenido del mensaje "Epic sadface: Username and password do not match any user in this service"
    assert "do not match" in mensaje_error, f"Mensaje inesperado: {mensaje_error}"

   #5. Validar que la URL no contenga "/inventory.html" (resultado esperado, no deberia entrar el usuario)
    assert "/inventory.html" not in driver.current_url

    logger.info(f"Mensaje de error mostrado: {mensaje_error}")