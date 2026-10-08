# Pre-entrega Automation Testing – Rafael Pérez

Automatización de pruebas E2E sobre [saucedemo.com](https://www.saucedemo.com/) con **Python, Selenium WebDriver y Pytest**, desarrollada como pre-entrega del curso de QA Automation de Talento Tech.

## 🎯 Propósito

Automatizar tres flujos críticos de un e-commerce de demostración:

1. **Login**: acceso con credenciales válidas y manejo de credenciales inválidas.
2. **Catálogo**: verificación del inventario, sus productos y los elementos principales de la interfaz.
3. **Carrito**: agregar un producto y validar que el contador y el contenido del carrito sean correctos.

## 🛠️ Tecnologías

| Herramienta | Uso |

| Python 3 | Lenguaje principal |
| Selenium WebDriver | Automatización del navegador (Chrome) |
| Pytest | Estructura, ejecución y fixtures de los tests |
| pytest-html | Reporte HTML de resultados |
| logging (Python) | Logs de ejecución en consola y archivo |
| Git / GitHub | Control de versiones |

## 📁 Estructura del proyecto

```
- **`tests/`**: casos de prueba
  - `test_login.py`: Etapa 1, login exitoso y casos negativos
  - `test_catalogo.py`: Etapa 2, título, productos e interfaz
  - `test_carrito.py`: Etapa 3, agregar producto y validar carrito
- **`utils/`**: funciones auxiliares
  - `helpers.py`: funciones reutilizables (login, carga de datos)
- **`datos/`**: datos de prueba externos
  - `usuarios.json`: credenciales de prueba (válidas e inválidas)
- **`reports/`**: evidencias de ejecución
  - `reporte.html`: reporte HTML de la última ejecución
  - `ejecucion.log`: log de la última ejecución
  - `screenshots/`: capturas automáticas de tests fallidos
- `conftest.py`: fixtures del driver y captura en fallos
- `pytest.ini`: configuración de Pytest y logging
- `requirements.txt`: dependencias del proyecto
```

## ✅ Casos de prueba

| Archivo | Test | Qué valida |

| `test_login.py` | `test_login_exitoso` | Redirección a `/inventory.html`, título "Swag Labs" y encabezado "Products" |
| `test_login.py` | `test_login_usuario_bloqueado` | Mensaje de error de usuario bloqueado y que no se acceda al inventario |
| `test_login.py` | `test_login_password_incorrecta` | Mensaje de credenciales inválidas y que no se acceda al inventario |
| `test_catalogo.py` | `test_titulo_inventario` | Título de la pestaña y encabezado de la página |
| `test_catalogo.py` | `test_productos_visibles` | Existencia de productos y nombre/precio del primero |
| `test_catalogo.py` | `test_elementos_interfaz` | Visibilidad del menú, el filtro y el ícono del carrito |
| `test_carrito.py` | `test_agregar_primer_producto_al_carrito` | Contador de 0 a 1 y que el producto en el carrito sea el agregado |

## ⚙️ Instalación

**Requisitos previos:** Python 3.10 o superior, Git y Google Chrome instalados. El driver de Chrome se gestiona automáticamente con Selenium.

```bash
# 1. Clonar el repositorio
git clone https://github.com/rafaeljosepa/pre-entrega-automation-testing-rafael-perez.git
cd pre-entrega-automation-testing-rafael-perez

# 2. Crear y activar el entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Windows PowerShel
source .venv/bin/activate           # macOS / Linux

# 3. Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Ejecución

```bash
# Ejecutar todos los tests
pytest

# Ejecutar todos los tests y generar el reporte HTML
pytest --html=reports/reporte.html --self-contained-html

# Ejecutar un solo archivo
pytest tests/test_login.py

# Ejecutar un solo test
pytest tests/test_login.py::test_login_exitoso
```

## 📊 Evidencias

- **Reporte HTML:** `reports/reporte.html`. Abrirlo en cualquier navegador.
- **Logs de ejecución:** se muestran en consola y se guardan en `reports/ejecucion.log`, con fecha, hora y nivel.
- **Capturas en fallos:** cuando un test falla, se guarda automáticamente una captura en `reports/screenshots/` y se adjunta al reporte HTML. La captura incluida en el repositorio proviene de un fallo forzado a propósito para validar el mecanismo.

## 💡 Buenas prácticas aplicadas

- **Esperas explícitas** (`WebDriverWait`) en lugar de `time.sleep()`.
- **Tests independientes:** cada test abre y cierra su propio navegador mediante fixtures.
- **Fixtures reutilizables:** `driver` y `driver_logueado` evitan repetir código de configuración y login.
- **Datos externos:** las credenciales viven en `datos/usuarios.json`, separadas del código.
- **Casos negativos:** se valida también el comportamiento ante credenciales inválidas.
- **Asserts con mensajes descriptivos** que muestran el valor obtenido cuando un test falla.
- **Logs sin datos sensibles:** nunca se registran contraseñas.

## 👤 Autor

**Rafael Pérez** – QA Analyst - Engineer
[GitHub](https://github.com/rafaeljosepa) · [LinkedIn](https://www.linkedin.com/in/rafael-perez-4578ab272/)