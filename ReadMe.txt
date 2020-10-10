Code location:
git clone http://git.Intelegencia.com/atin.amit/EmailMonitor.git
git clone http://git.Intelegencia.com/atin.amit/ApiHarness_Bot.git

#Old email monitor main.py execution
#./run.sh 
python3 main.py $1

#Download training data from email - assistant@intelegencia.com
#./getTrainingData.sh 
python3 getTrainingData.py $1
#python3 getTestData.py $1
python executeAnalysis.py

#build the email tf-idf model based on training data
python3 buildEmailTfIdf.py >> tfidfmodel.out

#for w in `cat tfidfmodel.out`; do echo $w; done|sort|uniq -c >>countcheck.txt

mv tfidfmodel.out data/uniqueword.out 
remove the {} brackets in the file
sed -i 's/,/\n/g' uniqueword.out
sed -i 's/ //g' uniqueword.out
sed -i "s/'//g" uniqueword.out

open the file in excel and remove the count column
remove lines with words containing digits/numerics
sed 's/[a-zA-Z0-9]*[0-9][a-zA-Z0-9]*//g' uniqueword.out >>uniqueword.temp
remove empty lines
sed '/^$/d' uniqueword.temp >>uniqueword.txt
sort the words alphabetically by opening in excel file
remove all the email sender names from the file uniqueword.txt
Generate testcase data using java code for permutation combination generator - TrainingDataGenerator.

open the file uniqueword-testdata.txt in excel file and remove the column uniqueword and sort on asc for column A and B
save the file as cnn_model_training_data.txt
add 3 column in front for: 
1.class/label
2.trakid
3.odderid
First fill all rows with string 'trakid' and 'odderid', then start adding label based on words from the highest class number.
After marking classes/label 4,3,2 for the below words, make a copy with file name - cnn_model_training_data.master
Make copies of this to make different combination based on 'trakid' and 'odderid' for data present or none.
Following 4 combination needs to be created:
1. none, none
2. none, odderid
3. trakid, none
4. trakid, odderid

cat cnn_model_training_data.none_none cnn_model_training_data.none_odderid cnn_model_training_data.trakid_none cnn_model_training_data.trakid_odderid > cnn_model_training_data.txt

diff cnn_model_training_data.txt ../cnn_model_training_data.txt > diff.out

replace comma with space:
sed -i 's/,/ /g' cnn_model_training_data.txt
sed -i 's/0 /0,/g' cnn_model_training_data.txt
sed -i 's/1 /1,/g' cnn_model_training_data.txt
sed -i 's/2 /2,/g' cnn_model_training_data.txt
sed -i 's/3 /3,/g' cnn_model_training_data.txt
sed -i 's/4 /4,/g' cnn_model_training_data.txt



#test the email tf-idf model based on test data
python3 executeEmailTfIdf.py >> tfidfexecute.out

#create DNN model
python3 buildModel.py >> dnnmodel

#execute DNN model
python3 executeModel.py

#create CNN model
python3 buildCNNModel.py >> cnnmodel

#execute CNN model
python3 executeCNNModel.py

unknown_template - 0
status_template - 1 - status,any word other than handled categories for track, cancel, complain
track_template - 2 - day,deliv,deliveri,receiv,ship,shipment,time,track,week
cancel_template - 3 - cancel,refund,return
complain_template - 4 - defect,complain,complaint,damag,wrong,replac,replacement,issu


Starting API Harness:
Use the run.sh script in the root folder of project ApiHarness_Bot
/avishekdata/IL/ApiHarness_Bot$ gunicorn --reload app:app
http://127.0.0.1:8000/tracking/404-0414899-4343144


sudo launchctl load -F /Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist
sudo launchctl unload -F /Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist

