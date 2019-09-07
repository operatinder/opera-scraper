import requests
from bs4 import BeautifulSoup
import csv
import sys

source = sys.argv[1]
exportFile = sys.argv[2]

print(source)

r = requests.get(source)

soup = BeautifulSoup(r.text, 'lxml')

table = soup.find("div", {"id": "table_div"})

scenes = table.findChildren("div" , recursive=False)

export_file = open(exportFile, mode='w',encoding="UTF-8",newline='')
export_writer = csv.writer(export_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

for scene in scenes:
    scene_id = scene.find("span",{"class":"s_id"}).contents[0]
    scene_title = scene.find("span",{"class":"s_title"}).find("a").contents[0]
    scene_opera = scene.find("span",{"class":"s_opera"}).contents[1]
    scene_composer = scene.find("span",{"class":"s_composer"}).contents[1]
    scene_act = scene.find("span",{"class":"s_act"}).contents[1]
    scene_type = scene.find("span",{"class":"s_type"}).contents[1]
    scene_voice = ''
    if len(scene.find("span",{"class":"s_voice"}).contents) > 1:
        scene_voice = scene.find("span",{"class":"s_voice"}).contents[1]
    scene_lang = scene.find("span",{"class":"s_lang"}).contents[1]
    scene_role = ''
    rolesTag = scene.find("span",{"class":"s_role"}).findAll("span")
    for role in rolesTag:
        if role.contents[0] != "Roles: ":
         scene_role += role.contents[0]
         if rolesTag.index(role) != len(rolesTag)-1:
            scene_role += "/"
    export_writer.writerow([scene_id, scene_title, scene_opera,scene_composer,scene_composer,scene_act,scene_type,scene_voice,scene_role])

export_file.close()