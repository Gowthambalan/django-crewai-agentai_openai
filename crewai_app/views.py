# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .crew_orchestrator import route_query


# #  Browser view (renders HTML page)
# def home(request):
#     result = None
#     query = None

#     if request.method == "POST":
#         query = request.POST.get("query")
#         if query:
#             result = route_query(query)

#     return render(request, "home.html", {"result": result, "query": query})


# #  API endpoint for Postman (returns JSON)
# @csrf_exempt  # disable CSRF just for testing via Postman
# def api_query(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             user_query = data.get("query")

#             if not user_query:
#                 return JsonResponse({"error": "Missing 'query' field"}, status=400)

#             result = route_query(user_query)
#             return JsonResponse({
#                 "query": user_query,
#                 "decision": result["decision"],
#                 "response": result["answer"]
#             })

#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)

#     return JsonResponse({"error": "Only POST method allowed"}, status=405)


from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import QueryLogSerializer
from .crew_orchestrator import route_query
from django.views.decorators.csrf import csrf_exempt
from .models import QueryLog


def home(request):
    result = None
    query = None

    if request.method == "POST":
        query = request.POST.get("query")
        if query:
            result = route_query(query)

    return render(request, "home.html", {"result": result, "query": query})

@csrf_exempt
@api_view(['POST'])
def api_query(request):
    user_query = request.data.get('query')
    if not user_query:
        return Response({"error": "Missing 'query' field"}, status=400)

    # Get AI response
    result = route_query(user_query)

    # Save to DB
    query_log = QueryLog.objects.create(
        user_query=user_query,
        decision=result['decision'],
        response=result['answer']
    )

    # Serialize the DB object to JSON
    serializer = QueryLogSerializer(query_log)
    return Response(serializer.data)
