# Analysis-of-UK-School-Performance

An Exploratory Data Analysis (EDA) project interested in investigating the performance of primary schools in the UK, with a focus on the proportion of students with English as an aditional language (EAL).

To obtain the data for this EDA, I will first scrape the *gov.uk* website.

# Running the Code

The code in this repository was tested with Python 3.12. 

To run this code: 

1. Dowload and install [anaconda](https://www.anaconda.com/download).

2. Fork and clone this GitHub repo:
    - Click the [`Fork`](https://github.com/Adam-Calleja/Analysis-of-UK-School-Performance#fork-destination-box) button in the right-top corner of this page. 
    - Clone the repo, where `YourUsername` is yor GitHub username
    
        ```
        $ git clone https://github.com/YourUsername/Analysis-of-UK-School-Performance
        $cd Analysis-of-UK-School-Performance
        ```

    - Add the following to your remotes:

        ```
        $ git remote add upstream https://github.com/Adam-Calleja/Analysis-of-UK-School-Performance
        ```

3. Create a conda environment with all the required packages:

    ```
    $ conda env create -f environment.yml
    ```

4. Activate the conda environment.

    On Linux / Mac OS X:

    ```
    $ source activate UK-School-Analysis
    ```

    On Windows: 

    ```
    $ activate UK-School-Analysis
    ```

You can learn more about conda environments in the [Managing Environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment) section of the conda documentation. 

# Getting the latest code

If you followed all of the instructions above:

- forked the repo.
- cloned the repo.
added the `upstream` remote repository.

then you can always grab the latest code by running a git pull:

```
$ cd Analysis-of-UK-School-Performance
$ git pull upstream master
```

# Acknowledgements

Contains public sector information licensed under the Open Government Licence v3.0.
