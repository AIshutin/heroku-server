# -*- coding: utf-8 -*- 
import requests
import bs4
import XMLparser
import TextParser as TP
import LogicGroups as LG
import time
#¯\_(ツ)_/¯ 

def request_code(string):
    #print(string)
    return int(list(string[1:-1].split())[1][1:-1])

def get_standart(word): # возвращает инфинитив слова
    url = "http://search1.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&dpp=&spp=&spd=&text=lexform&mode=main&sort=gr_tagging&lang=ru&nodia=1&req="
    try:
        
        z = requests.get(url + word)
        if request_code(str(z)) != 200:
            return word    
        z = z.text
        soup = bs4.BeautifulSoup(z, "lxml")
        t = soup.find_all("br")
        s = "/download-xml.xml?env=alpha&amp;mycorp=&amp;mysent=&amp;mysize=&amp;mysentsize=&amp;mydocsize=&amp;text=lexform&amp;mode=main&amp;sort=gr_tagging&amp;lang=ru&"
        soup2 = list(list(str(soup).split("\n"))[-5].split(">"))
        ind = soup2.index("Леммы</span")
        soup2[:] = soup2[ind:]
        ind = soup2.index("<td") + 1
        need = soup2[ind][:-4]
        return need
    except:
        return word
    
def get_article(word): # get article from ru.wiktioary.org about word
    url = "https://ru.wiktionary.org/wiki/"
    z = requests.get(url + word)
    result = ""
    i = 0
    while i < 1:
        try:
            z = z.text
            first = z.find("<!-- Saved in parser cache with ")
            z = z[first + len("<!-- Saved in parser cache with "):]
            last = z.find("-->")
            z = z[:last]
            items = z.split(" and ")
            data = dict()
            for el in items:
                #print(el)
                pairs = list(el.split())
                data[" ".join(pairs[:-1])] = pairs[-1]
            #print("data = ", data)
            z = requests.get(url + word, data = data)
            resp = request_code(str(z))
            if resp == 404:
                break
            result = z.text
        except:
            break
        i += 1
    
    #print(result)
    return result

def get_info(word): #get info about word
    w = word
    word = ""
    for el in w:
        word = word + TP.make_lower(el)    
    text = get_article(word)
    if not text:
        #print("Word not found")
        return False
    soup =  bs4.BeautifulSoup(text, "lxml")
    q = XMLparser.define_type(soup)
    #исправить разные имена родов у сущ и прил
    #два файла: полностью известные, другие
    #
    
    if q == "существительное":  
        z = [word, q, XMLparser.noun_prop(soup), XMLparser.noun_changing(soup)]#сделать отмену у собственных
    elif q == "прилагательное":
        z = [word, q, XMLparser.adjective_prop(soup), XMLparser.adjective_changing(soup)]#, XMLparser.noun_changing(soup)
    elif q == "глагол":
        z = [word, q, XMLparser.verb_prop(soup), XMLparser.verb_changing(soup)]
    elif q == "наречие":
        z = [word, q, XMLparser.adverb_prop(soup)]
    else:
        return False
    if "собств." in z[2]:
        return     False
    return z
    #черт - чёрт
    
def webreq(word):
    prev = get_standart(word)
    z = get_info(prev)
    return z

if __name__ == "__main__":
        
    fin = open("input.txt", encoding = "utf-8")
    s = " ".join(fin.readlines()) + "#"
    prev = ""
    was = set()
    time.clock()
    i = 0
    for el in s:
        if el not in LG.alpha:
            try:
                if len(prev) < 3:
                    continue
                prev = get_standart(prev)
                if prev not in was:
                    z = get_info(prev)
                    was.add(prev)
                    if z:
                        print(prev, i)
                        fout = open("dictionary.txt", "a", encoding = "utf-8")
                        print(str(z).replace("set()", "{}").replace("None", "[]"), file = fout)
                        fout.close()
                        i += 1
            except:
                pass
            prev = ""
        else:
            prev = prev + TP.make_lower(el)
    fin.close()
    
    print(time.clock())
