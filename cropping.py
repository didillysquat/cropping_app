#!/usr/bin/env python3.6
import pandas as pd
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description='simple script for corpping the gaps on the begninning and end of alignments', epilog='For support email: benjamin.hume@kaust.edu.sa')
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-i', '--input', help='path to aligned fasta to crop', required=True)
    required_named.add_argument('-o', '--output', help='path to write out the cropped and aligned fasta to', required=True)

    args = parser.parse_args()

    # read in the path to the input fasta as list object
    try:
        fasta_to_crop = read_file_to_list(args.input)
    except:
        sys.exit('error reading in the aligned fasta')

    # input_path = '{}/test_fastas/tester_aligned.fasta'.format(os.getcwd())
    # output_path = '{}/test_fastas/tester_aligned_cropped.fasta'.format(os.getcwd())
    # try:
    #     fasta_to_crop = read_file_to_list(input_path)
    # except:
    #     sys.exit('error reading in the aligned fasta')

    # create a df from the fasta
    fasta_as_pandas_df = fasta_to_pandas_df(fasta_as_list=fasta_to_crop)

    # crop the df
    cropped_fasta_as_df = crop_aligned_fasta_df(aligned_fasta_as_pandas_df_to_crop=fasta_as_pandas_df)

    # convert the df back to list object ready to write out
    cropped_fasta_list = pandas_df_to_fasta(cropped_fasta_df=cropped_fasta_as_df)

    # now write out the corpped fasta list
    write_list_as_file_to_path(cropped_fasta_list, args.output)


def read_file_to_list(filename):
    with open(filename, mode='r') as f:
         return [line.rstrip() for line in f]

def write_list_as_file_to_path(file, path):
    with open(path, 'w') as f:
        for line in file:
            f.write('{}\n'.format(line))

def fasta_to_pandas_df(fasta_as_list):
    temp_df = pd.DataFrame([list(line) for line in fasta_as_list if not line.startswith('>')])
    seq_names = [line[1:] for line in fasta_as_list if line.startswith('>')]
    temp_df.index=seq_names
    return temp_df

def crop_aligned_fasta_df(aligned_fasta_as_pandas_df_to_crop):
    columns_to_drop = []
    for i in list(aligned_fasta_as_pandas_df_to_crop):
        # if there is a gap in the column at the beginning
        if '-' in list(aligned_fasta_as_pandas_df_to_crop[i]) or '*' in list(aligned_fasta_as_pandas_df_to_crop[i]):
            columns_to_drop.append(i)
        else:
            break
    for i in reversed(list(aligned_fasta_as_pandas_df_to_crop)):
        # if there is a gap in the column at the end
        if '-' in list(aligned_fasta_as_pandas_df_to_crop[i]) or '*' in list(aligned_fasta_as_pandas_df_to_crop[i]):
            columns_to_drop.append(i)
        else:
            break

    # get a list that is the columns indices that we want to keep
    col_to_keep = [col_index for col_index in list(aligned_fasta_as_pandas_df_to_crop) if col_index not in columns_to_drop]

    # drop the gap columns
    return aligned_fasta_as_pandas_df_to_crop[col_to_keep]

def pandas_df_to_fasta(cropped_fasta_df):
    temp_fasta = []
    for ind in cropped_fasta_df.index.tolist():
        temp_fasta.extend(['>{}'.format(ind), ''.join(list(cropped_fasta_df.loc[ind]))])
    return temp_fasta

main()