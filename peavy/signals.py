from django.core.signals import got_request_exception
from django.db import transaction

@transaction.commit_on_success
def exception_handler(request=None, **kwargs):
    logger = logging.getLogger('peavy.signals.exception_handler')

    if transaction.is_dirty():
        transaction.rollback()

    logger.exception('Exception: {0}'.format(exc_type), exc_info=True)

got_request_exception.connect(exception_handler)

