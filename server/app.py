from flask import Flask, request, jsonify, render_template
# import moondream as md
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from transformers import AutoModelForCausalLM
import torch 
import os 
import json

app = Flask(__name__)

# model = md.vl(api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiIxODZjZjY2Ny0zNDllLTQ3MzktYjFhNy00YjA0NzU2M2MxNDQiLCJvcmdfaWQiOiJaWjlRakVoeXdjaTRldVpGOUhOOEhUeHJlNmFxVTFRTCIsImlhdCI6MTc1ODY3OTIxNCwidmVyIjoxfQ.M8dIwLg8VGKb1UnZX9y7cO6TY1ZEU7yhq4LKGO-_igU")
model = AutoModelForCausalLM.from_pretrained("vikhyatk/moondream2",
                                          trust_remote_code=True,
                                          device_map="cuda",
                                          dtype=torch.float16,
                                          revision="main")
# print("CUDA available:", torch.cuda.is_available())


# print("CUDA device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None")
imgs_path = r"C:\Users\abdul\Desktop\work\00_UE-work\moondream-test\server\INPUT"
sorted_imgs = sorted(os.listdir(imgs_path))


SAVE_PATH = r"C:\Users\abdul\Desktop\work\00_UE-work\moondream-test\server\SAVE_PATH/"

# You can add multiple objects to detect by passing a list of object names.
# objects_to_detect = ["car", "pothole", "street light and pole", "motocycles", "buildings", "road matking", "buidking signs"]  # Add more objects as needed
objects_to_detect = ["car", "pothole", "street light and pole",]  # Add more objects as needed

# the main function 

def detect_objects(model, sorted_imgs, objects_to_detect, SAVE_PATH):
 
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

    return ("Detection completed and results saved.")




@app.route("/", methods=["GET", "POST"]) 
def index():
    if request.method == "POST":
        try:
            # Call the object detection function when button is clicked
            result = detect_objects(model, sorted_imgs, objects_to_detect, SAVE_PATH)
            return render_template("index.html", message=f"Object detection completed successfully!  { result }", success=True)
        except Exception as e:
            # Handle any errors that might occur
            return render_template("index.html", message=f"Error occurred: {str(e)}", success=False)
    
    # Initial page load
    return render_template("index.html", message="Click the button to start object detection")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)




