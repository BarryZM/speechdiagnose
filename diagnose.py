# -*- coding: utf-8 -*-
import json

#feature = ['牙龈疼','牙龈出血','出血反复','牙龈血多','有口臭','牙齿松']
init_diagnoses = {'胃火炽盛':[1,0,1,0,0,1], '肾阴虚火':[0,1,1,1,1,0], '脾不统血':[0,0,0,0,1,1], '风火上犯':[0,1,1,1,0,1],  '风寒外侵':[1,0,1,1,0,0], '风热牙疳':[0,0,0,0,1,0]}
init_solution = {
  '胃火炽盛':'应以清胃散煎汤，早晚各一剂。或使用具有相同疗效的云南白药牙膏早午晚刷牙一次', 
  '肾阴虚火':'应服用知柏地黄汤，早晚各一剂。或使用具有相同疗效的云南白药牙膏早午晚刷牙一次', 
  '脾不统血':'应服用归脾汤，早晚各一剂。或使用具有相同疗效的云南白药牙膏早午晚刷牙一次',
  '风火上犯':'应以清胃散煎汤，早晚各一剂。或使用具有相同疗效的云南白药牙膏早午晚刷牙一次', 
  '风寒外侵':'应服用知柏地黄汤，早晚各一剂。或使用具有相同疗效的云南白药牙膏早午晚刷牙一次', 
  '风热牙疳':'应服用知柏地黄汤，早晚各一剂。或使用具有相同疗效的云南白药牙膏早午晚刷牙一次', 
}
init_prescriptions={'胃火炽盛':'清胃散', '肾阴虚火':'知柏地黄汤', '脾不统血':'归脾汤', '风火上犯':'知柏地黄汤', '风寒外侵':'归脾汤', '风热牙疳':'清胃散'}

def handler(event, context):
    mark = []
    debug = {}
    input = json.loads(event)
   
    text = "未断诊"
    
    #print event
    index = 0
    descp = 0
    for index_key in input.keys():
        if input[index_key] and (index_key not in handler.input_last.keys() ) :
            
            if index_key == 'R':
                handler.index_next = 0
                handler.index_last = 0
                handler.input_last = {}
                handler.diagnoses = init_diagnoses
                debug.update( { "descp":descp, "index_cur":index , 'index_next': handler.index_next, 'diagnoses':  handler.diagnoses}) ###
                return json.dumps( {"duiWidget": "text", "text": '对话缓存清空', "extra": { 'index_next': 'end', 'diagnose': 'diagnosing', "prescription": "diagnosing"}, "input":input.keys(), "debug":debug } )
            index_sub = 0
            try:
                index_sub = int(input[index_key])
                mark.append(index_key)
                mark.append(input[index_key])
                mark.append('index_last')
                mark.append(handler.index_next )
            except:
                if index_key == '+':
                    index_sub = 0
                elif index_key == '-':
                    index_sub = 1
            #print 'index_sub' , index_sub
            if index_sub  <= 0: # index_sub = object_index
                index_sub = -index_sub
            elif index_sub > 0: # index_sub = object_index*10
                descp = index_sub % 2
                index_sub = index_sub / 2
                if handler.index_next  > 0:
                    index_sub = 0

            print 'index_sub', index_sub
            index += index_sub
            #mark.append(index) ###
            debug['imput_val'] = mark ###
    index += handler.index_next 
    #handler.input_last = input
    # locate diagnose with symptoms. i.e. featres value equal to 'descp'
    diagnoses_refine = {} 
    diagnoses_sum = [0,0,0,0,0,0]
    num_refine = 0
    #print 'index', index
    #print 'descp', descp
    for key in handler.diagnoses.keys():
        if handler.diagnoses[key][index] == descp:
            diagnoses_refine[key] = handler.diagnoses[key]
            #print 'key', key
            #sum all diagnoses_refine vectors
            diagnoses_sum = map( lambda x, y: x + y, diagnoses_sum, diagnoses_refine[key] )
            num_refine += 1
            
    handler.diagnoses = diagnoses_refine #update diagnoses

    # final goal is to make only one diagnose in handler.diagnoses, equally, find the diagnose
    if num_refine == 1:
        for key in handler.diagnoses.keys():
            handler.index_next = 0
            #handler.index_last = 0
            #handler.input_last = {}
            handler.diagnoses = init_diagnoses
            
            debug.update( { "descp":descp, "index_cur":index , 'index_next': handler.index_next, 'diagnoses':  handler.diagnoses})
            return json.dumps( {"duiWidget": "text", "text": handler.solution[key], "extra": { 'index_next': 'end', 'diagnose': key, "prescription": handler.prescriptions[key] }, "input":input.keys(), "debug":debug } )

    # index next symptom(feature) to ask(identify)
    for i, feat_sum in enumerate(diagnoses_sum):
        if feat_sum != 0 and feat_sum != num_refine: #different value between the diagnose_refine sympthoms(features) 
            handler.index_next = i #identify the sympthoms value
            print 'index_next', handler.index_next
            break

    debug.update( { "descp":descp, "index_cur":index , 'index_next': handler.index_next, 'diagnoses':  handler.diagnoses})
    return json.dumps( {"duiWidget": "text", "text": text, "extra": { 'index_next': handler.index_next, 'diagnose': 'diagnosing', "prescription": "diagnosing" }, "input":input.keys(), "debug":debug } )


handler.index_next = 0
handler.index_last = 0
handler.input_last = {}
handler.diagnoses = init_diagnoses
handler.solution = init_solution
handler.prescriptions = init_prescriptions