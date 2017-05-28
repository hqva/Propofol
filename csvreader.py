import csv
from patient_state import PatientState

csvfile = "propofol.csv"

def read_patient_csv():
    patients = []

    read = open(csvfile, 'r')
    # Read header line
    read.readline()

    pid = None
    current_patient = __build_new_patient()

    for row in csv.reader(read):
        newid = row[0]

        if newid != pid:
            pid = newid
            current_patient = __build_new_patient()
            patients.append(current_patient)

            current_patient['id'] = pid
            current_patient['age'] = float(row[6])
            current_patient['weight'] = float(row[7])
            current_patient['height'] = float(row[8])
            current_patient['sex'] = __patient_sex(int(row[9]))

        cp = float(row[2])
        is_measurement = cp != 0

        if is_measurement:
            event = {
                "type": "measurement",
                "time_mins": float(row[1]),
                "cp": float(row[2])
            }
            current_patient["events"].append(event)
        else:
            propofol_mg = float(row[3])
            if propofol_mg == 0:
                raise ValueError("Found row with no CP measurement or propofol amount for patient %s" % pid)

            event = {
                "type": "start_infusion",
                "time_mins": float(row[1]),
                "propofol_mg": propofol_mg,
                "rate_mg_per_min": float(row[4])
            }
            current_patient["events"].append(event)

    return patients

def __patient_sex(code):
    if code == 1:
        return "m"
    elif code == 2:
        return "f"
    else:
        raise ValueError("Unknown value for patient sex '%s'. Expected '1' or '2'" % sex)

def __build_new_patient():
    return {
        "events": []
    }
