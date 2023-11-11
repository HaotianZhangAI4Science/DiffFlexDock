from multiprocessing import Pool
import subprocess
from glob import glob
import os.path as osp
from tqdm import tqdm
import argparse
from rdkit import Chem

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
    # preprocess the pdb and ligand files for successful parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--complex_path', type=str, default='./apo_time_split')
    parser.add_argument('--pdb_suffix', type=str, default='_apo.pdb')
    parser.add_argument('--ligand_suffix', type=str, default='_ligand.sdf')
    args = parser.parse_args()

    targets = glob(osp.join(args.complex_path),"*" )

    pdb_files = []
    for target in targets:
        pdb_files.extend(glob(osp.join(target, f'*{args.pdb_suffix}')))

    pool = Pool(processes=12)
    results = list(tqdm(pool.imap(execute_command, pdb_files), total=len(pdb_files)))
    pool.close()
    pool.join()
    for result in results:
        print(result)
    
    for target in targets:
        ligand_files = glob(osp.join(target, '*'+args.ligand_suffix))
        if len(ligand_files) == 0:
            continue
        if args.ligand_suffix[-4:] == '.sdf':
            mol = read_sdf(ligand_files[0])
        elif args.ligand_suffix[-4:] == 'mol2':
            mol = Chem.MolFromMol2File(ligand_files[0])
        else:
            raise NotImplementedError('Only support sdf and mol2 file')
        if mol is None:
            continue
        ligand_prefix = ligand_files[0][:-4]
        write_sdf([mol], osp.join(target, ligand_prefix+'_ligand.sdf'))




