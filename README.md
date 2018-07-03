## Run Many ANI comparisons on CHTC

This workflow runs many ANI comparisons, pairwise within sets of directories.
It will run all pairwise comparisons for the fasta files that end in `*.fna` within each directory.
You need to change the extensions to `.fna` if they are `.fa` or `.fasta`.
These files should only be the **nucleotide sequences** for the coding regions.  **No tRNA or rRNA gene sequences should be included.**

This setup uses [ANI calculator from JGI](https://ani.jgi-psf.org/html/home.php?).
[Link to direct download software](https://ani.jgi-psf.org/download_files/ANIcalculator_v1.tgz).

This workflow is meant to run using HTCondor DAG's on a HTC system (UW CHTC).

I originally set this up to run on a bunch of folders which contained genomes which were from the same phylum but you can put them all in one directory or split them into groups at your discretion.  I later added a functionality so that with some setup changes it will run ANI comparisons between two directories instead of within every directory given.


### Setup
1. Download and unpack the ANIcalculator tarball to your home folder.
```
wget https://ani.jgi-psf.org/download_files/ANIcalculator_v1.tgz
tar -xzvf ANIcalculator_v1.tgz
```
2. Clone this `ani_compare_dag` folder to your home folder.  Switch into the `ani_compare_dag` directory and place the directories you want to run ANI compareisons within. You need to change the extensions to `.fna` if they are `.fa` or `.fasta`.  These files should only be the **nucleotide sequences** for the coding regions.  **No tRNA or rRNA gene sequences should be included.**
```
git clone https://github.com/sstevens2/ani_compare_dag.git
cd ani_compare_dag
```
**OR** you can rename the `ani_compare_dag` if you'd like.  I did this because I cloned a new `ani_compare_dag` for each lake dataset I analyzed, so I wanted them each named by the dataset I ran it on.  Below they will still be referenced as `ani_compare_dag`.
```
git clone https://github.com/sstevens2/ani_compare_dag.git myFavLake
cd an_compare_dag myFavLake
```
Then transfer your directories of gene fna files into the `ani_compare_dag` using your favorite transfer method (scp, cyberduck, etc).

3. In the `ani_compare_dag` directory, create a file called `groupslist.txt` that contains a list of each of the directories to run comparisons on. It doesn't have to be separated by phylum but that is how it was originally designed. The program with run all pairwise ANI comparisons within each directory given. It will **not** run self verses self because ANI calculator doesn't like running on the same file twice. It will **only** run the comparison in one direction because ANI calculator runs both directions by default.  The `groupslist.txt` file should have one directory per line with no `/` after it.  Example:
```
$ head groupslist.txt
acidobacteria
actinobacteria
bacteroidetes
chlorobi
chloroflexi
```
3. In `group.sub` change the `executable = ` and `transfer_input_files = ` lines in  to match where you installed `ANIcalculator` and `nsimscan`.  You will likely only need to change `sstevens2` to your username.

#### Optional additional Setup
##### Check Number of Comparisons
To check how many comparisons will be run for a directory.
Example directory called `cyanobacteria`
```
./makeANIcombos.py cyanobacteria
wc -l cyanobacteria/ani_combos_cyanobacteria.txt
```
The results from this should tell you how many comparisons you will be submitting.
If you are submitting **a lot** (more than 200 genomes in any group) of jobs, you should consider turning on flocking or OSG so it can use those additional resources. (See below) 

##### Additions you may want if submitting lots of jobs
If you are running a big number of comparisons, you may want to change the `wantFlocking`(send jobs to other UW clusters) or `WantGlideIn` (send jobs to OSG) lines.  For these lines remove from the `#` to before the `+`. There is a little info about when to use these lines in [this HTC guide](http://chtc.cs.wisc.edu/helloworld.shtml).  

##### Compare lists instead all v. all
If you want to compare all genomes in each phylum/directory against each other the setup above will work.
However you may have two groups of genomes you want to check against each other (and not within groups), for example you may want to compare all the Actinobacteria in one lake vs the Actinobacteria in another lake.
To run it in this manner, you will need to provide lists for each group.
This is especially needed if you have a large group of genomes (>150) to compare and you don't want to waste time/effort/compute running the comparisons within your groups (otherwise you may as well run the all v. all). 
The lists need to end in `genome_list.txt` and be the only files ending like that. 
Example: `acidobacteria/cb_acidobacteria_genome_list.txt` and `acidobacteria/ml_acidobacteria_genome_list.txt`, where each list contains a different `fna` file from that group on each line.
If the wrong number of lists are found it will give an error.
If the no lists are provided it will do all v all comparison within that phylum.
This is decided on a phylum/directory basis, so you could include these two lists in those where you want to run the comparison between two groups and not include them in the groups where you want to run all v all comparisons.

##### Change the number of comparisons which are batched together
By default this will submit them in groups of 50 comparisons each.  If you'd like to change that, change `50` to your desired group size in the `arguments=` line of `writeCompareDAG.sub`.


### Running the pipeline (after setup)
1. Run the following.
```
condor_submit_dag runAllANIcompare.dag
```

#### A little on how it works

`runAllANIcompare.dag` 
1. Makes the `err` directories for runfiles to write to for each group
2. Submits the script to write up a subDAG and splices for all of the possible combinations
3. Runs the subDAG that was written in step 2, which runs all of the ani comparisons.
4. Puts together the result files by group.

#### Output files
- `groupname.all.ani.out` - concatenated all of the raw results together
- `groupname.all.ani.out.cleaned` - `groupname.all.ani.out` without the headers or filenames
- `groupname/anioutput` - All the individual output files for each ani comparison
- `groupname.spl` - SPLIT file for each group (needed for running the splits)
- Bunch of `log` and `err` and `out` files from the job submissions - these are mostly important to look through if your run failed

### What are the other files in this repo???
`combineANI.sh` - script that puts together all of the output from each group directory  
`errdirs.sh` - creates the error directories for each group/directory  
`header.all.ani.out` - header for all ANIcalculator output  
`makeANIcombos.py` - script that makes a list of all the ANI combinations for a directory or between two lists
`group.sub` - submission script for each group/directory included  
`runAllANIcompare.dag` - DAGman file to run the whole workflow  
`writeCompareDAG.py` - script that writes the `compare.dag` and `compare.dag.config` files, edit this if you need to change the DAGman config  
`writeCompareDAG.sub` - submission script for the script above  

