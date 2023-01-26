from django.shortcuts import render, redirect
import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from hello.forms import TopicForm, MessageForm
from hello.models import LogMessage
from django.views.generic import ListView
from hello.kafka_utils import create_topic, topic_list, produce
from django.contrib import messages



def home(request):
    return render(request, 'hello/home.html')


def list(request):
    full_list = topic_list()

    return render(request, 'hello/list.html', context={'full_list': full_list})


def create(request):
    form = TopicForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            topicName = form['topic_name'].value()
            partitions = int(form['partitions'].value())
            replicas = int(form['replicas'].value())
            create_topic(topicName, partitions, replicas)
            # messages.success(request, 'Topic created successfully')
            return redirect("list")
            # return HttpResponse(f"Created topic: {topicName}")
            # return render(request, "hello/create.html", {"form": TopicForm(request.GET)})
        else:
            messages.error(request, 'Invalid form')
            messages.error(request, form.errors)
    else:
        form = TopicForm()

    return render(request, "hello/create.html", context={"form": form})


def log_message(request):
    form = MessageForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            topicName = form['topic_name'].value()
            message = form['message'].value()
            produce(topicName, message)
            return render(request, "hello/log_message.html", {"form": MessageForm(request.GET)})
        else:
            messages.error(request, 'Invalid form')
            messages.error(request, form.errors)
    else:
        form = MessageForm()

    return render(request, "hello/log_message.html", {"form": form})


def hello_there(request, name):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

