from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QLineEdit, QInputDialog, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter
import os


app = QApplication([])
main_win = QWidget()
main_win.resize(700, 500)
main_win.setWindowTitle("Easy Editor")

picture = QLabel("картинка")

w_list = QListWidget()

folder_btn = QPushButton("Папка")
left_btn = QPushButton("Ліворуч")
right_btn = QPushButton("Праворуч")
mirror_btn = QPushButton("Дзеркало")
blure_btn = QPushButton("Різкість")
colour_btn = QPushButton("Ч/Б")

v_line_1 = QVBoxLayout()
v_line_2 = QVBoxLayout()
h_line_1 = QHBoxLayout()
h_line_2 = QHBoxLayout()

v_line_1.addWidget(folder_btn)
v_line_1.addWidget(w_list)

h_line_1.addWidget(left_btn)
h_line_1.addWidget(right_btn)
h_line_1.addWidget(mirror_btn)
h_line_1.addWidget(blure_btn)
h_line_1.addWidget(colour_btn)

v_line_2.addWidget(picture)
v_line_2.addLayout(h_line_1)

h_line_2.addLayout(v_line_1)
h_line_2.addLayout(v_line_2)

main_win.setLayout(h_line_2)


workdir = ""

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(filenames, extensions):
    result = []
    for file in filenames:
        for ext in extensions:
            if file.endswith(ext):
                result.append(file)
    return result

def showFilenameList():
    extensions = ["jpg", "jpeg", "png", "gif", "bmp"]
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    w_list.clear()
    for file in filenames:
        w_list.addItem(file)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.workdir = None
        self.savedir = "Modified/"

    def loadImage(self, filename):
        self.filename = filename 
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)
    
    def saveImage(self):
        path = os.path.join(workdir, self.savedir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        picture.hide()
        pixmapimage = QPixmap(path)
        w, h = picture.width(), picture.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        picture.setPixmap(pixmapimage)
        picture.show()
    
workimage = ImageProcessor()

def showChosenImage():
    if w_list.currentRow() > 0:
        filename = w_list.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)




w_list.currentRowChanged.connect(showChosenImage)
left_btn.clicked.connect(workimage.do_left)
right_btn.clicked.connect(workimage.do_right)
blure_btn.clicked.connect(workimage.do_sharpen)
mirror_btn.clicked.connect(workimage.do_flip)
colour_btn.clicked.connect(workimage.do_bw)
folder_btn.clicked.connect(showFilenameList)












main_win.show()
app.exec_()