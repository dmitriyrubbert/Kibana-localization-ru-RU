#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re, json, os, time
from googletrans import Translator

template = {  "messages": {
# 1: "Spaces, commas, and the characters {characterList} are not allowed.",
2: "Change the \"xpack.rollup.enabled\" setting to \"xpack.rollup.ui.enabled\".",
3: "Delete \"{name}\" tag to \"{name2}\" ",
# 4: "You are about to delete {isSingleSelection, plural, one {this job} other {these jobs}}",
# 5: "Enable the creation of index patterns which capture rollup indices,\n              which in turn enable visualizations based on rollup data.",
# 6: "{count, plural, one {1 saved object} other {# saved objects}}",
7: "\"xpack.security.authc.providers.saml.<provider-name>.maxRedirectURLSize\" has no effect",
# 8: "{isLoading, select, true{Activating {count, plural, one{user} other{users}}…} other{Activate {count, plural, one{user} other{users}}}}",
9: "\"To\" email address is required.",
10: "Determines how many terms will be visualized when clicking the \"visualize\" button, in the field drop downs, in the discover sidebar.",
} }

variables = {}
data = {}
source_language = 'en'
openfile = 'en_integreted.json' # исходный файл локализации
savefile = 'ru-RU.json' # получаемый файл русской локализации

def replace_var(matchobj):
    key = len(variables)+10000
    variables[key] = matchobj.group(0)
    return str(key)

def translate(text):
    translator = Translator()
    try:
        result = translator.translate(text, src=source_language, dest='ru').text
    except Exception as e:
        print(f"translator error: {text}")
        time.sleep(3600)
        result = translator.translate(text, src=source_language, dest='ru').text
    return result

def open_json(openfile):
    position = ''
    if os.path.exists('.lock'):
        print('Restore position from file')
        os.system(f'cp {savefile} {savefile}.bak')
        openfile = savefile
        with open('.lock', 'r', encoding='utf-8') as lockfile:
            position = json.load(lockfile)
    # print(f'open {openfile}')
    with open(openfile, 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    return data, position

def save_json(dictionary, savefile, position):
    with open(savefile, 'w', encoding='utf-8') as file:
        json.dump(dictionary, file, indent=4, ensure_ascii=False)
    # save position
    with open('.lock', 'w', encoding='utf-8') as lockfile:
        json.dump(position, lockfile, indent=4, ensure_ascii=False)

def replace_and_translate(eng_string):
    type = ''

    if re.search( '\\"{([^}\\"]+)}\\"' , eng_string) != None:
        type = '\"\{ var\"\}'
        string = re.sub('\\"{([^}\\"]+)}\\"', replace_var, eng_string)
        string = translate(string)

    # elif re.search( '{([^}]+)}' , eng_string) != None:
    elif re.search( '{(.+)}' , eng_string) != None:
        type = '{var}'
        string = re.sub('{([^}]+)}', replace_var, eng_string)
        string = translate(string)

    elif re.search( '\\"([^\\"]+)\\"' , eng_string) != None:
        type = '\\\"var\\\"'
        string = re.sub('\\"([^\\"]+)\\"', replace_var, eng_string)
        string = translate(string)

    else:
        string = translate(eng_string)

    for key in variables: string = string.replace(str(key),f'{variables[key]}')
    print( f"Type'{type}': '{eng_string}' => '{string}'" )

    if string != None:
        return string
    return ''


en_json_file, position = open_json(openfile)
# en_json_file, position = template, 2
start_translation = False
x=0
for key in en_json_file["messages"]:

    if key == position:
        start_translation = True
    elif position == '':
        start_translation = True
        for key in en_json_file["messages"]:
            position = key
            break

    if start_translation:

        # save in file
        x+=1
        if x == 5:
            save_json(en_json_file, savefile, key)
            x=0

        # translate
        eng_string = en_json_file["messages"][key]
        ru_string = replace_and_translate(eng_string)

        # replace sentences in original dict
        en_json_file["messages"][key] = ru_string

print('Complete')
if os.path.exists('.lock'):
    os.remove('.lock')
