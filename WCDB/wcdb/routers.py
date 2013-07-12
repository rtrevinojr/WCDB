from django.conf import settings

class test_router (object) :
    def db_for_read(self, model, **hints) :
        if settings.RUNNING_OFF_TEST_DB :
            return 'test'
        return 'default'

    def db_for_write(self, model, **hints) :
        if settings.RUNNING_OFF_TEST_DB :
            return 'test'
        return 'default'
