# -*- coding: utf-8 -*-
import json

#feature = ['牙龈疼','牙龈出血','出血反复','牙龈血多','有口臭','牙齿松']
init_diagnoses = {'胃火炽盛':[1,0,1,0,0,1], '肾阴虚火':[0,1,1,1,1,0], '脾不统血':[0,0,0,0,1,1], 
                  '风火上犯':[0,1,1,1,0,1],  '风寒外侵':[1,0,1,1,0,0], '风热牙疳':[0,0,0,0,1,0]}
init_solution = {
  '胃火炽盛':'应以清胃散煎汤，早晚各一剂。或使用具有相同疗效的云南白药牙膏早午晚刷牙一次', 
  '肾阴虚火':'应服用知柏地黄汤，早晚各一剂。或使用具有相同疗效的云南白药牙膏早午晚刷牙一次', 
  '脾不统血':'应服用归脾汤，早晚各一剂。或使用具有相同疗效的云南白药牙膏早午晚刷牙一次',
  '风火上犯':'应以清胃散煎汤，早晚各一剂。或使用具有相同疗效的云南白药牙膏早午晚刷牙一次', 
  '风寒外侵':'应服用知柏地黄汤，早晚各一剂。或使用具有相同疗效的云南白药牙膏早午晚刷牙一次', 
  '风热牙疳':'应服用知柏地黄汤，早晚各一剂。或使用具有相同疗效的云南白药牙膏早午晚刷牙一次', 
}
init_prescriptions={'胃火炽盛':'清胃散', '肾阴虚火':'知柏地黄汤', '脾不统血':'归脾汤', '风火上犯':'知柏地黄汤', '风寒外侵':'归脾汤', '风热牙疳':'清胃散'}
init_questions = [
'牙龈疼吗？',
'牙龈出血吗？',
'出血反复吗？',
'出血量多吗？',
'有口臭吗？',
'有牙齿松吗？',
]
round_num = 2
round_max = 2
def handler(event, context):
    mark = []
    debug = {}
    input = json.loads(event)
   


    ## get input

    

    #print event
    text = ''
    index_sub = 0
    descps = []
    indexes = []
    ## get feature index
    for index_key in input.keys():
        if input[index_key]:
            if index_key == 'R': # reset dialog memory 
                handler.index_next = []
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
                    descps.append(index_num % 2)
                    indexes.append(index_num / 2)
                elif index_key == '-':
                    index_num = 1

            if index_num  < 0 or input[index_key] == '-0': # index of obj
                handler.index_obj = -index_num
            if index_num > 0 or input[index_key] == '0': # index of description
                descps.append(index_num % 2)
                indexes.append(index_num / 2)
            #print mark
            debug['index_obj'] = handler.index_obj ###
            debug['imput_val'] = mark ###


    #debug['context'] = str(context) ###
    ## calculate multiple feature indexes from sayings
    indexes_len = len(indexes)
    index_last_len = len(handler.index_next)
    if index_last_len > 0: #if questions are asked, match answers
        for i in range(indexes_len):
            indexes[i] = indexes[i] + handler.index_obj
            for j in range(index_last_len):
                if indexes[i] == handler.index_next[j]:
                    handler.index_next.pop(j)
                    break
    else:
        for i in range(indexes_len):
            indexes[i] = indexes[i] + handler.index_obj

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
            handler.index_next = []
            handler.diagnoses = init_diagnoses
            debug.update( { "descps":descps, "index_cur":indexes , 'index_next': handler.index_next, 'diagnoses':  handler.diagnoses})
            return json.dumps( {"duiWidget": "text", "text": handler.solution[key], "extra": { 'index_next': 'end', 'diagnose': key, "prescription": handler.prescriptions[key] }, "input":input.keys(), "debug":debug } )

    # index next symptom(feature) to ask(identify)
    round_count = 0
    print ('handler.index_next', handler.index_next)
    print (diagnoses_sum)
    print num_refine
    if handler.index_next == []: #all questions get match answers
        for i, feat_sum in enumerate(diagnoses_sum):
            if feat_sum != 0 and feat_sum != num_refine: #different value between the diagnose_refine sympthoms(features) 
                handler.index_next.append(i) #identify the sympthoms value
                round_count += 1
                print 'round_count', round_count
                if round_count >= round_max:
                    break

    else: #keep ask questions werer not answered
        text = '抱歉，我没有明白你的回答，'

    ##look up qusetions
    text = text + '请问您'
    for question_idx in handler.index_next:
        
        text = text + init_questions[question_idx]
    
    debug.update( { "descps":descps, "index_cur":indexes , 'index_next': handler.index_next, 'diagnoses':  handler.diagnoses})
    return json.dumps( {"duiWidget": "text", "text": text, "extra": { 'index_next': handler.index_next, 'diagnose': 'diagnosing', "prescription": "diagnosing" }, "input":input.keys(), "debug":debug } )


handler.index_next = []
handler.index_obj = 0
handler.input_last = {}
handler.diagnoses = init_diagnoses
handler.solution = init_solution
handler.prescriptions = init_prescriptions


if __name__ == '__main__':
    import json
    data = { 'obj' : '0', 'descp' : '0'}#, 'descp2' : '0'
#     data = { 'neg' : 2}
    event = json.dumps(data)
    res = json.loads(handler(event, 'context'))
    print json.dumps(res, ensure_ascii=False, encoding='UTF-8')  