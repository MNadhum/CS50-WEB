from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

from . import util

import os


def redirect(request):
    return HttpResponseRedirect("/")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, entry):
    found = True
    information = util.get_entry(entry)
    if information == None:
        found = False
        initial_entry = entry
        entry = "Not Found"
        information = "<h1>Entry \"" + initial_entry + "\" Does Not Exist </h1>"
        information += "<br>"
    return render(request, "encyclopedia/entry_page.html", {
        "entry": entry,
        "information": information,
        "found": found
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


def create(request):
    title = request.GET.get("title")
    content = request.GET.get("content")

    information = util.get_entry(title)
    if title != None:
        if information != None:
            messages.error(request, "Page already exists")
            return render(request, "encyclopedia/create.html", {})
        else:
            new_file = open( os.path.join("./entries" ,(str(title) + ".md")), "w")
            new_file.write("# " + str(title) + '\n')
            content = content.replace('\n','')
            new_file.write(content)
            new_file.close()
            return HttpResponseRedirect(('/wiki/' + str(title)))
    return render(request, "encyclopedia/create.html", {})


def edit(request, entry):
    content = request.GET.get("content")
    if content != None:
        try:
            os.remove(os.path.join("./entries" ,(str(entry) + ".md")))
        except:
            pass
        rewrite = open(os.path.join("./entries" ,(str(entry) + ".md")), "w")
        content = content.replace('\n','')
        rewrite.write(content)
        rewrite.close()
        return HttpResponseRedirect(('/wiki/' + str(entry)))
    else:
        open_file = open(os.path.join("./entries" ,(str(entry) + ".md")), "r")
        content = open_file.read()
        open_file.close()
        if content != None:
            return render(request, "encyclopedia/edit.html", {
                "entry": entry,
                "content": content
            })
    return render(request, "encyclopedia/index.html", {})

