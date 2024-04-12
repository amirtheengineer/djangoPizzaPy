from django.contrib import admin

from assistant.models import ConversationState, UserResponseOption, ConversationScript


# Register your models here.
@admin.register(ConversationState)
class ConversationStateAdmin(admin.ModelAdmin):
    pass


@admin.register(UserResponseOption)
class UserResponseOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(ConversationScript)
class ConversationScriptAdmin(admin.ModelAdmin):
    pass