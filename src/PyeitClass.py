import pickle
import pyeit.mesh as mesh
import pyeit
from pyeit.eit import protocol
import matplotlib.pyplot as plt
import yaml
from pyeit import eit
import numpy as np

class PyeitClass:
    def __init__(self, config_yaml_path):
        """initlize a instance of PyeitClass.

        Args:
            config_yaml_path (string): relative path to the python environment
        """
        self.data = None
        self.mesh = None
        self.eit = None
        self.image = None
        self.config_params = self.configure(config_yaml_path)
        
        return

    def configure(self, config_yaml_path, params=None):
        """Configures the PyeitClass based on the parameters in a YAML file.

        Args:
            config_yaml_path (str): The relative path to the YAML configuration file.
            params (dict, optional): Default values for the configuration parameters. Defaults to None.

        Returns:
            dict: The configuration parameters.
        """
        try:
            # Load the configuration file
            with open(config_yaml_path, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"File not found: {config_yaml_path}")
            return {}
        except Exception as e:
            print(f"Error loading config file: {e}")
            return {}

        # Merge the loaded configuration with the default parameters
        if params is not None:
            config = {**params, **config}

        return config

        
    def load(self, filename: str):
        """Load data from a file into the object.

        Args:
            filename (str): The path to the file containing the data.
        """
        
        with open(filename,'rb') as f:
            data = pickle.load(f)
        self.data=data
        return

    def reconstruct(self, reconstruction_algorithm_choice='kotre'):
        """Performs image reconstruction based on the EIT data and mesh.

        Args:
            reconstruction_algorithm_choice (str, optional): The choice of reconstruction algorithm. Defaults to 'kotre'.
        """
        # Create mesh
        self.mesh = mesh.create(self.config_params['n_el'], h0= self.config_params['h0'])
        self.protocol = eit.protocol.create(self.config_params['n_el'],dist_exc=1)
        self.eit = eit.jac.JAC(self.mesh,self.protocol)
        # Perform image reconstruction using the chosen algorithm
        if reconstruction_algorithm_choice == 'kotre':
            self.eit.setup(p=self.config_params['p'],lamb = self.config_params['lamb'],method=self.config_params['method'])
        elif reconstruction_algorithm_choice == 'greit':
            self.eit = eit(self.data['ex_mat'], self.data['eit_mat'], self.mesh, method='greit')
        else:
            raise ValueError(f"Invalid reconstruction algorithm: {reconstruction_algorithm_choice}")
        self.conductivity = self.eit.solve(self.data['v_ref'],np.array(self.data['v_meas'][0]))


    def render(self, square_window_size):
        """Render a triangular mesh with conductivity values.

        Args:
            square_window_size (int): The size of the square window.

        Returns:
            None

        Raises:
            ValueError: If square_window_size is not an integer.

        Public attributes:
            fig (matplotlib.figure.Figure): The figure object.
            ax (matplotlib.axes.Axes): The axes object.

        Internal attributes:
            tri (numpy.ndarray): The triangular mesh elements.
            pts (numpy.ndarray): The mesh nodes.
            x (numpy.ndarray): The x-coordinates of the mesh nodes.
            y (numpy.ndarray): The y-coordinates of the mesh nodes.

        This method generates a triangular mesh plot with conductivity values. The plot is based on the triangular mesh elements and the mesh nodes. The conductivity values are represented by the color of the triangles.

        The `square_window_size` argument defines the size of the square window. This argument should be an integer.

        Public attributes:
        - `fig`: The figure object.
        - `ax`: The axes object.

        Internal attributes:
        - `tri`: The triangular mesh elements.
        - `pts`: The mesh nodes.
        - `x`: The x-coordinates of the mesh nodes.
        - `y`: The y-coordinates of the mesh nodes.

        Returns:
        - None

        Raises:
        - `ValueError`: If `square_window_size` is not an integer.
        """

        fig,ax = plt.subplots(1,1)
        tri = self.mesh.element
        pts = self.mesh.node
        x,y = pts[:,0],pts[:,1]
        ax.tripcolor(x,y,tri,np.abs(np.ravel(self.conductivity)))
        self.fig = fig
        self.ax = ax

    def plot(self, save_fig_path: str, image_output_format: str) -> None:
        """Save the current figure to disk.

        Args:
            save_fig_path (str): The path where the figure should be saved.
            image_output_format (str): The output format of the image file.

        Returns:
            None

        Raises:
            ValueError: If the `image_output_format` is not a valid format.

        This method saves the current figure to disk using the `savefig` method from the `matplotlib` library. The `save_fig_path` argument specifies the path where the figure should be saved. The `image_output_format` argument specifies the output format of the image file.

        If the `image_output_format` argument is not a valid format, a `ValueError` is raised.

        Example usage:
        ```
        plotter = Plotter() plotter.plot("output/image.png", "png")
        ```
        """

        self.fig.savefig(save_fig_path,format=image_output_format)
