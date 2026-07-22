from pivdataprocessor.A01_toolbox import WriteHandler as WH

wh = WH(['time','press(kPa)'])
wh.loaddata([left.time, left.press+ env_press])
wh.write(fig_path+'/left.txt')
wh.loaddata([right.time, right.press+ env_press])
wh.write(fig_path+'/right.txt')