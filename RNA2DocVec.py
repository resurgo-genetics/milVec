import sys
from gensim.models import Word2Vec
import pandas as pd
import numpy as np
import pickle
import pdb

min_count = 5
dims = [50,]
windows = [5,]
allWeights = []

def get_6_trids():
    nucle_com = []
    chars = ['A', 'C', 'G', 'U']
    base=len(chars)
    end=len(chars)**6
    for i in range(0,end):
        n=i
        ch0=chars[n%base]
        n=n/base
        ch1=chars[n%base]
        n=n/base
        ch2=chars[n%base]
        n=n/base
        ch3=chars[n%base]
        n=n/base
        ch4=chars[n%base]
        n=n/base
        ch5=chars[n%base]
        nucle_com.append(ch0 + ch1 + ch2 + ch3 + ch4 + ch5)
    return  nucle_com   

def get_7_trids():
    nucle_com = []
    chars = ['A', 'C', 'G', 'U']
    base=len(chars)
    end=len(chars)**7
    for i in range(0,end):
        n=i
        ch0=chars[n%base]
        n=n/base
        ch1=chars[n%base]
        n=n/base
        ch2=chars[n%base]
        n=n/base
        ch3=chars[n%base]
        n=n/base
        ch4=chars[n%base]
        n=n/base
        ch5=chars[n%base]
        n=n/base
        ch6=chars[n%base]
        nucle_com.append(ch0 + ch1 + ch2 + ch3 + ch4 + ch5 + ch6)
    return  nucle_com   

def get_4_nucleotide_composition(tris, seq):
    seq_len = len(seq)
    tri_feature = []
    k = len(tris[0])
    #tmp_fea = [0] * len(tris)
    for x in range(len(seq) + 1- k):
        kmer = seq[x:x+k]
        if kmer in tris:
            ind = tris.index(kmer)
            tri_feature.append(str(ind))
    #tri_feature = [float(val)/seq_len for val in tmp_fea]
        #pdb.set_trace()        
    return tri_feature

def test_rna():
    tris = get_6_trids()
    seq = 'GGCAGCCCATCTGGGGGGCCTGTAGGGGCTGCCGGGCTGGTGGCCAGTGTTTCCACCTCCCTGGCAGTCAGGCCTAGAGGCTGGCGTCTGTGCAGTTGGGGGAGGCAGTAGACACGGGACAGGCTTTATTATTTATTTTTCAGCATGAAAGAC'
    seq = seq.replace('T', 'U')
    pdb.set_trace()
    trvec = get_4_nucleotide_composition(tris, seq)

def read_RNA_fasta_file(fasta_file):
    seq_dict = {}    
    fp = open(fasta_file, 'r')
    name = ''
    for line in fp:
        #let's discard the newline at the end (if any)
        line = line.rstrip()
        #distinguish header from sequence
        if line[0]=='>': #or line.startswith('>')
            #it is the header
            name = line[1:] #discarding the initial >
            seq_dict[name] = ''
        else:
            #it is sequence
            seq_dict[name] = seq_dict[name] + line.upper().replace('T', 'U')
    fp.close()
    
    return seq_dict

def read_fasta_file(fasta_file):
    seq_dict = {}    
    fp = open(fasta_file, 'r')
    name = ''
    for line in fp:
        #let's discard the newline at the end (if any)
        line = line.rstrip()
        #distinguish header from sequence
        if line[0]=='>': #or line.startswith('>')
            #it is the header
            name = line[1:] #discarding the initial >
            seq_dict[name] = ''
        else:
            #it is sequence
            seq_dict[name] = seq_dict[name] + line.upper()
    fp.close()
    
    return seq_dict

def train_rnas(seq_file = 'utrs.fa', outfile= 'rnadocEmbedding25.pickle'):
    min_count = 5
    dim = 25
    window = 5

    print('dim: ' + str(dim) + ', window: ' + str(window))
    seq_dict = read_fasta_file(seq_file)
    
    #text = seq_dict.values()
    tris = get_6_trids()
    sentences = []
    for seq in seq_dict.values():
        seq = seq.replace('T', 'U')
        trvec = get_4_nucleotide_composition(tris, seq)
        
        #for aa in range(len(text)):
        sentences.append(trvec)
    #pdb.set_trace()
    print(len(sentences))
    model = None
    #model = Word2Vec(sentences, min_count=min_count, size=dim, window=window, sg=1, iter = 10, batch_words=100)
    model = gensim.models.doc2vec.Doc2Vec(size=50, min_count=2, iter=55)
    model.build_vocab(train_corpus)
    model.train(train_corpus)
    '''vocab = list(model.vocab.keys())
    print vocab
    fw = open('rna_doc_dict', 'w')
    for val in vocab:
        fw.write(val + '\n')
    fw.close()
    #print model.syn0
    #pdb.set_trace()
    embeddingWeights = np.empty([len(vocab), dim])

    for i in range(len(vocab)):
        embeddingWeights[i,:] = model[vocab[i]]  

    allWeights.append(embeddingWeights)

    '''
    #model.infer_vector(['only', 'you', 'can', 'prevent', 'forrest', 'fires'])
    #with open(outfile, 'w') as f:
    #    pickle.dump(model, f)
    # store the model to mmap-able files
    model.save(outfile)
    # load the model back
    model_loaded = Doc2Vec.load(outfile)


if __name__ == "__main__":
    #test_rna()
    input_file = sys.argv[1]
    train_rnas(input_file)
