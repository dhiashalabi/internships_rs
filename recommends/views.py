import os
from django.http import HttpResponse, JsonResponse
import pandas as pd
from django.shortcuts import render
from django.views.generic import CreateView
from .models import UserProfile, UserProfileItem
from .utils import knowledge, prepping, recommendation


file_path = os.path.join(os.path.dirname(__file__), "utils/recomm_df.csv")
df = pd.read_csv(file_path)


class RecommendsView(CreateView):
    template_name = "site/recommends.html"

    def dispatch(self, request, *args, **kwargs):
        self.city = request.GET.get("rs_city") or "all"
        self.category = request.GET.get("rs_category") or "all"
        self.internship_type = request.GET.get("rs_internship_type") or "all"
        self.search = request.GET.get("rs_search") or ""
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        clean_df = knowledge.knowledge_based_filters(
            df,
            self.city.lower().strip(),
            self.category.lower().strip(),
            self.search.lower().strip(),
        )
        if isinstance(clean_df, pd.DataFrame):
            len_clean_df = clean_df.shape[0]
            context = {
                "recommendations": clean_df.to_dict(orient="records"),
                "len_clean_df": len_clean_df,
                "ids_list": clean_df["id"].values.tolist(),
            }
        else:
            context = {"recommendations": [], "len_clean_df": 0, "ids_list": []}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        response = {}
        recommendation_id = request.POST.get("recommendation_id")
        if recommendation_id:
            df_id = df[df["id"] == int(recommendation_id)]
            if df_id.empty:
                response = {
                    "status": "error",
                    "message": "no recommendation found",
                }
            else:
                data = df_id.to_dict(orient="records")
                data[0]["profile_id"] = data[0].pop("id")
                data[0]["company"] = data[0].pop("company_name")
                data[0]["location"] = data[0].pop("loc")
                if not UserProfile.objects.filter(user=request.user).exists():
                    user_profile = UserProfile.objects.create(user=request.user)
                    user_profile.save()
                else:
                    user_profile = UserProfile.objects.get(user=request.user)
                if user_profile:
                    for item in data:
                        if UserProfileItem.objects.filter(
                            user_profile=user_profile,
                            profile_id=item["profile_id"],
                        ).exists():
                            UserProfileItem.objects.filter(
                                user_profile=user_profile, profile_id=item["profile_id"]
                            ).delete()
                            response = {
                                "status": "success",
                                "operation": "d",
                                "message": "recommendation deleted",
                            }
                        else:
                            user_profile_item = UserProfileItem.objects.create(user_profile=user_profile, **item)
                            user_profile_item.save()
                            response = {
                                "status": "success",
                                "operation": "a",
                                "message": "recommendation saved",
                            }
        else:
            response = {
                "status": "success",
                "message": "no recommendation id found",
            }
        return JsonResponse(response)


def save_csv_file(request):
    if request.method == "POST":
        recommendation_id = request.POST.get("recommendation_id")
        if recommendation_id:
            df_id = df[df["id"] == int(recommendation_id)]
            df_id.to_csv("{0}_profile_{1}.csv".format(request.user.username, recommendation_id))
            with open("{0}_profile_{1}.csv".format(request.user.username, recommendation_id), "rb") as fh:
                response = HttpResponse(fh, content_type="text/csv")
                response["Content-Disposition"] = "attachment; filename=" + os.path.basename(
                    "{0}_profile_{1}.csv".format(request.user.username, recommendation_id)
                )
                return response


def make_recommendation(request):
    if request.method == "POST":
        index = request.POST.get("index")
        recommend = request.POST.get("recommendation")
        city = request.POST.get("city")
        category = request.POST.get("category")
        internship_type = request.POST.get("internship_type")
        search = request.POST.get("search")
        clean_df = knowledge.knowledge_based_filters(
            df,
            city.lower().strip(),
            category.lower().strip(),
            search.lower().strip(),
        )
        len_clean_df = clean_df.shape[0]
        if len_clean_df == 0:
            return JsonResponse({"status": "error", "message": "no recommendations found"})
        if int(recommend) < 1 or int(recommend) > len_clean_df:
            return JsonResponse({"status": "error", "message": "recommendation number out of range"})
        sim = prepping.return_sim(clean_df)
        df_recs = recommendation.make_recs(sim, clean_df, int(index), recommend)
        df_recs.to_csv("df_recommendations.csv")
        with open("df_recommendations.csv", "rb") as fh:
            response = HttpResponse(fh, content_type="text/csv")
            response["Content-Disposition"] = "attachment; filename=" + os.path.basename("df_recommendations.csv")
            return response
