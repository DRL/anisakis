#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os, re, sys, argparse, subprocess
from progressbar import Bar, Percentage, ProgressBar, ETA

def parse_query_file(query_file):
	'''Parses query_file and write to temp file'''
	seq_id = ''
	seq = ''
	dataset = {}
	with open(query_file) as fh_in :
		for line in fh_in:
			if line.startswith(">"):
				seq_count += 1
				seq_id = line.lstrip(">").rstrip("\n")
				sys.exit("[ERROR] - " + seq_id + " is duplicated.") if seq_id in dataset
				if (seq):	
					dataset[seq_id] = {}
					dataset[seq_id]['seq'] = seq
					dataset[seq_id]['tax'] = 'N/A'
					dataset[seq_id]['hits'] = set()
					dataset[seq_id]['hit_by'] = set()
					seq = ''
			else:
				seq += line.rstrip("\n")

		sys.exit("[ERROR] - " + seq_id + " is duplicated.") if seq_id in dataset
		if (seq):	
			dataset[seq_id] = {}
			dataset[seq_id]['seq'] = seq
			dataset[seq_id]['tax'] = 'N/A'
			dataset[seq_id]['hits'] = set()
			dataset[seq_id]['hit_by'] = set()
			seq = ''

	return dataset

def parse_blob_file(blob_file, dataset):
	with open(blob_file) as fh_in :
		for line in fh_in:
			if not line.startswith("id"):
				field = line.split("\t")
				seq_id = field[0]
				tax = field[4].split(";")[2].replace("phylum=", "")
				sys.exit("[ERROR] - " + seq_id + " not in assembly.") if not seq_id in dataset
				dataset[seq_id]['tax'] = tax
	return dataset

def analyse_blast_file(blast_file, data):

	dataset = ''
	with open(blast_file) as fh_in :
		for line in fh_in:
			field = line.split("\t")
			query, subject = field[0], field[1]
			if query in data['A']:
				if float(fields[10]) <= float(eval_threshold) and int(fields[12]) >= int(len_threshold): # eval threshold + query len threshold
					data['A'][query]['hits'].add(subject)
					data['B'][query]['hit_by'].add(subject)
			elif query in data['B']:
				if float(fields[10]) <= float(eval_threshold) and int(fields[12]) >= int(len_threshold): # eval threshold + query len threshold
					data['B'][query]['hits'].add(subject)
					data['A'][query]['hit_by'].add(subject)
			else:
				sys.exit("[ERROR] - " + field[0] + " not in assembly.")

def count_contigs_with_tax(dataset):
	contigs_with_tax = 0
	for seq_id in dataset:
		if dataset[seq_id]['tax'] == 'N/A':
			pass
		else:
			contigs_with_tax += 1
	return contigs_with_tax

def count_contigs_hit_by(dataset):
	contigs_hit_by = 0
	for seq_id in dataset:
		if len(dataset[seq_id]['hit_by']) == 0:
			pass
		else:
			contigs_hit_by += 1
	return contigs_hit_by

def count_reciprocal_best_hits(data):
	reciprocal_best_hits = 0
	for seq_id in data['A']:
		if len(data['A'][seq_id]['hits']) == 0:
			pass
		elif len(data['A'][seq_id]['hit_by']) == 0:
			pass
		else:
			print seqid 
			print data['A'][seq_id]['hit']
			print data['A'][seq_id]['hit_by'] 
			reciprocal_best_hits += 1
	return reciprocal_best_hits

def count_data(data):
	contigs_in_A = len(data['A'])
	contigs_in_B = len(data['B'])
	contigs_in_A_with_tax = count_contigs_with_tax(data['A'])
	contigs_in_B_with_tax = count_contigs_with_tax(data['B'])
	contigs_in_A_without_tax = contigs_in_A - contigs_in_A_with_tax
	contigs_in_B_without_tax = contigs_in_B - contigs_in_B_with_tax
	contigs_in_A_hit_by_B = count_contigs_hit_by(data['A'])
	contigs_in_B_hit_by_A = count_contigs_hit_by(data['B'])
	contigs_reciprocal = count_reciprocal_best_hits(data)

if __name__ == '__main__':

	assembly_A = sys.argv[1]
	assembly_B = sys.argv[2]

	blast_A = sys.argv[3]
	blast_B = sys.argv[4]
	
	blob_A = sys.argv[5]
	blob_B = sys.argv[6]

	data = {}
	data['A'] = parse_query_file(assembly_A)
	data['B'] = parse_query_file(assembly_B)

	data['A'] = parse_blob_file(blob_A, data['A'])
	data['B'] = parse_blob_file(blob_B, data['B'])

	data = analyse_blast_file(blast_A, data)
	data = analyse_blast_file(blast_A, data)

	count_data(data)