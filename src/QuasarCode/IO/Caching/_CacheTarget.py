import os
import pickle

class CacheTarget(object):
    """
    A class to manage caching of data to and from pickle files.

    Parameters:
        str relative_file_path:
            The relative file path to the cache file.
            This path is relative to the root directory provided when saving or loading data.
    """

    def __init__(self, relative_file_path: str) -> None:
        self.__relative_file_path: str = relative_file_path

    @property
    def relative_filepath(self) -> str:
        """
        The relative file path to the cache file.

        Returns:
            str -> The relative file path as a string.
        """
        return self.__relative_file_path
    
    def get_filepath(self, root_directory: str) -> str:
        """
        Constructs a full file path by combining the provided root directory 
        with the relative file path of the cache target.

        Parameters:
            str root_directory:
                The root directory to which the relative file path will be appended.

        Returns:
            str -> The full file path constructed from the root directory and 
                 the relative file path.
        """
        return os.path.join(root_directory, self.__relative_file_path)
    
    def save_data(self, root_directory: str, data: dict[str, object]) -> None:
        """
        Save data to a pickle file using this target from a given root directory.

        Parameters:
            str root_directory:
                The root directory to which the relative file path will be appended.
        """
        filepath = self.get_filepath(os.path.abspath(root_directory))
        directory = os.path.dirname(self.get_filepath(root_directory))
        if not os.path.exists(directory):
            paths_to_make = []
            test_path = directory
            while not os.path.exists(test_path):
                paths_to_make.append(test_path)
                test_path = os.path.dirname(test_path)
            for path in paths_to_make[::-1]:
                os.mkdir(path)
        with open(filepath, "wb") as file:
            pickle.dump(data, file)

    def load_data(self, root_directory: str) -> dict[str, object]:
        """
        Load data from a pickle file using this target from a given root directory.

        Parameters:
            str root_directory:
                The root directory to which the relative file path will be appended.

        Returns:
            dict[str, object] -> The data loaded from the pickle file.
        """
        filepath = self.get_filepath(os.path.abspath(root_directory))
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Unable to locate cache file at \"{filepath}\".")
        with open(filepath, "rb") as file:
            return pickle.load(file)
