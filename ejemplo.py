
Conversación abierta. 1 mensaje leído.

Ir al contenido
Uso de Correo de PROYECTOS FORMACIÓN Y SERVICIOS S.L. con lectores de pantalla
gpt 

Fwd: Código ChatGPT para Resoluciones Judiciales
Recibidos

Francisco García Cortés
Adjuntos
jue, 30 mar, 9:57 (hace 9 días)
para Gonzalo, Rubén, Germán, Andrés

Buenas!!

Os comparto un código optimizado por Andrés Akle para preguntarle a cualquier documento en pdf una serie de preguntas y guardar las respuestas en un formato almacenable en una BBDD. 

Darle una vuelta y vemos los casos de uso que podría tener en nuestro mercado y clientes. 

Un abrazo,
Paco



---------- Forwarded message ---------
De: Andrés Akle <aakle@telepro.com.mx>
Date: jue, 30 mar 2023 a las 2:10
Subject: Código ChatGPT para Resoluciones Judiciales
To: Iván Santiago <ivan.santiago@pfsgroup.es>, Francisco García <francisco.garcia@pfstech.es>, Ramón Carbajo Galve <ramon.carbajo@pfsgroup.es>, Diego Rodriguez <diego.rodriguez@pfsgroup.es>, Francisco José Zamorano Gómez <fran.zamorano@pfsgroup.es>


Hola a todos.

Como quedé, les mando el código que utilicé para leer una sentencia (también la adjunto) para hacerle algunas preguntas que puedan quedar en un formato para guardar en una BD.

Este código realmente puede ser usado para cualquier documento en pdf que no sea muy largo. También pueden cambiar las preguntas que hacen al texto. Por supuesto que se puede optimizar el código y hacer funciones específicas para ciertas tareas porque fue creado como prueba de concepto.

Si no tienen credenciales para AWS Textract o para ChatGPT por favor avísenme para pedir que se las den.

Además incluyo la presentación que hice.

Abrazo.




   Andrés Akle

   t. +52 (55) 5276 1100 ext. 430

   m. +52 1 (55) 9199 3995

   e. aakle@telepro.com.mx



Antes de imprimir este e-mail evalúa si realmente es necesario hacerlo. Cuidemos el mundo.   

"Este correo electrónico puede contener información confidencial, sólo está dirigida al destinatario del mismo, la información puede ser privilegiada.  Se prohíbe que cualquier persona distinta al destinatario copie o distribuya este correo. Si usted no es el destinatario, por favor notifique esto de inmediato y destruya el correo, lo mismo que cualquier evidencia de la información. Los correos electrónicos en Internet, no son privados, seguros ni confiables. Ningún miembro de Servicios Telepro, S.A. de C.V. que en lo sucesivo se denominará Telepro, será responsable de los errores u omisiones en el contenido o transmisión de este correo electrónico. Cualquier opinión contenida en este correo es responsabilidad única y exclusiva del autor del mismo. Sus datos personales en Telepro están protegidos conforme a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares. Consulte el aviso de privacidad en: http://telepro.com.mx/aviso-de-privacidad/ . Gracias”

3
 archivos adjuntos
•  Analizado por Gmail
GRACIAS!Genial!MUCHAS GRACIAS.
from PyPDF2 import PdfReader
import openai
import tiktoken
import re
import boto3
from pdf2image import convert_from_path
import io

# local file path
pdf_path = "PATH_TO_FILE/TestFile_NoText.pdf"
# set up AWS textract
AWS_REGION = 'YOUR_REGION_NAME'
AWS_ACCESS_KEY_ID = 'YOUR_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'YOUR_SECRET_ACCESS_KEY'
# set up openai
model = "gpt-3.5-turbo"
encoding = tiktoken.encoding_for_model(model)
openai.api_key = "YOUR_API_KEY"
# set up Textract client
client = boto3.client('textract', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_REGION)

# read local file and convert to images
print('Reading file...')
pages = convert_from_path(pdf_path, 300)
# send file to Textract and concatenate answers
text = ''
print('\tSending pages to AWS Textract...')
for i, page in enumerate(pages):
    # convert PIL image to bytes
    img_bytes = io.BytesIO()
    page.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()
    print('\t Sending page ' + str(i+1))
    response = client.detect_document_text(Document={'Bytes': img_bytes})
    # extract text from response
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + '\n'

# # If pdf already has text
# reader = PdfReader(file_path)
# text = ''
# for page in reader.pages:
#     text = text + '\n' + page.extract_text()

print('\nText received...')
print('\tFormatting text...')

# Eliminate non-significant text to reduce tokens used by ChatGPT
text = "\"" + text + "\""
text = text.replace("-", "")
text = re.sub(r'\n{2,}', '\n', text)
print('\tPrinting first 10 lines...\n')
lines = text.split('\n')
for i in range(10):
    print(lines[i])

# Create ChatGTP prompt
question1 = "Si soy el demandante, ¿gane?"
question2 = "¿Cuál es el principal que debe pagar en culpable?"
question3 = "¿Que juzgado fue utilizado?"
question4 = "¿Existe un pagaré como respaldo?"
statement = "La primera pregunta respondela en una palabra, si o no. " \
            "La segunda pregunta respondela solamente en cifra. " \
            "La tercera pregunta respondela en el menor número de palabras posible. " \
            "La cuarta pregunta respondela en una palabra, si o no " \
            "Cada respuesta debe de ir en un reglon independiente."
messages = [
    {"role": "user", "content": "Aqui esta un texto: " + text},
    {"role": "user", "content": question1},
    {"role": "user", "content": question2},
    {"role": "user", "content": question3},
    {"role": "user", "content": question4},
    {"role": "user", "content": statement},
]
# Check tokens used
print('\nChecking tokens used for ChatGPT...')
tokens_used = len(encoding.encode(text + question2))
print('\tTokens: ' + str(tokens_used))

# Send request to Chat GPT model for Chat Completion
if tokens_used >= 4097:     # maximum tokens allowed for Chat Completion for GTP 3.5 is 4097
    print("Error: max context length is 4097, message is " + str(tokens_used))
else:
    response = openai.ChatCompletion.create(model=model, messages=messages, temperature=0)
    # Extract the text from the response and create an array item for each line
    text = response['choices'][0]['message']['content'].splitlines()
    # Print the results
    print('\nResulting array for [won, amount due, juzgado]')
    print(text)
chatgpt_q&a_short_text.py
