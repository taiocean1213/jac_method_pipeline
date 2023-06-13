# Import the PyeitClass
from PyeitClass import PyeitClass
import os
# TODO define the constants that are used
config_file_path = os.path.join( os.path.dirname(__file__),"../cache/config.yaml")
data_rel_path = os.path.join( os.path.dirname(__file__),"../cache/simulated_data.pkl") # relative path of the pkl file
reconstruction_algorithm_options = ["kotre"]
reconstruction_algorithm_choice = reconstruction_algorithm_options[0]
square_image_window_pixel_size = 256
image_output_format_options = ["png", "jpeg", "bmp"]
image_output_format = image_output_format_options[0]
save_fig_path = os.path.join( os.path.dirname(__file__),"../output/image.png") 
# main function
def main():
    """
    This main function is the 
    entry point of the python project
    """
    # 
    
    # instantiate the class that
    # acts as a wrapper for the 
    # Pyeit algorithm
    pyeitObject = PyeitClass(config_file_path)
    
    # Now call the method that loads
    # the data to the class via pickle
    # TODO: file need to use OS module to properly import data
    pyeitObject.load(data_rel_path)
    
    # Then set up the meshes that are 
    # used to also perform the image 
    # reconstruction in this method call
    pyeitObject.reconstruct(reconstruction_algorithm_choice)
    
    # Over here, we render the image to 
    # be saved later (i.e. basically store the 
    # image generated from the pyEIT using )
    pyeitObject.render(square_image_window_pixel_size)
    
    # Now plot the image to the 
    # output directory
    pyeitObject.plot(save_fig_path,image_output_format)
    
    # return the function
    return


# This is the entry point of the 
# entire python software
if __name__ == "__main__":
    main()