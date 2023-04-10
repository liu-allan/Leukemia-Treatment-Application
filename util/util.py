# helper function to display the oncologist's name in the ToolBar
def getLastNameFromFullName(full_name):
    split = full_name.split()
    return split[-1].capitalize()

# helper function to delete all elements in a layout recursively
def clearLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clearLayout(item.layout())