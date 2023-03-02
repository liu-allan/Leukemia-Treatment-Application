class Patient:
    def __init__(self, id, user_id, name, weight, height, ancMeasurement, birthday, dosageMeasurement, phoneNumber, age, bloodType, allType, bsa, assignedDoctor):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.weight = weight
        self.height = height
        self.ancMeasurement = ancMeasurement
        self.birthday = birthday
        self.dosageMeasurement = dosageMeasurement
        self.phoneNumber = phoneNumber
        self.age = age
        self.bloodType = bloodType
        self.allType = allType
        self.bsa = bsa
        self.assignedDoctor = assignedDoctor

    def save(self, user_id, name, weight, height, bsa, allType, age, bloodType, birthday, phoneNumber, assignedDoctor, dosageMeasurement, dosageEdited, ancMeasurement, ancEdited):
        self.user_id = user_id
        self.name = name
        self.weight = weight
        self.height = height
        self.bsa = bsa
        self.allType = allType
        self.age = age
        self.bloodType = bloodType
        self.birthday = birthday
        self.phoneNumber = phoneNumber
        self.assignedDoctor = assignedDoctor
        if dosageEdited:
            self.dosageMeasurement.append(dosageMeasurement)
        if ancEdited:
            self.ancMeasurement.append(ancMeasurement)
