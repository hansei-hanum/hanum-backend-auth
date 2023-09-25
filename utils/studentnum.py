CLASS_BINDING = {
    "CLOUD_SECURITY": "C",
    "NETWORK_SECURITY": "N",
    "HACKING_SECURITY": "H",
    "METAVERSE_GAME": "M",
    "GAME": "G",
}


class StudentNumber:
    def __init__(self, department: str, grade: int, classroom: int, number: int):
        self.department = department
        self.grade = grade
        self.classroom = classroom
        self.number = number

    def __str__(self) -> str:
        if self.department not in CLASS_BINDING:
            raise ValueError("Invalid department")

        return f"{CLASS_BINDING[self.department]}{self.grade}{self.classroom}{str(self.number).zfill(2)}"
