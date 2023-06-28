from PIL import Image
import os
import json
import random

cur_dir = os.getcwd()
if 'layers' not in os.listdir(cur_dir):
    print(f"layers directory does not exist in {cur_dir}")
    exit()

layers_dir = cur_dir + os.sep + 'layers'
components = os.listdir(layers_dir)
for component in components:
    component_dir = layers_dir + os.sep + component
    if not os.path.isfile(component_dir + os.sep + 'info.json'):
        print(f"info.json does not exist in {component_dir}")
        exit()

    file = open(component_dir + os.sep + 'info.json')
    info = json.load(file)
    file.close()

    color = tuple([random.randint(0, 256) for x in range(3)])  # todo change this to a background image
    image = Image.new("RGBA", (256, 256), color=color)
    index = 0
    for key in info:
        value = info[key]
        image_data = {"attributes": []}
        for chosen_value in range(1, value+1):
            index += 1
            element = f"{key}_{chosen_value}.png"
            foreground_picture = Image.open(component_dir + os.sep + element)

            if not os.path.isfile(component_dir + os.sep + f"{key}_{chosen_value}.json"):
                print(f"{key}_{chosen_value}.json does not exist in {component_dir}")
                exit()
            file = open(component_dir + os.sep + f"{key}_{chosen_value}.json")
            traits = json.load(file)
            file.close()

            image.paste(foreground_picture, (0, 0), foreground_picture)
            image_data["attributes"].append(traits.update({key: chosen_value}))

            save_path = cur_dir + os.sep + "results"
            if not os.path.exists(save_path):
                os.mkdir(save_path)

            save_path += os.sep + component

            if not os.path.exists(save_path):
                os.mkdir(save_path)

            image.save(save_path + os.sep + f"{component}_{index}.png", format="png")

            image_data['name'] = f"{component}_{index}"
            image_data["ipfs_url"] = "ipfs://IMAGE_CID"
            with open(save_path + os.sep + f"{component}_{index}_data.json", "w") as outfile:
                outfile.write(json.dumps(image_data))

print("done")
exit()
