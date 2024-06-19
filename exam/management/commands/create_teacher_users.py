# exam/management/commands/create_teacher_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from exam.models import teacherTable

class Command(BaseCommand):
    help = 'Create users for teachers and add them to the Teacher group'

    def handle(self, *args, **kwargs):
        teacher_group, created = Group.objects.get_or_create(name='Teacher')
        
        teachers = teacherTable.objects.filter(user__isnull=True)
        for teacher in teachers:
            username = teacher.name.split()[0]  # Assuming first name as username
            default_password = "defaultpassword"  # Set a default password
            
            user, created = User.objects.get_or_create(username=username, defaults={
                'password': default_password,
            })
            
            if created:
                user.set_password(default_password)  # Set the default password
                user.save()
                teacher.user = user
                teacher.save()
                teacher_group.user_set.add(user)
                self.stdout.write(self.style.SUCCESS(f'Created user {username} for teacher {teacher.name} with password {default_password}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {username} already exists'))
