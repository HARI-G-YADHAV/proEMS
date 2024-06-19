# myapp/management/commands/import_data.py

from django.core.management.base import BaseCommand
from exam.models import teacherTable,Department
import pandas as pd

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def handle(self, *args, **options):
        # Path to the CSV file containing teacher data
        csv_file_path = '~/Desktop/PROJECT/EMS/data/teachersdata.csv'
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)
        
        for index, row in df.iterrows():
            print(f"{row=}")
            # Create and save an instance of teacherTable for each row in the DataFrame
            teacher = teacherTable(
                teacher_id=row['teacher_id'],
                dept_id=Department.objects.get(dept_id=row['dept_id']),
                name=row['name']
            )
            teacher.save()
        
        # Output a success message
        self.stdout.write(self.style.SUCCESS('Data import completed.'))
