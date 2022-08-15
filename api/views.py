import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from .models import User, Rates, Port
from django.core import serializers
# Create your views here.
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import DeleteView


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
@login_required
def add(request):
    req = json.loads(request.body)
    source_port = Port.objects.filter(name=req["source"]).first()
    destination_port = Port.objects.filter(name=req["destination"]).first()
    print(source_port, destination_port, user, req["container_size"])
    rate = Rates.objects.create(
        source=source_port,
        destination=destination_port,
        container_size=req["container_size"],
        exim=req["exim"],
        rate=req["rate"],
    )
    rate.save()
    return JsonResponse({"status": "success"}, status=200)


@require_http_methods(["POST"])
@login_required
def add_port(request):
    req = json.loads(request.body)
    Port.objects.create(name=req["name"])
    return JsonResponse({"status": "success"}, status=200)


@require_http_methods(["GET"])
@login_required
def search(request):
    req = request.GET
    exim = req.get("exim", "")
    source = req.get("source", "")
    destination = req.get("destination", "")
    container_size = req.get("container_size", "")

    query = Rates.objects.raw(
        f"""
        SELECT * from api_rates
        WHERE source_id like '%{source}%'
        AND destination_id like '%{destination}%'
        AND container_size like '%{container_size}%'
        AND exim like  '%{exim}'
        GROUP BY source_id,destination_id,container_size
        HAVING MAX(created_at) ORDER BY created_at
        """
    )

    resp = [x["fields"] for x in serializers.serialize("python", query)]
    return JsonResponse(resp, safe=False, status=200)


@require_http_methods(["GET"])
@login_required
def ports(request):
    query = Port.objects.all()
    print()
    resp = [x["pk"] for x in serializers.serialize("python", query)]
    return JsonResponse(resp, safe=False, status=200)


@require_http_methods(["POST"])
@login_required
def delete_rate(request):
    Rates.objects.filter(id=request["id"]).first().delete()
    return JsonResponse({"status": "success"}, safe=False, status=200)
