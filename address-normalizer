from pullenti_wrapper.langs import (
    set_langs,
    RU,
    EN
)
from pullenti_wrapper.referent import Referent
set_langs([RU])
from ipymarkup import show_span_ascii_markup as show_markup
from pullenti_wrapper.processor import (
    Processor,
    GEO,
    ADDRESS
)

result = Processor([ADDRESS, GEO])


def display_shortcuts(referent, level=0):
    tmp = {}
    a = ""
    b = ""
    for key in referent.__shortcuts__:
        value = getattr(referent, key)
        if value in (None, 0, -1):
            continue
        if isinstance(value, Referent):
            display_shortcuts(value, level + 1)
        else:
            if key == 'type':
                a = value
            if key == 'name':
                b = value
                # print('ok', value)
            if key == 'house':
                a = "дом"
                b = value
                tmp[a] = b
            if key == 'flat':
                a = "квартира"
                b = value
                # print('ok', value)
                tmp[a] = b
            if key == 'corpus':
                a = "корпус"
                b = value
                tmp[a] = b
        tmp[a] = b
        addr.append(tmp)


def process_display(line, analyzers):
    processor = Processor(analyzers)
    result = processor(line)
    spans = [_.span for _ in result.matches]
    show_markup(result.text, spans)

    assert len(result.matches) == 1
    referent = result.matches[0].referent
    display_shortcuts(referent)

lines = [
    'г. Москва ул Октябрьская д 105 кв 154',
    'г Москва ул Затонная д2 кв150',
    'г. Москва ул. Приображенский вал 14-66'
]

addr = []
for line in lines:
    process_display(line, [GEO, ADDRESS])

li = []
for i in addr:
  if i not in li:
    li.append(i)

print(li)
