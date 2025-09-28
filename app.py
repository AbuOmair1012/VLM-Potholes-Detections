import moondream as md
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from transformers import AutoModelForCausalLM
import torch 
import os 
import json

# model = md.vl(api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiIxODZjZjY2Ny0zNDllLTQ3MzktYjFhNy00YjA0NzU2M2MxNDQiLCJvcmdfaWQiOiJaWjlRakVoeXdjaTRldVpGOUhOOEhUeHJlNmFxVTFRTCIsImlhdCI6MTc1ODY3OTIxNCwidmVyIjoxfQ.M8dIwLg8VGKb1UnZX9y7cO6TY1ZEU7yhq4LKGO-_igU")
model = AutoModelForCausalLM.from_pretrained("vikhyatk/moondream2",
                                          trust_remote_code=True,
                                          device_map="cuda",
                                          dtype=torch.float16,
                                          revision="main")


print("CUDA available:", torch.cuda.is_available())
# print("CUDA device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None")
imgs_path = r"C:\Users\abdul\Desktop\work\00_UE-work\moondream-test\INPUT"
sorted_imgs = sorted(os.listdir(imgs_path))

# imgs = [Image.open(os.path.join(imgs_path, img_name)) for img_name in sorted_imgs if img_name.lower().endswith(('.png', '.jpg', '.jpeg'))]
# img = Image.open(r"C:\Users\abdul\Desktop\work\00_UE-work\moondream-test\INPUT\GOPRO-20250325-011208-000016.jpg")

SAVE_PATH = r"C:\Users\abdul\Desktop\work\00_UE-work\moondream-test\SAVE_PATH/"
# caption = model.describe(img)["caption"]
# print("Generated Caption:", caption)

# answer = model.query("What is the pothole in the image?")["answer"]
# print("ANswer:", answer)

# for chunk in model.caption(img, stream=True)["caption"]:
#     print(chunk, end="", flush=True)


# You can add multiple objects to detect by passing a list of object names.
# objects_to_detect = ["car", "pothole", "street light and pole", "motocycles", "buildings", "road matking", "buidking signs"]  # Add more objects as needed
objects_to_detect = ["car", "pothole", "street light and pole",]  # Add more objects as needed

# ...existing code until the loop...

model_output_json = {}
for img_name in sorted_imgs:
    if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
        
    img = Image.open(os.path.join(imgs_path, img_name))
    model_output_json[img_name] = {}
    
    # Create figure once per image
    plt.figure(figsize=(8, 8))
    plt.imshow(img)
    ax = plt.gca()
    
    # Detect all objects for this image
    for obj_class in objects_to_detect:
        result = model.detect(img, object=obj_class)
        detections = result["objects"]
        model_output_json[img_name][obj_class] = detections
        
        # Plot detections for this class
        for detection in detections:
            x_min = detection["x_min"] * img.width
            y_min = detection["y_min"] * img.height
            x_max = detection["x_max"] * img.width
            y_max = detection["y_max"] * img.height
            
            width = x_max - x_min
            height = y_max - y_min
            
            rec = patches.Rectangle(
                (x_min, y_min), 
                width, 
                height, 
                linewidth=2, 
                edgecolor='r', 
                facecolor='none'
            )
            ax.add_patch(rec)
            plt.text(x_min, y_min, obj_class, color='white', fontsize=12, backgroundcolor='red')
    
    # Save annotated image and JSON for this image
    plt.axis('off')
    save_name = img_name.split('.')[0]
    plt.savefig(
        f"{SAVE_PATH}detection_{save_name}.jpg",
        bbox_inches='tight',
        pad_inches=0,
        dpi=300
    )
    plt.close()
    
    # Save JSON with all detections for this image
    with open(f"{SAVE_PATH}detection_{save_name}.json", "w") as f:
        json.dump(model_output_json[img_name], f, indent=4)





# model_output_json = {}
# for img_name in sorted_imgs: 
#     # Ensure we're only processing image files
#     # img = Image.open(os.path.join(imgs_path, img_name))
#     # print(img_name)
     
#     for objs in objects_to_detect:
#         img = Image.open(os.path.join(imgs_path, img_name))
#         result = model.detect(img, object=objs)
#         detection = result["objects"]
#         # print(f"Detection for {objs}: {detection}")
#         model_output_json["img_name"] = [img_name]
#         model_output_json[objs] = detection
        
#         # print(f"Detection for {img_name}: {model_output_json}")
    

#         # Visualize the detection results
#         plt.figure(figsize=(8, 8))
#         plt.imshow(img)
#         ax = plt.gca()

#     for obj in model_output_json:
#         # img_name_json = str(obj["img_name"][0])
#         # print(img_name_json)
#         # break
#         img_pltted = Image.open(os.path.join(imgs_path, obj["img_name"][0]))

#         for ob_name in model_output_json[obj]:
            
#             x_min = obj["x_min"] * img_pltted.width
#             y_min = obj["y_min"] * img_pltted.height
#             x_max = obj["x_max"] * img_pltted.width
#             y_max = obj["y_max"] * img_pltted.height

#             width = x_max - x_min
#             height = y_max - y_min

#             rec = patches.Rectangle((x_min, y_min), width, height, linewidth=2, edgecolor='r', facecolor='none')
#             # print(f"Object: {objs}, BBox: ({x_min}, {y_min}), ({x_max}, {y_max})")
                
#             ax.add_patch(rec)
#             plt.text(x_min, y_min, f"{obj}", color='white', fontsize=2, backgroundcolor='red')
#         plt.axis('off')
#         plt.savefig(
#             f"{SAVE_PATH}detection_{x_min}.jpg",
#             bbox_inches='tight',
#             pad_inches=0,
#             dpi=900)
#             # dpi=img.info.get('dpi', (img.width / plt.gcf().get_size_inches()[0]))
        
#         plt.close()
#         # print(f"the json output: {model_output_json}")
#         # break 
#         # with open(f"{SAVE_PATH}model_output_{obj["img_name"][0].split('.')[0]}.json", "w") as f: 
#         with open(f"{SAVE_PATH}model_output_{x_min}.json", "w") as f: 
#             json.dump(model_output_json, f, indent=4)
        
#         # if objs != "":
#         #     plt.savefig(f"{SAVE_PATH}detection_{objs}.jpg", bbox_inches='tight', pad_inches=0)
#         #     plt.close()
#         # else: 
#         #     plt.savefig(f"{SAVE_PATH}No_detections.jpg", bbox_inches='tight', pad_inches=0)
#         #     plt.close()
        
