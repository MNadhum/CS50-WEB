from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, entry):
    information = util.get_entry(entry)
    if information == None:
        initial_entry = entry
        entry = "Not Found"
        information = "<h1>Entry \"" + initial_entry + "\" Does Not Exist </h1>"
        information += "<br> Please <a href=encyclopedia:new> Create New Page </a>"
    return render(request, "encyclopedia/entry_page.html", {
        "entry": entry,
        "information": information
    })

def search(request):
    query = request.GET.get("q")
    if util.get_entry(query) != None:
            return page(request, query)
    else:
        sub_string_entries = []
        entries = util.list_entries()
        for entry in entries:
            if entry.find(query) >= 0:
                sub_string_entries.append(entry)

        for entry in sub_string_entries:
            print(entry)
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "entries": sub_string_entries
        })
