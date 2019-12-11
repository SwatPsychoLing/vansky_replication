# Replication
Implementing the code by [**van Schijndel & Linzen (2018)**](https://vansky.github.io/assets/pdf/vanschijndel_linzen-2018-emnlp_adapt-joint.pdf). This set of instructions combines some of the steps from van Schijndel's own [GitHub](https://github.com/vansky/replications/blob/master/vanschijndel_linzen-2018-emnlp/vanschijndel_linzen-2018-emnlp-replication.md) with steps for how to run the models on an Amazon EC2 server and some tips for solving issues that might arise from Letitia Ho's [Github](https://github.com/LetitiaHo/Replication). 

# 1. Launching Amazon EC2 Instance 
### 1.0 Create an AWS account
Create an Amazon EC2 server by creating an [AWS](https://aws.amazon.com/) account. You will be creating a server that will provide you with access to GPUs, which will be required to run the neural networks training and testing in seconds instead of hours or days. If you are from an educational institution, check your institution's information on AWS as you may be eligible for free starting credits in your account through AWS Educate. 

If you wish to not use your own credit card for initializing the account, you can acquire virtual debit cards from __________

### 1.1 Extend your access to AWS EC2 servers with GRUs
Go to your [EC2 Management Console](https://aws.amazon.com/console/), click the *Limits* link on the top of the menu on the left. Locate *Running On-Demand p2.xlarge instances* in the list of instances that come up and click `Request limit increase`. Under *Requests*, select `US East (Ohio)` for *Region*, and `p2.xlarge` for *Primary Instance Type*, and `1` for *New limit value*.
### 1.2 Wait
Wait for Amazon to approve of the limit increase. This might take a day or two.
### 1.3 Get a key
Go to *Key Pairs* under *Network & Security* on the left side menu at your [EC2 Management Console](https://aws.amazon.com/console/). Click `Create Key Pair`, give your key an easy name to type and remember, click `Create`. Your `.pem` key file should automatically download. Save it to a directory you are sure to remember.
### 1.4 Launching your instance 
- **Launch your instance (first time)**
    Go to your [EC2 Management Console](https://aws.amazon.com/console/), click `Launch Instance` and search for the *Deep Learning AMI (Ubuntu) Version* and click `Select`. Within the list of instance types that comes up, select *p2.xlarge* and click `Review and Launch` at the bottom. Click <Launch>. Select the key pair you created in **Step 3**, check the box and click `Launch Instances`.
- **Relaunch your instance (after creation)**
    To relaunch your instance after it's been created, go to your EC2 Management Console and click on the instance you wish to launch. Then click the 'Actions' button, --> 'Instance State' --> 'Start'.
- **Stopping your instance**
    Be sure you stop your instance once you are done running it to prevent overcharging on the account. To stop the instance, go once again to 'Actions' --> 'Instance State' and press 'Stop'.
### 1.5 Connect to your instance
Your new instance should now appear in your [EC2 Management Console](https://aws.amazon.com/console/). From now I will assume `/XPATH/` refers to the path where a certain file is stored (e.g. `/XPATH/key.pem` refers to the file path of your Amazon key `.pem` file). 

You will need **1.** the file path to your Amazon key `.pem` file from **Step 3** and **2.** the *Public DNS* of your instance. You can find this on your [EC2 Management Console](https://aws.amazon.com/console/), when you select your instance, the menu at the bottom will display the properties of your instance, its *Public DNS* will be listed there. You may also find instructions with screenshots for Linux [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html). 

To launch your instance, go to terminal and type:
``` 
cd /XPATH/<your key>.pem 
chmod 0400 <your key>.pem
ssh -L localhost:8888:localhost:8888 -i <your key>.pem ubuntu@<Public DNS>
```
You will asked whether you want to continue connecting, answer *yes*. Once you are connected, type:
```
jupyter notebook
```
Copy and past the link that comes up into your browser, this will allow you to access your EC2 server from your browser.

***For Windows users***, connect to your instance via PuTTY, an SSH Client. Instructions on how to do so can be found [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html?icmpid=docs_ec2_console). This link also includes information on SSH file transfer between your computer and your Linux instance, which is important for future steps in the replication process.


# 2. Preparing files 
    see own bash file?? 
    distinguish between: files needed for all, files for natstor, files for fine and jaeger 
    
### 2.0 For all replications (naturalstories and Fine and Jaeger)
- ***2.0.1 Get Pytorch v0.3.0***
``` 
pip install http://download.pytorch.org/whl/cu80/torch-0.3.0.post4-cp36-cp36m-linux_x86_64.whl
```
- ***2.0.2 Get the adaptive LM***
```
git clone https://github.com/vansky/neural-complexity
cd neural-complexity
git checkout tags/v1.0.0
```
You should now have a file in your directory called `neural-complexity`.
- ***2.0.3 Get the base LM Weights and model vocab*** In neural-complexity directory (from previous step):
```
wget “https://dl.fbaipublicfiles.com/colorless-green-rnns/training-data/English/vocab.txt”
wget "https://dl.fbaipublicfiles.com/colorless-green-rnns/best-models/English/hidden650_batch128_dropout0.2_lr20.0.pt"
```
- ***2.0.4 Get Extended Penn Tokenizer***
```
cd ~   #go back to home directory
git clone https://github.com/vansky/extended_penn_tokenizer.git
```
- ***2.0.5 Get Modelblocks*** Still in home directory: 
```
git clone https://github.com/modelblocks/modelblocks-release.git
```

### 2.1 For naturalstories replication
- ***2.1.1 Get Natural Stories corpus***
```
cd
git clone https://github.com/languageMIT/naturalstories.git
```
- ***2.1.2 Make necessary components***
Go to the `modelblocks-release` directory then split each story into individual `.linetoks` files to be used for testing. `%fairy.linetoks` contains all the fairytale stories and `%doc.linetoks` contains all the documentary documents. 
*Run below code to do the above instructions.*
```
cd modelblocks-release
mkdir config  
echo '/XPATH/naturalstories/' > config/user-naturalstories-directory.txt  
echo '/XPATH/extended_penn_tokenizer/' > config/user-tokenizer-directory.txt  
make workspace  
cd workspace  
make genmodel/naturalstories.linetoks  
```
- ***2.1.3 Split up Natural Stories Corpus***
Run below code to split up the corpus for analysis. 
```
cat genmodel/naturalstories.linetoks | head -n 57 > genmodel/naturalstories.0.linetoks  
cat genmodel/naturalstories.linetoks | head -n 94 | tail -n 37 > genmodel/naturalstories.1.linetoks  
cat genmodel/naturalstories.linetoks | head -n 149 | tail -n 55 > genmodel/naturalstories.2.linetoks  
cat genmodel/naturalstories.linetoks | head -n 204 | tail -n 55 > genmodel/naturalstories.3.linetoks  
cat genmodel/naturalstories.linetoks | head -n 249 | tail -n 45 > genmodel/naturalstories.4.linetoks  
cat genmodel/naturalstories.linetoks | head -n 313 | tail -n 64 > genmodel/naturalstories.5.linetoks  
cat genmodel/naturalstories.linetoks | head -n 361 | tail -n 48 > genmodel/naturalstories.6.linetoks  
cat genmodel/naturalstories.linetoks | head -n 394 | tail -n 33 > genmodel/naturalstories.7.linetoks  
cat genmodel/naturalstories.linetoks | head -n 442 | tail -n 48 > genmodel/naturalstories.8.linetoks  
cat genmodel/naturalstories.linetoks | head -n 485 | tail -n 43 > genmodel/naturalstories.9.linetoks  
cat genmodel/naturalstories.{0,1,2,3,4,5,6}.linetoks > genmodel/naturalstories.fairy.linetoks  
cat genmodel/naturalstories.{7,8,9}.linetoks > genmodel/naturalstories.doc.linetoks
```
### 2.2 For Fine and Jaeger (2016) Replication
*Copied from vansky replication page linked at top* 
Requires stimuli from Fine and Jaeger (2016), which come in the form of 16 lists: ListA1, ListA1_reversed, ListA2, etc.

Ensure that the stimulus sentences are tokenized properly by passing them through the extended_penn_tokenizer. The below commands assume these are named things like ListA1.linetoks, and are stored in home directory (~).

Put the lists in data/fj16 and make an output file using code below.
```
cd neural-complexity
mkdir data/fj16
mv ~/ListA1.linetoks data/fj16  ##perform for every list 
mkdir fj-output
```

# 3. Naturalstories Replication - Testing the Model
### 3.0 Preparing files
Put the `.linetoks` files in a subdirectory `natstor` within the `neural-complexity/data` directory. 
```
mkdir /home/ubuntu/neural-complexity/data/natstor
mv /home/ubuntu/modelblocks-release/workspace/genmodel/*.linetoks /home/ubuntu/neural-complexity/data/natstor
```
### 3.1 Analysis 1: Adapting the model to full Natural Stories Corpus
Use the following quickstart adaptation command to adapt to full text of naturalstories.linetoks
```
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > full_corpus.adapted.results
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.linetoks' --test --words > full_corpus.notadapted.results
```
**If you are receiving the error message** *"RuntimeError: cuDNN version mismatch: PyTorch was compiled against 7003 but linked against 7301"*, run the following:
```
unset LD_LIBRARY_PATH
```

The final step in each line of code outputs the perplexity results into `full_corpus.adapted.results` and `full_corpus.notadapted.results`. Check the results with:
```
cat full_corpus.notadapted.results
```
### 3.2 Analysis 2: Adapting the model to specific story genres.
Repeating the above with stories in `genmodel/naturalstories.fairy.linetoks` and `genmodel/naturalstories.doc.linetoks`. Copy and run each line of the below code into the command line. The first two commands run on `naturalstories.fairy.linetoks`, while the second two commands run on `naturalstories.doc.linetoks`.
```
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.fairy.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > fairy.adapted.results
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.fairy.linetoks' --test --words > fairy.notadapted.results   
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.doc.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > doc.adapted.results
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.doc.linetoks' --test --words > doc.notadapted.results   
```
### 3.3 Analysis 3: Adapting the model to individual stories
Repeat the above with each of genmodel/naturalstories.{0,1,2,3,4,5,6}.linetoks compared with each of genmodel/naturalstories.{7,8,9}.linetoks
```
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.0.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > naturalstories.0.adapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.0.linetoks' --test --words > naturalstories.0.noadapt.results
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.1.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > naturalstories.1.adapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.1.linetoks' --test --words > naturalstories.1.noadapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.2.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > naturalstories.2.adapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.2.linetoks' --test --words > naturalstories.2.noadapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.3.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > naturalstories.3.adapt.results   
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.3.linetoks' --test --words > naturalstories.3.noadapt.results 
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.4.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > naturalstories.4.adapt.results    
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.4.linetoks' --test --words > naturalstories.4.noadapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.5.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > naturalstories.5.adapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.5.linetoks' --test --words > naturalstories.5.noadapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.6.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > naturalstories.6.adapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.6.linetoks' --test --words > naturalstories.6.noadapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.7.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > naturalstories.7.adapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.7.linetoks' --test --words > naturalstories.7.noadapt.results   
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.8.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > naturalstories.8.adapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.8.linetoks' --test --words > naturalstories.8.noadapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.9.linetoks' --test --words --adapt --adapted_model 'adapted_model.pt' > naturalstories.9.adapt.results  
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/natstor/' --testfname 'naturalstories.9.linetoks' --test --words > naturalstories.9.noadapt.results  
```
### 3.4 Processing resulting data 
Below is copied directly from **Section 4** of vansky replication with slight modifications for bug fixes.
***NOTE: Bug Fixes***
- modify “/home/ubuntu/modelblocks-release/resource-rt/scripts/toks2sents.py” line 26 print statement to include parenthesis 
- modify “vim /home/ubuntu/modelblocks-release/resource-rt/scripts/toks2sents.py” line 16 to: cur += w.decode(‘UTF-8’)      (for running w python 3)
- Run code using python2 to fix other bugs 

You'll need `R` along with the following R packages:
* optparse
* optimx
* lme4

Then you'll need to get [R-hacks](https://github.com/aufrank/R-hacks).

Copy the scripts within the `R-hacks` repository into the `modelblocks-release/resources-rhacks/scripts` directory

Use the results from Section 3 Analysis 3, which I'll refer to as `naturalstories.0.{adapt,noadapt}.results`, etc based on the numbers in the linetoks filenames and on whether the model was adaptive or not.

Rename the `surp` column in `naturalstories.0.noadapt.results` to `surpnoa`

```
    sed -i '1 s/surp/surpnoa/' naturalstories.0.noadapt.results
```

Paste the `surpnoa` column from each `%noadapt.results` file to the corresponding `%adapt.results` file.

```
    n=0; paste -d' ' <(cut -d' ' -f-5 "naturalstories.${n}.adapt.results") <(cut -d' ' -f5 "naturalstories.${n}.noadapt.results") <(cut -d' ' -f6- "naturalstories.${n}.adapt.results") > naturalstories.${n}.results
```

Increment $n until all files have been joined. Then create one long `%results` file

```
    head -n -3 naturalstories.0.results > naturalstories.full.results  
    head -n -3 naturalstories.1.results | tail -n+2 >> naturalstories.full.results  
    head -n -3 naturalstories.2.results | tail -n+2 >> naturalstories.full.results  
    head -n -3 naturalstories.3.results | tail -n+2 >> naturalstories.full.results  
    head -n -3 naturalstories.4.results | tail -n+2 >> naturalstories.full.results  
    head -n -3 naturalstories.5.results | tail -n+2 >> naturalstories.full.results  
    head -n -3 naturalstories.6.results | tail -n+2 >> naturalstories.full.results  
    head -n -3 naturalstories.7.results | tail -n+2 >> naturalstories.full.results  
    head -n -3 naturalstories.8.results | tail -n+2 >> naturalstories.full.results  
    head -n -3 naturalstories.9.results | tail -n+2 >> naturalstories.full.results  
```

Copy `naturalstories.full.results` to your `modelblocks-release/workspace/` directory  
Copy `naturalstories/naturalstories_RTS/processed_RTs.tsv` to the `modelblocks-release/workspace` directory and cd to that directory.  

Note: This next section could be made easier, but the modelblocks target syntax changes occasionally (and is currently going through changes as I write this), so to better future-proof things, we'll manually generate most of the needed files. 

```
    make genmodel/naturalstories.mfields.itemmeasures  
    echo 'word' > natstor.toks  
    sed 's/ /\n/g' genmodel/naturalstories.linetoks >> natstor.toks  
    paste -d' ' natstor.toks <(cut -d' ' -f2-6 naturalstories.full.results) | python2 ../resource-rt/scripts/roll_toks.py <(sed 's/(/-LRB-/g;s/)/-RRB-/g;' genmodel/naturalstories.mfields.itemmeasures) sentid sentpos > naturalstories.lstm.itemmeasures  
    cut -d' ' -f4- naturalstories.lstm.itemmeasures  | paste -d' ' genmodel/naturalstories.mfields.itemmeasures - > naturalstories.lstm.mergable.itemmeasures  
    python ../resource-naturalstories/scripts/merge_natstor.py <(cat processed_RTs.tsv | sed 's/\t/ /g;s/peaked/peeked/g;' | python ../resource-rt/scripts/rename_cols.py WorkerId subject RT fdur) naturalstories.lstm.mergable.itemmeasures | sed 's/``/'\''/g;s/'\'\''/'\''/g;s/(/-LRB-/g;s/)/-RRB-/g;' | python ../resource-rt/scripts/rename_cols.py item docid > naturalstories.lstm.core.evmeasures  
    python ../resource-rt/scripts/rm_unfix_items.py < naturalstories.lstm.core.evmeasures | python ../resource-rt/scripts/rm_na_items.py > naturalstories.lstm.filt.evmeasures  
    mkdir scripts  
```

Create a `scripts/spr.lmeform` file that contains these lines:

```
    fdur  
    z.(wlen) + z.(sentpos)  
    z.(wlen) + z.(sentpos)  
    (1 | word)
```

Now we use the `naturalstories.lstm.filt.evmeasures` file for regressions:

#### Dev regressions

```
    ../resource-lmefit/scripts/evmeasures2lmefit.r naturalstories.lstm.filt.evmeasures naturalstories.lstm.filt.base.lme.rdata -d -N -S -C -F -A surp+surpnoa -a surp+surpnoa -b scripts/spr.lmeform > naturalstories.lstm.filt.-NSCFd.base.lme  
    ../resource-lmefit/scripts/evmeasures2lmefit.r naturalstories.lstm.filt.evmeasures naturalstories.lstm.filt.surp.lme.rdata -d -N -S -C -F -A surp+surpnoa -a surpnoa -b scripts/spr.lmeform > naturalstories.lstm.filt.-NSCFd.surp.lme  
    ../resource-lmefit/scripts/evmeasures2lmefit.r naturalstories.lstm.filt.evmeasures naturalstories.lstm.filt.surpnoa.lme.rdata -d -N -S -C -F -A surp+surpnoa -a surp -b scripts/spr.lmeform > naturalstories.lstm.filt.-NSCFd.surpnoa.lme  
    ../resource-lmefit/scripts/evmeasures2lmefit.r naturalstories.lstm.filt.evmeasures naturalstories.lstm.filt.both.lme.rdata -d -N -S -C -F -A surp+surpnoa -b scripts/spr.lmeform > naturalstories.lstm.filt.-NSCFd.both.lme  
```

#### Test regressions

```
    ../resource-lmefit/scripts/evmeasures2lmefit.r naturalstories.lstm.filt.evmeasures naturalstories.lstm.filt.base.lme.rdata -t -N -S -C -F -A surp+surpnoa -a surp+surpnoa -b scripts/spr.lmeform > naturalstories.lstm.filt.-NSCFt.base.lme  
    ../resource-lmefit/scripts/evmeasures2lmefit.r naturalstories.lstm.filt.evmeasures naturalstories.lstm.filt.surp.lme.rdata -t -N -S -C -F -A surp+surpnoa -a surpnoa -b scripts/spr.lmeform > naturalstories.lstm.filt.-NSCFt.surp.lme  
    ../resource-lmefit/scripts/evmeasures2lmefit.r naturalstories.lstm.filt.evmeasures naturalstories.lstm.filt.surpnoa.lme.rdata -t -N -S -C -F -A surp+surpnoa -a surp -b scripts/spr.lmeform > naturalstories.lstm.filt.-NSCFt.surpnoa.lme  
    ../resource-lmefit/scripts/evmeasures2lmefit.r naturalstories.lstm.filt.evmeasures naturalstories.lstm.filt.both.lme.rdata -t -N -S -C -F -A surp+surpnoa -b scripts/spr.lmeform > naturalstories.lstm.filt.-NSCFt.both.lme  
```

# 4. Fine and Jaeger (2016) Replication

### 4.1 Running stimuli through model
For this part, you will be using the data from the folders you created in **Step 2**. For each list in the dataset (List = {ListA1.linetoks, ListA1_Reversed.linetoks, ListB1.linetoks, ListB1_Reversed.linetoks, ListA2.linetoks, ...}), run the below two lines of code:
```
time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --data_dir './data/fj16/' --testfname "${list}.linetoks" --test --words > "fj-output/${list}.notadapting.output"  
    time python main.py --model_file 'hidden650_batch128_dropout0.2_lr20.0.pt' --vocab_file 'vocab.txt' --cuda --single --lr ${learnrate} --data_dir './data/fj16/' --testfname "${list}.linetoks" --test --words --adapt --adapted_model "fj-output/adapted_model-${list}.pt" > "fj-output/${list}.adapting.output"
```

### 4.2 Analyzing results 
We ran the output through post-processing code, found in the included *process_output.py* file. Read through the file to see what must be provided to the commandline (and see sample command line call below), as well as how to set directory destinations for the program to find the results files. We did our best interpretation of how to proces based off of the information provided in the vansky replication github, but are unsure if it is fully the same. 

**NOTE:** To move your results folder from your AWS instance to your computer (since the below doesn't rely on GPUs to run), you can look up using WinSCP for Windows in the above **Step 1**: *Connecting to SSH Client*. 

Sample command line:
```
python process_output.py ListA1.adapting finejaeger.csv
```

We then ran the R processing code to generate graphs in our university's R Studio. 

```
library('ggplot2')  
library('stringr')  
theme_set(theme_gray(base_size = 16))  

#df <- read.table('finejaeger.csv',sep=',',header=T)  
#Pull out just the disambiguating region
disamb <- df[((df$sentpos >=7 & df$sentpos <=9) & df$condition=="ambig") | ((df$sentpos >=9 & df$sentpos <=11) & df$condition=="unambig"),]
df<-disamb

df$residsurp <- residuals(lm(surp~order,data=df)) 

ggplot(df, aes(order+1, residsurp, group=condition, colour=condition, fill=condition)) + stat_summary(fun.y=mean, geom="point", aes(colour=condition,shape=condition)) + geom_smooth(method=lm, formula= y ~ log(x+1), aes(linetype=condition)) + scale_colour_manual("condition",labels=c('ambiguous','unambiguous'),values=c("red","blue")) + scale_shape_manual("condition",labels=c('ambiguous','unambiguous'),values=c(1,2)) + scale_linetype_manual("condition",labels=c('ambiguous','unambiguous'),values=c('solid','dashed')) + xlab('Item order (#RCs seen)') + ylab('Order-corrected surprisal (bits)')
ggplot(df, aes(order+1, surp, group=condition, colour=condition, fill=condition)) + stat_summary(fun.y=mean, geom="point", aes(colour=condition,shape=condition)) + geom_smooth(method=lm, formula= y ~ log(x+1), aes(linetype=condition)) + scale_colour_manual("condition",labels=c('ambiguous','unambiguous'),values=c("red","blue")) + scale_shape_manual("condition",labels=c('ambiguous','unambiguous'),values=c(1,2)) + scale_linetype_manual("condition",labels=c('ambiguous','unambiguous'),values=c('solid','dashed')) + xlab('Item order (#RCs seen)') + ylab('Order-corrected surprisal (bits)')

```
This should generate the proper analysis graphs for the experiment. In our case, it created different graphs from what we expected, which we are looking into. 
**NOTE:** We made minor modifications to the replication code on vansky's github since that code did not fully work. 
