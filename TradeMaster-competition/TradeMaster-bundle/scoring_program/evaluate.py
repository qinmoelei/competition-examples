import numpy as np
import os
from sys import argv
return_rate_list_1=np.array([[ 0.01236373,  0.00485304,  0.00533715,  0.04395227,  0.0081801 ,
         0.00549229,  0.00045497,  0.02703342,  0.00427741,  0.02237733,
         0.00807053,  0.00245256,  0.01775051,  0.01892495,  0.01175717],
       [-0.00863642, -0.01307246, -0.00054443, -0.03266522, -0.01176473,
        -0.0026246 ,  0.00194595, -0.00959131, -0.01845099, -0.00908101,
         0.00758214,  0.00802383,  0.00633485, -0.00388032,  0.00048293],
       [ 0.00695864,  0.00144689,  0.02212956, -0.00690953,  0.00375215,
         0.03233118,  0.00522144,  0.00916117,  0.02411661,  0.00195723,
         0.00819001, -0.00124386, -0.00022517,  0.0085938 , -0.00924858],
       [ 0.01984473, -0.00273734,  0.01992466,  0.02618578,  0.00899733,
         0.02737658,  0.00781101,  0.02615299, -0.02601772,  0.0277584 ,
        -0.00550061,  0.01645211,  0.00353744,  0.02481022,  0.00152974],
       [ 0.012546  ,  0.00065932, -0.02755974, -0.03389966, -0.00018489,
         0.01116307, -0.0018847 , -0.03084814, -0.00998037, -0.0001627 ,
         0.00207249, -0.00891475, -0.01055575,  0.02808084, -0.00115707],
       [-0.00335403,  0.0003072 , -0.00755354,  0.0151117 ,  0.02479778,
        -0.02378473,  0.00252388,  0.01825438,  0.00198057,  0.02023106,
         0.00827352,  0.01599268,  0.00092035, -0.00203516,  0.00034539],
       [ 0.01687244, -0.00798663,  0.02584676,  0.04062156,  0.00795412,
         0.00465175,  0.00470507,  0.02941488,  0.0144885 ,  0.02562262,
         0.00511636,  0.0098651 ,  0.01248402,  0.01191604, -0.00364679],
       [ 0.0097987 ,  0.01806222, -0.0032338 ,  0.00286695, -0.01723635,
        -0.00019804,  0.0005207 , -0.00720372,  0.00147206, -0.01403801,
         0.00457402,  0.00727881,  0.00752896,  0.01062974, -0.00320067],
       [-0.03926385,  0.01518815,  0.00468438, -0.02374251,  0.01787211,
        -0.02661134,  0.00634075,  0.00934581, -0.0109707 ,  0.0191326 ,
        -0.02030357, -0.00071507,  0.02290634,  0.00315776,  0.0109267 ]])
return_rate_list_2=np.array([[ 0.00542711,  0.01132428,  0.0376586 ,  0.03127447, -0.00287739,
         0.01698412, -0.00528289,  0.0262787 ,  0.00478297, -0.02262382,
        -0.00870857,  0.00383548,  0.00490687,  0.00712053,  0.01547096],
       [-0.02445656, -0.007754  ,  0.02398561,  0.02428968, -0.00421649,
        -0.03499321, -0.00856765,  0.01122602, -0.00866251,  0.01054569,
        -0.01125676,  0.00208148,  0.01687028, -0.02188113, -0.01760787],
       [ 0.01870788,  0.02207359,  0.00752951, -0.00522914, -0.00025797,
         0.02184017,  0.005256  , -0.0081519 , -0.00816182,  0.00954221,
         0.00849947,  0.00200537, -0.00037703,  0.01293027,  0.00293898],
       [-0.01237682, -0.01358208,  0.00731494,  0.03865436,  0.01501827,
        -0.01676241,  0.00018897, -0.01066078,  0.01456334,  0.01080566,
         0.00453787,  0.03121238,  0.0030688 ,  0.01423052, -0.00153788],
       [-0.00420371, -0.003385  ,  0.00965455, -0.00542595,  0.00533531,
        -0.00877334, -0.00949018,  0.00201786,  0.04145962,  0.02350976,
        -0.00108667,  0.00303115, -0.00423976,  0.01321661, -0.0015906 ],
       [ 0.01025713,  0.00943945,  0.00438183,  0.03164525,  0.02049379,
         0.01713967,  0.00549639,  0.02576883,  0.01450439,  0.01409558,
        -0.00455595,  0.00619237,  0.00366611,  0.02345705, -0.01019841],
       [ 0.01415841,  0.00198637,  0.01216258,  0.00281516, -0.00326208,
         0.00335968,  0.00848237,  0.01088617,  0.00662974,  0.03116398,
         0.00921987,  0.00704913, -0.00666149,  0.00897699,  0.00226103],
       [ 0.00666667, -0.00969139, -0.01206797, -0.03127544, -0.01097691,
         0.00523751, -0.00471452,  0.00393767,  0.00252483, -0.00424891,
         0.05726528, -0.00494451, -0.00344918,  0.00576313, -0.00519818],
       [-0.00657826, -0.00496487,  0.00201429, -0.00466462, -0.00602904,
         0.00310367, -0.00531582, -0.00440862,  0.00684443, -0.00176081,
        -0.00219062, -0.00202379,  0.00419946, -0.00173645,  0.00443016]])
def check_action_score(action_score_list):
    true_action_list=[]
    for action_score in action_score_list:
        if np.sum(action_score)==1:
            action=action_score_list
        else:
            action=np.exp(action_score)/np.sum(np.exp(action_score))
        true_action_list.append(action)
    return true_action_list

def comput_return_rate(action_list, return_list):
    total_log_return=0
    for action, return_rate in zip(action_list,return_list):
        daily_return_rate=np.dot(action,return_rate)
        log_return=np.log(daily_return_rate+1)
        total_log_return+=log_return
    return total_log_return
if __name__ == "__main__":
    input_dir = argv[1]
    output_dir = argv[2]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    score_file = open(os.path.join(output_dir, 'scores.txt'), 'w')
    html_file = open(os.path.join(output_dir, 'scores.html'), 'w')
    predict_file_1 = os.path.join(input_dir, 'res', 'action1.npy')
    predict_file_2 = os.path.join(input_dir, 'res', 'action2.npy')
    action_score_1=np.load(predict_file_1)
    action_score_2=np.load(predict_file_2)
    return_score_1=check_action_score(action_score_1)
    return_score_2=check_action_score(action_score_2)
    average_score=(return_score_1+return_score_2)/2
    
        
