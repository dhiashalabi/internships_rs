from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .forms import UserForm
from .models import City, Internship, InternshipCategory, UserInterest


class IndexView(CreateView):
    template_name = "site/index.html"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Home",
        }
        return render(request, self.template_name, context)


class LoginView(LoginView):
    template_name = "site/auth/login.html"
    next_page = "index"


def logout_view(request):
    logout(request)
    return redirect("signin")


class SignUpView(CreateView):
    template_name = "site/auth/signup.html"

    def get(self, request, *args, **kwargs):
        form = UserForm()
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data["password"])
            user.is_active = True
            user.save()
            return redirect("signin")
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)


class GetInternshipsView(CreateView):
    template_name = "site/internships.html"

    def dispatch(self, request, *args, **kwargs):
        self.internship_category = request.GET.get("internship_category")
        self.city = request.GET.get("city")
        self.q = request.GET.get("q")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        filters = Q()
        title = "Internships"
        if self.internship_category:
            internship_category = InternshipCategory.objects.get(id=self.internship_category)
            filters = Q(internship_category=self.internship_category)
            title = internship_category.name
            if "internship" not in title.lower() and "internships" not in title.lower():
                title = internship_category.name + " Internships"
        elif self.city:
            city = City.objects.get(id=self.city)
            title = city.name + " Internships"
            filters = Q(city=self.city)
        elif self.q:
            filters = (
                Q(title__icontains=self.q)
                | Q(description__icontains=self.q)
                | Q(internship_category__name__icontains=self.q)
            )
        internships = Internship.objects.filter(filters) if filters else Internship.objects.all()
        if request.user.is_authenticated:
            for internship in internships:
                internship.is_interested = False
                if UserInterest.objects.filter(user=request.user).exists():
                    user_interests = UserInterest.objects.get(user=request.user)
                    if user_interests.internships.filter(id=internship.id).exists():
                        internship.is_interested = True
        context = {
            "internships": internships,
            "title": title,
        }
        return render(request, self.template_name, context)


def user_interest(request):
    response = {}
    if request.method == "POST":
        internship_id = request.POST.get("internship_id")
        if internship_id:
            if Internship.objects.filter(id=internship_id).exists():
                if UserInterest.objects.filter(user=request.user).exists():
                    user_interests = UserInterest.objects.get(user=request.user)
                    if user_interests.internships.filter(id=internship_id).exists():
                        internship = user_interests.internships.get(id=internship_id)
                        user_interests.internships.remove(internship)
                        response = {
                            "status": "success",
                            "operation": "d",
                            "message": "Interest removed from internship",
                        }
                    else:
                        user_interests.internships.add(internship_id)
                        response = {
                            "status": "success",
                            "operation": "a",
                            "message": "Interest added to internship",
                        }
                else:
                    user_interest = UserInterest.objects.create(user=request.user)
                    user_interest.internships.add(internship_id)
                    response = {"status": "success", "message": "Interest added to internship"}
    return JsonResponse(response)
