import csv
from django.core.management.base import BaseCommand, CommandError
from exam.models import Course, Department

class Command(BaseCommand):
    help = 'Load courses from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to be loaded')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    department = Department.objects.get(id=row['dept_id'])
                    Course.objects.create(
                        course_id=row['course_id'],
                        course_title=row['course_title'],
                        dept_id=department,
                        Syllabus_year=row['Syllabus_year'],
                        sem=row['sem'],
                        course_code=row['course_code'],
                        grad_level=row['grad_level']
                    )
            self.stdout.write(self.style.SUCCESS('Successfully uploaded courses from %s' % csv_file))
        except FileNotFoundError:
            raise CommandError('CSV file "%s" does not exist' % csv_file)
        except Exception as e:
            raise CommandError('Error while uploading courses: %s' % str(e))