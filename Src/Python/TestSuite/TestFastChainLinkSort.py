import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rc
rc( 'text', usetex=True )

from scipy.spatial import Delaunay
import gc

import Triangulation as tr

nInside = 20
nOutside = 40
nBetween = 250

th1 = np.linspace( 0, 2.*np.pi, nInside+1 )[:-1]
th2 = np.linspace( 0, 2.*np.pi, nOutside+1 )[:-1]
th = 2. * np.pi * np.random.rand( nBetween )
r = 1. + np.random.rand( nBetween )

X = np.concatenate( ( np.cos( th1 ).reshape( 1, -1 ), np.sin( th1 ).reshape( 1, -1 ) ), axis=0 )
Y = 2. * np.concatenate( ( np.cos( th2 ).reshape( 1, -1 ), np.sin( th2 ).reshape( 1, -1 ) ), axis=0 )
Z = np.concatenate( ( ( r*np.cos( th ) ).reshape( 1, -1 ), ( r*np.sin( th ) ).reshape( 1, -1 ) ), axis=0 )

P = np.concatenate( ( X, Y, Z ), axis=1 )
tri = Delaunay( P.T ).simplices

trilist = [ list( i ) for i in tri ]
tri2 = np.array( 
    [ i for i in trilist if 
        i[0] >= nInside or i[1] >= nInside or i[2] >= nInside ]
)

### This is the bit of code being tested ######

T = tr.Triangulation( tri2, P )
FB = T.freeBoundary()

###############################################

V = P[ :, FB[:,1] ] - P[ :, FB[:,0] ]

plt.clf()

plt.triplot( P[0], P[1], tri2, label='Complete triangulation' )
plt.quiver( 
    P[ 0, FB[:,0] ], P[ 1, FB[:,0] ], 
    V[0], V[1],
    units='xy',
    label='Free boundaries' )

plt.title( r'Test of routine \texttt{Triangulation.\_FastChainLinkSort}' )
plt.axis( 'equal' )
plt.legend( loc='best' )
plt.grid( which='both' )
plt.show()

gc.collect()
