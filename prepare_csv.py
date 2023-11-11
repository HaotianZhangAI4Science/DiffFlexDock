from multiprocessing import Pool
import subprocess
from glob import glob
import os.path as osp
from tqdm import tqdm
import argparse
from rdkit import Chem
import pandas as pd

def execute_command(pdb_file):
    pdb_out_file = pdb_file[:-4] + '_added.pdb'
    command = f'pdbfixer {pdb_file} --output {pdb_out_file} --replace-nonstandard --add-atoms=all --add-residues'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return f'Execution failed for {pdb_file}. Error: {result.stderr}'
    return f'Execution successful for {pdb_file}'

def read_sdf(sdf_file):
    supp = Chem.SDMolSupplier(sdf_file)
    mols_list = [i for i in supp]
    return mols_list

def write_sdf(mol_list,file, voice=False):
    writer = Chem.SDWriter(file)
    mol_cnt = 0
    for i in mol_list:
        try:
            writer.write(i)
            mol_cnt+=1
        except:
            pass
    writer.close()
    if voice: 
        print('Write {} molecules to {}'.format(mol_cnt,file))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--complex_path', type=str, default='/home/haotian/Molecule_Generation/Flexible-docking/data/apo_time_split')
    parser.add_argument('--pdb_suffix', type=str, default='_apo_added.pdb')
    parser.add_argument('--ligand_suffix', type=str, default='_ligand.sdf')
    parser.add_argument('--csv_name', type=str, default='apo_time_split.csv')
    args = parser.parse_args()

    targets = glob(osp.join(args.complex_path,"*") )

    pdb_files = []
    ligand_files = []
    for target in targets:
        pdb_file = glob(osp.join(target, '*' + args.pdb_suffix))
        ligand_file = glob(osp.join(target, '*' + args.ligand_suffix))
        if len(pdb_file) == 0 or len(ligand_file) == 0:
            continue
        pdb_files.append(pdb_file[0])
        ligand_files.append(ligand_file[0])
    
    complex_names = []
    for i in range(len(pdb_files)):
        protein_path = pdb_files[i]
        ligand_description = ligand_files[i]
        complext_name = osp.basename(protein_path).split('.')[0] +'_' +osp.basename(ligand_description).split('.')[0] 
        complex_names.append(complext_name)

    assert len(pdb_files) == len(ligand_files)

    # 创建一个DataFrame
    df = pd.DataFrame({
        'complex_name': complex_names,
        'protein_path': pdb_files,
        'ligand_description': ligand_files,
        'protein_sequence': 'NaN'  # 使用'NaN'作为缺省值
    })

    # 将DataFrame保存为CSV文件
    df.to_csv(args.csv_name, index=False)
