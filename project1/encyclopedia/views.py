from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

from . import util

import os
import random


def redirect(request):
    """
    Redirects links to index page, used when user attempts to acces an empty wiki or edit page

    request: HttpRequest object with information about user's request

    return: HttpResponseRedirect to index page
    """

    return HttpResponseRedirect("/")


def index(request):
    """
    Used for loading index page

    request: HttpRequest object with information about user's request

    return: render of index.html
    """

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() # all encyclopedia entries for web page to load
    })


def page(request, entry):
    """
    Used to load specific encyclopedia entry pages

    request: HttpRequest object with information about user's request

    return: render of entry_page.html
    """

    found = True
    information = util.get_entry(entry)

    if information == None:
        found = False
        initial_entry = entry
        entry = "Not Found"
        information = "<h1>Entry \"" + initial_entry + "\" Does Not Exist </h1>"
        information += "<br>"

    return render(request, "encyclopedia/entry_page.html", {
        "entry": entry, # title of entry
        "information": information, # entry's content
        "found": found # bool whether entry was found or not
    })


def search(request):
    """
    Used to run search function of website

    request: HttpRequest object with information about user's request

    return: render of web page
    """

    query = request.GET.get("q")

    # if search query == name of an entry, then loads that entry's page
    if util.get_entry(query) != None:
            return page(request, query)
    else:
        sub_string_entries = []
        entries = util.list_entries()

        # checks if search query is substring in every entry name
        for entry in entries:
            if entry.find(query) >= 0:
                sub_string_entries.append(entry)

        return render(request, "encyclopedia/search.html", {
            "query": query, # search query
            "entries": sub_string_entries # entries list where query is substr
        })


def create(request):
    """
    Used to load Create New Page webpage

    request: HttpRequest object with information about user's request

    return: render of create.html, or redirect to newly created web page
    """

    title = request.GET.get("title")
    content = request.GET.get("content")
    information = util.get_entry(title)

    # if user entered a title
    if title != None:
        # if entry already exists
        if information != None:
            # alers user that entry already exists
            messages.error(request, "Page already exists")

            return render(request, "encyclopedia/create.html", {})
        else:
            # creates new entry page with user submitted information
            new_file = open( os.path.join("./entries" ,(str(title) + ".md")), "w")
            new_file.write("# " + str(title) + '\n')
            content = content.replace('\n','')
            new_file.write(content)
            new_file.close()

            return HttpResponseRedirect(('/wiki/' + str(title)))

    return render(request, "encyclopedia/create.html", {})


def edit(request, entry):
    """
    Used to load edit page for entries

    entry: title of entry user is requesting to edit

    request: HttpRequest object with information about user's request

    return: redirect to entry page, render of index page
    """

    content = request.GET.get("content")

    # if user submitted content for entry
    if content != None:
        # if entry alreqady exits, delete initial file
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
                "entry": entry, # title of entry
                "content": content # content of entry
            })

    return render(request, "encyclopedia/index.html", {})

def random_page(request):
    """
    Used for Random Page feature of website

    request: HttpRequest object with information about user's request

    return: redirect to random encyclopedia entry
    """

    entries = util.list_entries()

    page_index = random.randint(0, (len(entries) - 1))
    title = entries[page_index]

    return HttpResponseRedirect(('/wiki/' + str(title)))
