import json
  
# Opening JSON file

model_file = open("/Users/marsk757/topic2themes/topics2themes/data_folder/demokrati/topics2themes_exports_folder_created_by_system/60dc905c75dee5d0a5438d89_model.json")
model_data = json.load(model_file)

name_file = open("/Users/marsk757/topic2themes/topics2themes/data_folder/demokrati/topics2themes_exports_folder_created_by_system/60dc905c75dee5d0a5438d89_topic_name.json")
name_data = json.load(name_file)

name_dict = {}
for el in name_data:
    name_dict[int(el["topic_id"])] = el["topic_name"]
    
document_info = {}
for nr, topic in enumerate(model_data["topic_model_output"]["topics"]):
    
    description = "-"
    if topic["id"] in name_dict:
        description = name_dict[topic["id"]]

    topic_terms = [t["term"] for t in topic["topic_terms"]]
    terms_to_write = []
    for t in topic_terms:
        list_this_term = []
        sp = t.split(" / ")
        sp.sort(key=lambda s: len(s))
        for dt in sp:
            already_added = False
            for i, previous_term in enumerate(list_this_term[:]):
                #print(dt, previous_term)
                if dt.find(previous_term.replace("*", "")) != -1:
                    already_added = True
                    list_this_term[i] = list_this_term[i].replace("*", "") + "*"
            if not already_added:
                list_this_term.append(dt)
        terms_to_write.append("/".join(list_this_term))
    output = "{\\bf " + str(nr + 1) + ": " +  description + "} \\newline " + ", ".join(terms_to_write) + "\\newline"
    output = output.replace("_", " ")
    print(output)
