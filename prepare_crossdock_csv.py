from multiprocessing import Pool
import subprocess
from glob import glob
import os.path as osp
from tqdm import tqdm
import argparse
from rdkit import Chem
import pandas as pd
import pickle

def read_pkl(pkl_file):
    with open(pkl_file, 'rb') as f:
        data = pickle.load(f)
    return data
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
    parser.add_argument('--complex_path', type=str, default='/home/haotian/Molecule_Generation/Flexible-docking/data/crossdock')
    parser.add_argument('--index_path', type=str, default='/home/haotian/Molecule_Generation/Flexible-docking/data/crossdock_index.pkl')
    parser.add_argument('--start', type=int, default=5)
    parser.add_argument('--end', type=int, default=10)
    args = parser.parse_args()

    crossdock_index = read_pkl(args.index_path)
    target_names = list(crossdock_index.keys())
    target_used = target_names[args.start:args.end]

    complex_names = []
    protein_paths = []
    ligand_descriptions = []
    for target_name in target_used:
        for item in crossdock_index[target_name]:
            protein_path = item[0]
            ligand_description = item[1]
            complext_name = osp.basename(protein_path).split('.')[0] +'_' +osp.basename(ligand_description).split('.')[0] 
            complex_names.append(complext_name)
            protein_paths.append(osp.join(args.complex_path, protein_path))
            ligand_descriptions.append(osp.join(args.complex_path, ligand_description))

    df = pd.DataFrame({
        'complex_name': complex_names,
        'protein_path': protein_paths,
        'ligand_description': ligand_descriptions,
        'protein_sequence': 'NaN'  # 使用'NaN'作为缺省值
    })

    df.to_csv(f'./crossdock_{args.start}_{args.end}.csv', index=False)
