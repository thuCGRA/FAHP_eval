import input_generate as ipg

# Helper: linear interpolation function 
def interpolate(fraction, start, end):
    return (1 - fraction) * start + fraction * end

# Transform the score to vector
def score2vector(score):
    # define base vectors
    base_vectors = {
        0:  [1, 0, 0, 0, 0],
        10: [0.7,0.2,0.1,0,0],
        20: [0.5,0.3,0.15,0.05,0],
        30: [0.2,0.5,0.2,0.1,0],
        40: [0.15,0.4,0.3,0.15,0],
        50: [0.1,0.2,0.4,0.2,0.1],
        60: [0,0.15,0.3,0.4,0.15],
        70: [0,0.1,0.2,0.5,0.2],
        80: [0, 0.05, 0.15, 0.3, 0.5],
        90: [0,0,0.1,0.2,0.7],
        100:[0, 0, 0, 0, 1]
    }
    # Find the interval where the score is located and the corresponding score point
    start_score=score//10*10
    end_score=start_score+10
    # Calculate the relative position of scores within the interval
    fraction = (score - start_score) / (end_score - start_score)
    # Interpolation calculation of vector
    start_vector = base_vectors[start_score]
    end_vector = base_vectors.get(end_score, base_vectors[100])
    interpolated_vector = [interpolate(fraction, start, end) for start, end in zip(start_vector, end_vector)]
    # Normalized vector
    total = sum(interpolated_vector)
    if total != 0:
        risk_vector = [value / total for value in interpolated_vector]
    else:
        risk_vector = interpolated_vector  # If the total sum is 0, keep it as it is
    
    return risk_vector

# Transform the metric calculation results to vector
def result2vector(fomula_results,MORE_IS_BETTER):
    min_result, max_result=min(fomula_results), max(fomula_results)
    if max_result==min_result:
        scores_10_90=[50 for i in fomula_results]
    else:
        if MORE_IS_BETTER == True:
            scores_10_90=[ 10+(i-min_result)/(max_result-min_result)*80 for i in fomula_results ]
        else:
            scores_10_90=[ 10+(max_result-i)/(max_result-min_result)*80 for i in fomula_results ]
    return [ score2vector(i) for i in scores_10_90 ]

