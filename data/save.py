#! encoding = utf-8

''' Save data '''


import numpy as np
import datetime


def save_lwa(filename, y, h_info):
    ''' Save lockin scan in the JPL .lwa format
        Arguments
            filename: str
            y: y data, np.array
            h_info: header information tuple
              (itgtime [ms], sensitivity [V], tc [s], mod_freq [kHz], mod_depth [kHz])
    '''

    d = datetime.datetime.today()
    itgtime, sens, tc, mod_freq, mod_depth, start_freq, step, avg, comment = h_info
    # rescale y based on sensitivity, full scale is 1e4
    yscale = y / sens * 1e4

    with open(filename, 'a') as f:
        # write first line
        f.write('DATE ' + d.strftime('%m-%d-%Y'))
        f.write(' TIME ' + d.strftime('%H:%M:%S'))
        f.write(' SH 9')
        f.write(' IT {:.3g}'.format(itgtime))
        f.write(' SENS {:.3g}'.format(sens))
        f.write(' TAU {:.3g}'.format(tc))
        f.write(' MF {:.3f}'.format(mod_freq))
        f.write(' MA {:.3f}'.format(mod_depth))

        # write second line
        f.write('\n {:s}'.format(comment))

        # write third line
        f.write('\n {:.3f}   {:.6f}  {:d}'.format(start_freq, step, len(y)))
        f.write(' {:d} 1 1  1.887  0.000 0 0 START\n'.format(avg))

        # write y data
        fmt = '{:10.3f}'*10     # 10 numbers each row
        for i in range(len(y)//10 + 1):
            f.write(fmt.format(*yscale[i:i+10]))
            f.write('\n')

    return None
