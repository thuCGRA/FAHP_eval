import json

# Read the multi-chiplet system information
def sip_info_generate(TEST_MODE, n_solutions_TEST):
    # Chiplet libary file read
    file = open("configuration/chiplets.json", "r")
    chiplet_libary = json.loads(file.read())
    file.close()

    # Multi-chiplet system file read
    if TEST_MODE == True:
        file = open("configuration/TEST_SiP_configuration.json", "r")
        sip_conf = json.loads(file.read())
        sip_conf = {f'sol{i+1}': sip_conf['sol_test'] for i in range(n_solutions_TEST)}
    else:
        file = open("configuration/SiP_configuration.json", "r")
        sip_conf = json.loads(file.read())
    file.close()

    solutions_parameters=[]
    for sol_key, sol_value in sip_conf.items():
        temp_basic={}
        # architecture complexity
        temp_basic['arch_complexity']=sol_value['arch_complexity']
        # chiplet info
        temp_basic['chiplet_info']={}
        for chiplet, n_chiplet in sol_value['chiplets'].items():
            chiplet_info={}
            # area
            size_x=chiplet_libary[chiplet]['size']['x']
            size_y=chiplet_libary[chiplet]['size']['y']
            chiplet_area=size_x*size_y*n_chiplet
            chiplet_info['area']=chiplet_area
            # chiplet complexity
            n_module=chiplet_libary[chiplet]['num_modules']
            n_module_type=chiplet_libary[chiplet]['num_modules_type']
            tech_complexity=chiplet_libary[chiplet]['tech_complexity']
            chiplet_complexity=n_module*n_module_type*tech_complexity
            chiplet_info['complexity']=chiplet_complexity
            # process node
            chiplet_info['process']=chiplet_libary[chiplet]['process_node']
            # power
            chiplet_info['power']=chiplet_libary[chiplet]['power']*n_chiplet
            # computility
            chiplet_info['computility']=chiplet_libary[chiplet]['computility']*n_chiplet
            temp_basic['chiplet_info'][chiplet]=chiplet_info
        # integration complexity
        n_chiplets=sum(sol_value['chiplets'].values())
        n_chiplet_type=len(sol_value['chiplets'])
        integration_complexity=n_chiplets*n_chiplet_type
        temp_basic['integration_complexity']=integration_complexity
        # interconnect complexity
        n_interconnects=sol_value['interconnects']['num_inter']
        n_interconnect_type=sol_value['interconnects']['num_inter_type']
        interconnect_complexity=n_interconnects*n_interconnect_type
        interconnect_area=n_interconnects/n_interconnect_type
        temp_basic['interconnect_complexity']=interconnect_complexity
        temp_basic['interconnect_area']=interconnect_area
        # designer ability
        temp_basic['designer_ability']=sol_value['designer_ability']
        solutions_parameters.append(temp_basic)
    return solutions_parameters

# Read the development information
def development_info_read():
    file = open("configuration/development_info.json", "r")
    development_info = json.loads(file.read())
    file.close()
    return development_info


