#histogram.py

import numpy as np
import pylab as pl

data=np.random.normal(5.0,3.0,1000);
pl.hist(data);
pl.xlabel('data');
pl.show();


