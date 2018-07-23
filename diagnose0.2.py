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
   
    #print event
    text = "未断诊"
    index_main = 0
    index_sub = 0
    descps = []
    indexes = []
    for index_key in input.keys():
        if input[index_key]:
            if index_key == 'R': # reset dialog memory 
                handler.index_next = 0
                handler.index_last = 0
                handler.input_last = {}
                handler.diagnoses = init_diagnoses
                debug.update( { "descps":descps, "index_cur":indexes , 'index_next': handler.index_next, 'diagnoses':  handler.diagnoses}) ###
                return json.dumps( {"duiWidget": "text", "text": '对话缓存清空', "extra": { 'index_next': 'end', 'diagnose': 'diagnosing', "prescription": "diagnosing"}, "input":input.keys(), "debug":debug } )
            index_num = 0
            try:
                index_num = int(input[index_key]) #get index number form saying
                mark.append(index_key) ###
                mark.append(input[index_key]) ###
                mark.append('index_last') ###
                mark.append(handler.index_next ) ###
            except:
                if index_key == '+':
                    index_num = 0
                elif index_key == '-':
                    index_num = 1

            if index_num  < 0 or input[index_key] == '-0': # index of obj
                index_main = -index_num
            if index_num > 0 or input[index_key] == '0':# index of description
                descps.append(index_num % 2)
                indexes.append(index_num / 2)
            #print mark
            debug['imput_val'] = mark ###

    #debug['context'] = str(context) ###
    ## calculate multiple feature indexes from sayings
    indexes_len = len(indexes)
    if handler.index_next > 0: #ignore index_sub if index is identified in last question
        for i in range(indexes_len):
            indexes[i] = handler.index_next
    else:
        for i in range(indexes_len):
            indexes[i] = indexes[i] + index_main

    #handler.input_last = input
    # locate diagnose with symptoms. i.e. featres value equal to 'descps'
    diagnoses_refine = {} 
    diagnoses_sum = [0,0,0,0,0,0]
    num_refine = 0
    #print 'index', index
    #print 'descps', descps
    for key in handler.diagnoses.keys():
        count = 0
        
        for i in indexes:
            if handler.diagnoses[key][i] == descps[count]:
                count += 1
            else:
                break
        if count == indexes_len:
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
            
            debug.update( { "descps":descps, "index_cur":indexes , 'index_next': handler.index_next, 'diagnoses':  handler.diagnoses})
            return json.dumps( {"duiWidget": "text", "text": handler.solution[key], "extra": { 'index_next': 'end', 'diagnose': key, "prescription": handler.prescriptions[key] }, "input":input.keys(), "debug":debug } )

    # index next symptom(feature) to ask(identify)
    for i, feat_sum in enumerate(diagnoses_sum):
        if feat_sum != 0 and feat_sum != num_refine: #different value between the diagnose_refine sympthoms(features) 
            handler.index_next = i #identify the sympthoms value
            print 'index_next', handler.index_next
            break

    debug.update( { "descps":descps, "index_cur":indexes , 'index_next': handler.index_next, 'diagnoses':  handler.diagnoses})
    return json.dumps( {"duiWidget": "text", "text": text, "extra": { 'index_next': handler.index_next, 'diagnose': 'diagnosing', "prescription": "diagnosing" }, "input":input.keys(), "debug":debug } )


handler.index_next = 0
handler.index_last = 0
handler.input_last = {}
handler.diagnoses = init_diagnoses
handler.solution = init_solution
handler.prescriptions = init_prescriptions


if __name__ == '__main__':
    import json
    data = { 'obj' : '0', 'descp' : '2', 'descp2' : '0'}
#     data = { 'neg' : 2}
    event = json.dumps(data)
    res = json.loads(handler(event, 'context'))
    print res