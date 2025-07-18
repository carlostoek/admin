# Telegram VIP Bot

Bot de Telegram para gestión de canales VIP y gratuitos con Aiogram 3.

## Características

- Acceso VIP mediante tokens configurables (nombre, precio, duración)
- Gestión de suscripciones VIP (expulsión y recordatorio de vencimiento)
- Acceso gratuito con delay y aprobación automática
- Panel de administración para admins
- Seguridad, logging y tests incluidos

## Instalación

1. Clona el repositorio
2. Crea un entorno virtual y activa
3. Instala dependencias:
   
   pip install -r requirements.txt
  
4. Copia .env.example a .env y configura tus variables
5. Inicializa la base de datos:
   
   python -c "import asyncio; from database import init_db; asyncio.run(init_db())"
  
6. Ejecuta el bot:
   
   python main.py
  

## Tests

pytest tests/

## Seguridad

- Sanitización de entradas
- Logging de eventos y errores
- Protección contra ataques comunes

## Licencia

MIT