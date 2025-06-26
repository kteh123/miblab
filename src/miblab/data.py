import os
import zipfile
import subprocess
from .rat import RAT_PROJECTS
from tqdm import tqdm

# Try importing optional dependencies
try:
    import requests
    from osfclient.api import OSF
    from tqdm import tqdm
    import_error = False
except ImportError:
    import_error = True

# Zenodo DOI of the repository
DOI = {
    'MRR': "15285017",    
    'TRISTAN': "15301607", 
    'RAT': "10675642",     # Added for rat datasets from rat.py
}

# miblab datasets
DATASETS = {
    'KRUK.dmr.zip': {'doi': DOI['MRR']},
    'tristan_humans_healthy_controls.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_healthy_ciclosporin.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_healthy_metformin.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_healthy_rifampicin.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_patients_rifampicin.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_rats_healthy_multiple_dosing.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_rats_healthy_reproducibility.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_rats_healthy_six_drugs.dmr.zip': {'doi': DOI['TRISTAN']},
}

def zenodo_fetch(dataset:str, folder:str, doi:str=None, filename:str=None):
    """Download a dataset from Zenodo.

    Note if a dataset already exists locally it will not be downloaded 
    again and the existing file will be returned. 

    Args:
        dataset (str): Name of the dataset
        folder (str): Local folder where the result is to be saved
        doi (str, optional): Digital object identifier (DOI) of the 
          Zenodo repository where the dataset is uploaded. If this 
          is not provided, the function will look for the dataset in
          miblab's own Zenodo repositories.
        filename (str, optional): Filename of the downloaded dataset. 
          If this is not provided, then *dataset* is used as filename.

    Raises:
        NotImplementedError: If miblab is not installed with the data
          option
        requests.exceptions.ConnectionError: If the connection to 
          Zenodo cannot be made.

    Returns:
        str: Full path to the downloaded datafile.
    """
    if import_error:
        raise NotImplementedError(
            'Please install miblab as pip install miblab[data]'
            'to use this function.'
        )
        
    # Create filename 
    if filename is None:
        file = os.path.join(folder, dataset)
    else:
        file = os.path.join(folder, filename)

    # If it is already downloaded, use that.
    if os.path.exists(file):
        return file
    
    # Get DOI
    if doi is None:
        if dataset in DATASETS:
            doi = DATASETS[dataset]['doi']
        else:
            raise ValueError(
                f"{dataset} does not exist in one of the miblab "
                f"repositories on Zenodo. If you want to fetch " 
                f"a dataset in an external Zenodo repository, please "
                f"provide the doi of the repository."
            )
    
    # Dataset download link
    file_url = "https://zenodo.org/records/" + doi + "/files/" + dataset

    # Make the request and check for connection error
    try:
        file_response = requests.get(file_url) 
    except requests.exceptions.ConnectionError as err:
        raise requests.exceptions.ConnectionError(
            f"\n\n"
            f"A connection error occurred trying to download {dataset} "
            f"from Zenodo. This usually happens if you are offline."
            f"The detailed error message is here: {err}"
        ) 
    
    # Check for other errors
    file_response.raise_for_status()

    # Create the folder if needed
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(file, 'wb') as f:
        f.write(file_response.content)

    return file

