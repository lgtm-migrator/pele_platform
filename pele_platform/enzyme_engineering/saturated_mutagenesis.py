from copy import deepcopy
import glob
from itertools import cycle
import os
import re
import shutil
import warnings

from pele_platform.Utilities.Parameters import parameters
from pele_platform.Utilities.Helpers import helpers
from pele_platform.Adaptive import simulation
from pele_platform.context import context


def set_starting_point(logged_subsets):
    indexes = [int(subset.replace("Subset_", "")) for subset in logged_subsets]
    next_index = max(indexes) + 1
    return next_index


class SaturatedMutagenesis:
    """
    Interface to run saturated mutagenesis simulation from another repository.
    """
    def __init__(self, start=1, subset_folder="Subset_"):
        self.already_computed = list()
        self.all_jobs = list()
        self.original_dir = os.path.abspath(os.getcwd())
        self.subset_folder = subset_folder
        self.start = start
        self.all_mutations = list()

    def run(self):
        """
        Runs the simulation for all inputs.

        Returns
        -------
        all_jobs : list
            A list of job parameters (EnviroBuilder objects) for each
            simulation subset
        """
        self.check_cpus()
        self.set_working_folder()
        self.all_mutations = self.retrieve_inputs()
        self.restart_checker()
        self.split_into_subsets()

        for idx, subset in enumerate(self.mutation_subsets, self.start):
            context.yaml_parser.no_metal_constraints = True  # TODO: need to investigate that
            context.yaml_parser.input = subset
            context.yaml_parser.cpus = context.yaml_parser.cpus_per_mutation * len(subset) + 1
            context.yaml_parser.folder = os.path.join(
                self.working_folder, "{}{}".format(self.subset_folder, idx)
            )
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAa context.yaml_parser.folder", context.yaml_parser.folder)
            print("AAAAAAAAAAAAAAAAAAAAA subset", subset)
            context.parameters_builder.build_adaptive_variables()
            context.parameters.create_files_and_folders()

            with helpers.cd(self.original_dir):
                simulation.run_adaptive()
                self.postprocessing(context.parameters)
                self.all_jobs.append(deepcopy(context.parameters))
                self.logger(context.parameters)

        return self.all_jobs

    def restart_checker(self):
        """
        If adaptive_restart: true, check which mutations were already
        completed based on the log file, get the right ID for the subset
        output folder and set adaptive_restart to False (since we're not
        restarting adaptive for real, just ignoring some input files).
        """
        logger_file = os.path.join(self.working_folder, "completed_mutations.log")
        logged_systems = []
        logged_subset_folders = []
        pattern = (
            r"Completed (?P<system>.+\.pdb) simulation .+ "
            + r"directory (?P<folder>Subset_\d+)"
        )

        # Check what systems and folders are already in the log
        if os.path.exists(logger_file) and context.yaml_parser.adaptive_restart:
            with open(logger_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    match = re.search(pattern, line)
                    logged_systems.append(match.group("system"))
                    logged_subset_folders.append(match.group("folder"))

            # Remove mutations that were already completed
            self.all_mutations = [
                mutation
                for mutation in self.all_mutations
                if os.path.basename(mutation) not in logged_systems
            ]

            # Remove subset folders that exist but were not completed
            # according to the log
            existing_subsets = glob.glob(
                os.path.join(self.working_folder, "{}*".format(self.subset_folder))
            )
            to_remove = [
                subset
                for subset in existing_subsets
                if os.path.basename(subset) not in logged_subset_folders
            ]

            for folder in to_remove:
                shutil.rmtree(folder)

            # Set parameters for the next run
            self.start = set_starting_point(logged_subset_folders)
            context.yaml_parser.adaptive_restart = False

    def postprocessing(self, job):
        """
        Matches output reports and trajectories with a particular system
        within the subset and copies them to the right folder.

        Parameters
        ----------
        job : parameters.Parameters
            Output job parameters.
        """
        output_path = os.path.join(job.pele_dir, job.output)
        reports_path = os.path.join(
            output_path, "[0-9]*", "{}*".format(job.report_name)
        )
        trajectory_path = os.path.join(output_path, "[0-9]*", "trajectory*")

        # Sort all trajectories and reports by their IDs
        sorted_reports = self.sort_numerically(reports_path)
        sorted_trajectories = self.sort_numerically(trajectory_path)

        new_dirs = [os.path.splitext(os.path.basename(file))[0] for file in job.input]
        abs_new_dirs = [os.path.join(output_path, path) for path in new_dirs]
        abs_new_dirs = abs_new_dirs[1:] + abs_new_dirs[:1]

        for folder in abs_new_dirs:
            os.mkdir(folder)

        for directory, report, traj in zip(
            cycle(abs_new_dirs), sorted_reports, sorted_trajectories
        ):
            shutil.move(report, directory)
            shutil.move(traj, directory)

    def logger(self, job):
        """
        Creates a logger file in the top level directory and appends the
        list of completed mutations after each run.

        Parameters
        ----------
        job: parameters.Parameters
            Object returned from simulation.run_adaptive
        """
        logger_file = os.path.join(self.working_folder, "completed_mutations.log")
        if isinstance(job.input, list):
            finished_systems = job.input
        else:
            finished_systems = [job.input]
        self.already_computed.extend(finished_systems)

        with open(logger_file, "a+") as logger:
            for inp in finished_systems:
                logger.write(
                    "Completed {} simulation in directory {}\n".format(
                        os.path.basename(inp), os.path.basename(job.pele_dir)
                    )
                )

    def retrieve_inputs(self):
        """
        Retrieve all inputs regardless of how they were defined in YAML.

        Returns
        -------
            List of strings containing paths to input PDBs.
        """
        if "*" in context.yaml_parser.system:
            all_mutations = glob.glob(context.yaml_parser.system)
        else:
            all_mutations = context.yaml_parser.system

        if isinstance(all_mutations, str):
            all_mutations = [all_mutations]

        return sorted(all_mutations)

    def split_into_subsets(self):
        """
        Finds all PDB files with mutations and splits them into subsets
        according to the available CPUs.
        """
        available_cpus = context.yaml_parser.cpus - 1
        if available_cpus % context.yaml_parser.cpus_per_mutation != 0:
            warnings.warn(
                "The total number of CPUs - 1 should be divisible by the "
                + "number of CPUs per mutation."
            )

        max_systems = int(available_cpus / context.yaml_parser.cpus_per_mutation)
        self.mutation_subsets = [
            self.all_mutations[i : i + max_systems]
            for i in range(0, len(self.all_mutations), max_systems)
        ]

    def check_cpus(self):
        """
        Checks if there are enough available CPUs.

        Raises
        ------
        ValueError if the number of CPUs per mutation is higher than the
            total number of available CPUs
        """
        if context.yaml_parser.cpus_per_mutation > context.yaml_parser.cpus - 1:
            raise ValueError(
                "The number of CPUs per mutation needs to be lower than "
                + "the total number of CPUs - 1."
            )

    def set_working_folder(self):
        """
        Sets top level working folder named after the residue (unless the
        user specified 'working_folder' in YAML. Folders for each mutation
        subset are enumerated automatically and placed within the top
        level directory.
        """
        resname_folder = os.path.abspath("{}_Pele".format(context.yaml_parser.residue))
        if not context.yaml_parser.folder:
            self.working_folder = (
                helpers.get_next_peledir(resname_folder)
                if not context.yaml_parser.adaptive_restart
                else helpers.get_latest_peledir(resname_folder)
            )
        else:
            self.working_folder = os.path.abspath(context.yaml_parser.folder)

    @staticmethod
    def sort_numerically(path):
        """
        Extracts IDs of reports or trajectories, uses them to sort the paths
        numerically, then returns sorted list.

        Parameters
        ----------
        path : str
            The pattern where to find the reports or trajectories that will
            be numerically sorted

        Returns
        -------
        sorted_list : list[str]
            The list of reports or trajectories numerically sorted
        """
        all_files = sorted(glob.glob(path))
        dictionary = {}

        for file in all_files:
            file_name = os.path.basename(file)
            key = re.findall(r"\d+", file_name)[0]
            dictionary[int(key)] = file

        sorted_dict = sorted(dictionary.items())
        sorted_list = [element[1] for element in sorted_dict]

        return sorted_list
