import numpy as np
from skimage.draw import polygon

import parser

label_registry = {
    'paragraph': 2,
    'marginalia': 3,
    'caption': 4,
    'graphic': 5}


def label_image(file_name):
    xml_file_name = file_name.split('.')[0] + '.xml'
    image_info, text_region_data = parser.load_xml_as_dict(xml_file_name)
    im_height = int(image_info['imageHeight'])
    im_width = int(image_info['imageWidth'])
    labels = np.ones((im_height, im_width), dtype=np.uint8)
    for text_region in text_region_data:
        points = text_region['points']
        region_type = text_region['type']
        rr, cc = polygon(points[:, 1], points[:, 0])
        labels[rr, cc] = label_registry.get(region_type, 6)
    return labels
