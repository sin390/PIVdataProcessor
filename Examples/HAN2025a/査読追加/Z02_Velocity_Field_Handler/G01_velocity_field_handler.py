''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/12/04  =
=========================
'''

from Z01_Filtered_Velocity_Field.G01_filter_manager import FilterManager as FM
import numpy as np 

def commonrange(range1,range2):
    '''
        range [[left,right],[bottom,up]]
        return the common area between range1 and range2
    '''
    left1, right1, bottom1, up1 = VelocityFieldHandler.unpackrange(range1)
    left2, right2, bottom2, up2 = VelocityFieldHandler.unpackrange(range2)
    left = max(left1,left2)
    right = min(right1, right2)
    bottom = max(bottom1, bottom2)
    up = min(up1,up2)
    return [[left, right], [bottom, up]]

class VelocityFieldHandler():
    def __init__(self, casename:str, filter:str, filter_id):
        self.casename = casename
        assert filter in ('gaussian','gaussian_bp','gaussian_hp','wavelet')
        self.filter = filter
        self.filter_id = filter_id
        self.X = None
        self.dX_in_mm = None
        self.central_pos_grid = None
        self.effctive_range = None
        self.u = None
        self.dudx = None
        self.frames_in_runs = None
        self.scale_in_grid = None

    def middle_path(self):
        match self.filter:
            case 'gaussian_bp':
                return f'/{self.filter}/{self.filter_id[0]}_{self.filter_id[1]}'
            case _:
                return f'/{self.filter}/{self.filter_id}'
        return

    
    def load_X(self):
        match self.filter:
            case 'gaussian':
                self.fm = FM(self.casename)
                self.fm.load_X()
                self.X = self.fm.X
                self.frames_in_runs = self.fm.filter_param_table.get(0)['frames_in_runs']
                self.central_pos_grid = self.fm.filter_param_table.get(0)['central_pos_grid']
                self.effctive_range = self.fm.filter_param_table.get(self.filter_id)['effective_range']
                self.scale_in_grid = self.fm.filter_param_table.get(self.filter_id)['scale_in_grid']
            
            case 'gaussian_hp':
                self.fm = FM(self.casename)
                self.fm.load_X()
                self.X = self.fm.X
                self.frames_in_runs = self.fm.filter_param_table.get(0)['frames_in_runs']
                self.central_pos_grid = self.fm.filter_param_table.get(0)['central_pos_grid']
                self.effctive_range = self.fm.filter_param_table.get(self.filter_id)['effective_range']
                self.scale_in_grid = self.fm.filter_param_table.get(self.filter_id)['scale_in_grid']                
 
            case 'gaussian_bp':
                self.fm = FM(self.casename)
                self.fm.load_X()
                self.X = self.fm.X
                self.frames_in_runs = self.fm.filter_param_table.get(0)['frames_in_runs']
                self.central_pos_grid = self.fm.filter_param_table.get(0)['central_pos_grid']
                ef1 = self.fm.filter_param_table.get(self.filter_id[0])['effective_range']
                ef2 = self.fm.filter_param_table.get(self.filter_id[1])['effective_range']
                self.effctive_range = commonrange(ef1,ef2)
                scale1 = self.fm.filter_param_table.get(self.filter_id[0])['scale_in_grid']
                scale2 = self.fm.filter_param_table.get(self.filter_id[1])['scale_in_grid']
                self.scale_in_grid = [scale1, scale2]

            # case 'wavelet':
            #     self.wt = WT(self.casename)
            #     self.wt.load_X()
            #     self.X = self.wt.X
            #     self.frames_in_runs = self.wt.param_table_wt.get(0)['frames_in_runs']
            #     self.central_pos_grid = self.wt.param_table_wt.get(0)['central_pos_grid']
            #     self.effctive_range = self.wt.param_table_wt.get(self.filter_id)['effective_range']
            #     self.scale_in_grid = self.wt.param_table_wt.get(self.filter_id)['scale_in_grid']
        self.dX_in_mm = np.array([self.X[0,1,1]-self.X[0,0,0], self.X[1,1,1]-self.X[1,0,0]])
        self.dX_in_m = self.dX_in_mm / 1000.0


    
    def load_field(self, run_id, frame_id):
        match self.filter:
            case 'gaussian':
                self.fm.load_field(self.filter_id, run_id, frame_id, if_cal_du=True)
                self.u = self.fm.u
                self.dudx = self.fm.dudx
            
            case 'gaussian_hp':
                self.fm.load_field(-1, run_id, frame_id, if_cal_du=True)
                u1 = self.fm.u.copy()
                dudx1 = self.fm.dudx.copy()
                self.fm.load_field(self.filter_id, run_id, frame_id, if_cal_du=True)
                self.u = u1 - self.fm.u
                self.dudx = dudx1 - self.fm.dudx                

            case 'gaussian_bp':
                self.fm.load_field(self.filter_id[0],run_id, frame_id, if_cal_du=True)
                u1 = self.fm.u.copy()
                dudx1 = self.fm.dudx.copy()
                self.fm.load_field(self.filter_id[1], run_id, frame_id, if_cal_du=True)
                self.u = u1 - self.fm.u
                self.dudx = dudx1 - self.fm.dudx
            # case 'wavelet':
            #     self.wt.load_field(self.filter_id, run_id, frame_id, if_cal_du=True)
            #     self.u = self.wt.u
            #     self.dudx =self.wt.dudx
    @staticmethod
    def unpackrange(range):
        '''
        range [[left,right],[bottom,up]]
        return left,right,bottom,up
        '''
        return range[0][0],range[0][1],range[1][0],range[1][1]

