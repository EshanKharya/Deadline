from rest_framework import serializers
from base.models import Profile, CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "second_name",
            "last_name",
            "gender",
            "nationality",
            "github",
            "linkedin",
            "privacy_status",
        ]

    def validate(self, data):
        errors = {}
        gender = data.get("gender")
        github = data.get("github")
        linkedin = data.get("linkedin")
        privacy = data.get("privacy_status")

        if gender and gender not in [choice[0] for choice in Profile.GENDER_CHOICES]:
            errors["gender"] = ["Gender choice invalid!"]

        if github and not (
            github.startswith("http://") or github.startswith("https://")
        ):
            errors["github"] = ["Github link invalid!"]

        if linkedin and not (
            linkedin.startswith("http://") or linkedin.startswith("https://")
        ):
            errors["linkedin"] = ["Linkedin link invalid!"]

        if privacy and privacy not in [choice[0] for choice in Profile.PRIVACY_CHOICES]:
            errors["privacy_status"] = ["Privacy choice invalid!"]

        if errors:
            raise serializers.ValidationError({"error": errors})

        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
