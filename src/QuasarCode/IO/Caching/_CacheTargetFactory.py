from ._CacheTarget import CacheTarget

class CacheTargetFactory(object):
    """
    A factory class for creating cache targets with common path templates.

    Parameters:
        str filename_template:
            The template for the (relative) file path of cache targets.
            It should contain format placeholders for the labels using the names of each label provided to 'label_names'.
            This path will be relative to the cache directory and, as such, should have no drive component or preceding "/".
        (args) tuple[str,...] label_names:
            The names of the labels that will be used to create the file path.

    Examples:
        ```
        ctf = CacheTargetFactory(
            "{software_name}/{run_name}/{name}.pickle",
            "software_name", "run_name", "name"
        )
        ctf.new(software_name="MySoftware", run_name="Run1", name="DataFile")
        # target a file at: {cache-directory}/MySoftware/Run1/DataFile.pickle
        ```
    """

    def __init__(self, filename_template: str, *label_names: str) -> None:
        self.__relative_filepath_template: str = filename_template
        self.__label_names: tuple[str, ...] = label_names

    def new(self, **labels: str) -> CacheTarget:
        """
        Creates a new CacheTarget instance using the provided labels.

        Parameters:
            (kwargs) dict[str,str] labels: A dictionary of label names and their corresponding values.
                Each label name specified in the constructor must be provided.

        Returns:
            CacheTarget -> A new CacheTarget instance.

        Raises:
            KeyError:
                If a required label is missing from the provided labels.
                See 'label_names' for the required labels.
        """
        for label_name in self.__label_names:
            if label_name not in labels:
                raise KeyError(f"No value provided for required label \"{label_name}\".")
        return CacheTarget(self.__relative_filepath_template.format(**{ label_name : labels[label_name] for label_name in self.__label_names }))

    @property
    def label_names(self) -> tuple[str, ...]:
        """
        The name of each label requiring an argument when creating a new cache target.

        Returns:
            tuple[str,...] -> A tuple containing the label names as strings.
        """
        return self.__label_names
    
    @property
    def template(self) -> str:
        """
        The template used to create the file path for the cache target.

        Returns:
            str -> The template string.
        """
        return self.__relative_filepath_template
