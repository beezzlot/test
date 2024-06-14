from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

comments_file = 'comments.xml'

def create_comments_xml():
    root = ET.Element('comments')
    tree = ET.ElementTree(root)
    tree.write(comments_file)

if not os.path.exists(comments_file):
    create_comments_xml()

def save_comment_to_xml(name, text):
    tree = ET.parse(comments_file)
    root = tree.getroot()
    comment = ET.SubElement(root, 'comment')
    ET.SubElement(comment, 'name').text = name
    ET.SubElement(comment, 'text').text = text
    tree.write(comments_file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        save_comment_to_xml(name, comment)
    
    tree = ET.parse(comments_file)
    root = tree.getroot()
    comments = []
    for comment in root.findall('comment'):
        name = comment.find('name').text
        text = comment.find('text').text
        comments.append({'name': name, 'text': text})
    
    return render_template('index.html', comments=comments)

@app.route('/rss')
def rss_feed():
    return ET.tostring(ET.parse(comments_file).getroot(), encoding='unicode')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
