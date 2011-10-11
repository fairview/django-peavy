from django.utils.translation import gettext_lazy as _

from django.contrib import admin

from peavy.models import LogRecord

class LogRecordAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'application', 'origin_server', 'client_ip', 'user', 'logger', 'level', 'message')
    list_filter = ('application', 'origin_server', 'user', 'logger', 'level')
    search_fields = ('application', 'origin_server', 'client_ip', 'user', 'logger', 'level', 'message')

    fieldsets = (
        (
            _('Server details'),
            {
                'fields': (
                    'timestamp',
                    'application',
                    'origin_server'
                )
            }
        ),
        (
            _('Request details'),
            {
                'fields': (
                    'client_ip',
                    'user',
                )
            }
        ),
        (
            _('Logging details'),
            {
                'fields': (
                    'logger',
                    'level',
                    'message'
                )
            }
        ),
        (
            _('Exception details'),
            {
                'fields': (
                    'stack_trace',
                    'debug_page'
                )
            }
        )
    )

    readonly_fields = LogRecord._meta.get_all_field_names()

admin.site.register(LogRecord, LogRecordAdmin)
