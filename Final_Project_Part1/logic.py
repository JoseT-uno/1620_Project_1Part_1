import csv
from PyQt6.QtWidgets import *
from gui import *

class Logic(QMainWindow, Ui_MainWindow):
    """Main window that manages candidate input, selection, and result generation."""

    def __init__(self) -> None:
        """Initialize the user interface, connect button actions, and hide unused widgets"""
        super().__init__()
        self.setupUi(self)
        self.submit_button.clicked.connect(lambda: self.submit())
        self.choose_button.clicked.connect(lambda: self.choose())
        self.generate_button.clicked.connect(lambda: self.generate_final_result())
        self.clear_button.clicked.connect(lambda: self.clear_data())

        self.candidate_opt_drpdwn.setVisible(False)

        self.choose_button.setVisible(False)
        self.generate_button.setVisible(False)
        self.clear_button.setVisible(False)

        # Hide candidate checkboxes until they are needed
        self.checkBoxCandidate1.setVisible(False)
        self.checkBoxCandidate2.setVisible(False)
        self.checkBoxCandidate3.setVisible(False)
        self.checkBoxCandidate4.setVisible(False)

        self.output_section.setVisible(False)

    def submit(self) -> None:
        """Validate the entered name and score, then save the candidate to the CSV file"""
        name = self.input_Name.text().strip()
        raw_score = self.input_Score.text().strip()

        if name == "" or raw_score == "":
            self.output_section.setVisible(True)
            error = "You haven't filled in one or both sections"
            self.output_section.setText(error)
            return

        try:
            score = int(raw_score)
            duplicate_found = False
            try:
                with open('data.csv', 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) == 2:
                            if row[0].strip().lower() == name.lower():
                                duplicate_found = True
                                break
            except FileNotFoundError:
                pass

            if duplicate_found:
                self.output_section.setVisible(True)
                self.output_section.setText("This user has already been entered")
                self.input_Name.clear()
                self.input_Score.clear()
                return

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

    def choose(self) -> None:
        """Assign the selected candidate from the dropdown to the next available checkbox."""
        index_value = self.candidate_opt_drpdwn.currentIndex()
        selected_candidate = self.candidate_opt_drpdwn.currentText()
        if selected_candidate == "Candidate" or selected_candidate == "":
            self.output_section.setText("You haven't chosen a valid candidate")
            return

        if not self.checkBoxCandidate1.isVisible():
            self.checkBoxCandidate1.setText(selected_candidate)
            self.checkBoxCandidate1.setVisible(True)
            self.output_section.setText(f"You have assigned {selected_candidate} to Candidate 1")
            self.candidate_opt_drpdwn.removeItem(index_value)

        elif not self.checkBoxCandidate2.isVisible():
            self.checkBoxCandidate2.setText(selected_candidate)
            self.checkBoxCandidate2.setVisible(True)
            self.output_section.setText(f"You have assigned {selected_candidate} to Candidate 2")
            self.candidate_opt_drpdwn.removeItem(index_value)

        elif not self.checkBoxCandidate3.isVisible():
            self.checkBoxCandidate3.setText(selected_candidate)
            self.checkBoxCandidate3.setVisible(True)
            self.output_section.setText(f"You have assigned {selected_candidate} to Candidate 3")
            self.candidate_opt_drpdwn.removeItem(index_value)

        elif not self.checkBoxCandidate4.isVisible():
            self.checkBoxCandidate4.setText(selected_candidate)
            self.checkBoxCandidate4.setVisible(True)
            self.output_section.setText(f"You have assigned {selected_candidate} to Candidate 4")
            self.candidate_opt_drpdwn.removeItem(index_value)

        else:
            self.output_section.setText("All candidate checkboxes are full")
        self.generate_button.setVisible(True)

    def generate_final_result(self) -> None:
        """Calculate and display the final grades for the selected candidates"""
        selected_candidate: list = []
        checkbox_opt: list = [
            self.checkBoxCandidate1,
            self.checkBoxCandidate2,
            self.checkBoxCandidate3,
            self.checkBoxCandidate4
        ]
        for checkbox in checkbox_opt:
            if checkbox.isVisible() and checkbox.isChecked():
                selected_candidate.append(checkbox.text())
        if len(selected_candidate) == 0:
            self.output_section.setText("Please choose one or more checkbox/candidate")
            return
        final_result: str = "Final Result:\n"
        try:
            with (open('data.csv', 'r') as csvfile):
                reader: list = list(csv.reader(csvfile))
                all_scores: list = []

                for row in reader:
                    if len(row) == 2:
                        try:
                            score_as_int: int = int(row[1].strip())
                            all_scores.append(score_as_int)
                        except ValueError:
                            continue
                if not all_scores:
                    self.output_section.setText("No valid score value found in csv file")
                    return
                best_score: int = max(all_scores)
                for row in reader:
                    if len(row) == 2:
                        name_from_csv: str = row[0]
                        try:
                            score_as_int: int = int(row[1].strip())
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

            for checkbox in checkbox_opt:
                checkbox.setChecked(False)

            self.clear_button.setVisible(True)

        except FileNotFoundError:
            self.output_section.setVisible(True)
            self.output_section.setText("No data found!\nSubmit a Name and Score")

    def reset_candidates(self) -> None:
        """Clear all selected candidates and reset the related interface elements."""
        checkboxes: list = [ #type hint: list of checkbox widgets
            self.checkBoxCandidate1,
            self.checkBoxCandidate2,
            self.checkBoxCandidate3,
            self.checkBoxCandidate4
        ]
        for checkbox in checkboxes:
            checkbox.setChecked(False)
            checkbox.setVisible(False)
            checkbox.setText("")
        self.candidate_opt_drpdwn.clear()
        self.candidate_opt_drpdwn.setVisible(False)
        self.generate_button.setVisible(False)
        self.output_section.clear()
        self.output_section.setVisible(False)
        self.choose_button.setVisible(False)
        self.clear_button.setVisible(False)

    def clear_data(self) -> None:
        """Reset the interface and clear all saved candidate data from the CSV file"""
        self.reset_candidates()
        open("data.csv", "w").close()
        self.input_Name.clear()
        self.input_Score.clear()