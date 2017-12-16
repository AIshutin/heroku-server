# -*- coding: utf-8 -*- 
import bs4
from LogicGroups import *
import TextParser as TP
import LogicGroups as LG

def noun_changing(soup):
    param = {"style": "float:right; clear:right; margin-left:0.5em; margin-bottom:0.5em; border: 1px solid #6699CC; border-collapse:collapse;", "cellpadding":"2", "rules":"all", "width":"250"}
    tables = soup.find_all("table", param)
    for el1 in tables:
        try:
            items = el1.find_all("tr")[1:]
            #print(el1)
            ans = [dict(), dict()]
            for el in items:
                z = el.find_all("td")
                q = str(z[0].find("a"))
                name = q[q.find(">") + 1: q.rfind("<")]
                z = z[1:]
                for i in range(len(z)):
                    q = str(z[i])
                    q = q[q.find(">") + 1:q.rfind("<")]
                    ans[i][name] = []
                    q = list(q.split("<br/>"))
                    for el in q:
                        if el[0] == "\n":
                            el = el[2:]
                        y1 = []
                        for j in range(len(el)):
                            if el[j] not in alpha:
                                el = el[:j - 1] + chr(ord(el[j - 1]) - ord("а") + ord("А")) + el[j:]
                                y1.append(j)
                        t1 = 0
                        for j in range(len(el)):
                            if el[j] == "ё":
                                el = el[:j] + "Ё" + el[j + 1:]
                        for y in y1:
                            y -= t1
                            t1 += 1
                            el = el[:y] + el[y + 1:]
                        strange = False
                        for j in el:
                            if j not in alpha:
                                strange = True
                        if strange:
                            ans[i][name].append("-")
                        else:
                            ans[i][name].append(el)
            return ans
        except:
            pass
    return [dict(), dict()]

def define_type(soup): #noun, verb, etc.
    #Прилагательное
    type1 = soup.find_all("p")
    for el in type1:
        #print(el)
        try:
            text = ""
            for el in el.text:
                text = text + TP.make_lower(el)
            for z in types:
                if text.find(z) != -1:
                    return z
            #print(text)
        except:
            pass
    #print()
    
    #Существительные, глаголы
    type1 = soup.find_all("p")
    for el in type1:
        q = el.find("a")
        if q != None:
            #print(1, el)
            try:  
                b = True
                name1 = q.get("title")
                #print(q)
                for el in name1:
                    if el not in alpha:
                        b = False
                if b and name1 in types:
                    return name1
                    
            except:
                pass

    return "другое"

def noun_prop(soup):
    type1 = soup.find_all("p")
    for el in type1:
        q = el.find("a")
        if q != None:
            #print(el.text)
            #print(atr)
            ans = set()
            atr = el.text
            #print(atr)
            for el in LG.terms:
                if atr.find(el) != -1:
                    ans.add(LG.terms[el])
            if ans != {}:
                return ans
    print("XMLParser свойства существительного не найдены")
    return ["другое"]        

def normalize(s): #проставление ударений, нормализация строчек с переводами строки
    l = list(s.replace("△", "").split("\n"))
    ans = []
    for z in l:
        text = ""
        prev = ""
        for el in z:
            if el not in alpha:
                text = text + TP.make_bigger(prev)
                prev = ""
            elif el == "ё":
                text = text + prev + "Ё"
                prev = ""
            else:
                text = text + prev
                prev = el
        ans.append(text + el)
    return ans