def osf_fetch(dataset: str, folder: str, project: str = "un5ct", token: str = None, extract: bool = True, verbose: bool = True):
    """
    Download a dataset from OSF (Open Science Framework).

    This function downloads a specific dataset (folder or subfolder) from a public or private OSF project.
    Files are saved into the specified local directory. If a zip file is found, it will be extracted by default.

    Args:
        dataset (str): Subfolder path inside the OSF project. If an empty string, all files in the root will be downloaded (use with caution).
        folder (str): Local folder where the dataset will be saved.
        project (str, optional): OSF project ID (default is "un5ct").
        token (str, optional): Personal OSF token for accessing private projects. Read from OSF_TOKEN environment variable if needed.
        extract (bool, optional): Whether to automatically unzip downloaded .zip files (default is True).
        verbose (bool, optional): Whether to print progress messages (default is True).

    Raises:
        FileNotFoundError: If the specified dataset path does not exist in the OSF project.
        NotImplementedError: If required packages are not installed.

    Returns:
        str: Path to the local folder containing the downloaded data.

    Example:
        >>> from miblab import osf_fetch
        >>> osf_fetch('TRISTAN/RAT/bosentan_highdose/Sanofi', 'test_download')
    """
    if import_error:
        raise NotImplementedError(
            "Please install miblab as pip install miblab[data] to use this function."
        )

    # Prepare local folder
    os.makedirs(folder, exist_ok=True)

    # Connect to OSF and locate project storage
    osf = OSF(token=token)  #osf = OSF()  for public projects
    project = osf.project(project)
    storage = project.storage('osfstorage')

    # Navigate the dataset folder if provided
    current = storage
    if dataset:
        parts = dataset.strip('/').split('/')
        for part in parts:
            for f in current.folders:
                if f.name == part:
                    current = f
                    break
            else:
                raise FileNotFoundError(f"Folder '{part}' not found when navigating path '{dataset}'.")

    # Recursive download of all files and folders
    def download(current_folder, local_folder):
        os.makedirs(local_folder, exist_ok=True)
        files = list(current_folder.files)
        iterator = tqdm(files, desc=f"Downloading to {local_folder}") if verbose and files else files
        for file in iterator:
            local_file = os.path.join(local_folder, file.name)
            try:
                with open(local_file, 'wb') as f:
                    file.write_to(f)
            except Exception as e:
                if verbose:
                    print(f"Warning downloading {file.name}: {e}")

        for subfolder in current_folder.folders:
            download(subfolder, os.path.join(local_folder, subfolder.name))

    download(current, folder)

    # Extract all downloaded zip files if needed
    if extract:
        for dirpath, _, filenames in os.walk(folder):
            for filename in filenames:
                if filename.lower().endswith('.zip'):
                    zip_path = os.path.join(dirpath, filename)
                    extract_to = os.path.join(dirpath, filename[:-4])
                    os.makedirs(extract_to, exist_ok=True)
                    try:
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            bad_file = zip_ref.testzip()
                            if bad_file:
                                raise zipfile.BadZipFile(f"Corrupt file {bad_file} inside {zip_path}")
                            zip_ref.extractall(extract_to)
                        os.remove(zip_path)
                        if verbose:
                            print(f"Unzipped and deleted {zip_path}")
                    except Exception as e:
                        if verbose:
                            print(f"Warning unzipping {zip_path}: {e}")
    return folder

def osf_upload(folder: str, dataset: str, project: str = "un5ct", token: str = None, verbose: bool = True, overwrite: bool = True):
    """
    Upload a file to OSF (Open Science Framework) using osfclient.

    This function uploads a single local file to a specified path inside an OSF project.
    Intermediate folders must already exist in the OSF project; osfclient does not create them.
    If the file already exists, it can be overwritten or skipped.

    Args:
        folder (str): Path to the local file to upload.
        dataset (str): OSF path where the file should be placed (e.g., "Testing/filename.txt").
        project (str): OSF project ID (default: "un5ct").
        token (str): OSF personal token for private/write access.
        verbose (bool): Whether to print progress messages (default True).
        overwrite (bool): Whether to replace an existing file if it already exists (default True).

    Raises:
        FileNotFoundError: If the file does not exist.
        NotImplementedError: If osfclient is not installed.
        RuntimeError: If upload fails for any reason.

    Example:
        >>> from miblab import osf_upload
        >>> osf_upload(
        ...     folder='data/results.csv',
        ...     dataset='Testing/results.csv',
        ...     project='un5ct',
        ...     token='your-osf-token',
        ...     verbose=True,
        ...     overwrite=True
        ... )
    """
    import os

    # Check that optional dependencies are installed
    if import_error:
        raise NotImplementedError("Please install miblab[data] to use this function.")

    # Check that the specified local file exists
    if not os.path.isfile(folder):
        raise FileNotFoundError(f"Local file not found: {folder}")

    # Authenticate and connect to the OSF project
    from osfclient.api import OSF
    osf = OSF(token=token)
    project = osf.project(project)
    storage = project.storage("osfstorage")

    # Clean and prepare the remote dataset path
    full_path = dataset.strip("/")

    # Check if the file already exists on OSF
    existing = next((f for f in storage.files if f.path == "/" + full_path), None)
    if existing:
        if overwrite:
            if verbose:
                print(f"File '{full_path}' already exists. Deleting before re-upload...")
            try:
                existing.remove()
            except Exception as e:
                raise RuntimeError(f"Failed to delete existing file before overwrite: {e}")
        else:
            if verbose:
                print(f"File '{full_path}' already exists. Skipping (overwrite=False).")
            return

    # Upload the file
    size_mb = os.path.getsize(folder) / 1e6
    with open(folder, "rb") as f:
        if verbose:
            print(f"Uploading '{os.path.basename(folder)}' ({size_mb:.2f} MB) to '{full_path}'...")
        try:
            storage.create_file(full_path, f)
            if verbose:
                print("Upload complete.")
        except Exception as e:
            raise RuntimeError(f"Failed to upload file: {e}")
        
