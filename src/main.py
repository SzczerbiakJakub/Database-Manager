import sys
import app
from PyQt5.QtWidgets import QApplication



def main():
    aplication = QApplication(sys.argv)
    window = app.MainWindow()
    #window.show()
    window.showMaximized() 
    sys.exit(aplication.exec_())



if __name__ == "__main__":
    main()