# 📊 Sistema CLI de Reportes de Clientes

Sistema de gestión y generación de reportes de clientes con interfaz de línea de comandos (CLI) desarrollado en Python.

## 🚀 Características

- **Gestión completa de clientes**: CRUD (Crear, Leer, Actualizar, Eliminar)
- **Generación de reportes**: PDF, Excel y CSV
- **Dashboard interactivo**: Estadísticas en tiempo real
- **Sistema de autenticación**: Login y registro de usuarios
- **Base de datos SQLite**: Almacenamiento local integrado
- **Interfaz CLI intuitiva**: Menús interactivos con Rich

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/pattterns/reportes-clientes.git
   cd reportes-clientes
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

## 🎯 Uso

### Primera ejecución

Al ejecutar la aplicación por primera vez, se te pedirá crear un usuario administrador:

```
¡Bienvenido! Es la primera vez que ejecutas la aplicación.
Necesitamos crear un usuario administrador.

Ingresa tu nombre de usuario: admin
Ingresa tu contraseña: [contraseña oculta]
✓ Usuario administrador creado exitosamente
```

### Menú principal

La aplicación presenta un menú principal con las siguientes opciones:

1. **🔐 Iniciar Sesión** - Acceder con usuario existente
2. **📝 Registrar Usuario** - Crear nuevo usuario
3. **ℹ️ Acerca de** - Información de la aplicación
4. **❓ Ayuda** - Guía de uso
5. **🔧 Información del Sistema** - Detalles técnicos
0. **🚪 Salir** - Cerrar aplicación

### Dashboard principal

Una vez autenticado, accedes al dashboard con:

1. **👥 Gestión de Clientes**
   - Listar clientes
   - Agregar cliente
   - Editar cliente
   - Eliminar cliente
   - Buscar clientes

2. **📄 Gestión de Reportes**
   - Crear reportes
   - Generar reportes en PDF/Excel/CSV
   - Ver historial de reportes

3. **📊 Estadísticas y Dashboard**
   - Estadísticas de clientes
   - Estadísticas de reportes
   - Gráficos y análisis

4. **📤 Exportar Datos**
   - Exportar a PDF
   - Exportar a Excel
   - Exportar a CSV

5. **⚙️ Configuración**
   - Configuración del sistema
   - Gestión de usuarios

## 📁 Estructura del proyecto

```
reportes-clientes/
├── main.py                 # Aplicación principal
├── requirements.txt        # Dependencias
├── README.md              # Documentación
├── data/                  # Base de datos SQLite
├── reports/               # Reportes generados
├── templates/             # Plantillas
└── src/                   # Código fuente
    ├── __init__.py
    ├── database.py        # Gestión de base de datos
    ├── auth.py           # Sistema de autenticación
    ├── cli_menus.py      # Menús interactivos
    ├── reports.py        # Generación de reportes
    └── utils.py          # Utilidades
```

## 🗄️ Base de datos

El sistema utiliza SQLite con las siguientes tablas:

- **users**: Usuarios del sistema
- **clients**: Información de clientes
- **reports**: Reportes generados
- **report_data**: Datos específicos de reportes

## 📊 Generación de reportes

### Formatos soportados

- **PDF**: Reportes profesionales con ReportLab
- **Excel**: Hojas de cálculo con OpenPyXL
- **CSV**: Datos separados por comas

### Tipos de reportes

1. **Reporte individual de cliente**
2. **Lista completa de clientes**
3. **Reporte de estadísticas**
4. **Reportes personalizados**

## 🔧 Configuración

### Variables de entorno

Puedes configurar las siguientes variables:

- `DB_PATH`: Ruta de la base de datos (default: `data/reportes.db`)
- `REPORTS_DIR`: Directorio de reportes (default: `reports/`)
- `LOG_LEVEL`: Nivel de logging (default: `INFO`)

### Personalización

- Modifica `src/utils.py` para cambiar colores y estilos
- Edita `src/reports.py` para personalizar formatos de reporte
- Ajusta `src/cli_menus.py` para modificar la interfaz

## 🚀 Desarrollo

### Estructura de código

- **database.py**: Manejo de SQLite y operaciones CRUD
- **auth.py**: Autenticación con bcrypt
- **cli_menus.py**: Interfaz de usuario con Rich
- **reports.py**: Generación de reportes
- **utils.py**: Utilidades y helpers

### Agregar nuevas funcionalidades

1. Crea el módulo en `src/`
2. Importa en `main.py`
3. Agrega opción en `cli_menus.py`
4. Actualiza documentación

## 🐛 Solución de problemas

### Error de dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Error de base de datos

```bash
rm data/reportes.db
python main.py
```

### Error de permisos

```bash
chmod +x main.py
```

## 📝 Changelog

### v1.0.0
- Sistema CLI completo
- Gestión de clientes
- Generación de reportes
- Dashboard con estadísticas
- Sistema de autenticación

## 🤝 Contribuciones

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**Marcos** - [@pattterns](https://github.com/pattterns)

## 🙏 Agradecimientos

- [Rich](https://github.com/Textualize/rich) - Interfaz CLI
- [ReportLab](https://www.reportlab.com/) - Generación de PDF
- [Pandas](https://pandas.pydata.org/) - Análisis de datos
- [SQLite](https://www.sqlite.org/) - Base de datos

---

**¡Gracias por usar el Sistema CLI de Reportes de Clientes!** 🎉
