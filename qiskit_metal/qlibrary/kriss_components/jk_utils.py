# Jaseung Ku
# 2025 Aug
# Collection of useful functions in designing qubit chips

import numpy as np

from qiskit_metal.qlibrary.kriss_components.transmon_pocket_6_cl import TransmonPocket6CL
from qiskit_metal.qlibrary.tlines.meandered import RouteMeander
from qiskit_metal.qlibrary.couplers.coupled_line_tee import CoupledLineTee



def calculate_coupledT_length(coupled_line_tee:CoupledLineTee):
    """ 
        Calcuate the length of the L section in couplted line tee in mm.
    """
    
    coupled_line_length = (
        coupled_line_tee.p.down_length +
        coupled_line_tee.p.coupling_length + 
        coupled_line_tee.p.fillet*(np.pi/2 - 2)
        )    

    return coupled_line_length

def calculate_only_meander_length_between_qubit_and_coupledlineT(
        total_resonator_length:float, # in mm
        transmon:TransmonPocket6CL, 
        coupled_line_tee: CoupledLineTee,
        transmon_connection_pad_name:str="readout"
    ):
    """
        Calculate the length of meander only given transmon and coupledlineT.
        Return: length in mm
    """
    assert isinstance(transmon, TransmonPocket6CL)

    if transmon.p.connection_pads[transmon_connection_pad_name].loc_W == 0:
        transmon_length = (
            transmon.p.pocket_height/2 - 
            transmon.p.pad_gap/2 - 
            transmon.p.pad_height -
            transmon.p.connection_pads[transmon_connection_pad_name].pad_gap +
            transmon.p.connection_pads[transmon_connection_pad_name].cpw_extend
            )
    else: # loc_W=0
        transmon_length = (
            transmon.p.pocket_width/2 - 
            transmon.p.pad_width/2 +
            transmon.p.connection_pads[transmon_connection_pad_name].pad_width +
            transmon.p.connection_pads[transmon_connection_pad_name].cpw_extend
            )

    # coupled_line_length = (
    #     coupled_line_tee.p.down_length +
    #     coupled_line_tee.p.coupling_length + 
    #     coupled_line_tee.p.fillet*(np.pi/2 - 2)
    #     )    
    coupled_line_length = calculate_coupledT_length(coupled_line_tee)

    meander_length = (
        total_resonator_length - 
        transmon_length -
        coupled_line_length
        )
    
    print(f"total_res_length = {total_resonator_length} mm")
    print(f"transmon_length = {transmon_length} mm")    
    print(f"coupled_line_length = {coupled_line_length} mm")
    print(f"meander_length = {meander_length} mm")

    return meander_length

def calculate_total_readout_res_length_between_qubit_and_feedline(
        transmon:TransmonPocket6CL, 
        meander:RouteMeander,
        coupled_line_tee:CoupledLineTee,
        transmon_connection_pad_name:str="readout"
        ):
    """ 
        Calculate the total length of readout resonator 
        
        Return: (Total length of resonator, transmon_length, meander_length, coupled_line_lenght) in mm

    """
    
    assert isinstance(transmon, TransmonPocket6CL)

    if transmon.p.connection_pads[transmon_connection_pad_name].loc_W == 0:
        transmon_length = (
            transmon.p.pocket_height/2 - 
            transmon.p.pad_gap/2 - 
            transmon.p.pad_height -
            transmon.p.connection_pads[transmon_connection_pad_name].pad_gap +
            transmon.p.connection_pads[transmon_connection_pad_name].cpw_extend
            )
    else: # loc_W=0
        transmon_length = (
            transmon.p.pocket_width/2 - 
            transmon.p.pad_width/2 +
            transmon.p.connection_pads[transmon_connection_pad_name].pad_width +
            transmon.p.connection_pads[transmon_connection_pad_name].cpw_extend
            )

    meander_length = meander.p.total_length 

    # coupled_line_length = (
    #     coupled_line_tee.p.down_length +
    #     coupled_line_tee.p.coupling_length + 
    #     coupled_line_tee.p.fillet*(np.pi/2 - 2)
    #     )    
    
    coupled_line_length = calculate_coupledT_length(coupled_line_tee)

    total_res_length = (
        transmon_length +
        meander_length +
        coupled_line_length
        )
    
    print(f"total_res_length = {total_res_length} mm")
    print(f"transmon_length = {transmon_length} mm")
    print(f"meander_length = {meander_length} mm")
    print(f"coupled_line_length = {coupled_line_length} mm")

    return total_res_length

