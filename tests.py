import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = 'peavy_demo.settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)

print "DJANGO_SETTINGS_MODULE:", os.getenv('DJANGO_SETTINGS_MODULE')
print "sys.path:", sys.path

from django.test.utils import get_runner
from django.conf import settings

def main():
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    test_runner = get_runner(settings)(interactive=False, verbosity=2)
    failures = test_runner.run_tests(['peavy'])
    sys.exit(failures)

if __name__ == '__main__':
    main()

