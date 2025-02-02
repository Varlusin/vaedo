from django.shortcuts import render
from django.utils.translation import gettext as _

from django.db import connection
from pprint import pprint


def index(request):
    context = {"title" : _("Home")}
    pprint(connection.queries)
    return render(request, "main/index.html", context)
