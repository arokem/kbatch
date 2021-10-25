import zipfile

from rest_framework import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from django_kbatch_server.models import User, Job, Upload


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = [
            "url",
            "command",
            "image",
            "name",
            "env",
            "user",
            "upload",
            "upload_data",
        ]

    user = serializers.ReadOnlyField(source="user.username")

    # TODO: Might want to make this a JSON field with things like
    # content, name, content-type, ...
    upload_data = serializers.CharField(
        allow_blank=True, allow_null=True, required=False, write_only=True
    )

    def create(self, validated_data):
        upload = validated_data.get("upload")
        upload_data = validated_data.pop("upload_data", None)

        if upload and upload_data:
            raise ValidationError("Cannot provide both 'upload', and 'upload_data'.")

        elif upload_data:
            content = upload_data.encode()
            upload = Upload(
                user=validated_data["user"], file=SimpleUploadedFile("upload", content)
            )
            upload.save()

            validated_data["upload"] = upload

        result = super().create(validated_data)
        return result


class ZipFileField(serializers.FileField):
    default_error_messages = {
        **dict(serializers.FileField.default_error_messages),
        **{"zip": _("The submitted file must be a ZIP archive.")},
    }

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if not zipfile.is_zipfile(data.file):
            self.fail("zip")
        return data


class UploadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Upload
        fields = ["url", "file", "user"]

    file = ZipFileField(write_only=True)
    user = serializers.ReadOnlyField(source="user.username")
