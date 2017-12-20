﻿*EDU BOT*

0. Что это?
Это телеграмм-бот, умеющий выводить грамм. информацию о слове.

1. Что умеет делать этот бот?
При поступлении запроса пользователю телеграмма @aishutin_edu_bot в формате: \<слово>, где \<слово> - это слово, выводит информацию о нем в markdown в следующем формате:

\<инфинитив>
Часть речи: \<тип>
Характеристики: \<грамм>
Формы: \<формы>

Где \<инфинитив> - инфинитив слова.
Где \<тип> - часть речи слова. Возможные ответы:
	* существительное
	* прилагательное
	* глагол
Где \<грамм> - грамматические характеристики слова, зависящие от типа слова.
Где \<формы> - (возможно) многострочный текст, зависящий от части речи слова. Возможно отсутствует.
Возможные ответы: любые, похожие на следующие:
	* для существительных:
Ед. ч.:
    Им.: \<word>
    Р.: \<word>
    Д.: \<word>
    В.: \<word>
    Тв.: \<word>
    Пр.: \<word>
Ед. ч.:
    Им.: \<word>
    Р.: \<word>
    Д.: \<word>
    В.: \<word>
    Тв.: \<word>
    Пр.: \<word>

Где \<word> это строка следующего формата:
либо ""
лиюо "—"
либо \<word> + ", " + (\<word> с первого или со второго символа)
либо слово русского языка, написанное строчными русскими буквами и одной заглавной, к-я указывает на ударение о слове, и возможно символ(ы) ́ .  

	* для прилагательных
м. р.
    Им.: \<word>
    Рд.: \<word>
    Дт.: \<word>
    Вн.: \<word>
    Тв.: \<word>
    Пр.: \<word>
    Кр.: \<word>
ж. р.
    Им.: \<word>
    Рд.: \<word>
    Дт.: \<word>
    Вн.: \<word>
    Тв.: \<word>
    Пр.: \<word>
    Кр.: \<word>
ср. р.
    Им.: \<word>
    Рд.: \<word>
    Дт.: \<word>
    Вн.: \<word>
    Тв.: \<word>
    Пр.: \<word>
    Кр.: \<word>
мн. ч.
    Им.: \<word>
    Рд.: \<word>
    Дт.: \<word>
    Вн.: \<word>
    Тв.: \<word>
    Пр.: \<word>
    Кр.: \<word>

Где \<word> - строка такого же формата как \<word> у существительных

	* для глагола
гл.
    н. вр.
        я: \<word>
        ты: \<word>
        он: \<word>
        мы: \<word>
        вы: \<word>
        они: \<word>
    пр. вр.
        я: \<word>
        ты: \<word>
        он: \<word>
        мы: \<word>
        вы: \<word>
        они: \<word>
    б. вр.
        я: \<word>
        ты: \<word>
        он: \<word>
        мы: \<word>
        вы: \<word>
        они: \<word>
    повелит.
        я: \<word>
        ты: \<word>
        он: \<word>
        мы: \<word>
        вы: \<word>
        они: \<word>
прич.
    действ. дееприч.: \<word>
    страд. дееприч.: \<word>
деепр.
    деепр.: \<word>

