# DiffFlexDock

Prepare the Input

Use pdbfixer and rdkit to process the raw complex data. The default format can be found in the ./example/apo_time_split.

```shell
# change the pdb and ligand suffix in the script. Default is _protein.pdb _ligand.sdf  
python pdbprocessing.py --complex_path './apo_time_split' --pdb_suffix '_apo.pdb' --ligand_suffix '_ligand.sdf'
# the processed pdb will be saved automatically as pdb_file[:-4] + '_added.pdb'
```

prepare csv file for the input. The raw data can be downloaded [here](https://doi.org/10.5281/zenodo.10205365).  

```shell
python prepare_csv.py --complex_path './apo_time_split' --pdb_suffix '_apo_added.pdb' --ligand_suffix '_ligand.sdf' --csv_name apo_time_split

# for the crossdock dataset, since it will output num_pdb*2 complex, so we select several targets for testing, default is 5-10.  
python prepare_crossdock_csv.py --complex_path './crossdock' --index_path './crossdock_index.pkl' --start 5 --end 10
```

After getting the csv file, we know the complex name and the corresponding pdb and sdf paths. Then we need to prepare the fasta file for ESM embedding, generate ESM embedding, and perform the DiffFlexDock. 

```shell
python command_process.py --name apo_time_split
```

It will print three commands, and run them one by one in the terminal. 

For example

```shell
# generate the fasta file for esm embedding
python esm_embedding_preparation.py --protein_ligand_csv /home/haotian/Molecule_Generation/ReDock-master/data/apo_time_split.csv --out_file /home/haotian/Molecule_Generation/ReDock-master/data/apo_time_split_esm.fasta
# generate the esm embedding 
python esm_embedding_preparation.py --protein_ligand_csv /home/haotian/Molecule_Generation/ReDock-master/data/apo_time_split.csv --out_file /home/haotian/Molecule_Generation/ReDock-master/data/apo_time_split_esm.fasta
# perform DiffFlexDock
python -m ReDock_evaluate --protein_ligand_csv data/apo_time_split.csv --out_dir results/apo_time_split --inference_steps 20 --samples_per_complex 40 --batch_size 40 --model_dir ReDock_baseline --ckpt best_ema_inference_epoch_model.pt --actual_steps 18 --no_final_step_noise --num_workers 1 --esm_embeddings_path data/apo_time_split_ems_embeddings --save_all
```