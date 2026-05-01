import csv
from PyQt6.QtWidgets import *
from gui import *

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        """
        This section only focuses on the button actions and the function their connected to.
        """
        self.submit_button.clicked.connect(lambda: self.submit())
        self.choose_button.clicked.connect(lambda: self.choose())
        self.generate_button.clicked.connect(lambda: self.generate_final_result())
        self.clear_button.clicked.connect(lambda: self.clear_func())

        self.candidate_opt_drpdwn.setVisible(False)

        self.choose_button.setVisible(False)
        self.generate_button.setVisible(False)
        self.clear_button.setVisible(False)

        """"
        This section covers our Checkbox 
        """
        self.checkBoxCandidate1.setVisible(False)
        self.checkBoxCandidate2.setVisible(False)
        self.checkBoxCandidate3.setVisible(False)
        self.checkBoxCandidate4.setVisible(False)

        self.output_section.setVisible(False)

    def submit(self):
        name = self.input_Name.text().strip()
        raw_score = self.input_Score.text().strip()

        if name == "" or raw_score == "":
            self.output_section.setVisible(True)
            error = "You haven't filled-in one or both section"
            self.output_section.setText(error)
            return

        try:
            score = int(raw_score)
            with open('data.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([name, score])

            self.output_section.setVisible(True)
            self.output_section.setText(f"You have entered \nName: {name}\nScore: {score}")
            self.input_Name.clear()
            self.input_Score.clear()

            self.candidate_opt_drpdwn.setVisible(True)
            self.candidate_opt_drpdwn.addItem(name)
            self.choose_button.setVisible(True)

        except ValueError:
            self.output_section.setVisible(True)
            self.output_section.setText("Your score value is invalid")

    def choose(self):
        index_value = self.candidate_opt_drpdwn.currentIndex()
        selected_candidate = self.candidate_opt_drpdwn.currentText()
        if selected_candidate == "Candidate" or selected_candidate == "":
            self.output_section.setText("You haven't chosen a valid candidate")
            return

        if not self.checkBoxCandidate1.isVisible():
            self.checkBoxCandidate1.setText(selected_candidate)
            self.checkBoxCandidate1.setVisible(True)
            self.output_section.setText(f"You have Assigned {selected_candidate} to Candidate 1")
            self.candidate_opt_drpdwn.removeItem(index_value)

        elif not self.checkBoxCandidate2.isVisible():
            self.checkBoxCandidate2.setText(selected_candidate)
            self.checkBoxCandidate2.setVisible(True)
            self.output_section.setText(f"You have Assigned {selected_candidate} to Candidate 2")
            self.candidate_opt_drpdwn.removeItem(index_value)

        elif not self.checkBoxCandidate3.isVisible():
            self.checkBoxCandidate3.setText(selected_candidate)
            self.checkBoxCandidate3.setVisible(True)
            self.output_section.setText(f"You have Assigned {selected_candidate} to Candidate 3")
            self.candidate_opt_drpdwn.removeItem(index_value)

        elif not self.checkBoxCandidate4.isVisible():
            self.checkBoxCandidate4.setText(selected_candidate)
            self.checkBoxCandidate4.setVisible(True)
            self.output_section.setText(f"You have Assigned {selected_candidate} to Candidate 4")
            self.candidate_opt_drpdwn.removeItem(index_value)

        else:
            self.output_section.setText("All candidate checkboxes are full")
        self.generate_button.setVisible(True)

    def generate_final_result(self):
        selected_candidate = []
        checkbox_opt = [
            self.checkBoxCandidate1,
            self.checkBoxCandidate2,
            self.checkBoxCandidate3,
            self.checkBoxCandidate4
        ]
        for cb in checkbox_opt:
            if cb.isVisible() and cb.isChecked():
                selected_candidate.append(cb.text())
        if len(selected_candidate) == 0:
            self.output_section.setText("Please choose one or more checkbox/candidate")
            return
        final_result = "Final Result:\n"
        try:
            with open('data.csv', 'r') as csvfile:
                reader = list(csv.reader(csvfile))
                all_scores = []

                for row in reader:
                    if len(row) == 2:
                        try:
                            score_as_int = int(row[1].strip())
                            all_scores.append(score_as_int)
                        except ValueError:
                            continue
                if not all_scores:
                    self.output_section.setText("No valid score value found in csv file")
                    return
                best_score = max(all_scores)
                for row in reader:
                    if len(row) == 2:
                        name_from_csv = row[0]
                        try:
                            score_as_int = int(row[1].strip())
                        except ValueError:
                            continue
                        if name_from_csv in selected_candidate:
                            if score_as_int >= best_score - 10:
                                grade = "A"
                            elif score_as_int >= best_score - 20:
                                grade = "B"
                            elif score_as_int >= best_score - 30:
                                grade = "C"
                            elif score_as_int >= best_score - 40:
                                grade = "D"
                            else:
                                grade = "F"
                            final_result += f"Candidate: {name_from_csv} | Score: {score_as_int} | Grade: {grade}\n \n"
            self.output_section.setText(final_result)
            self.output_section.setVisible(True)

            for cb in checkbox_opt:
                cb.setChecked(False)

            self.clear_button.setVisible(True)

        except FileNotFoundError:
            self.output_section.setVisible(True)
            self.output_section.setText("No data found!\nSubmit a Name and Score")

    def reset_candidates(self):
        checkboxes = [
            self.checkBoxCandidate1,
            self.checkBoxCandidate2,
            self.checkBoxCandidate3,
            self.checkBoxCandidate4
        ]
        for cb in checkboxes:
            cb.setChecked(False)
            cb.setVisible(False)
            cb.setText("")
        self.candidate_opt_drpdwn.clear()
        self.candidate_opt_drpdwn.setVisible(False)
        self.generate_button.setVisible(False)
        self.output_section.clear()
        self.output_section.setVisible(False)
        self.choose_button.setVisible(False)
        self.clear_button.setVisible(False)

    def clear_func(self):
        self.reset_candidates()
        open("data.csv", "w").close()
        self.input_Name.clear()
        self.input_Score.clear()
