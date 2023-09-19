from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


def export(pixmap, items):
    result = pixmap.copy().scaled(800, 800, Qt.KeepAspectRatio)
    painter = QPainter(result)
    texts = items.keys()
    margins = [(800 - result.width()) // 2, (800 - result.height()) // 2]
    for text in texts:
        item = items[text][0]
        painter.setFont(item.font())
        painter.setPen(items[text][-1])
        painter.drawText(item.x() - 10 - margins[0],
                         item.y() - margins[1],
                         item.text())
    return result
