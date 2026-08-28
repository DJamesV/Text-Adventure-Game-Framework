## NOTE: This is the only piece of AI code in the project.
# It came with the project, my friend creating the alternate reality game wanted to display images before I had hands on it.
# I have not yet changed it because it seems fairly clean

import sys
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Image path from subprocess argument
image_path = sys.argv[1]

# Create the Qt application
app = QApplication([])

# Create a label to hold the image
label = QLabel()
pixmap = QPixmap(image_path)
label.setPixmap(pixmap)

# ------------------ POLISH ------------------
label.setWindowTitle("Visuals")

# Make the window always on top but not steal focus
label.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
label.setWindowFlag(Qt.WindowType.Tool)  # avoids taskbar entry
label.setWindowFlag(Qt.WindowType.WindowDoesNotAcceptFocus)

# Position window off to the right
x_offset = 750
y_offset = 100
label.move(x_offset, y_offset)

# Resize window to fit the image
label.resize(pixmap.width(), pixmap.height())

# Show the window
label.show()

# Start the Qt event loop
sys.exit(app.exec())
