import json
import os


with open(os.path.join("tarot-images.json"), "r", encoding="utf-8") as file:
    student_details = json.loads(file.read())

# Print Dictionary
print(student_details)

