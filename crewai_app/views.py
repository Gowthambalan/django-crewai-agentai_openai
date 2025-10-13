from django.shortcuts import render
from .crew_orchestrator import route_query

def home(request):
    result = None
    query = None

    if request.method == "POST":
        query = request.POST.get("query")
        if query:
            result = route_query(query)

    return render(request, "home.html", {"result": result, "query": query})
