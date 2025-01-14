version: 1.0.0

processed data: 10.5281/zenodo.14639522

The data and code are the supporting materials for the article "Prime editor-based high-throughput screening reveals functional synonymous mutations in the human genome."

## 1. Read count
Contains the read count of D0 and D35 for each cell line. This file is obtained from fastq, and the fastq files can be downloaded from the GSA website, GSA-Human: HRA007615.
Precise search is performed using regular expressions.

```python
RTT_PBS_linker_pattern = re.compile("GGTGC[ATGC]{34,39}CGCGG")
barcode_pattern = re.compile("AGAAT{4,}[ATCG]{4}CTCGA")
```


And a fuzzy search using blastn for the backbone is used, which can increase reads by approximately 5%.

## 2. epegRNA performance
The above read count is processed using [ZFC-eBAR](https://github.com/UronicAcid/ZFC-eBAR) 

## 3. Mutation performance
Each mutation retains a top score (best-performing epegRNA) and a top2mean score (the mean score of the top two epegRNAs).
The code can be found in top2mean.R.

## 4. Features

The collated features of all synonymous mutations. 

### (1) Dataset Construction
Deleterious synonymous mutations (defined as mean minus four standard deviations, mean – 4sd) were fully included to construct the dataset. Neutrality (defined as mean ± 1 standard deviation, mean ± 1sd) was randomly sampled at a ratio of 1:10, with random seeds fixed at 1:9 and 42.
The file also includes basic information for screening.

```
Related columns:
mutation_name
guide: PBS + RTT + linker
TTTTT: Whether the sequence contains poly T
transcript_mut
gene.y: Gene name
in_clinvar: Whether the mutation is in clinvar
in_synmicdb: Whether the mutation is in synmicdb
mutation_type
simple_name
mean_score: The average of the screening scores of the two best-performing epegRNAs
top_score: The best-performing epegRNA
enrich: Whether it is enriched during screening
median_lfc, min_lfc, max_lfc
mean_ctrl, mean_exp: The average read counts of ctrl (Day 0) and exp (Day 35) respectively
```
### (2) Feature Construction

  We selected feature candidate sets from several different sources:

- DepMap data: Downloaded Chronos Score, CERES Score, gene effect, dependency, and gene expression from DepMap (22Q2 and 24Q2).
    HCT116 uses the data from 22Q2, while other cell lines use the data from 24Q2.

```
Related columns: *_Chronos，*_CERES，*_expression
```
- HCT116 data: Calculated TPM (Transcripts Per Million) for AAVS1, PEmax, WT, and nontargeting using bulk RNA-seq in this study. Quality control was performed on raw data using FastQC (v0.11.9, http://www.bioinformatics.babraham.ac.uk/projects/fastqc/), and adapters were trimmed using fastp. The sequencing data was aligned to the genome using STAR, and TPM was obtained using RSEM.

```
Related columns: HCT116_NT_TPM, HCT116_WT_TPM, HCT116_SC19_TPM
```
- Codon frequencies: Obtained codon frequencies from http://www.kazusa.or.jp/codon/.	

```
Related columns: new_codon, old_codon, old_codon_freq, new_codon_freq, codon_freq_change, old_codon_norm_freq, new_codon_norm_freq, codon_freq_norm_change
```
- Splice site prediction: Used SpliceAI to predict splice site changes, generating eight values: DS_AG (Delta score, acceptor gain), DS_AL (Delta score, acceptor loss), DS_DG (Delta score, donor gain), DS_DL (Delta score, donor loss), DP_AG (Delta position, acceptor gain), DP_AL (Delta position, acceptor loss), DP_DG (Delta position, donor gain), DP_DL (Delta position, donor loss). The highest delta score among the four was taken as the splicing score. Delta scores range from 0 to 1, indicating the probability of splice changes. SpliceAI reference thresholds are 0.2 (high recall), 0.5 (recommended), and 0.8 (high precision).

```
Related columns:
- DS_AG, DS_AL, DS_DG, DS_DL, DP_AG, DP_AL, DP_DG, DP_DL
- splicing_score: the max of scores
```
- Splicing scores: Obtained splicing scores for corresponding tissues from AbSplice.

```
Related columns: AbSplice*
```
KYSE30: AbSplice_DNA_Esophagus_Muscularis
A549: AbSplice_DNA_Lung
HCT116: AbSplice_DNA_Colon_Transverse

- Synonymous mutation analysis: Used SilVA to analyze synonymous mutations 10, providing SilVA prediction scores and rankings, along with RSCU, dRSCU, GERP scores, CpG sites, exon CpG scores, SR, FAS6, MES, MEC, PESE, and PESS.

```
Related columns: silva*
```
- Transcript information: Recorded transcript length and the relative position of the site within the transcript.

```
Related columns: 
- gene_aa_num, position
- relativa_position: position / gene_aa_num
- annovar annotation: annovar_ExonicFunc.refGene, annovar_AAChange.refGene, transcript_exon_mut (not used but make sure the mutation is synonymous)
- old_codon_index3/new_codon_index3
```
- RNA folding: Predicted RNA folding energy using RNAfold, calculating free energy for mutated and wild-type transcripts, the change in energy, and the proportion of energy change.

```
Related columns:
- energy
- wildtype_energy
- energy_change, energy_change_ratio, energy_change_abs_ratio
```
- CADD scores: Recorded RawScore and PHRED from CADD.

```
Related columns: CADD*
```
### (3) Feature Selection
We calculated the significance of differences in screen scores between groups of synonymous mutations using a t-test, selecting a union of significant features across different cell lines, totaling 22 features. Numeric features were standardized using StandardScaler, and missing values were imputed with zero, assuming no specificity for these features. CatBoost handled categorical features directly, while for other models, “mutated codon position3” and “original codon position3” were transformed using one-hot encoding.

## 5. Model Testing
We tested SVM, RandomForest, GradientBoosting, LogisticRegression, KNN, NaiveBayes, LDA, XGBoost, LightGBM, and CatBoost, initially using default parameters. Five-fold cross-validation was used for evaluation, calculating AUC across ten dataset subsets.

## 6. CatBoost Parameter Tuning
Focusing on AUC as the primary performance metric, the model was set to run in silent mode to minimize output during training. The loss function was “Logloss,” with a depth of 6, “Uniform” feature_border_type, and “Depthwise” grow policy. The parameter search range included iterations, subsample size, random strength, column sampling rate, and L2 regularization strength, chosen to explore potential performance improvements. Grid Search with five-fold stratified cross-validation identified the optimal model configuration based on roc_auc scoring.