def adjective_changing(soup):
    #print(soup)
    param = {"style": "float:right; clear:right; margin-left:0.5em; margin-bottom:0.5em; border: 1px solid #6699CC; border-collapse:collapse;", "cellpadding":"2", "rules":"all", "width":"210"}
    table = soup.find("table", param)
    if not table:
        return
    rows = table.find_all("tr")
    if len(rows) <= 7: #8 - 10
        return
    #print(table)
    rows = rows[2:]
    ans = dict()
    ans["м. р."] = dict()
    ans["ж. р."] = dict()
    ans["ср. р."] = dict()
    ans["мн. ч."] = dict()
    for row in rows:
        arr = ["м. р.", "ср. р.", "ж. р.", "мн. ч."]
        cols = row.find_all("td")
        title = cols[0].text[:3]
        if title[-1] != ".":
            title = title[:-1] + '.' 
        i = 0
        #print(cols)
        if len(cols) < 5:
            continue
        
        while i < 4:
            #print(cols[-(4 - i)].text.replace("△", ""))
            l = normalize(cols[-(4 - i)].text)
            ans[arr[i]][title] = []
            for el in l:
                ans[arr[i]][title].append(el)
            i += 1
    return ans

def adjective_prop(soup):
    type1 = soup.find_all("p")
    ans = set()
    for el in type1:
        try:
            t = el.text
            start = t.find(" Сравнительная степень — ")
            if start == -1:
                continue
            forms = list(t[start + len(" Сравнительная степень — "):-1].split(", "))
            for el in forms:
                ans.add(normalize(el))
        except:
            pass
    if ans != []:
        return ans
    #print("XMLParser свойства прилагательного не найдены")
    return []     

def normalize2(string): # для парсинга будущего времени
    l = list(string.split())
    main_word = normalize(l[-1])
    spec = list(l[0][:-1].split("/"))
    ans = []
    for el in spec:
        ans.append([el, main_word])
    return ans

def verb_changing(soup):
    param = {"style": "float:right; clear:right; padding:3; margin-left:0.5em; margin-bottom:0.5em; border: 1px solid #6699CC; border-collapse:collapse;", "cellpadding": "2", "rules":"all"}
    table = soup.find("table", param)
    #print(table)
    ans = {"гл.": {"н. вр.": dict(), "пр. вр.": dict(), "б. вр.": dict(), "повелит.": dict()}, "прич.": dict(), "деепр.": dict()}
    if not table:
        return
    rows = table.find_all("tr")
    types = []
    cols = rows[0].find_all("th")[1:]
    for el in cols:
        types.append(LG.terms[el.find("a").get("title")])
    for row in rows[1:7]:
        cols = row.find_all("td")
        title = cols[0].find("a").get("title")
        i = 0
        for el in cols[1:]:
            ans["гл."][types[i]][title] = normalize(el.text)
            i += 1
    for row in rows[7:]:
        cols = row.find_all("td")
        title = cols[0].find("a").get("title")
        if title.find("деепр") != -1: #деепричастие
            if title in LG.terms:
                title = LG.terms[title]
            else:
                print("Add to terms in LogicGroups", title)            
            ans["деепр."][title] = normalize(cols[1].find("a").text)
        else: # причастие и будущее
            if title in LG.terms:
                title = LG.terms[title]
            else:
                print("Add to terms in LogicGroups", title)
            try:
                ans["прич."][title] = normalize(cols[1].find("a").text)
            except:
                ans["гл."][title] = normalize2(cols[1].text)
    return ans

def verb_prop(soup):
    p = soup.find_all("p")
    ans = set()
    for el in p:
        a = el.find_all("a")
        if len(a) < 3:
            continue
        if a[0].text != "Глагол":
            continue
        for prop in a[1:]:
            if prop.text in LG.terms:
                ans.add(LG.terms[prop.text])
        return ans
    return set()
    
def adverb_prop(soup):
    p = soup.find_all('p')
    
    for el in p:
        if el.find("a", {"title": "наречие"}) == None:
            continue
        ans = set()
        a = el.find_all("a")[1:]
        s = el.text
        #print(s)
        ad = []
        l = list(s.split(". "))
        if len(l) >= 2:
            props, forms = l[0], l[1]
            forms = list(forms[forms.find(" — ") + 3:-1].split(", "))
            for el1 in forms:
                ad.append(normalize(el1))
        else:
            props = l[0]
        for el1 in LG.terms:
            if props.find(el1) != -1:
                ans.add(LG.terms[el1])
        return [ans, ad]
    return [set(), []]