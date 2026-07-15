

class Patient:
    def __init__(self, name, age, id, ailment):
        super().__init__(name, age, id)
        self.ailment = ailment

    def display_info(self):
        details=super().display_info()
        details.update({"Ailment": self.ailment})
        return details