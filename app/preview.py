import dearpygui.dearpygui as dpg
import filetype
from PIL import Image
import numpy as np

from app.settings import UserSettings


def preview_if_possible(path, context):
    pn : str = path.name
    if pn[pn.rfind('.')+1:].lower() in context.get_settings().text_formats:
        dpg.delete_item('file_preview_text')
        line_limit = context.get_settings().file_preview_text_line_limit
        contents = ''
        try:
            with open(path) as f:
                while line_limit > 0:
                    try:
                        line = f.readline()
                    except EOFError:
                        break
                    contents += line
                    line_limit -= 1
                if line_limit == 0:
                    contents += '<...>'
        except:
            dpg.add_text("Unable to load text file")
            return
        dpg.add_text(contents, label='file_preview_text')
    elif filetype.is_image(str(path)):
        dpg.delete_item('file_preview_texture')
        
        try:
            image = Image.open(path)
            image = image.convert('RGBA')
        except:
            dpg.add_text("Unable to load image file")
            return
        w, h = image.size
        k = 360 / h
        w = int(w * k)
        h = int(h * k)

        image = image.resize((w, h))

        image_data = np.asarray(image) / 255
        height, width, channels = image_data.shape
        

        with dpg.texture_registry():
            dpg.add_static_texture(width=width, height=height, default_value=image_data.flatten(), tag="file_preview_texture")
        dpg.add_image("file_preview_texture")
    elif filetype.is_audio(str(path)):
        dpg.delete_item('file_preview_audio_start')
        dpg.delete_item('file_preview_audio_stop')
        
        context.open_audio_player(path)

        def start_callback():
            context.get_audio_player().play()
        def stop_callback():
            context.get_audio_player().stop()
        
        dpg.add_button(label="Play audio file", callback=start_callback, id='file_preview_audio_start')
        dpg.add_button(label="Stop audio file", callback=stop_callback, id='file_preview_audio_stop')
        