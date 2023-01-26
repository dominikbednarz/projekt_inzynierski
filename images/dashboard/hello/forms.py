from django import forms
from hello.models import LogMessage
from hello.kafka_utils import topics



class TopicForm(forms.Form):
    topic_name = forms.CharField(max_length = 100)
    partitions = forms.IntegerField(
                    min_value=1, max_value=10,
                    help_text = "Enter number of partition"
                    )
    replicas = forms.IntegerField(
                    min_value=1, max_value=10,
                    help_text = "Enter number of replicas"
                    )


class MessageForm(forms.Form):
    CHOISES = topics()

    topic_name = forms.ChoiceField(
                    widget=forms.RadioSelect,
                    choices=CHOISES
                    )

    message = forms.CharField(max_length = 100)