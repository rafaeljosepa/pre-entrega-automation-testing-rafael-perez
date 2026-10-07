"""
  conftest.py
  Configuración compartida por todos los tests. Pytest detecta este archivo automáticamente.
  Fixtures:
    - driver: abre un navegador nuevo antes de cada test y lo cierra al terminar.
    - driver_logueado: igual que driver, pero con sesión iniciada en la página de inventario.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import login, cargar_usuario, TIEMPO_ESPERA


@pytest.fixture
def driver():
    # Desactivamos el gestor de contraseñas de Chrome para evitar popups
    # que interrumpan el flujo (con standard_user, Chrome avisa "contraseña filtrada").
    opciones = webdriver.ChromeOptions()
    opciones.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    opciones.add_argument("--start-maximized")

    navegador = webdriver.Chrome(options=opciones)

    yield navegador   # <- aquí se ejecuta el test que pidió la fixture

    navegador.quit()  # <- se ejecuta SIEMPRE al final, pase o falle el test


@pytest.fixture
def driver_logueado(driver):
    """Driver con sesión iniciada (usuario válido), ubicado en la página de inventario."""
    usuario, password = cargar_usuario("valido")
    login(driver, usuario, password)
    WebDriverWait(driver, TIEMPO_ESPERA).until(EC.url_contains("/inventory.html"))
    return driver