from django.core.mail import EmailMessage
from decouple import config

# Los 'datos' que definiste en la imagen
datos = { 
    'nomina': 'NOM-2024-001',
    'fecha': '2024-01-15',
    'motivo': 'Revisión de desempeño anual',
    'imagen_url': 'https://example.com/imagen_nomina.png'
}

subject = f"Cita agendada: David"

html_body = f"""
    <DOCTYPE html>
    <html>
        <body>
            <h1>¡Hola MIKE!</h1>
            <p>Se ha agendado una cita con el siguiente motivo: {datos['motivo']}</p>
            <img src="{datos['imagen_url']}" alt="Imagen de nómina" />
            <p>Saludos cordiales.</p>
        </body>
    </html>
"""

# 1. Pide el destinatario
email_to = input("Ingrese el correo electrónico del destinatario: ")

# 2. Crea la instancia de EmailMessage
email = EmailMessage(
    subject='test',
    body=html_body,
    from_email=config('EMAIL_HOST_USER'), # Usar el correo configurado en settings.py
    to=[email_to], # Lista de destinatarios
)

# 3. Especifica el tipo de contenido y envía
email.content_subtype = "html" 

email.send()