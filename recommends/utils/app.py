import knowledge, prepping, recommendation
import pandas as pd

df = pd.read_csv("recomm_df.csv")

print("Enter a specific location you want to search for. If you want no filters on location, type all: ")
loc = input()
print("Enter a specific skill/category you want to search for. If you want no filters on this, type all: ")
skill_cat = input()
clean_df = knowledge.knowledge_based_filters(df, loc.lower().strip(), skill_cat.lower().strip())
print("These ids represent the most relevant profiles:", clean_df["id"].values.tolist())
print("Please enter one of these ids to save the profile related to this id in your current directory: ")
id_int = int(input())
df_id = clean_df[clean_df["id"] == id_int]
df_id.to_csv("id_profile_" + str(id_int) + ".csv")
len_clean_df = clean_df.shape[0]
print("Please enter the no. of recommended internships you want to make between 1-{}: ".format(len_clean_df))
n_int = int(input())
sim = prepping.return_sim(clean_df)
df_recs = recommendation.make_recs(sim, clean_df, id_int, n_int)
print(df_recs)
df_recs.to_csv("df_recommendations.csv")
print("Saved your recommendations in your current directory")
