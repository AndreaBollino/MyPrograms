# filecmp_dircmp_report.py
#https://robyp.x10host.com/3/filecmp.html

import filecmp
import os
from filecmp import dircmp

os.getcwd()

#filecmp.cmpfiles('V:\\batch', 'V:\\batch_gov', regole_switch_OICR.csv, shallow=True)
#print(filecmp.cmp('V:\\batch\\regole_switch_OICR.csv','V:\\batch_gov\\regole_switch_OICR.csv'), end=' ')
print(filecmp.cmp('V:\\batch\\regole_switch_OICR.csv',
                  'V:\\batch_gov\\regole_switch_OICR.csv',
                  shallow=False))

#filecmp.cmp('V:\\batch\\regole_switch_OICR.csv','V:\\batch_gov\\regole_switch_OICR.csv')
dc = filecmp.dircmp('V:\\batch', 'V:\\batch_gov')
dc.report_full_closure()
finito = input()
