class Patient:
    def __init__(self, id, name, weight, height, dosage, ancMeasurement):
        self.id = id
        self.name = name
        self.weight = weight
        self.height = height
        self.dosage = dosage
        self.ancMeasurement = [ancMeasurement]

    def save(self, name, weight, height, dosage, bsa, ancMeasurement, ancEdited):
        self.name = name
        self.weight = weight
        self.height = height
        self.dosage = dosage
        self.bsa = bsa
        if ancEdited:
            self.ancMeasurement.append(ancMeasurement)
