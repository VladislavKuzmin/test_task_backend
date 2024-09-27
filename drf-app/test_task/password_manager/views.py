from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import PasswordEntry
from .serializers import PasswordEntrySerializer


@api_view(["GET"])
def password_api_root(request, format=None):
    return Response(
        {
            "list-create": reverse(
                "password-list-create", request=request, format=format
            ),
            "search": f"{reverse('password-list-create', request=request, format=format)}?service_name=example",
            "retrieve": reverse(
                "password-retrieve",
                kwargs={"service_name": "example"},
                request=request,
                format=format,
            ),
        }
    )


class PasswordEntryView(generics.ListCreateAPIView):
    serializer_class = PasswordEntrySerializer

    def create(self, request, *args, **kwargs):
        service_name = request.data.get("service_name")
        password = request.data.get("password")

        try:
            entry = PasswordEntry.objects.get(service_name=service_name)
            entry.set_password(password)
            entry.save()
            serializer = self.get_serializer(entry)
            return Response(serializer.data)
        except PasswordEntry.DoesNotExist:
            return super().create(request, *args, **kwargs)

    def get_queryset(self):
        service_name = self.request.query_params.get("service_name", None)
        if service_name:
            return PasswordEntry.objects.filter(service_name__icontains=service_name)
        return PasswordEntry.objects.all()


class PasswordEntryRetrieveView(generics.RetrieveAPIView):
    queryset = PasswordEntry.objects.all()
    serializer_class = PasswordEntrySerializer
    lookup_field = "service_name"

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(service_name=kwargs["service_name"])
        except PasswordEntry.DoesNotExist:
            raise NotFound("Password entry not found")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
