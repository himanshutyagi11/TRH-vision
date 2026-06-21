import os, sys, django
sys.path.append(r"c:\Users\12tya\Desktop\Ohm\TRH")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TRH.settings")
django.setup()

from vision.models import LearningMaterial
from vision.admin import _auto_extract_docx

materials = LearningMaterial.objects.exclude(file='').all()
count = 0
for obj in materials:
    if str(obj.file.name).lower().endswith('.docx'):
        # Force re-extract
        print(f"Re-extracting logic for {obj.title} (File: {obj.file.name})")
        old_content = obj.content
        try:
            _auto_extract_docx(obj)
            if old_content != obj.content:
                obj.save()
                print(" -> Updated!")
            else:
                print(" -> No change in content.")
            count += 1
        except Exception as e:
            print(f" -> Error: {e}")

print(f"Processed {count} docx files.")
