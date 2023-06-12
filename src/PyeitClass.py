import pickle
import pyeit.mesh as mesh
import pyeit
import matplotlib.pyplot as plt

from AttributeContainerFactory import AttributeContainerFactory


class PyeitClass:
    def __init__(self):
        """initlize a instance of PyeitClass."""
        self.data = None
        self.mesh = None
        self.eit = None
        self.image = None

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

    def reconstruct(self):
        # Create mesh
        self.mesh = mesh.create(self.data['shape'], h0=None, p=0.2)

        # Perform image reconstruction
        self.eit = pyeit.eit(self.data['ex_mat'], self.data['eit_mat'], self.mesh, method='kotre')
        self.image = self.eit.solve()

    def render(self):
        # Render the image
        plt.imshow(self.image)

    def plot(self):
        # Save the image to the output directory
        plt.savefig('output_image.png')
