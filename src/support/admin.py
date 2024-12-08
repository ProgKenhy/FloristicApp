from django.contrib import admin

from support.models import ChatSupportSession, ChatSupportMessage


class ChatSupportMessagesInline(admin.TabularInline):
    model = ChatSupportMessage
    extra = 0



@admin.register(ChatSupportSession)
class ChatSupportMessagesAdmin(admin.ModelAdmin):
    inlines = [ChatSupportMessagesInline, ]
    list_display = ('user', 'created_at',)
    fields = ('user', 'created_at',)
    readonly_fields = ('user', 'created_at',)
