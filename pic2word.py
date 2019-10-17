# encoding: utf-8
from flask import Flask, request, redirect, render_template, Markup,jsonify,send_from_directory
from flask import Blueprint
from common_func import *
import os
from pdf2image import convert_from_path,convert_from_bytes
import pytesseract
import sys
from PIL import Image
import uuid
reload(sys)
sys.setdefaultencoding('utf8')

pic2word_view = Blueprint('pic2word', __name__)
app=Flask(__name__)
logger = logging.getLogger('pic2word')
logger.setLevel(logging.DEBUG)
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('/pic2word.log')
fh.setLevel(logging.DEBUG)
# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])  # 允许上传的文件后缀
OUT_FOLDER = 'out_text'
file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
out_path = os.path.join(basedir, OUT_FOLDER)

def pdf2text(in_filepath,out_filepath):
    pdf_images = convert_from_path(in_filepath)
    # filename=str(int(time.time()))+'.txt'
    # outtext_path=os.path.join(out_path,filename)
    for image in pdf_images:
        text =pytesseract.image_to_string(image,lang='chi_sim')
        with open(out_filepath,'a') as f:
            f.write(text)

def img2text(in_filepath,out_filepath):
    filename = str(int(time.time())) + '.txt'
    # outtext_path = os.path.join(out_path, filename)
    image = Image.open(in_filepath)
    text = pytesseract.image_to_string(image, lang='chi_sim')
    with open(out_filepath, 'a') as f:
        f.write(text)


@pic2word_view.route('')
def hello_index():
    return render_template('upload.html')

@pic2word_view.route('/upload_file',methods=['GET','POST'])
def upload_file():
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f:  # 判断是否是允许上传的文件类型
        fname = f.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # 修改文件名
        in_filepath=os.path.join(file_dir, new_filename)
        out_filename=str(uuid.uuid1()).replace('-', '')+'.txt'
        out_filepath=os.path.join(out_path, out_filename)
        f.save(in_filepath)  # 保存文件到upload目录
        if file_type(fname)=="pdf":
            pdf2text(in_filepath,out_filepath)
        else:
            img2text(in_filepath,out_filepath)

        return jsonify({"out_filename": out_filename, "errmsg": "上传成功"})
        # return "转换成功"
    else:
        # return jsonify({"errno": 1001, "errmsg": "上传失败"})
        return "fail"
@pic2word_view.route('/download_file',methods=['GET','POST'])
def download_file():
    out_filename=request.args.get('out_filename')

    return send_from_directory(out_path,out_filename,as_attachment=True)

# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def file_type(filename):
    return filename.rsplit('.', 1)[1]
