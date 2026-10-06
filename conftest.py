"""
conftest.py
Configuración compartida por todos los tests. Pytest detecta este archivo automáticamente.
Contiene la fixture 'driver': abre un navegador nuevo antes de cada test y lo cierra al terminar.
"""
import pytest
from selenium import webdriver


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