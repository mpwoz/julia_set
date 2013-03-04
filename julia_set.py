import numpy as np
from pylab import *
from scipy import mgrid
import time
    
#--------------------------------------------
#   Constants
#--------------------------------------------

# size of the image
height = 1000
width = 1000

# min/max for each coordinate
xbound = 1.2
ybound = 1.2

max_iterations = 50


#--------------------------------------------
#   Quadratic iteration
#--------------------------------------------
def quadratic_iterate(z, phi):
    """Given a starting point and iteration function, iterate until z exceeds 2.0 
    or we perform the maximum number of iterations
    """
    count = 0
    # Keep iterating until the value of z exceeds 2.0, or we hit max. iterations
    while( abs(z) < 2.0 ):
        count += 1
        z = phi(z)

        # It probably won't diverge past this number of iterations
        if count == max_iterations:
            break
    return count


#--------------------------------------------
#   Matrix plotting
#--------------------------------------------
def plot_matrix(M, filename, colormap):
    figsize = (np.array(M.shape) / 50.0)[::-1]  # array of form [ M.width, M.height ] (scaled down)
    fig = figure( figsize = figsize )
    axes( [0,0,1,1] ) # Make plot occupy whole canvas
    axis('off')
    fig.set_size_inches(figsize)
    imshow(M, origin='lower', cmap=colormap)
    savefig(filename, facecolor='black', edgecolor='black', dpi=50)
    close(fig)
    
    
   
    

#--------------------------------------------
#   Main Method
#--------------------------------------------
if __name__ == '__main__':

    # Iteration function
    c = 0.233 + 0.53780j
    #c = -0.62772 + 0.42193j
    c = -0.7 - 0.3j             # cauliflower
    c = 1j             # dendrite
    c = -0.7 + -.35j             # frost
    phi = lambda z: z**2 + c

    # Count the number of iterations taken for each pixel
    M = np.zeros(height * width).reshape(height, width)

    # The "width" and "height" of each pixel in coordinate space
    yfactor = ybound / (height / 2)
    xfactor = xbound / (width / 2)

    # Second-largest count (for things that diverge) since this is drastically smaller than max-count usually
    # Do this for purposes of normalizing the color map to get the depth right
    second_largest = 0

    # Try each pixel
    for h in range( -height/2, height/2 ):
        # Scale y to be within the bound.  This is the imaginary part
        y = yfactor * h
        for w in range( -width/2, width/2 ):
            # Scale x to be within the coordinate bound.  This is the real part
            x = xfactor * w
            
            # Complex coordinate of our pixel
            z = x + (y*1j)

            # Count how many iterations we go through until it diverges (or reaches max)
            count = quadratic_iterate(z, phi)

            # Update second_largest count if necessary
            if second_largest < count < max_iterations:
                second_largest = count

            # We want things in the set to be black (0 when count == max_count )
            inverse_count = max_iterations - count
            M[h + (height/2), w + (width/2)] = count

    # Find how far we are from 0 after inverting
    constant = max_iterations - second_largest 

    # Multiplier for normalizing to 255 (color limit)
    multiplier = 255.0 / second_largest
    
    

    # Make the matrix the right color depth 
    for h, row in enumerate(M):
        for w, val in enumerate(row):

            # skip black elements (already in set)
            if val == 0.0:
                continue

            # invert and normalize everything not in set
            val = max_iterations - val
            val *= multiplier
            M[h,w] = val


    timestamp = str( int(time.time()) )
    filename = "output/julia_" + timestamp + ".png"


    colormap = cm.hot
    colormap = cm.copper
    colormap = cm.Spectral

    plot_matrix(M, filename, colormap)





















