# making a function to create filters to view relevant ids

import pandas as pd


def knowledge_based_filters(clean_df, location="all", skill_cat="all", search=""):
    """
    تقوم الدالة بارجاع مجموعة فرعيه من اطار البيانات وفقا للموقع والمهارات
    clean_df الداتا
    location الموقع
    skill_cat الفئات او المهارات المطلوبه

    """
    if location != "all":
        # لايجاد التدريبات ذات الموقع المطلوب str.contains نستخدم دالة ال
        clean_df = clean_df[(clean_df["loc"].str.contains(location[:5]))]
    if skill_cat != "all":
        # نفس الدالة لايجاد التدريبات المشابهه للفئه والمهارات المطلوبه
        clean_df = clean_df[(clean_df.title.str.contains(skill_cat[:3])) | clean_df.details.str.contains(skill_cat[:3])]
    if search != "":
        # نفس الدالة لايجاد التدريبات المشابهه للكلمات المطلوبه
        clean_df = clean_df[
            (clean_df.title.str.contains(search[:3]))
            | clean_df.company_name.str.contains(search[:3])
            | clean_df["loc"].str.contains(search[:3])
            | clean_df.details.str.contains(search[:3])
        ]
    try:
        clean_df.iloc[0, :]
    except:
        return None
    return clean_df
