import os, sys, django
sys.path.append(r"c:\Users\12tya\Desktop\Ohm\TRH")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TRH.settings")
django.setup()

from vision.models import LearningMaterial
from docx import Document
import io

lm = LearningMaterial.objects.exclude(file='').order_by('-id').first()
if not lm or not str(lm.file.name).endswith('.docx'):
    sys.exit(0)

lm.file.open('rb')
file_data = io.BytesIO(lm.file.read())
lm.file.close()

document = Document(file_data)
import xml.etree.ElementTree as ET

with open('diag_clean.txt', 'w', encoding='utf-8') as f:
    # Just dump the raw body XML
    f.write(document.element.body.xml)
