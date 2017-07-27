## Run Many ANI comparisons on CHTC

This workflow runs many ANI comparisons, pairwise within sets of directories.
It will run all pairwise comparisons for the fasta files that end in `*.fna` within each directory.
You need to change the extensions to `.fna` if they are `.fa` or `.fasta`.
These files should only be the **nucleotide sequences** for the coding regions.  **No tRNA or rRNA gene sequences should be included.**

This setup uses ANI calculator from (https://ani.jgi-psf.org/html/anicalculator.php)[https://ani.jgi-psf.org/html/anicalculator.php]
(link to direct download software)[https://ani.jgi-psf.org/download_files/ANIcalculator_v1.tgz].

This workflow is meant to run using HTCondor DAG's on a HTC system (UW CHTC).


### Setup
1. Download and unpack the ANIcalculator tarball to your home folder.
```
wget https://ani.jgi-psf.org/download_files/ANIcalculator_v1.tgz
tar -xzvf ANIcalculator_v1.tgz
```
2. In this directory place the directories you want to run ANI compareisons within. You need to change the extensions to `.fna` if they are `.fa` or `.fasta`.  These files should only be the **nucleotide sequences** for the coding regions.  **No tRNA or rRNA gene sequences should be included.**
3. Create a file called `phyladirs.txt` that contains a list of each of the directories to run comparisons on. It doesn't have to be separated by phylum but that is how it was originally designed. The program with run all pairwise ANI comparisons within each directory given. It will **not** run self verses self because ANI calculator doesn't like running on the same file twice. It will **only** run the comparison in one direction because ANI calculator runs both directions by default.  The `phyladirs.txt` file should have one directory per line with no `/` after it.  Example:
```
$ head phyladirs.txt
acidobacteria
actinobacteria
bacteroidetes
chlorobi
chloroflexi
```
3. In `phylum.sub` change the `executable = ` and `transfer_input_files = ` lines in  to match where you installed `ANIcalculator` and `nsimscan`.  You will likely only need to change `sstevens2` to your username.

#### Optional additional Setup
1. Check how many comparisons will be run for a directory.  Example directory called `cyanobacteria`
```
./makeANIcombos.py cyanobacteria
wc -l cyanobacteria/ani_combos_cyanobacteria.txt
```
The results from this should tell you how many comparisons you will be submitting.
If you are submitting **a lot** of jobs, you should consider turning on flocking or OSG so it can use those additional resources. (See below)
2. If you are running a big number of comparisons, you may want to change the `wantFlocking`(send jobs to other UW clusters) or `WantGlideIn` (send jobs to OSG) lines.  For these lines remove from the `#` to before the `+`. There is a little info about when to use these lines in [this HTC guide](http://chtc.cs.wisc.edu/helloworld.shtml).
3.changing how anicombos are written - still working on this!!! test before finishing this section

### Running the pipeline (after setup)
1. Run the following.
```
condor_submit_dag runAllANIcompare.dag
```

### What are the files in this repo???
`combineANI.sh` - script that puts together all of the output from each phylum directory  
`errdirs.sh` - creates the error directories for each phylum/directory  
`header.all.ani.out` - header for all ANIcalculator output  
`makeANIcombos.py` - script that makes a list of all the ANI combinations for a directory  
`phylum.sub` - submission script for each directory/phylum included  
`runAllANIcompare.dag` - DAGman file to run the whole workflow  
`writeCompareDAG.py` - script that writes the `compare.dag` and `compare.dag.config` files, edit this if you need to change the DAGman config  
`writeCompareDAG.sub` - submission script for the script above  


### ISSUES
1. `combineAll.sh` expects that the output worked properly, if it didn't you may need to come up with a new way to combine all `*.out` files in each directory
3. make changes to how to anicombos runs! - take lists and not run if files exist? - WORK ON THIS WHEN YOU COMPARE CB AND ML
