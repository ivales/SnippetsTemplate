from django.contrib.auth.models import User
from django.core.management.base import BaseCommand



class Command(BaseCommand):
   help = 'get all users'

   def handle(self, *args, **options):
       return ' '.join(user.username for user in User.objects.all())