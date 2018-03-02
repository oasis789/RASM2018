import os
import xml.etree.ElementTree as ET
import numpy as np
from skimage.io import imread

SCHEMA = '{http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15}'
PATH_TO_TRAINING_DATA = '/Users/uwaisiqbal/Desktop/RASM_Project/Training_Data/'


def parse_coords(points):
    return np.array([tuple(int(p) for p in point.split(','))
                     for point in points.split()])


def load_xml_as_dict(file_name, path_to_file=PATH_TO_TRAINING_DATA):
    tree = ET.parse(os.path.join(path_to_file, file_name))
    root = tree.getroot()
    metadata = root.find(f'{SCHEMA}Metadata')
    page = root.find(f'{SCHEMA}Page')
    image_info = page.attrib
    text_region_data = []
    for text_region in page:
        text_region_id = text_region.attrib.get('id')
        text_region_type = text_region.attrib.get('type', 'graphic')
        text_region_coords = text_region.find(f'{SCHEMA}Coords').attrib.get('points')
        text_line_list = text_region.findall(f'{SCHEMA}TextLine')
        text_line_data = []
        for text_line in text_line_list:
            text_line_id = text_line.attrib['id']
            text_line_coords = text_line.find(f'{SCHEMA}Coords').attrib.get('points')
            text_line_text = text_line.find(f'{SCHEMA}TextEquiv')[0].text
            text_line_data.append({
                'id': text_line_id,
                'points': parse_coords(text_line_coords),
                'text': text_line_text
            })

        text_region_data.append({
            'id': text_region_id,
            'type': text_region_type,
            'points': parse_coords(text_region_coords),
            'lines': text_line_data
        })
    return image_info, text_region_data


def load_image(file_name):
    return imread(os.path.join(PATH_TO_TRAINING_DATA, file_name))


def load_all_images(ext='.tif'):
    file_list = os.listdir(PATH_TO_TRAINING_DATA)
    file_list = [f for f in file_list if f.endswith(ext)]
    return {f: load_image(os.path.join(PATH_TO_TRAINING_DATA, f))
              for f in file_list}

