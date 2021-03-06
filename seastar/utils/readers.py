import os
import glob
import configparser
import xarray as xr


def _readConfig(config_file_path):
    """Reads the configuration ini file.

    :param config_file_path: path to the configuration file
    :type config_file_path: ``str``

    :return: the configuration object read from the lconfiguration file
    :rtype: ``configparser``

    :meta private:
    """

    configuration = configparser.ConfigParser()
    configuration.read(config_file_path)

    return configuration


def findNetCDFilepaths(directory_path, recursive=False):
    """Returns a list of netCDF files fom a given directory with
    a recursive option.

    :param directory_path: path to the directory to look in
    :type directory_path: ``str``

    :param recursive: whether to search in sub-directories
    :type recursive: ``boolean``, optional

    :return: a list of file paths with '.nc' extension that were found
    :rtype: ``list``
    """

    if not os.path.isdir(directory_path):
        print(f'WARNING: {directory_path} is not a directory')
        return []

    netCDF_filepaths = glob.glob(pathname=directory_path+'/*.nc',
                                 recursive=recursive)

    return netCDF_filepaths


def readNetCDFFile(netCFD_path):
    """Reads a netCDF file and returns it as an xarray.

    :param netCFD_path: path to the netCDF file
    :type netCFD_path: ``str``

    :raises: ``ValueError`` if file cannot be read as netCDF and \
    returns ``None`` object

    :return: xrray read from the netCDF file
    :rtype: ``xarray``
    """

    data_xr = None
    try:
        data_xr = xr.open_dataset(netCFD_path)

    except ValueError:
        print(f'WARNING "{netCFD_path}" is not a readable netCDF file')

    return data_xr


def doSomethingElse(data_xr):
    """Performs some examples on the data in the xarray.

    :param data_xr: the data to be processed
    :type data_xr: ``xarray``
    """

    attributes = data_xr.attrs
    for key in attributes.keys():
        print(f'\t{key}, {attributes[key]}')