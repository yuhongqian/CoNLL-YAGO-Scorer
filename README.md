# CoNLL-YAGO-Scorer

This is a scorer for the [CoNLL-YAGO](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/ambiverse-nlu/aida/ "CoNLL-YAGO") entity linking dataset. 

The scorer outputs the **micro average**, which is defined to be: true positive/(true positive + negative positive) 

### Running the Scorer 
To run the scorer, you need the gold-standard file distributed as part of the CoNLL-YAGO dataset. Once the dataset is downloaded, the file can be found under` aida-yago2-dataset/AIDA-YAGO2-annotations.tsv`. 

While CoNLL-YAGO dataset contains a blank line between every two adjacent files, the scorer assumes no such blank line in the system output. Also, the scorer only evaluates the correctness of index (0th column) and Wikipedia entity name (column 1). Therefore, only these two columns are required. The following example shows an expected output format: 
```
-DOCSTART- (1 topic)
1	China 
3	United_States
4	--NME--
-DOCSTART- (2 topic)
10	Michael_Jordan
12	--NME--
20	National_Basketball_Association
...
```


Assuming your system output is under` ./output/system_output.tsv`, the following is a sample script to run the scorer: 
```bash
python yagoScorer.py \
  --gold_std="./aida-yago2-dataset/AIDA-YAGO2-annotations-trunc.tsv"  \
  --system_out="./output/system_output.tsv" \
  --report="./output/report.txt"
```
