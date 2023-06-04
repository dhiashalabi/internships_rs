# امبورت للمكاتب التي سنستخدمها
import requests
import pandas as pd
import json

# استخدام مكتبة ريكوست لكشط الداتا من الموقع
url = requests.get("https://sa.jooble.org/jobs-internship?p=4")
# هنا نخزن التكست الذي حصلنا عليه من كشط الصفحه في المتغير داتا
data = url.text

# الحين المتغير داتا يحتوي على كل شي تم الحصول عليه من كشط الصفحه اي انه يحتوي على كل وظائف التدريب
# من اجل يقوم بلتقسيم بناء على هاذا النص  {\"url\" اعطينا دالة اسبليت
# وذالك لان وظائف التدريب تفصل بين كل وظيفة والاخرى هاذا النص
l_job = data.split('{"url"')
# استخدمنا دالة اسبليت للتقسيم من اجل تخزين وظائف التدريب في لسته
# الحين اللسته تحتوي على وظاىف التدريب بلاضافه الى عنصرين ليست من ضمن وظائف التدريب
# العنصرين هما العنصر صفر وواحد في اللست
# الحين قمنا بحذف العنصرين الذان ليسا من وظائف التدريب بعمل تغيير لقيمة اللسته بحيث تساوي
# اللسته نفسها من العنصر الثاني الى النهايه اي بدون العنصرين الاولين
l_job = l_job[2:]
# هنا قمنا بحذف اربع وظائف تدريب بسبب وجود مشاكل في تنسيق بياناتها تمنعنا من التعامل معا البيانات واستراجها
del l_job[19]
del l_job[38]
del l_job[57]
del l_job[61]
# لسته فارغه من اجل تعبئة بيانات وظائف التدريب فيها بعد استخراجها بشكل مرتب
l_data = []
for i in range(len(l_job)):
    # {\"url\" هنا قمنا باضافة النص
    # لكل تدريب وذالك لانه تم حذفه اثناء عملية التقسيم لان دالة سبليت تقوم بلتقسيم بين النصين
    l_job[i] = '{"url"' + l_job[i]
    # هنا دالة ريبليس تاخذ قيمتين تقوم باستبدال القيمة الاولى بلقيمة الثانيه
    # باستخدام دالة ريبلس سنقوم بمعالجة الداتا حتى تكون بتنسيق قابل للاستخدم
    # هاذه الدالة تاخذ نص وتعيده بشكل قائمة دكشنري json.loads لدى دالة
    # نستخدم هاذه الدالة من اجل استخراج كل تدريب بشكل قائمة تحتوي على بياناته مثل الموقع والشركة والتفاصيل
    # هنا قمنا باستبدال قوس الاغلاق  ب
    # "N",
    # json.loads وذالك لان دالة
    # تقوم بتغيير النص الذي بين القوسين ولان النص يحتوي
    # على اقواس في وسطه غير اقواس البدايه والنهايه لذالك نقوم باستبدال هاذه الاقواس
    l_job[i] = l_job[i].replace("{", '"N",')
    # عملية معالجة لكل رمز يسبب مشاكل في عمل الدالة التي تقوم بتحويل البيانات الى شكل قائمة دكشنري
    l_job[i] = l_job[i].replace("}", "")
    l_job[i] = l_job[i].replace(',"N",', ",")
    l_job[i] = l_job[i].replace(",,", ",")
    l_job[i] = "{" + l_job[i][4:-1] + "}"
    l_job[i] = l_job[i].replace('location":"N","name"', 'location":"N","loc_name"')
    # هنا استخدمنا المكتبة جايسون وقمنا باستخدام دالة لود التي تقوم بتحويل النص الى قائمة
    l_data.append(json.loads(l_job[i]))


# لستات فارغه نقوم بتعباتها بلبيانات
url = []
job_title = []
company_name = []
job_loc = []
details = []
# فور لقراة لستة الداتا التي تحتوي على قوائم التدريب
for i in l_data:
    # url تعبئة اللست الاولى بقيمة ال
    url.append(i["url"])
    # هوا المفتاح الذي يمثل التايتل في الداتا position تعبئة اللست الثانية بتايتل التدريب ال
    job_title.append(i["position"])
    # تعبئة اللست الثالثه باسم الشركة
    company_name.append(i["name"])
    # تعبئة اللست الرابعه بلموقع
    job_loc.append(i["loc_name"])
    # تعبئة اللست الخامسة بلتفاصيل
    details.append(i["fullContent"])

# انشاء داتا فريم باستخدام مكتبة باندا وتسمية الاعمدة الخاصه بها واعطاء كل عمود اللست التي تحتوي على بياناته
df = pd.DataFrame({"url": url, "title": job_title, "company_name": company_name, "loc": job_loc, "details": details})
# تخزين الداتا في ملف اكسل
df.to_csv("data_links.csv")

print(df)