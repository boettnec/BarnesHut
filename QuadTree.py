"""
Creating the QuadTree

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

# =============================================================================
# Classes
# =============================================================================


class Body():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node():
    def __init__(self, x0, y0, w, h, points):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.points = points
        self.children = []

class QTree():
    """
    Creates a QuadTree.
    
    data   : x and y coordinates, must be 2D array of shape [n,2]      
    k      : number of max points per node (integer)
    points
    """
    
    def __init__(self, data, k):        
        self.threshold = k
        self.data      = [Body(data[i,0], data[i,1]) for i in range(len(data))]
        
        self.X_dim    = (np.amax(data[:,0])-np.amin(data[:,0]))
        self.Y_dim    = (np.amax(data[:,1])-np.amin(data[:,1]))
        self.X_origin = np.amin(data[:,0])-0.1*self.X_dim
        self.Y_origin = np.amin(data[:,1])-0.1*self.Y_dim
        self.X_dim    = (np.amax(data[:,0])-self.X_origin)*1.1
        self.Y_dim    = (np.amax(data[:,1])-self.Y_origin)*1.1
        
        self.root = Node(self.X_origin, self.Y_origin, self.X_dim, self.Y_dim, self.data)
        
        self.__subdivide()

    def __subdivide(self):
        recursive_subdivide(self.root, self.threshold)
    
    def graph(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.title("Quadtree")
        leaves = find_leaves(self.root)
        for n in leaves:
            ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
        x = [point.x for point in self.data]
        y = [point.y for point in self.data]
        plt.plot(x, y, 'ro')
        plt.show()
        return

# =============================================================================
# Helper functions
# =============================================================================

def recursive_subdivide(node, k):
    if len(node.points)<=k:
        return
    
    w_ = float(node.width/2)
    h_ = float(node.height/2)

    p = contains(node.x0, node.y0, w_, h_, node.points)
    sw = Node(node.x0, node.y0, w_, h_, p)
    recursive_subdivide(sw, k)

    p = contains(node.x0, node.y0+h_, w_, h_, node.points)
    nw = Node(node.x0, node.y0+h_, w_, h_, p)
    recursive_subdivide(nw, k)

    p = contains(node.x0+w_, node.y0, w_, h_, node.points)
    se = Node(node.x0 + w_, node.y0, w_, h_, p)
    recursive_subdivide(se, k)

    p = contains(node.x0+w_, node.y0+w_, w_, h_, node.points)
    ne = Node(node.x0+w_, node.y0+h_, w_, h_, p)
    recursive_subdivide(ne, k)

    node.children = [nw, ne, se, sw]
    
    
def contains(x, y, w, h, points):
    pts = []
    for point in points:
        if point.x >= x and point.x <= x+w and point.y>=y and point.y<=y+h:
            pts.append(point)
    return pts

def find_leaves(node):
    if not node.children:
        return [node]
    else:
        leaves = []
        for child in node.children:
            leaves += (find_leaves(child))
    return leaves

# =============================================================================
# Main
# =============================================================================


def main():
    
    data = np.random.rand(1000,2)
    QTree(data, 1).graph()

if __name__ == "__main__":
    main()