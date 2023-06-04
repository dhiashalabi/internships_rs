import pandas as pd

# قراة ملف الداتا
df = pd.read_csv("data_links.csv")
# حذف عمود واضافة عمود الاي دي لترقيم التدريبات بحيث يبداء من واحد
del df["Unnamed: 0"]
df["id"] = range(1, df.shape[0] + 1)
df = pd.concat([df["id"], df.iloc[:, :-1]], axis=1)

# استخدام دالة الريبلس لتنظيف الداتا
df["details"] = df.details.str.replace("<h2>", "")
df["details"] = df.details.str.replace("</h2>", "")
df["details"] = df.details.str.replace("<p>", "")
df["details"] = df.details.str.replace("</p>", "")
df["details"] = df.details.str.replace("</b>", "")
df["details"] = df.details.str.replace("<b>", "")
df["details"] = df.details.str.replace("</ul>", "")
df["details"] = df.details.str.replace("<ul>", "")
df["details"] = df.details.str.replace("</li>", "")
df["details"] = df.details.str.replace("<li>", "")
df["details"] = df.details.str.replace("<br>", "")
df["details"] = df.details.str.replace('<p simplifier="block">', "")
df["details"] = df.details.str.replace("<h3>", "")
df["details"] = df.details.str.replace("</h3>", "")
df["details"] = df.details.str.replace("</u>", "")
df["details"] = df.details.str.replace("<u>", "")
df["details"] = df.details.str.replace("</em>", "")
df["details"] = df.details.str.replace("<em>", "")
df["details"] = df.details.str.replace('<u simplifier="inline">', "")
df["details"] = df.details.str.replace('<em simplifier="inline">', "")
df["details"] = df.details.str.replace("<strong>", "")
df["details"] = df.details.str.replace("</strong>", "")
df["details"] = df.details.str.replace("<i>", "")
df["details"] = df.details.str.replace("</i>", "")
df["details"] = df.details.str.replace("<ol>", "")
df["details"] = df.details.str.replace("</ol>", "")
df["details"] = df.details.str.replace('<b simplifier="inline">', "")
df["details"] = df.details.str.replace("<dt>", "")
df["details"] = df.details.str.replace("</dt>", "")
df["details"] = df.details.str.replace("<dl>", "")
df["details"] = df.details.str.replace("</dl>", "")
df["details"] = df.details.str.replace("<dd>", "")
df["details"] = df.details.str.replace("</dd>", "")
df["details"] = df.details.str.replace("<td>", "")
df["details"] = df.details.str.replace("</td>", "")
df["details"] = df.details.str.replace("<tr>", "")
df["details"] = df.details.str.replace("</tr>", "")
df["details"] = df.details.str.replace("<tbody>", "")
df["details"] = df.details.str.replace("</tbody>", "")
df["details"] = df.details.str.replace("<table>", "")
df["details"] = df.details.str.replace("</table>", "")
df.iloc[:, 1:] = (
    df.iloc[:, 1:]
    .apply(lambda x: x.str.replace("\t", " "))
    .apply(lambda x: x.str.replace("\n", " "))
    .apply(lambda x: x.str.replace("\r", " "))
)
df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.str.strip())
# تحويل كل الاحرف الى احرف صغيره
df = pd.concat([df.id, df.iloc[:, 2:].apply(lambda x: x.str.lower()), df.url], axis=1)
# حفظ الداتا بعد تنظيفها في ملف اكسل
df.to_csv("recomm_df.csv", sep=",", index=False)
