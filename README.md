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

3. replicating natural stories

4. replicating fine and jaeger
