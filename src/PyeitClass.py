import pickle
import pyeit.mesh as mesh
import pyeit
import matplotlib.pyplot as plt

from AttributeContainerFactory import AttributeContainerFactory


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
        
        factory = AttributeContainerFactory()
        
        try:
            self.data = factory.load(filename)
        except FileNotFoundError:
            print("Input file not found: {}".format(filename))
        except ValueError as e:
            print("Error loading data: {}".format(str(e)))
        except:
            print("Unknown error loading data")
        
        return

    def reconstruct(self, reconstruction_algorithm_choice='kotre'):
        """Performs image reconstruction based on the EIT data and mesh.

        Args:
            reconstruction_algorithm_choice (str, optional): The choice of reconstruction algorithm. Defaults to 'kotre'.
        """
        try:
            # Create mesh
            self.mesh = mesh.create(self.data['shape'], h0=None, p=0.2)

            # Perform image reconstruction using the chosen algorithm
            if reconstruction_algorithm_choice == 'kotre':
                self.eit = pyeit.eit(self.data['ex_mat'], self.data['eit_mat'], self.mesh, method='kotre')
            elif reconstruction_algorithm_choice == 'greit':
                self.eit = pyeit.eit(self.data['ex_mat'], self.data['eit_mat'], self.mesh, method='greit')
            else:
                raise ValueError(f"Invalid reconstruction algorithm: {reconstruction_algorithm_choice}")
            
            self.image = self.eit.solve()
        except Exception as e:
            print(f"Error performing image reconstruction: {e}")

    # TODO: need to implement
    def render(self, square_window_size):
        pass

    # TODO: need to implement
    def plot(self,image_output_format):
        pass