def calculate_only_meander_length_between_qubits(
        total_resonator_length:float, # in mm
        transmon1:TransmonPocket6CL, 
        transmon2:TransmonPocket6CL,
        transmon1_connection_pad_name:str="bus_l",
        transmon2_connection_pad_name:str="bus_2"
        ):
    """ 
        Calculate the only meander length between two qubits.
        
        Return: meander_length in mm

    """
    
    if transmon1.p.connection_pads[transmon1_connection_pad_name].loc_W == 0: # loc_W=0
        transmon1_length = (
            transmon1.p.pocket_height/2 -
            transmon1.p.pad_gap/2 -
            transmon1.p.pad_height -
            transmon1.p.connection_pads[transmon1_connection_pad_name].pad_gap +
            transmon1.p.connection_pads[transmon1_connection_pad_name].cpw_extend
            )
    else: # loc_W = -1 or +1
        transmon1_length = (
            transmon1.p.pocket_width/2 - 
            transmon1.p.pad_width/2 +
            transmon1.p.connection_pads[transmon1_connection_pad_name].pad_width +
            transmon1.p.connection_pads[transmon1_connection_pad_name].cpw_extend
            )

    if transmon2.p.connection_pads[transmon2_connection_pad_name].loc_W == 0: # loc_W=0
        transmon2_length = (
            transmon2.p.pocket_height/2 -
            transmon2.p.pad_gap/2 -
            transmon2.p.pad_height -
            transmon2.p.connection_pads[transmon2_connection_pad_name].pad_gap +
            transmon2.p.connection_pads[transmon2_connection_pad_name].cpw_extend
            )
    else: # loc_W = -1 or +1
        transmon2_length = (
        transmon2.p.pocket_width/2 - 
        transmon2.p.pad_width/2 +
        transmon2.p.connection_pads[transmon2_connection_pad_name].pad_width +
        transmon2.p.connection_pads[transmon2_connection_pad_name].cpw_extend
        )
    
    
    meander_length = (
        total_resonator_length - 
        transmon1_length -
        transmon2_length
        )
    
    print(f"total_bus_length = {total_resonator_length} mm")
    print(f"transmon1_length = {transmon1_length} mm")
    print(f"transmon2_length = {transmon2_length} mm")
    print(f"meander_length = {meander_length} mm")
    
    return meander_length

def calculate_total_bus_res_length_between_qubits(
        transmon1:TransmonPocket6CL, 
        meander:RouteMeander,
        transmon2:TransmonPocket6CL,
        transmon1_connection_pad_name:str="bus_l",
        transmon2_connection_pad_name:str="bus_2"
        ):
    """ 
        Calculate the total length of resonator 
        
        Return: (Total length of resonator, transmon_length, meander_length, coupled_line_lenght) in mm

    """
    
    if transmon1.p.connection_pads[transmon1_connection_pad_name].loc_W == 0: # loc_W=0
        transmon1_length = (
            transmon1.p.pocket_height/2 -
            transmon1.p.pad_gap/2 -
            transmon1.p.pad_height -
            transmon1.p.connection_pads[transmon1_connection_pad_name].pad_gap +
            transmon1.p.connection_pads[transmon1_connection_pad_name].cpw_extend
            )
    else: # loc_W = -1 or +1
        transmon1_length = (
            transmon1.p.pocket_width/2 - 
            transmon1.p.pad_width/2 +
            transmon1.p.connection_pads[transmon1_connection_pad_name].pad_width +
            transmon1.p.connection_pads[transmon1_connection_pad_name].cpw_extend
            )

    if transmon2.p.connection_pads[transmon2_connection_pad_name].loc_W == 0: # loc_W=0
        transmon2_length = (
            transmon2.p.pocket_height/2 -
            transmon2.p.pad_gap/2 -
            transmon2.p.pad_height -
            transmon2.p.connection_pads[transmon2_connection_pad_name].pad_gap +
            transmon2.p.connection_pads[transmon2_connection_pad_name].cpw_extend
            )
    else: # loc_W = -1 or +1
        transmon2_length = (
        transmon2.p.pocket_width/2 - 
        transmon2.p.pad_width/2 +
        transmon2.p.connection_pads[transmon2_connection_pad_name].pad_width +
        transmon2.p.connection_pads[transmon2_connection_pad_name].cpw_extend
        )
    
    meander_length = meander.p.total_length 
    
    total_bus_length = (
        transmon1_length +
        meander_length +
        transmon2_length
        )
    
    print(f"total_bus_length = {total_bus_length} mm")
    print(f"transmon1_length = {transmon1_length} mm")
    print(f"meander_length = {meander_length} mm")
    print(f"transmon2_length = {transmon2_length} mm")

    
    return total_bus_length