import os
import sys

import django


def run_tests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    django.setup()

    from django.test.runner import DiscoverRunner

    test_runner = DiscoverRunner(verbosity=2)
    failures = test_runner.run_tests(['habits', 'telegram_bot', 'users'])

    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests()
