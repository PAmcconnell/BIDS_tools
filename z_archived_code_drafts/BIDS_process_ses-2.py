import argparse
import subprocess
import os

def execute_commands(sourcedata_root_dir, subject_id, session_id):
    commands = [
        "process_T1.py",
        "process_func_learn.py",
        "process_fmap_gre_ses_2.py",
        "process_fmap_EPI_ses_2.py",
        "process_func_learn_beh.py"
    ]
    
    base_command = "python ~/Documents/MATLAB/software/iNR/BIDS_tools/{} {}{}/{}/dicom_sorted/ ~/Documents/MRI/LEARN/BIDS_test/dataset"
    base_command_beh = "python ~/Documents/MATLAB/software/iNR/BIDS_tools/{} {}{}/{}/beh/preprocessed/ ~/Documents/MRI/LEARN/BIDS_test/dataset"

    # Determine bids_root_dir by going up two levels from sourcedata_root_dir and into the dataset directory
    bids_root_dir = os.path.join(os.path.dirname(os.path.dirname(sourcedata_root_dir)), 'dataset')

    # Check if the directory exists in bids_root_dir, if not create it
    dir_to_create = os.path.join(bids_root_dir, subject_id, session_id)
    os.makedirs(dir_to_create, exist_ok=True)
    
    for command in commands:
        if command == "process_func_learn_beh.py":
            cmd = base_command_beh.format(command, sourcedata_root_dir, subject_id, session_id)
        else:
            cmd = base_command.format(command, sourcedata_root_dir, subject_id, session_id)
        
        print(f"Executing: {cmd}")
        # Uncomment the following line to actually execute the commands
        subprocess.run(cmd, shell=True)
    
    # Change the working directory to bids_root_dir and execute the cubids-validate command
    os.chdir(bids_root_dir)
    print(f"Current working directory: {os.getcwd()}")  # Debugging line to print current directory
    
    # Using the full path of cubids-validate and cubids-add-nifti-info
    cubids_add_nii_hdr_path = "~/anaconda3/envs/fmri/bin/cubids-add-nifti-info"
    cubids_add_nii_hdr_command = f"python {cubids_add_nii_hdr_path} {bids_root_dir}"
    cubids_validate_path = "~/anaconda3/envs/fmri/bin/cubids-validate"
    cubids_validate_command = f"python {cubids_validate_path} {bids_root_dir} cubids"

    
    print(f"Executing: {cubids_add_nii_hdr_command}")
    # Uncomment the following line to actually execute the command
    subprocess.run(cubids_add_nii_hdr_command, shell=True)

    print(f"Executing: {cubids_validate_command}")
    # Uncomment the following line to actually execute the command
    subprocess.run(cubids_validate_command, shell=True)

# Main code execution begins here
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Execute processing commands.')
    parser.add_argument('sourcedata_root_dir', type=str, help='Path to the sourcedata root directory.')
    parser.add_argument('subject_id', type=str, help='Subject ID.')
    parser.add_argument('session_id', type=str, help='Session ID.')
    
    args = parser.parse_args()
    
    execute_commands(args.sourcedata_root_dir, args.subject_id, args.session_id)
