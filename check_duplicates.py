import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TRH.settings')
django.setup()

from vision.models import Task, LearningMaterial

# Find Data Analytics tasks for month 1 (required_period = 1)
tasks = list(Task.objects.filter(category='Data Analytics', required_period=1).order_by('id'))

print("Data Analytics Month 1 tasks:")
for i, task in enumerate(tasks, 1):
    print(f"{i}. {task.title} (ID: {task.id})")

# Get module 2 (second task in the list)
if len(tasks) >= 2:
    module_2 = tasks[1]
    print(f"\n===== MODULE 2: {module_2.title} (ID: {module_2.id}) =====")
    materials = list(LearningMaterial.objects.filter(task=module_2).order_by('week_number', 'order'))
    print(f"Total materials: {len(materials)}\n")

    for mat in materials:
        print(f"ID: {mat.id} | Week {mat.week_number}, Order {mat.order}: {mat.title}")
