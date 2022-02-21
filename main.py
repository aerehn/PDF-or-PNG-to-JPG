from PIL import Image
import os
import cv2
from pdf2image import convert_from_path
import pandas as pd
cwd = os.getcwd()

print(cwd)

files = os.listdir()
print(files)
name_conversion_table=pd.read_excel(cwd+"/export_grid.xlsx")
print(name_conversion_table)
old_names=list(name_conversion_table["vanhatilausnumero"])
new_names=list(name_conversion_table["sku"])
target_path = cwd + "/target"
source_path = cwd + "/source"
source_files = os.listdir(source_path)
print(source_files)




def turn_to_jpg(source_path,target_path):
    png_images = [file for file in os.listdir(source_path) if file.endswith('.png')]
    pdf_files = [file for file in os.listdir(source_path) if file.endswith('.pdf')]
    
    for file in png_images:
        image = cv2.imread(source_path+"/"+file, cv2.IMREAD_UNCHANGED)    

        #make mask of where the transparent bits are
        trans_mask = image[:,:,3] == 0

        #replace areas of transparency with white and not transparent
        image[trans_mask] = [255, 255, 255, 255]

        #new image without alpha channel...
        new_img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        #new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(target_path+"/"+file[:-3]+"jpg", new_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        #cv2.imwrite(target_path+"/"+file[:-3]+"jpg", new_img)

        index_of_new_name = old_names.index(file[:-4]) if file[:-4] in old_names else None
        if index_of_new_name != None:
            new_name=new_names[index_of_new_name]
            cv2.imwrite(target_path+"/"+new_name+".jpg", new_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        else:
            cv2.imwrite(target_path+"/"+file[:-4]+".jpg", new_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    for file in pdf_files:
        images = convert_from_path(source_path+"/"+file)
        
        index_of_new_name = old_names.index(file[:-4]) if file[:-4] in old_names else None
        if index_of_new_name != None:
            new_name=new_names[index_of_new_name]
            print(new_name)
            # Save pages as images in the pdf
            images[0].save(target_path+"/"+new_name+".jpg", 'JPEG')
        else:
            print(file[:-4])
            images[0].save(target_path+"/"+file[:-4]+".jpg", 'JPEG')

    files = os.listdir(source_path)
    subdirectories = []
    target_directories = []
    for item in files:
        #Filter for subdirectories
        if os.path.isdir(source_path+"/"+item):
            #print(item)
            subdirectories.append(source_path+"/"+item)
            target_directories.append(target_path+"/"+item)
            os.mkdir(target_path+"/"+item)
    print(subdirectories)
    if(len(subdirectories)>0):
        for s,t in zip(subdirectories,target_directories):
            turn_to_jpg(s,t)


turn_to_jpg(source_path,target_path)