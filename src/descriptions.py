from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtGui import QFont


def get_description_main_header(text):
    header = QLabel(text)
    font = QFont("Arial", 30)
    header.setFont(font)
    return header

def get_description_subheader(text):
    subheader = QLabel(text)
    subheader.setWordWrap(True)
    font = QFont("Arial", 20)
    subheader.setFont(font)
    return subheader

def get_description_segment(text_segment):
    description_segment = QLabel(text_segment)
    description_segment.setWordWrap(True)
    font = QFont("Arial", 13)
    description_segment.setFont(font)
    return description_segment


class MainDescritpionWidget(QLabel):

    header_text = "Welcome to DB Manager!"
    subheader_text = "A simple tool created to edit your database with ease."
    segment_2_text = "  DB Manager is a software tool designed " \
                    "to facilitate the management and manipulation of databases. It provides users with "\
                    "a graphical interface to interact with databases, enabling tasks such as adding, deleting, "\
                    "modifying, and querying data."
    segment_3_text = "  DB Manager supports importing/exporting .csv files."

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setFixedWidth(int(self.parent.width*0.9))
        self.setFixedHeight(int(self.parent.height*0.8))
        self.build_description()

    def build_description(self):
        desc_header = get_description_main_header(MainDescritpionWidget.header_text)
        self.layout.addWidget(desc_header)
        desc_segment_1 = get_description_subheader(MainDescritpionWidget.subheader_text)
        self.layout.addWidget(desc_segment_1)
        desc_segment_2 = get_description_segment(MainDescritpionWidget.segment_2_text)
        self.layout.addWidget(desc_segment_2)
        desc_segment_3 = get_description_segment(MainDescritpionWidget.segment_3_text)
        self.layout.addWidget(desc_segment_3)



class KeyDescritpionWidget(QLabel):

    main_header = "Key features: "
    list_of_features = {
        "   • simplicity",
        "   • graphic user interface ",
        "   • data security",
        "   • easy and quick data processing",
    }

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.height = int(self.parent.height/3)
        self.setFixedHeight(self.height)
        self.build_description()

    def build_description(self):
        key_desc_header = get_description_subheader(KeyDescritpionWidget.main_header)
        self.layout.addWidget(key_desc_header)
        self.build_features()

    def build_features(self):
        for feature in KeyDescritpionWidget.list_of_features:
            feature_segment = get_description_segment(feature)
            self.layout.addWidget(feature_segment)



class Placeholder(QLabel):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.width=  parent.width
        self.height = int(self.parent.height/4)
        self.setFixedHeight(self.height)
        self.setFixedWidth(self.width)