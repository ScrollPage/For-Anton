from django.core.management import BaseCommand

from datetime import datetime, timezone

from account.models import Account
from question.models import Question

class Command(BaseCommand):
	help = u"Fills db with dummy questions"

	def handle(self, *args, **options):
		try:
			user = Account.objects.get(email='dummy@dummy.com')
		except:
			user = Account.objects.create_user(
				email='dummy@dummy.com',
				username='dummy',
				password='QWERTYUIOP123'
			)
		for _ in range(1000):
			Question.objects.create(
				user=user,
				content='DUMMY QUESTION',
				question='????'
			)

