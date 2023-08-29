from rest_framework import serializers
from .models import Profile, Project, CertifyingInstitution, Certificate


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = "__all__"


class NestedCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "name", "profiles"]


class CertifyingInstitutionSerializer(serializers.ModelSerializer):
    certificates = NestedCertificateSerializer(many=True)

    class Meta:
        model = CertifyingInstitution
        fields = ["id", "name", "url", "certificates"]

    def create(self, validated_data):
        certificate_data = validated_data.pop("certificates")
        institution = CertifyingInstitution.objects.create(**validated_data)

        for certificate_data in certificate_data:
            Certificate.objects.create(
                certifying_institution=institution,
                **certificate_data,
            )
        return institution
