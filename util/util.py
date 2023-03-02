# helper function to display the oncologist's name in the ToolBar
def getLastNameFromFullName(full_name):
    split = full_name.split()
    return split[-1].capitalize()
