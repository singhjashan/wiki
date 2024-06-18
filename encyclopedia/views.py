from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random


def convert_md_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None :
        return None
    else:
        return markdowner.convert(content)
    


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request,title):
    html_content = convert_md_html(title)
    if html_content == None :
        return render(request,"encyclopedia/error.html", {
            "message":"This entry does not exist."
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "title": title ,
            "content": html_content
        })
        
def search(request):
    if request.method =="POST":
        entry_search = request.POST['q']
        html_content = convert_md_html(entry_search)
        if html_content is not None :
            return render(request,"encyclopedia/entry.html",{
            "title": entry_search ,
            "content": html_content
            })
        else:
            all_entris = util.list_entries()
            reco= []
            for entry in all_entris:
                if entry_search.lower() in entry.lower():
                    reco.append(entry)
            return render(request,"encyclopedia/search.html" , {
                "reco": reco
                
            })
            
def new_page(request):
    if request.method =="GET":
        return render(request,"encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request,"encyclopedia/error.html", {
                "message": " Entry page alredy exist."
            } )
        else:
            util.save_entry(title, content)
            print(title, content)
            html_content = convert_md_html(title)
            return render(request, 'encyclopedia/entry.html',{
                "title": title,
                "content": html_content
            })
            
def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request,'encyclopedia/edit.html',{
            "title": title,
            "content": content
        })
        
def save_edit (request):
    if request.method =="POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md_html(title)
        return render(request, 'encyclopedia/entry.html',{
            "title": title,
            "content": html_content
        })
        
def ran_dom(request):
    all_entris = util.list_entries()
    ran_entry = random.choice (all_entris)
    html_content = convert_md_html(ran_entry)
    return render (request,'encyclopedia/entry.html',{
        "title": ran_entry,
        "content":html_content
    })