from PIL import Image
import os


image_width=240  # Width for output image
image_height=240 # Height for output image
frame_name_list=[]
def create_default_file(output_folder,directory_new):
    """Creating file for display"""
    new_folder=f"{output_folder}\\{directory_new}"
    file_name=f"{new_folder}\\gif_frames.c"
    try:
        os.remove(file_name)
    except:
        print("File not present!")
    try:
      os.mkdir(new_folder)
    except FileExistsError:
        print("File name already present!")
    content=f'''#if defined(__AVR__)
#include <avr/pgmspace.h>
#elif defined(__PIC32MX__)
  #define PROGMEM
#elif defined(__arm__)
  #define PROGMEM
#endif\n\n\n'''
    try:
        with open(file_name, 'a') as file:
            file.write(content)
            file.close()
    except Exception as e:
        pass


def gif_to_jpg_sequence(input_path, output_folder,directory_new):
    """Converting the gif or short video into frames and resize"""
    
    new_folder=f"{output_folder}\\{directory_new}"
    gif_image = Image.open(input_path)
    for frame_number in range(gif_image.n_frames):
        gif_image.seek(frame_number)
        jpg_image = gif_image.convert("RGB")
        jpg_image = jpg_image.resize((image_width, image_height))
        file_save_name=f"{new_folder}/frame_{frame_number:03d}.jpg"
        jpg_image.save(file_save_name)
        frame_value=f"frame_{frame_number:03d}"
        frame_name_list.append(frame_value)
        rgb_to_binary(new_folder,file_save_name,frame_value)
    print(frame_name_list)
    create_frame_names(new_folder,frame_name_list)
    print(f"\nConversion completed successfully\n Data saved to {new_folder}.")


def image_hex_convertion(input_path, output_folder,directory_new):
    """Converting the image 
    """
    new_folder=f"{output_folder}\\{directory_new}"
    
    gif_image = Image.open(input_path)
    jpg_image = gif_image.convert("RGB")
    jpg_image = jpg_image.resize((image_width, image_height))
    file_save_name=f"{new_folder}/frame_1.jpg"
    jpg_image.save(file_save_name)
    frame_value="frame_1"
    frame_name_list.append(frame_value)
    rgb_to_binary(new_folder,file_save_name,frame_value)
    print(frame_name_list)
    create_frame_names(new_folder,frame_name_list)
    print(f"\nConversion completed successfully\n Data saved to {new_folder}.")

def rgb_to_binary(new_folder,file_save_name,frame_value):
    """Converting the image into RGB565 format"""
    img = Image.open(file_save_name)
    img = img.convert("RGB")
    img = img.resize((image_width, image_height))
    pixels = list(img.getdata())
    integer_pixel=''
    for pixel in pixels:
        r, g, b = pixel
        red5 = round(r / 255 * 31)
        green6 = round(g / 255 * 63)
        blue5 = round(b / 255 * 31)
        rgb565 = (red5 << 11) | (green6 << 5) | blue5
        integer_pixel+=(str(rgb565)+',')
        # print(rgb565,end=",")
    integer_pixel=integer_pixel[:-1]
    create_file(new_folder,integer_pixel,frame_value)
    print('\n',f'{frame_value} saved!')


def create_file(new_folder,integer_pixel,frame_value):
    """Creating .c file for arduino display """
    file_name=f"{new_folder}\\gif_frames.c"
    data="{" + str(integer_pixel) + "}"
    content=f'''const unsigned short {frame_value}[{image_width*image_height}] PROGMEM={data};\n\n\n'''
    try:
        with open(file_name, 'a') as file:
            file.write(content)
            file.close()
    except Exception as e:
        pass
    
    


def create_frame_names(new_folder,frame_name_list):
    """Assign frame name"""
    file_name=f"{new_folder}\\gif_frames.c"

    try:
        for frame in frame_name_list:
            content=f"tft.pushImage(0, 0, {image_width}, {image_height}, {frame})\n"
            with open(file_name, 'a') as file:
                file.write(content)
                file.close()
    except Exception as e:
        pass
input_path = "FILE_LOCATION_WITH_EXTENSION"
output_folder = "OUTPUT_FOLDER_NAME"
directory_new="DIRECTORY_NAME_FOR_OUTPUT_RESULT"
create_default_file(output_folder,directory_new)
gif_to_jpg_sequence(input_path, output_folder,directory_new)  # Uncomment if you want to convert gif into RGB565 format
# image_hex_convertion(input_path, output_folder,directory_new) # Uncomment if you want to convert image into RGB565 format


