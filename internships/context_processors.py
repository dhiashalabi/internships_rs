from django.db.models import Q
from .models import (
    Country,
    City,
    InternshipCategory,
    InternshipType,
    Internship,
    UserInterest,
)


def get_countries(request):
    return {"countries": Country.objects.all()}


def get_cities(request):
    return {"cities": City.objects.all()}


def get_internship_categories(request):
    return {"internship_categories": InternshipCategory.objects.all()}


def get_internship_types(request):
    return {"internship_types": InternshipType.objects.all()}


def get_internships(request):
    filters = Q()
    if request.GET.get("q"):
        filters &= Q(title__icontains=request.GET.get("q"))
    internships = Internship.objects.filter(filters)
    if request.user.is_authenticated:
        for internship in internships:
            internship.is_interested = False
            if UserInterest.objects.filter(user=request.user).exists():
                user_interests = UserInterest.objects.get(user=request.user)
                if user_interests.internships.filter(id=internship.id).exists():
                    internship.is_interested = True
        return {"internships": internships}
    return {"internships": Internship.objects.all()}
