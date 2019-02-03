import numpy as np
import pandas as pd

class Day:
    def __init__(self, ppl=None):
        if ppl is None:
            self.ppl = {}
        else:
            self.ppl = ppl
    
    def add_appt(self, ID, time):
        if self.check_appt(time) == -1:
            self.ppl[time] = ID
    
    def check_appt(self, time):
        if time in self.ppl:
            return self.ppl[time]
        return -1
    
    def remove_appt(self, time):
        if self.check_appt(time) != -1:
            self.ppl.pop(time)
    
    def to_string(self):
        output = ""
        for key in self.ppl:
            output = output + str(key) + " " + str(self.ppl[key]) + "\n"
        return output
            
class Week:
    def __init__(self, days=None, patient_data=None, possible_times=None):
        if days is None:
            self.days = {"Monday": Day(), "Tuesday": Day(), "Wednesday": Day(), "Thursday": Day(), "Friday": Day()}
        else:
            self.days = days
        
        if possible_times is None:
            self.possible_times = []
            for i in range(900, 1700, 100):
                for j in range(0, 60, 15):
                    self.possible_times.append(i + j)
        else:
            self.possible_times = possible_times
        print(self.possible_times)
        
    def add_appt(self, day, ID, time):
        if day in self.days:
            self.days[day].add_appt(ID, time)
    
    def check_appt(self, day, time):
        if day in self.days:
            return self.days[day].check_appt(time)
        return -2
    
    def cancel_appt(self, day, time):
        if self.check_appt(day, time) > -1:
            self.days[day].remove_appt(time)
            
    def to_string(self):
        output = ""
        daysofweek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for key in daysofweek:
            output = output + str(key) + ":\n" + self.days[key].to_string() + "\n"
        return output

    def __str__(self):
        return self.to_string();

def add_time(x, y):
    z = x + y

    if z - 100*(z % 100) >= 60:
        z = z + 40
    return z

def overlap_calculator(week, day, time):
    if add_time(time, 15) in week.days[day].ppl.keys():
        return 15
    return 0

def idleness_cost(week, day, ID, time, data):
    week.add_appt(day, ID, time)
    cost = 0
    for keys in week.days[day].ppl:
        overlap = overlap_calculator(week, day, keys)
        cost += ((30-overlap))#* data.loc(ID, "Cancellation Index"))
    week.cancel_appt(day, ID, time)
    return cost

def waiting_cost(week, day, ID, time, data):
    week.add_appt(day, ID, time)
    cost = 0
    for time in self.possible_times:
        cost += ((overlap_calculator(week=week, day=day, time=keys))*(1-data.loc(ID, "Cancellation Index")))
    week.cancel_appt(day, ID, time)
    return cost

def cost(week, day, ID, time, data):
    beta = 1
    gamme = 1
    return beta*idleness_cost(week, day, ID, time, data) + gamma*waiting_cost(week, day, ID, time, data)

def schedule_appt(week, day, ID, data):
    min_cost = -1
    min_appt_time = 0
    appt_time = 0
    while(appt_time < len(week.possible_times)):
        if week.check_appt(day, week.possible_times[appt_time]) < 0:
            appt_time += 1
        else:
            cur_cost = cost(week, day, ID, week.possible_times[appt_time], data)
            if min_cost == -1:
                min_appt_time = appt_time
                min_cost = cur_cost
            elif cur_cost < min_cost:
                min_appt_time = appt_time
                min_cost = cur_cost
            appt_time += 1
    week.add_appt(day, ID, week.possible_times[min_appt_time])

def complete_appt(week, day, time, noshow):
    pat_id = week.check_appt(day, time)

    if pat_id > 0:
        patient_info = patient_roster.loc[[ID]]
        patient_data = pd.merge(patient_data, patient_info)

        patient_roster.at[ID, "Previous No-Show Coefficient"] = 0.8 * noshow + 0.2 * patient_roster.at[ID, "Previous No-Show Coefficient"]

        week.cancel_appt(day, time)
