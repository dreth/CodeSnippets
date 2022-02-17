import json
import os

# check json files in current folder and only keep those of length 7, so an ISO alpha-2 language code like 'es' plu '.json' 
if len(os.listdir()) == 0:
    exit()
elif len(os.listdir()) == 1 and 'json' in os.listdir()[0] and len(os.listdir()[0])==7:
    translation_json = os.listdir()[0]
else:
    translation_json = [x for x in os.listdir() if 'json' in x and len(x)==7][0]

# keep filename
json_filename = translation_json

# load json
with open(translation_json) as f:
    translation_json = json.load(f)

# items with elements important to the UI should be translated manually in the json file
items_requiring_manual_json_manipulation = ['\n','{','}','<','>', '…']

# gather missed keys 
missed_translations_due_to_UI_elements = []

# items to re-check even if confirmed
items_to_recheck = []

# detect translation language
def detect_translation_language(d):
    for k,v in d.items():
        if isinstance(v, dict):
            if "en" in list(v.values())[0].keys():
                return [x for x in list(v.values())[0].keys() if x != "en"][0]
            else:
                detect_translation_language(v, translation_language)
        else:
            continue

# detect translation language var
translation_language = detect_translation_language(d=translation_json)

# walk the json recursively
def translate(d):

    # loop over k,v pairs
    for k,v in d.items():
        
        # if it's a dict check if the key 'en' is present, otherwise continue
        if isinstance(v, dict):

            # if the 'en' key is present, continue
            if "en" in v.keys():

                # avoid trying to translate items that require manual manipulation
                skip = False
                for item in items_requiring_manual_json_manipulation:
                    if item in v['en']:
                        
                        # save items that require manual manipulation and skip
                        missed_translations_due_to_UI_elements.append(k)
                        skip=True
                
                if skip == False:
                    # ask for translation
                    if v[translation_language] != "":
                        print(f"\n{'Original English text:':<22} {v['en']:>15}")
                        print(f"{'Current translation:':<22} {v[translation_language]:>16}\n")
                        while True:
                            correct = input(f"{'Is this correct? (y/y*/n):':<15} ")
                            if correct in ['y','Y','']:
                                break
                            elif correct in ['y*','Y*']:
                                items_to_recheck.append(k)
                                break
                            elif correct in ['n','N']:
                                v[translation_language] = input(f"\n{'New translation:':<15} {'':>8}")
                                break
                            else:
                                continue
                    
                    # if translation not present, ask for translation
                    else:
                        while True:
                            print(f"\n{'Original English text:':<15} {v['en']:>18}")
                            v[translation_language] = input(f"{'Translation:':<15} {'':>12}")
                            print(f"\nYou wrote: {v[translation_language]}\n")
                            correct = input(f"{'Is this correct? (y/y*/n):':<15} ")
                            if correct in ['y','Y','']:
                                break
                            elif correct in ['y*','Y*']:
                                items_to_recheck.append(k)
                                break
                            elif correct in ['n','N']:
                                continue
                else:
                    v[translation_language] = "MISSING TRANSLATION"
            
            # continue traversing the dict recursively
            else:
                translate(v)
    
    return (d,missed_translations_due_to_UI_elements,items_to_recheck)

# run the function
translation_json, missed_translations_due_to_UI_elements, items_to_recheck = translate(translation_json)

# dump json to file
with open(json_filename, 'w') as f:
    json.dump(translation_json, f, ensure_ascii=False, indent='	')

# save missed ui elements
with open('missed','a') as f:
    for item in missed_translations_due_to_UI_elements: 
        f.write(f'{item}\n')

# save items to re-check
with open('recheck','a') as f:
    for item in items_to_recheck:
        f.write(f'{item}\n')
