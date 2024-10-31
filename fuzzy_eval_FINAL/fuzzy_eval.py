import numpy as np
import terminal_metrics as tm
import visualizer as vis
import sys

# Generate Judge Matrix from weight Vector
def judge_mat(weight):
    n=weight.shape[1]
    j_mat=np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            j_mat[i,j]=weight[0,i]/weight[0,j]
    return j_mat

# Generate Weight Vector from Judge Matrix
def weight_mat(matrix):
    eig_val, eig_vec = np.linalg.eig(matrix)
    max_eig_vec = np.real(eig_vec[:, eig_val.argmax()])
    weight = np.abs(max_eig_vec / np.abs(max_eig_vec).sum())
    return weight.reshape(1,len(weight))

# Do consistency check for Judge Matrix
def consistency_check(matrix):
    n = len(matrix)
    if n<3:
        return True
    eig_val= np.linalg.eig(matrix)[0]
    max_eig_val = np.real(max(eig_val))
    consistency_index = (max_eig_val - n) / (n - 1)
    random_index = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
    consistency_ratio = consistency_index / random_index[n]
    if consistency_ratio < 0.1:
        return True
    else:
        return False

if __name__ == '__main__':    
    # Develop a comment set
    scores=np.transpose(np.matrix([[10,30,50,70,90]]))

    # Weight read process
    weights=tm.weight_read()
    weight_1=[[weights['time'],weights['cost'],weights['quality']]]
    weight_1=np.matrix(weight_1)
    weight_2=[[1,1,1],[1,1,1,1],[weights['qualities_weight']['area'],weights['qualities_weight']['power'],weights['qualities_weight']['computility'],weights['qualities_weight']['latency']]]

    # System metric calculation
    terminal_metrics=tm.generate_terminal_metrics(TEST_MODE = True if '-test' in sys.argv else False, n_solutions_TEST=300)


    # Evaluation for each multi-chiplet solution 
    n_solutions=len(terminal_metrics['time']['arch'])
    result_score=[]
    result_score_sub=[]
    result_score_quality=[]
    for i in range(n_solutions):
        # Create Relationship Matrix R
        R_mat_2_time=[terminal_metrics['time']['arch'][i],terminal_metrics['time']['chiplet'][i],terminal_metrics['time']['assembly'][i]]
        R_mat_2_cost=[terminal_metrics['cost']['design'][i],terminal_metrics['cost']['veri'][i],terminal_metrics['cost']['fab'][i],terminal_metrics['cost']['test'][i]]
        R_mat_2_quality=[terminal_metrics['quality']['area'][i],terminal_metrics['quality']['power'][i],terminal_metrics['quality']['computility'][i],terminal_metrics['quality']['latency'][i]]
        R_mat_2=[np.matrix(R_mat_2_time),np.matrix(R_mat_2_cost),np.matrix(R_mat_2_quality)]

        # Do consistency check
        if not consistency_check(judge_mat(weight_1)):
            print("Consistency ERROR in weight_1")
            exit()
        for j in range(weight_1.shape[1]):
            if not consistency_check(judge_mat(np.matrix([weight_2[j]]))):
                print("Consistency ERROR in weight_2[%d]"%(j))
                exit()
        
        # Calculate the overall score of multi-chiplet system
        R_mat_1=np.zeros((weight_1.shape[1],5))
        T_2=[]
        T_3=[] # quality
        for j in range(weight_1.shape[1]):
            R_mat_1[j]=np.dot(weight_mat(judge_mat(np.matrix([weight_2[j]]))),R_mat_2[j])
            F_2=np.dot(R_mat_1[j],scores)
            T_2.append(F_2)
        for k in range(len(weight_2[2])):
            F_3=np.dot(R_mat_2[2][k],scores)
            T_3.append(F_3)
        F=np.dot(weight_mat(judge_mat(weight_1)),R_mat_1)
        T=np.dot(F,scores)

        # Record the results for later plot
        result_score.append(T[0,0])
        sub_result=[T_2[0][0,0]-30,T_2[1][0,0],T_2[2][0,0]]
        result_score_sub.append([i*100/sum(sub_result) for i in sub_result])
        quality_result=[T_3[0][0,0],T_3[1][0,0],T_3[2][0,0],T_3[3][0,0]]
        result_score_quality.append([i*100/sum(quality_result) for i in quality_result])

        # Print text result in the console
        vis.text_result(i+1,weight_1.tolist()[0],weight_2,F.tolist()[0],T[0,0],T_2[0][0,0],T_2[1][0,0],T_2[2][0,0])
        
        
    # Project test, in which the number of solutions can be determined
    if '-test' in sys.argv:
        print('====================TEST MODE====================')
        vis.plot_result(result_score,result_score_sub,result_score_quality)
    # Run case study simulation
    elif '-standard' in sys.argv:
        print('====================CASE STUDY: STANDARD D2D INTERCONNECTION====================')
        vis.plot_result_STANDARD(result_score,result_score_sub,result_score_quality)
    # Run normal simulation
    else:
        print('====================NORMAL MODE====================')
        vis.plot_result(result_score,result_score_sub,result_score_quality)