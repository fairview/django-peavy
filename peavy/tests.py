import logging

from django.db import transaction
from django.test import TestCase
from django.test.client import Client

from peavy.models import LogRecord
from peavy_demo.models import Quote

class TransactionTest(TestCase):

    def testTransactionSeparation(self):
        """
        Under the demo application's settings, the app and peavy both log to
        the same database, but on different connections. This test verifies
        that this means a rollback of an application write does not undo
        the logging made in that code.
        """
        logger = logging.getLogger('peavy.tests.TransactionTest.testTransactionSeparation')

        try:
            with transaction.commit_on_success():

                Quote.objects.create(
                    submitter='Anonymous Browncoat',
                    show='Firefly',
                    character='Wash',
                    text='Ah, curse your sudden but inevitable betrayal!'
                )

                logger.info('Someone left a quote!')

                # peavy has just committed the log entry; now raise an
                # exception to undo the quote creation
                raise ValueError, 'As in: Fox miscalculated the value of Firefly.'

        except ValueError, e:
            pass
        
        self.assertTrue(Quote.objects.count() == 0, 'The quote was not rolled back.')
        self.assertTrue(LogRecord.objects.count() == 1, 'The log entry was not made.')
