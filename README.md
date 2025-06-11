# ⚽ Football Leagues Data Pipeline

## 📋 Descripción del Proyecto

Este proyecto forma parte de mi portafolio como **Data Engineer** y demuestra la implementación de un pipeline de datos completo para la extracción, transformación y carga (ETL) de información de las principales ligas de fútbol europeas.

El pipeline automatiza la recolección de datos de posiciones de equipos desde ESPN y los procesa para almacenarlos en un data warehouse en la nube, creando una fuente centralizada y actualizada de estadísticas de fútbol.

## 🎯 Objetivo

Crear un sistema automatizado que extraiga diariamente las posiciones y estadísticas de las principales ligas europeas de fútbol y las almacene en un formato estructurado para análisis posteriores.

## 🏗️ Arquitectura y Tecnologías

### **Orquestación de Workflows**
- **Apache Airflow**: Gestión y programación de pipelines de datos
- **Astronomer (Astro)**: Plataforma para desarrollo y despliegue de Airflow

### **Almacenamiento de Datos**
- **Snowflake**: Data warehouse en la nube para almacenamiento escalable
- **CSV Files**: Almacenamiento temporal para procesamiento de datos

### **Procesamiento y Transformación**
- **Python**: Lenguaje principal para lógica de negocio
- **Pandas**: Manipulación y transformación de datos
- **Web Scraping**: Extracción automatizada desde ESPN

### **Conectividad**
- **Snowflake Connector**: Integración nativa con el data warehouse
- **HTTP Requests**: Consumo de APIs y scraping web

## 📊 Fuentes de Datos

El pipeline extrae datos de las siguientes ligas europeas desde ESPN:

| Liga | País | URL Source |
|------|------|------------|
| La Liga | España | ESPN España |
| Premier League | Inglaterra | ESPN Inglaterra |
| Serie A | Italia | ESPN Italia |
| Bundesliga | Alemania | ESPN Alemania |
| Ligue 1 | Francia | ESPN Francia |
| Primeira Liga | Portugal | ESPN Portugal |
| Eredivisie | Holanda | ESPN Holanda |

## 🔄 Flujo de Trabajo (Pipeline)

### 1. **Extracción de Datos** (`EXTRACT_FOTBALL_DATA`)
- **Fuente**: Páginas web de ESPN de cada liga
- **Método**: Web scraping con `pandas.read_html()`
- **Proceso**: 
  - Itera sobre las 7 ligas principales
  - Extrae tablas de posiciones en tiempo real
  - Implementa delays aleatorios para evitar sobrecarga del servidor

### 2. **Transformación de Datos**
- **Limpieza**: Normalización de nombres de equipos y formato de datos
- **Enriquecimiento**: 
  - Añade identificadores únicos por equipo
  - Incorpora metadata de liga y fecha de extracción
  - Estandariza formato de columnas (J, G, E, P, GF, GC, DIF, PTS)
- **Validación**: Verificación de integridad y consistencia de datos

### 3. **Carga a Staging** (`upload_data_stage`)
- **Destino**: Stage área en Snowflake
- **Proceso**: Upload de archivo CSV comprimido
- **Formato**: Auto-compresión habilitada para optimización

### 4. **Ingesta Final** (`ingest_table`)
- **Destino**: Tabla principal en Snowflake
- **Proceso**: COPY INTO desde stage con manejo de errores
- **Estrategia**: Continuación en caso de errores para máxima disponibilidad

## 📈 Estructura de Datos

### **Tabla Principal**: `FOOTBALL_POSITIONS`
```sql
ID_TEAM     VARCHAR(50)    -- Identificador único del equipo
EQUIPO      VARCHAR(100)   -- Nombre del equipo
J           INTEGER        -- Partidos jugados
G           INTEGER        -- Partidos ganados
E           INTEGER        -- Partidos empatados
P           INTEGER        -- Partidos perdidos
GF          INTEGER        -- Goles a favor
GC          INTEGER        -- Goles en contra
DIF         INTEGER        -- Diferencia de goles
PTS         INTEGER        -- Puntos totales
LIGA        VARCHAR(50)    -- Liga de pertenencia
CREATED_AT  DATE           -- Fecha de extracción
```

## ⚡ Características Técnicas

### **Automatización**
- **Programación**: Ejecución diaria automática
- **Monitoreo**: Logs detallados y alertas de fallos
- **Recuperación**: Reintentos automáticos en caso de error

### **Escalabilidad**
- **Modular**: Fácil adición de nuevas ligas o fuentes
- **Parameterizable**: Configuración flexible mediante variables de Airflow
- **Performante**: Procesamiento en paralelo y optimizaciones de memoria

### **Calidad de Datos**
- **Validación**: Verificación de integridad en cada paso
- **Manejo de Errores**: Estrategias robustas para fallos de red o datos
- **Auditoría**: Trazabilidad completa del proceso ETL

## 🎯 Casos de Uso

Este pipeline de datos permite:

1. **Análisis Deportivo**: Seguimiento de rendimiento de equipos y ligas
2. **Business Intelligence**: Dashboards y reportes automatizados
3. **Machine Learning**: Datos históricos para modelos predictivos
4. **APIs de Datos**: Fuente confiable para aplicaciones de terceros

## 📚 Aprendizajes y Desafíos

### **Desafíos Técnicos Resueltos**
- **Web Scraping Resiliente**: Manejo de cambios en estructura HTML
- **Migración Airflow 2.x**: Actualización de operadores deprecados
- **Optimización Snowflake**: Configuración eficiente de conexiones y staging

### **Mejores Prácticas Implementadas**
- **Infrastructure as Code**: Configuración reproducible
- **Error Handling**: Manejo robusto de excepciones
- **Data Quality**: Validaciones en múltiples capas
- **Security**: Gestión segura de credenciales

## 🚀 Próximos Pasos

- **Expansión Geográfica**: Inclusión de ligas sudamericanas y asiáticas
- **Real-time Processing**: Implementación de streaming para datos en vivo
- **Data Lake Integration**: Almacenamiento de datos raw para análisis avanzado
- **API Development**: Exposición de datos via REST API

---

Este proyecto demuestra competencias en **Data Engineering**, **Cloud Computing**, **Workflow Orchestration** y **Data Warehouse Design**, elementos fundamentales en la arquitectura de datos moderna.