import json
import os

def gernerate_name_config(outputpath, labellist):
    with open(outputpath, 'w', encoding='utf-8') as f:
        for i, line in enumerate(labellist):
            f.write("item {"+'\n')
            f.write('name: "'+line+'"\n')
            f.write("id: "+str(i)+'\n')
            f.write("}"+'\n')
        f.close()

def read_json_find_label(fullpath, labellist):
    jsObj = json.load(open(fullpath))
    for key in jsObj:
        if "shapes" in jsObj:
            shapes = jsObj["shapes"]
            for key in shapes:
                if key["label"]:
                    if key["label"] in labellist:
                        continue
                    else:
                        labellist.append(key["label"])

def label_collector(filepath):
    labellist = []
    for root, dirs, files in os.walk(filepath):
        for name in files:
            if name.endswith(".json"):
                try:
                    full_output_path = os.path.join(root, os.path.basename(os.path.normpath(root)) + ".names")
                    full_file_path = os.path.join(root, name)
                    read_json_find_label(full_file_path, labellist)
                    gernerate_name_config(full_output_path, labellist)
                except:
                    print("Failed to load: ", full_file_path)


