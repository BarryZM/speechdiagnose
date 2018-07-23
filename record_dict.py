import json
import os

if os.path.exists('diagnse_vector.json'):
    diagn_vec = json.load('diagnse_vector.json')
else:
    diagn_vec = {'diagnoses':{}, 'descp':{'cur':0} }

if os.path.exists('prescp_vector.json'):
    prescp_vec = json.load('prescp_vector.json')
else:
    prescp_vec = {'name':{}, 'prescp':{}}

if os.path.exists('symptom_cn.json'):
    symptoms_cn = json.load('symptom_cn.json')
else:
    symptoms_cn = {'obj':{'cur_obj':1}, 'descp':{'cur_descp':0}, 'cur_diagnose':0}

if os.path.exists('symptom_index.json'):
    symptoms = json.load('symptom_index.json')
else:
    symptoms = {}

f_reference = open('symptom_reference.csv', 'wa')

# read raw data
with open('diagnoses.txt', 'r') as f:
    line = f.readline()
    while line:
        if line[0] == '-' and line[1] not in diagn_vec:
            diagn_vec[symptom_name] = []
            line = f.readline()
            # start to read symptoms of current 'symptom_name'
            while line[0] != '-':
                line = f.readline()
                len_line = len(line.split())
                if len_line == 1:
                    if line[0] not in symptoms_cn['descp']:
                        # update symptom_cn.json
                        symptoms_cn['descp'][ line[0] ] = symptoms_cn['descp']['cur_descp']
                        # update symptom_index.json
                        symptoms[0][ symptoms_cn['descp'][ line[0] ] ] = symptoms_cn['cur_diagnose']
                        # update symptom_reference.csv
                        f_reference.write( ','.join(symptoms_cn['cur_diagnose'], line[0],
                            '0', '空', symptoms_cn['descp'][ line[0] ], line[0]) )
                        symptoms_cn['descp']['cur_descp'] += 1
                        symptoms_cn['cur_diagnose'] += 1
                if len_line == 2:
                    new_symptom = False
                    if line[0] not in symptoms_cn['obj']:
                        # update symptom_cn.json
                        symptoms_cn['obj'][ line[0] ] = symptoms_cn['obj']['cur_obj']
                        symptoms_cn['obj']['cur_obj'] += 1
                        new_symptom = True
                    if line[1] not in symptoms_cn['descp']:
                        # update symptom_cn.json
                        symptoms_cn['descp'][ line[1] ] = symptoms_cn['descp']['cur_descp']
                        symptoms_cn['descp']['cur_descp'] += 1
                        new_symptom = True
                    if new_symptom:
                        # update symptom_index.json
                        symptoms[ symptoms_cn['obj'][ line[0] ] ][ symptoms_cn['descp'][ line[1] ] ] = symptoms_cn['cur_diagnose']
                        # update symptom_reference.csv
                        f_reference.write( ','.join(symptoms_cn['cur_diagnose'], line[0]+line[1],
                            symptoms_cn['obj'][ line[0] ], line[0], symptoms_cn['descp'][ line[1] ], line[1]) )
                        symptoms_cn['cur_diagnose'] += 1

            while line[0] != '=':
                line = f.readline()

            if line[0] == '=':
                prescp_vec['name'][]



with open('diagnse_vector.json', 'w') as f_diagn_vec:
    pass
with open('symptom_cn.json', 'w') as f_symptoms_cn:
    json.dump(symptom_cn, f_symptoms_cn)
with open('symptom_index.json', 'w') as f_symptoms:
    json.dump(symptoms, f_symptoms)