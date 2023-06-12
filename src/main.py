# Import the PyeitClass
import PyeitClass

# TODO define the constants that are used
pkl_rel_path = "" # relative path of the pkl file

# This is the entry point of the 
# entire python software
if __name__ == "__main__":
    
    # instantiate the class that
    # acts as a wrapper for the 
    # Pyeit algorithm
    pyeitObject = PyeitClass()
    
    
    
    # Now call the method that loads
    # the data to the class via pickle
    pyeitObject.load(pkl_rel_path)
    
    # Then set up the meshes that are 
    # used to also perform the image 
    # reconstruction in this method call
    pyeitObject.reconstruct()
    
    # Over here, we render the image to 
    # be saved later
    pyeitObject.render()
    
    # Now plot the image to the 
    # output directory
    pyeitObject.plot()
    