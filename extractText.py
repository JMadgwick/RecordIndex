import sys
import os

def detect_text(path):
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    textforfile = '{}\n\n\n\n'.format(texts[0].description) + 'Language_Locale: {}'.format(texts[0].locale)

    f1 = open(path[:-3] + "txt", "w")
    f1.write(textforfile)
    f1.close()

    info = ""
    for text in texts:
        info+='\n{}'.format(text.description)
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        info+=' -  bounds: {}'.format(','.join(vertices))

    f2 = open(path[:-3]+ "info.txt", "w")
    f2.write(info)
    f2.close()

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

filetoconvert = os.getcwd() + '/' + sys.argv[1]
print(filetoconvert)
detect_text(filetoconvert)
