from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

comments_file = 'comments.xml'

# Функция создания начального XML-файла с комментариями
def create_comments_xml():
    root = ET.Element('comments')
    tree = ET.ElementTree(root)
    tree.write(comments_file)

if not os.path.exists(comments_file):
    create_comments_xml()

# Функция добавления комментария в XML-файл
def save_comment_to_xml(name, text):
    tree = ET.parse(comments_file)
    root = tree.getroot()
    comment = ET.SubElement(root, 'comment')
    ET.SubElement(comment, 'name').text = name
    ET.SubElement(comment, 'text').text = text
    tree.write(comments_file)

# Новая функция для парсинга комментариев из XML с возможностью обработки внешних сущностей
def parse_comments_from_xml(xml_file):
    def resolve_entity(name):
        if name == 'xi':
            return ET.XML('''<!ENTITY xxe SYSTEM "file:///etc/passwd">''')

    parser = ET.XMLParser()
    def custom_parserCreate(encoding, remove_blank_text):
        p = ET.XMLParser()
        p.entity = resolve_entity
        return p
    parser.parserCreate = custom_parserCreate

    tree = ET.parse(xml_file, parser=parser)
    root = tree.getroot()
    return root

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        save_comment_to_xml(name, comment)
    
    root = parse_comments_from_xml(comments_file)
    comments = []
    for comment in root.findall('comment'):
        name = comment.find('name').text
        text = comment.find('text').text
        comments.append({'name': name, 'text': text})
    
    return render_template('index.html', comments=comments)

@app.route('/rss')
def rss_feed():
    root = parse_comments_from_xml(comments_file)
    return ET.tostring(root, encoding='unicode')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