def rat_fetch(dataset: str = None, folder: str = ".", doi: str = None):
    """
    Download rat imaging datasets grouped by project using the registry in `rat.py`.

    This function allows you to download:
    - A **specific project group** (e.g., 'bosentan_highdose', 'relaxivity') containing several ZIP files.
    - **All available groups** by setting `dataset="all"` or `dataset=None`.

    Downloads are made from Zenodo using the provided or default DOI (`DOI['RAT']`).
    Files are stored in the specified local folder. If a file already exists, it is skipped.

    Args:
        dataset (str, optional): The group of ZIP files to download.
            - If None, defaults to "bosentan_highdose".
            - If "all", downloads all known groups in `RAT_PROJECTS`.
        folder (str): Local directory where downloaded files will be saved.
        doi (str, optional): Zenodo DOI to use. If not provided, uses `DOI['RAT']`.

    Raises:
        ValueError: If `dataset` is not a valid group name and not "all".
        NotImplementedError: If required dependencies (e.g. `requests`) are missing.
        ConnectionError: If there is a network issue or file fetch fails.

    Returns:
        list[str]: List of full paths to the downloaded ZIP files.

    Example:
        >>> from data import rat_fetch
        >>> rat_fetch("bosentan_highdose", "./downloads")      # Download just this group
        >>> rat_fetch("all", "./all_datasets")                 # Download all groups
        >>> rat_fetch(folder="./default")                      # Downloads bosentan_highdose by default
    """
    if import_error:
        raise NotImplementedError(
            'Please install miblab as pip install miblab[data] to use this function.'
        )

    # Default dataset group to 'bosentan_highdose' if not specified
    if not dataset:
        dataset = "bosentan_highdose"

    # Determine which groups to download based on the dataset argument
    if dataset.lower() == "all":
        groups_to_download = RAT_PROJECTS.keys()  # Download all groups
    elif dataset in RAT_PROJECTS:
        groups_to_download = [dataset]  # Download a specific group
    else:
        # Raise error for invalid group name
        raise ValueError(
            f"'{dataset}' is not a valid project group in RAT_PROJECTS. "
            f"Available groups: {', '.join(RAT_PROJECTS)}"
        )

    # Use the provided DOI or fall back to the default RAT DOI
    doi = doi or DOI['RAT']

    # Ensure the destination folder exists
    os.makedirs(folder, exist_ok=True)
    paths = []  # List to store local file paths of downloaded files

    # Loop through each selected group
    for group in groups_to_download:
        file_list = RAT_PROJECTS[group]

        # Initialize progress bar for each group
        for fname in tqdm(file_list, desc=f"Downloading group '{group}'"):
            url = f"https://zenodo.org/records/{doi}/files/{fname}"
            out_path = os.path.join(folder, fname)

            # Skip file if already downloaded
            if os.path.exists(out_path):
                paths.append(out_path)
                continue

            # Attempt to download the file
            try:
                response = requests.get(url)
                response.raise_for_status()
            except Exception as e:
                raise ConnectionError(f"Failed to fetch {fname} from Zenodo: {e}")

            # Save the file to disk
            with open(out_path, 'wb') as f:
                f.write(response.content)

            paths.append(out_path)

    return paths
