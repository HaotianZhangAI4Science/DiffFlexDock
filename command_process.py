import argparse

if '__name__' == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default='apo_time_split')
    args = parser.parse_args()
    name = args.name
    print(f'python esm_embedding_preparation.py --protein_ligand_csv /home/haotian/Molecule_Generation/ReDock-master/data/{name}.csv --out_file /home/haotian/Molecule_Generation/ReDock-master/data/{name}_esm.fasta')
    print(f'HOME=esm-main/model_weights python esm-main/scripts/extract.py esm2_t33_650M_UR50D data/{name}_esm.fasta data/{name}_ems_embeddings --repr_layers 33 --include per_tok')
    print(f'python -m ReDock_evaluate --protein_ligand_csv data/{name}.csv --out_dir results/{name} --inference_steps 20 --samples_per_complex 40 --batch_size 40 --model_dir ReDock_baseline --ckpt best_ema_inference_epoch_model.pt --actual_steps 18 --no_final_step_noise --num_workers 1 --esm_embeddings_path data/{name}_ems_embeddings --save_all')