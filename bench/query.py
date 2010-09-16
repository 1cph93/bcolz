# Benchmark to compare the times for evaluating queries.
# Numexpr is needed in order to execute this.

import math
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
import numexpr as ne
import carray as ca
from time import time

N = 1e7       # the number of elements in x
clevel = 5    # the compression level
sexpr = "(x+1)<10"                    # small number of items
#sexpr = "(x+1)<1000000"              # large number
#sexpr = "(2*x**3+.3*y**2+z+1)<10"    # small number
#sexpr = "(2*x**3+.3*y**2+z+1)<1e15"  # medium number
#sexpr = "(2*x**3+.3*y**2+z+1)<1e20"  # large number

print "Creating inputs..."

cparms = ca.cparms(clevel)

x = np.arange(N)
cx = ca.carray(x, cparms=cparms)
if 'y' not in sexpr:
    t = ca.ctable((cx,), names=['x'])
else:
    y = np.arange(N)
    z = np.arange(N)
    cy = ca.carray(y, cparms=cparms)
    cz = ca.carray(z, cparms=cparms)
    t = ca.ctable((cx, cy, cz), names=['x','y','z'])

print "Querying '%s' with 10^%d points" % (sexpr, int(math.log10(N)))

t0 = time()
out = [r for r in x[eval(sexpr)]]
print "Time for plain numpy--> %.3f" % (time()-t0,)

t0 = time()
out = [r for r in cx[ca.eval(sexpr)]]
#out = [r for r in cx[sexpr]]   # XXX this must be supported!
print "Time for carray --> %.3f" % (time()-t0,)

# Uncomment the next for disabling threading
#ne.set_num_threads(1)
#ca.blosc_set_num_threads(1)
# Seems that this works better if we dividw the number of cores by 2.
# Maybe due to some contention between Numexpr and Blosc?
#ca.set_num_threads(ca.ncores//2)

t0 = time()
#cout = t[t.eval(sexpr, cparms=cparms)]
cout = [r for r in t.getif(sexpr)]
#cout = [r['x'] for r in t.getif(sexpr)]
#cout = [r['y'] for r in t.getif(sexpr, colnames=['x', 'y'])]
print "Time for ctable--> %.3f" % (time()-t0,)
print "cout-->", len(cout), cout[:10]

#assert_array_equal(out, cout, "Arrays are not equal")
