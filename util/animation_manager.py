from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QParallelAnimationGroup, QPoint, QEasingCurve, QRect, QAbstractAnimation, QObject, QEvent

class AnimationManager(QObject):

    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.duration = 200
        self._start_value = QRect()
        self._end_value = QRect()
        self.widget.installEventFilter(self)
        self.animation = QPropertyAnimation(widget, b"geometry")
        self.reset()

    def reset(self):
        self._start_value = QRect(self.widget.pos().x(), self.widget.pos().y(), self.widget.width(), self.widget.height())
        self._end_value = QRect(self.widget.pos().x() - 2.5, self.widget.pos().y() - 2.5, self.widget.width() + 5, self.widget.height() + 5)
        self.animation.setDuration(self.duration)

    def eventFilter(self, obj, event):
        if obj is self.widget:
            if event.type() == 10:
                self.start_enter_animation()
            elif event.type() == 11:
                self.start_leave_animation()
        return super().eventFilter(obj, event)

    def start_enter_animation(self):
        self.animation.stop()
        self.animation.setStartValue(self._start_value)
        self.animation.setEndValue(self._end_value)
        self.animation.start()

    def start_leave_animation(self):
        self.animation.stop()
        self.animation.setStartValue(self._end_value)
        self.animation.setEndValue(self._start_value)
        self.animation.start()