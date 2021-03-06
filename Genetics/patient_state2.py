class PatientState:
    # age: years
    # weight: kilos
    # height: cm
    # sex: 'm' or 'f'
    def __init__(self, age, weight, height, sex, params):
        self.params = params

        lean_body_mass = self.__lean_body_mass(weight, height, sex)

        self.v1 = params[12] * 6 #times by 5 to make parameter less than 1
        # TODO: Work out why v2 and v3 are not used in the algorithm
        v2 = params[9] + params[10] * (age - params[14])
        v3 = params[13] * 4000 #times by 200 to make parameter less than 1

        #make the weight offsets lesss than one by multiplying by 50-200
        params[14] = params[14] * 75
        params[15] = params[15] * 100
        params[16] = params[16] * 75
        params[17] = params[17] * 200

        # Initial concentration is zero in all components
        self.x1 = 0.0
        self.x2 = 0.0
        self.x3 = 0.0

        self.k10 = (params[0] + params[1] * (weight - params[15]) + params[2] * (lean_body_mass - params[16]) + params[3] * (height - params[17])) / 60
        self.k12 = (params[4] + params[5] * (age - params[14])) / 60
        self.k13 = params[6] / 60
        self.k21 = ((params[7] + params[8] * (age - params[14])) / (params[9] + params[10] * (age - params[14]))) / 60
        self.k31 = params[11] / 60

        self.keo = 0.456 / 60

        self.xeo = 0.0

    def give_drug(self, drug_milligrams):
        self.x1 = self.x1 + drug_milligrams / self.v1

    def wait_time(self, time_seconds):
        current_x1 = self.x1
        current_x2 = self.x2
        current_x3 = self.x3
        current_xeo = self.xeo

        self.x1 = current_x1 + (self.k21 * current_x2 - self.k12 * current_x1 + self.k31 * current_x3 - self.k13 * current_x1 - self.k10 * current_x1) * time_seconds
        self.x2 = current_x2 + (-self.k21 * current_x2 + self.k12 * current_x1) * time_seconds
        self.x3 = current_x3 + (-self.k31 * current_x3 + self.k13 * current_x1) * time_seconds
        self.xeo = current_xeo + (-self.keo * current_xeo + self.keo * current_x1) * time_seconds

    @staticmethod
    def with_schnider_params(age, weight, height, sex):
        params = PatientState.schnider_params()

        return PatientState(age, weight, height, sex, params)

    @staticmethod
    def schnider_params():
        params = {
            'k10a': 0.443,
            'k10b': 0.0107,
            'k10c': -0.0159,
            'k10d': 0.0062,
            'k12a': 0.302,
            'k12b': -0.0056,
            'k13': 0.196,
            'k21a': 1.29,
            'k21b': -0.024,
            'k21c': 18.9,
            'k21d': -0.391,
            'k31': 0.0035,
            'v1': 4.27,
            'v3': 238,
            'age_offset': 53,
            'weight_offset': 77,
            'lbm_offset': 59,
            'height_offset': 177
        }
        return params

    def __lean_body_mass(self, weight, height, sex):
        if sex != "m" and sex != "f":
            raise ValueError("Unknown sex '%s'. This algorithm can only handle 'm' and 'f'. :(" % sex)

        # TODO: Use better equation to calculate lean body mass
        # if sex == "m":
        #     return 1.1 * weight - self.params['weight_offset'] * ((weight/height) * (weight/height))
        # else:
        #     return 1.07 * weight - self.params['weight_offset'] * ((weight/height) * (weight/height))

        #use hume equation
        # Men: eLBM = 0.32810weight(kg) + 0.33929height(cm) - 29.5336
        # Women: eLBM = 0.29569weight(kg) + 0.41813height(cm) - 43.2933

        if sex == "m":
            return 0.32810 * weight + 0.33929 * height - 29.5336
        else:
            return 0.29569 * weight + 0.41813 * height - 43.2933

    def __repr__(self):
        return "PatientState(x1=%f, x2=%f, x3=%f, xeo=%f)" % (self.x1, self.x2, self.x3, self.xeo)


if __name__ == '__main__':
    patient = PatientState.with_schnider_params(50, 70, 180, "m")
    print "Initial state: " + str(patient)

    patient.give_drug(92.60001)
    print "After giving drug: " + str(patient)

    for t in range(130):
        patient.wait_time(1)
        print "After 1 sec: " + str(patient)
