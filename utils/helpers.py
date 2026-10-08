"""
utils/helpers.py
Funciones auxiliares reutilizables por todos los tests de saucedemo.com
"""
import logging

import json
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

URL_BASE = "https://www.saucedemo.com/"
TIEMPO_ESPERA = 10  # segundos máximos para las esperas explícitas

# Ruta al JSON construida desde la ubicación de este archivo,
# así funciona sin importar desde qué carpeta se ejecute pytest.
RUTA_USUARIOS = Path(__file__).parent.parent / "datos" / "usuarios.json"


def cargar_usuario(tipo):
    """Devuelve (usuario, password) del tipo indicado en datos/usuarios.json."""
    with open(RUTA_USUARIOS, encoding="utf-8") as archivo:
        usuarios = json.load(archivo)
    return usuarios[tipo]["usuario"], usuarios[tipo]["password"]


def login(driver, usuario, password):
    """Abre saucedemo.com e inicia sesión con las credenciales recibidas."""
    logger.info(f"Iniciando sesión con el usuario: {usuario}")
    driver.get(URL_BASE)
    espera = WebDriverWait(driver, TIEMPO_ESPERA)
    # Esperamos a que el campo usuario sea visible antes de escribir
    espera.until(EC.visibility_of_element_located((By.ID,"user-name"))).send_keys(usuario)
    driver.find_element(By.ID,"password").send_keys(password)
    driver.find_element(By.ID,"login-button").click()