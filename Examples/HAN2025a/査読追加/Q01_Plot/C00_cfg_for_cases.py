from itertools import cycle

palette_user = [
'#e41a1c',  # red
'#377eb8',  # blue
'#4daf4a',  # green
'#984ea3',  # purple
'#ff7f00',  # orange
'#a65628',  # yellow
"#000000"  # gray
]
colors = [palette_user[0], palette_user[1], palette_user[2], palette_user[3], palette_user[4], palette_user[5], palette_user[-1]]
linewidths = [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.0]
markers = ['o', 's', '^', 'D', 'v', 'X', 'p']
markersizes = [5,5,5,5,5,5,6]
linestyles = [
    '-',
    (5, (19, 3)),                  # 长破线，24
    (2, (14, 3, 2, 3)),            # 一点划线，24
    (1.5, (11, 3, 2, 3, 2, 3)),       
    '-',
    (5, (19, 3)),                  # 长破线，24
    (2, (14, 3, 2, 3)),           # 一点划线，24
    (1.5, (11, 3, 2, 3, 2, 3)),  
]