# Generate evaluation vectors according to the provided files
def generate_terminal_metrics(TEST_MODE,n_solutions_TEST):
    # Multi-chiplet system configuration 
    solutions_parameters=ipg.sip_info_generate(TEST_MODE,n_solutions_TEST)
    # Design & Manufacturing configuration 
    development_info=ipg.development_info_read()
    parameters=development_info['other_parameters']
    R_stab=parameters['demand_stability']
    E_tool=parameters['effciency']
    P_prod=parameters['production_line_effciency']
    V_test=parameters['test_coverage']
    E_test=parameters['test_effciency']
    G_tech=parameters['tech_metric']

    time_solutions={'arch':[], 'chiplet':[], 'assembly':[]}
    cost_solutions={'design':[], 'veri':[], 'fab':[], 'test':[]}
    quality_solutions={'area':[], 'power':[], 'computility':[], 'latency':[]}
    
    # For TEST MODE
    if TEST_MODE == True:
        arch_complexity_TEST = [20] * n_solutions_TEST
        n_inter_TEST = [10] * n_solutions_TEST
        n_inter_type_TEST = [ i for i in range(n_solutions_TEST)]
        interconnect_complexity_TEST = [ x * y for x, y in zip(n_inter_TEST,n_inter_type_TEST)]
        designer_ability = [10] * n_solutions_TEST

    for i,solution in enumerate(solutions_parameters):
        terminal_metrics={'time':{}, 'cost':{}, 'quality':{}}

        # Parameters setting
        if TEST_MODE == True:
            A_comp=arch_complexity_TEST[i]
            O_comp=interconnect_complexity_TEST[i]
            I_comp=solution['integration_complexity']
            T_ab=designer_ability[i]
        else:
            A_comp=solution['arch_complexity']
            O_comp=solution['interconnect_complexity']
            I_comp=solution['integration_complexity']
            T_ab=solution['designer_ability']
        O_area=solution['interconnect_area']
        area=[]
        C_comp=[]
        process=[]
        power=[]
        computility=[]
        complexity1process=[]
        for chiplet, chiplet_info in solution['chiplet_info'].items():
            area.append(chiplet_info['area'])
            C_comp.append(chiplet_info['complexity'])
            process.append(1/chiplet_info['process'])
            complexity1process.append(chiplet_info['complexity']/chiplet_info['process'])
            power.append(chiplet_info['power'])
            computility.append(chiplet_info['computility'])
        C1D_MAX=max(complexity1process)
        
        # Development time calculation
        time_arch_design=A_comp/(R_stab*E_tool*T_ab)
        time_arch_veri=A_comp/(R_stab*E_tool*T_ab)
        time_arch=time_arch_design+time_arch_veri
        time_solutions['arch'].append(time_arch)
        time_chiplet_design=C1D_MAX/(E_tool*T_ab)
        time_chiplet_veri=C1D_MAX*O_comp/(E_tool)
        time_chiplet_fab=sum(process)/(T_ab*P_prod)
        time_chiplet_test=sum(C_comp)*V_test/E_test
        time_chiplet=time_chiplet_design+time_chiplet_veri+time_chiplet_fab+time_chiplet_test
        time_solutions['chiplet'].append(time_chiplet)
        time_assembly_design=I_comp*G_tech/(T_ab*E_tool)
        time_assembly_veri=I_comp/(R_stab*T_ab*E_tool)
        time_assembly_fab=G_tech/(T_ab*P_prod)
        time_assembly_test=I_comp*V_test/E_test
        time_assembly=time_assembly_design+time_assembly_veri+time_assembly_fab+time_assembly_test
        time_solutions['assembly'].append(time_assembly)
        # Development cost calculation
        cost_design_chiplet=sum([x * y for x, y in zip(C_comp, area)])
        cost_design_arch=A_comp
        cost_design_assembly=I_comp*sum(area)
        cost_design=cost_design_chiplet+cost_design_arch+cost_design_assembly
        cost_solutions['design'].append(cost_design)
        cost_veri_chiplet=sum(C_comp)
        cost_veri_arch=A_comp
        cost_veri_assembly=I_comp
        cost_veri=cost_veri_chiplet+cost_veri_arch+cost_veri_assembly
        cost_solutions['veri'].append(cost_veri)
        cost_fab_chiplet=sum([x * y for x, y in zip(area, process)])
        cost_fab_assembly=sum(area)*G_tech
        cost_fab=cost_fab_chiplet+cost_fab_assembly
        cost_solutions['fab'].append(cost_fab)
        cost_test_chiplet=sum(C_comp)*V_test
        cost_test_assembly=I_comp*V_test
        cost_test=cost_test_chiplet+cost_test_assembly
        cost_solutions['test'].append(cost_test)
        # Product quality calculation
        quality_solutions['area'].append(sum(area)+O_area)
        quality_solutions['power'].append(sum(power))
        quality_solutions['computility'].append(sum(computility))
        quality_solutions['latency'].append(1/sum(power))
        # sum([1/i for i in power])/len(power)
    # Transform the result from score to vector
    time_metrics={'arch': result2vector(time_solutions['arch'],False),'chiplet': result2vector(time_solutions['chiplet'],False),'assembly': result2vector(time_solutions['assembly'],False)}
    cost_metrics={'design': result2vector(cost_solutions['design'],False),'veri': result2vector(cost_solutions['veri'],False),'fab': result2vector(cost_solutions['fab'],False),'test':result2vector(cost_solutions['test'],False)}
    quality_metrics={'area': result2vector(quality_solutions['area'],False),'power': result2vector(quality_solutions['power'],False),'computility': result2vector(quality_solutions['computility'],True),'latency':result2vector(quality_solutions['latency'],False)}
    terminal_metrics={'time': time_metrics, 'cost': cost_metrics, 'quality': quality_metrics}
    return terminal_metrics
# Read weight information
def weight_read():
    development_info=ipg.development_info_read()
    weights=development_info['user_preference']
    return weights
