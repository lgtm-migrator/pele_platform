"""
Dictionary with valid flags for platform in input.yalm
"""


VALID_FLAGS_PLATFORM = {
    "system": "system",
    "residue": "resname",
    "chain": "chain",
    "hbond": "hbond",
    "test": "test",
    "pele": "pele",
    "forcefield": "forcefield",
    "verbose": "verbose",
    "anm_freq": "anm_freq",
    "mpi_params": "mpi_params",
    "sidechain_freq": "sidechain_freq",
    "min_freq": "min_freq",
    "temperature": "temperature",
    "sidechain_resolution": "sidechain_res",
    "steric_trials": "steric_trials",
    "overlap_factor": "overlap_factor",
    "steering": "steering",
    "solvent": "solvent",
    "usesrun": "usesrun",
    "spawning": "spawning",
    "iterations": "iterations",
    "pele_steps": "steps",
    "cpus": "cpus",
    "density": "density",
    "cluster_values": "cluster_values",
    "cluster_conditions": "cluster_conditions",
    "simulation_type": "simulation_type",
    "equilibration": "equilibration",
    "equilibration_mode": "equilibration_mode",
    "eq_steps": "equilibration_steps",
    "adaptive_restart": "adaptive_restart",
    "input": "global_inputs",
    "report_name": "report",
    "traj_name": "traj",
    "adaptive": "adaptive",
    "epsilon": "epsilon",
    "bias_column": "bias_column",
    "gridres": "gridres",
    "core": "core",
    "mtor": "maxtorsion",
    "n": "n",
    "template": "templates",
    "ext_temp": "template",
    "rotamers": "rotamers",
    "mae_lig": "mae_lig",
    "skip_prep": "skip_preprocess",
    "gaps_ter": "TERs",
    "charge_ter": "charge_ters",
    "nonstandard": "nonstandard",
    "prepwizard": "prepwizard",
    "box_center": "box_center",
    "box_radius": "box_radius",
    "box": "box",
    "native": "rmsd_pdb",
    "atom_dist": "atom_dist",
    "debug": "debug",
    "folder": "working_folder",
    "output": "output",
    "randomize": "randomize",
    "full": "global",
    "proximityDetection": "proximityDetection",
    "poses": "poses",
    "precision_glide": "precision_glide",
    "msm": "msm",
    "precision": "precision",
    "clust": "exit_clust",
    "restart": "restart",
    "lagtime": "lagtime",
    "msm_clust": "msm_clust",
    "rescoring": "rescoring",
    "in_out": "in_out",
    "in_out_soft": "in_out_soft",
    "exit": "exit",
    "exit_value": "exit_value",
    "exit_condition": "exit_condition",
    "exit_trajnum": "exit_trajnum",
    "waters": "waters",
    "water_empty_selector": "water_empty_selector",
    "water_freq": "water_freq",
    "water_center": "water_center",
    "clust_type": "clust_type",
    "water_temp": "water_temp",
    "water_overlap": "water_overlap",
    "water_constr": "water_constr",
    "water_trials": "water_trials",
    "water_radius": "water_radius",
    "out_in": "out_in",
    "orthosteric_site": "orthosteric_site",
    "final_site": "final_site",
    "initial_site": "initial_site",
    "induced_fit_exhaustive": "induced_fit_exhaustive",
    "induced_fit_fast": "induced_fit_fast",
    "frag": "frag",
    "ca_constr": "ca_constr",
    "ca_interval": "ca_interval",
    "one_exit": "one_exit",
    "box_type": "box_type",
    "box_metric": "box_metric",
    "time": "time",
    "nosasa": "nosasa",
    "perc_sasa": "perc_sasa",
    "seed": "seed",
    "pdb": "pdb",
    "log": "log",
    "nonrenum": "nonrenum",
    "pele_exec": "pele_exec",
    "pele_data": "pele_data",
    "pele_documents": "pele_documents",
    "pca": "pca",
    "anm_direction": "anm_direction",
    "anm_mix_modes": "anm_mix_modes",
    "anm_picking_mode": "anm_picking_mode",
    "anm_displacement": "anm_displacement",
    "anm_modes_change": "anm_modes_change",
    "anm_num_of_modes": "anm_num_of_modes",
    "anm_relaxation_constr": "anm_relaxation_constr",
    "skip_refinement": "skip_refinement",
    "remove_constraints": "remove_constraints",
    "pca_traj": "pca_traj",
    "perturbation": "perturbation",
    "binding_energy": "binding_energy",
    "sasa": "sasa",
    "parameters": "parameters",
    "analyse": "analyse",
    "selection_to_perturb": "selection_to_perturb",
    "mae": "mae",
    "constrain_core": "constrain_core",
    "skip_ligand_prep": "skip_ligand_prep",
    "spawning_condition": "spawning_condition",
    "external_constraints": "external_constraints",
    "only_analysis": "only_analysis",
    "overwrite": "overwrite_analysis",
    "analysis_nclust": "analysis_nclust",
    "te_column": "te_column",
    "be_column": "be_column",
    "limit_column": "limit_column",
    "com": "COMligandConstraint",
    "pele_license": "pele_license",
    "schrodinger": "schrodinger",
    "no_check": "no_check",
    "frag_core": "frag_core",
    "frag_input": "frag_input",
    "frag_ligands": "frag_ligands",
    "growing_steps": "growing_steps",
    "gpcr_orth": "gpcr_orth",
    "frag_steps": "steps_in_gs",
    "frag_eq_steps": "sampling_steps",
    "protocol": "protocol",
    "frag_ai": "frag_ai",
    "frag_ai_iterations": "frag_ai_iterations",
    "frag_run": "frag_run",
    "frag_restart": "frag_restart",
    "frag_output_folder": "frag_output_folder",
    "chain_core": "chain_core",
    "n_components": "n_components",
    "frag_criteria": "frag_criteria",
    "frag_cluster_folder": "frag_cluster_folder",
    "ppi": "ppi",
    "center_of_interface": "center_of_interface",
    "protein": "protein",
    "ligand_pdb": "ligand_pdb",
    "site_finder": "site_finder",
    "permissive_metal_constr": "permissive_metal_constr",
    "constrain_all_metals": "constrain_all_metals",
    "no_metal_constraints": "no_metal_constraints",
    "n_waters": "n_waters",
    "rna": "rna",
    "cleanup": "cleanup",
    "polarize_metals": "polarize_metals",
    "polarization_factor": "polarization_factor",
    "constrain_core_spring": "constrain_core_spring",
    "frag_library": "frag_library",
    "frag_core_atom": "frag_core_atom",
    "analysis_to_point": "analysis_to_point",
    "interaction_restrictions": "interaction_restrictions",
    "constraint_level": "constraint_level",
    "terminal_constr": "terminal_constr",
    "saturated_mutagenesis": "saturated_mutagenesis",
    "cpus_per_mutation": "cpus_per_mutation",
    "clustering_method": "clustering_method",
    "bandwidth": "bandwidth",
    "kde_structs": "kde_structs",
    "kde": "kde",
    "inter_step_logger": "inter_step_logger",
    "max_top_clusters": "max_top_clusters",
    "min_population": "min_population",
    "max_top_poses": "max_top_poses",
    "top_clusters_criterion": "top_clusters_criterion",
    "cluster_representatives_criterion": "cluster_representatives_criterion",
}
