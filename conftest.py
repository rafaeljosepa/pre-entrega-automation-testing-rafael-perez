"""
  conftest.py
  Configuración compartida por todos los tests. Pytest detecta este archivo automáticamente.
  Fixtures:
    - driver: abre un navegador nuevo antes de cada test y lo cierra al terminar.
    - driver_logueado: igual que driver, pero con sesión iniciada en la página de inventario.
"""
import pytest
import logging
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest_html import extras as html_extras

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


CARPETA_SCREENSHOTS = Path(__file__).parent / "reports" / "screenshots"
logger = logging.getLogger(__name__)


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test falla, guarda una captura de pantalla y la adjunta al reporte HTML."""
    reporte = yield  # Pytest ejecuta el test y nos devuelve su resultado

    # 'setup' cubre fallos en la fixture (ej. login), 'call' cubre fallos en el test
    if reporte.when in ("setup", "call") and reporte.failed:
        navegador = item.funcargs.get("driver")
        if navegador is not None:
            CARPETA_SCREENSHOTS.mkdir(parents=True, exist_ok=True)
            marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta = CARPETA_SCREENSHOTS / f"{item.name}_{marca_tiempo}.png"

            # 1. Guardar la captura como archivo en reports/screenshots/
            navegador.save_screenshot(str(ruta))
            logger.error(f"Test fallido: {item.name}. Captura guardada en {ruta}")

            # 2. Incrustar la captura dentro del reporte HTML
            adjuntos = getattr(reporte, "extras", [])
            adjuntos.append(html_extras.image(navegador.get_screenshot_as_base64()))
            reporte.extras = adjuntos

    return reporte