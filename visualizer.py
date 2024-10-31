import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False

# Text result print
def text_result(index,weight_1,weight_2,result_mat,result_score,time_score,cost_score,quality_score):
    print('====================Fuzzy Evaluation Report @ solution No.%d===================='%(index))
    print('weight of level 1:',end='')
    print(weight_1)
    print('weight of level 2:',end='')
    for i in range(len(weight_2)):
        print(weight_2[i],end='')
    print('')
    print('Evaluation Result Matrix A:',end='')
    print(result_mat)
    print('Total Score=%.2f'%(result_score))
    print('Time score=%.2f, Cost score=%.2f, Quality score=%.2f'%(time_score,cost_score,quality_score))

# Plot the normal result
def plot_result(line_data,bar_datas,bar_datas_q):
    # Basic parameters setting
    categories = [i+1 for i in range(len(line_data))]
    categories_t = ['level1 No.%d'%(i+1) for i in range(len(line_data))]
    categories_q = ['quality No.%d'%(i+1) for i in range(len(line_data))]
    subcategory_labels = ['Time', 'Cost', 'Quality']
    subcategory_q_labels = ['Area', 'Power', 'Computility','latency']
    colors=['#55B3FF', '#51FF5C', '#FF4C39']
    colors_q=['#FF7C2D', '#FFB751', '#FFDC3B','#E7FF44']
    bar_width = 0.3
    ind = np.arange(len(categories))

    # Plot the percentages, in the form of bars
    for i, category in enumerate(categories_t):
        bottom = 0
        for j, sub_value in enumerate(bar_datas[i]):
            plt.bar(ind[i] - bar_width/9*5, sub_value, bar_width, bottom=bottom, label=(f'{subcategory_labels[j]}' if i == 0 else None), edgecolor='black', linewidth=1, color=colors[j])
            bottom += sub_value
    for i, category in enumerate(categories_q):
        bottom = 0
        for j, sub_value in enumerate(bar_datas_q[i]):
            plt.bar(ind[i] + bar_width/9*5, sub_value, bar_width, bottom=bottom, label=(f'{subcategory_q_labels[j]}' if i == 0 else None), edgecolor='black', linewidth=1,color=colors_q[j])
            bottom += sub_value

    plt.xticks(ind, [f"{l1}  {l2}\n{l3+1}" for l1, l2, l3 in zip([' Total']*len(categories), ['Quality']*len(categories), range(len(categories)))],fontsize=8)
    plt.xlabel('Solutions No.', fontsize=12)
    plt.ylabel('Percentage(%)', fontsize=14)
    plt.legend(loc='upper left')
    plt.subplots_adjust(bottom=0.2)

    # Plot the overall score
    ax2 = plt.twinx()
    ax2.plot(ind, line_data, marker='o', color='black', linewidth=2.0, label='Total Score')
    ax2.set_ylabel('Total Score',fontsize=14)
    plt.grid(axis='y', linestyle='--', which='major', color='black', alpha=0.3)

    # Draw the legend and show the plot
    handles1, labels1 = plt.gca().get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    plt.legend(handles1, labels1, loc='upper left')
    ax2.legend(handles2, labels2, loc='upper right')
    plt.show()

# Plot the case study result
def plot_result_STANDARD(line_data,bar_datas,bar_datas_q):
    # Basic parameters setting
    categories = [i+1 for i in range(len(line_data))]
    categories_t = ['level1 No.%d'%(i+1) for i in range(len(line_data))]
    categories_q = ['quality No.%d'%(i+1) for i in range(len(line_data))]
    subcategory_labels = ['Time', 'Cost', 'Quality']
    subcategory_q_labels = ['Area', 'Power', 'Computility','latency']
    colors=['#55B3FF', '#51FF5C', '#FF4C39']
    colors_q=['#FF7C2D', '#FFB751', '#FFDC3B','#E7FF44']
    bar_width = 0.3
    ind = np.arange(len(categories))

    # Plot the percentages, in the form of bars
    for i, category in enumerate(categories_t):
        bottom = 0
        for j, sub_value in enumerate(bar_datas[i]):
            plt.bar(ind[i] - bar_width/9*5, sub_value, bar_width, bottom=bottom, label=(f'{subcategory_labels[j]}' if i == 0 else None), edgecolor='black', linewidth=1, color=colors[j])
            bottom += sub_value
    for i, category in enumerate(categories_q):
        bottom = 0
        for j, sub_value in enumerate(bar_datas_q[i]):
            plt.bar(ind[i] + bar_width/9*5, sub_value, bar_width, bottom=bottom, label=(f'{subcategory_q_labels[j]}' if i == 0 else None), edgecolor='black', linewidth=1,color=colors_q[j])
            bottom += sub_value

    plt.xticks(ind, [f"{l1}  {l2}\n{l3}" for l1, l2, l3 in zip([' Total']*len(categories), ['Quality']*len(categories), [10,8,6,4,2,1])],fontsize=8)
    plt.xlabel('INTERFACE TYPES(#)', fontsize=12)
    plt.ylabel('Percentage(%)', fontsize=14)
    plt.legend(loc='upper left')
    plt.subplots_adjust(bottom=0.2)

    # Plot the overall score
    ax2 = plt.twinx()
    ax2.plot(ind, line_data, marker='o', color='black', linewidth=2.0, label='Total Score')
    ax2.set_ylabel('Total Score',fontsize=14)
    plt.grid(axis='y', linestyle='--', which='major', color='black', alpha=0.3)
    
    # Draw the legend and show the plot
    handles1, labels1 = plt.gca().get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    plt.legend(handles1, labels1, loc='upper left')
    ax2.legend(handles2, labels2, loc='lower right')
    plt.show()
