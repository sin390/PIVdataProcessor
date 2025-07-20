''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/07/20  =
=========================
'''

from Z21_Filtered_Velocity_Field.G00_filter_option import FilterOptionInfo as FOI
from Z21_Filtered_Velocity_Field.G01_filtered_velocity_field import FilteredVelocityField as FVF
from G01_triple_decomposition import TripleDecomposition

cases = ['Case01']
for case_id in range(len(cases)):
    FO = FOI(cases[case_id])
    FO.load()
    FV = TripleDecomposition(cases[case_id], ifinit=True, ifcleanfolder=True)
    for filter_option_id in range(FO.option_list_shape.total_options):
        FV = TripleDecomposition(cases[case_id], filter_option = (FO.option_list[0, filter_option_id], FO.option_list[1, filter_option_id]),ifinit=True)
        FV.calculate(ifparallel=False)