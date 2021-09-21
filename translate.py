import re
import uuid
import time

from deep_translator import GoogleTranslator

source_lang_code = 'en'
target_lang_codes = ['nl', 'fr', 'de', 'pl', 'es']
regex = '<(“[^”]*”|\'[^’]*’|[^\'”>])*>'

with open('source') as source:
    body = source.read()


def translate():
    result = open("result_" + time.strftime("%c") + ".txt", "w")

    print(source_lang_code)
    print(body)
    result.write("\n" + source_lang_code + "\n")
    result.write(body + "\n\n")

    pattern = re.compile(regex)
    htmlTags = pattern.finditer(body)

    for target_lang_code in target_lang_codes:

        translator = GoogleTranslator(source=source_lang_code, target=target_lang_code)

        replaceDictionary = dict()
        index = 0

        for tag in htmlTags:
            if tag.group() not in replaceDictionary.values():
                index += 1
                replaceDictionary[uuid.uuid4().hex[:6].upper()] = tag.group()

        newBody = body

        # remove html
        for key, value in replaceDictionary.items():
            newBody = newBody.replace(value, key)

        newTranslation = translator.translate(newBody)

        # re-add html
        for key, value in replaceDictionary.items():
            newTranslation = newTranslation.replace(key, value)

        translated_body = newTranslation

        print(target_lang_code)
        print(translated_body)

        result.write(target_lang_code + "\n")
        result.write(translated_body + "\n\n")


translate()

