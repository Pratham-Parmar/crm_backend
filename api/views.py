import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import User, Rates, Port, Exim
from django.core import serializers
# Create your views here.
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout


@require_http_methods(["POST"])
def login_user(request):
    req = json.loads(request.body)
    user = authenticate(request, username=req["username"], password=req["password"])
    if user is not None:
        login(request, user)
        return JsonResponse({"status": "Success"}, status=200)
    else:
        return JsonResponse({"status": "Invalid Credentials"}, status=401)


def logout_user(request):
    logout(request)
    return JsonResponse({"status": "Success"}, status=200)


@require_http_methods(["POST"])
# @login_required
def add(request):
    req = json.loads(request.body)
    source_port = Port.objects.filter(name=req["source"]).first()
    destination_port = Port.objects.filter(name=req["destination"]).first()
    user = User.objects.filter(email=req["email"]).first()
    Rates.objects.create(
        source=source_port,
        destination=destination_port,
        container_size=req["container_size"],
        exim=req["exim"],
        created_by=user,
        rate=req["rate"],
    )
    return JsonResponse({"status": "success"}, status=200)


@require_http_methods(["POST"])
@login_required
def add_port(request):
    req = json.loads(request.body)
    Port.objects.create(name=req["name"])
    return JsonResponse({"status": "success"}, status=200)


@require_http_methods(["GET"])
# @login_required
def search(request):
    req = request.GET
    source = req.get("source","")
    destination = req.get("destination","")
    container_size = req.get("container_size","")
    user = User.objects.filter(email=req["email"]).first()
    query = Rates.objects.filter(created_by=user)

    # query = Rates.objects.all()


    # query = Rates.objects.raw(
    #     f"""
    #     SELECT * from api_rates
    #     WHERE source_id like '%{source}%'
    #     AND destination_id like '%{destination}%'
    #     AND container_size like '%{container_size}%'
    #     GROUP BY source_id,destination_id,container_size
    #     HAVING MAX(created_at) ORDER BY created_at
    #     """
    # )


    resp = [x["fields"] for x in serializers.serialize("python", query)]
    return JsonResponse(resp, safe=False, status=200)


@require_http_methods(["GET"])
@login_required
def ports(request):
    query = Port.objects.all()
    print()
    resp = [x["pk"] for x in serializers.serialize("python", query)]
    return JsonResponse(resp, safe=False, status=200)
