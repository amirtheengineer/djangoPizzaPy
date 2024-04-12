from django.db import models


class ConversationState(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the conversation state")
    prompt = models.TextField(help_text="The message or question to present to the user in this state")

    def __str__(self):
        return self.name


class UserResponseOption(models.Model):
    state = models.ForeignKey(ConversationState, related_name='response_options', on_delete=models.CASCADE,
                              help_text="The conversation state this response option is associated with")
    keyword = models.CharField(max_length=50,
                               help_text="The expected keyword or input from the user that triggers this response")
    next_state = models.ForeignKey(ConversationState, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='+',
                                   help_text="The next conversation state to transition to based on this response")

    def __str__(self):
        return f"'{self.keyword}' in {self.state.name}"


class ConversationScript(models.Model):
    key = models.CharField(max_length=100, unique=True, help_text="A unique key to identify this script")
    text = models.TextField(help_text="The script text or message")

    def __str__(self):
        return self.key
