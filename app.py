from flask import Flask, render_template, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

comments_file = 'comments.xml'

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
    return render_template('index.html')

@app.route('/rss')
def rss_feed():
    return ET.tostring(ET.parse(comments_file).getroot(), encoding='unicode')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
