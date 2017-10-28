#!/usr/bin/env bash

export PATH=/mhome/aad/automl_2015/anaconda2/bin:$PATH

if [[ $(python --version 2>&1) == Python*2\.7\.10* ]]
then
    echo "Using Python 2.7.10"
else

    while true; do
		read -p "Found a different python version! Continue anyway? (y/[n]): " yn
		case $yn in
			y ) break;;
			n ) exit 1;;
			"") exit 1;;
			* ) echo "Please answer \"y\" or \"n\"!";;
		esac
	done
fi

echo "Check whether this repo is up-to-date"
if [ "`git log --pretty=%H ...refs/heads/master | head -n 1`" = "`git ls-remote origin -h refs/heads/master |cut -f1`" ]
then
    while true; do
        read -p "BeatAutosklearn is not up to date, continue anyway? [y|n]" yn
        case $yn in
            [Yy]* ) echo "continue"; break
            ;;
            [Nn]* ) exit 2
            ;;
            * ) echo "Please answer yes or no."
            ;;
        esac
    done
else
    echo "BeatAutosklearn is up to date"
fi

# First, create a temporary directory for zipping files
rm .zip -rf
rm build -rf
rm download -rf
mkdir .zip
mkdir .zip/BeatAutosklearn
mkdir build
mkdir download

# Add dependencies
pip install -t lib/ -b build --no-deps configspace==0.1.1;                                                          	if [[ $? -ne 0 ]]; then	exit $?;	fi
pip install git+ssh://git@github.com/mfeurer/liac-arff#egg=liac-arff -t lib/ -b build --no-deps;						if [[ $? -ne 0 ]]; then	exit $?;	fi
pip install -t lib/ -b build git+ssh://git@bitbucket.org/aadfreiburg/random_forest_run.git;								if [[ $? -ne 0 ]]; then	exit $?;	fi
pip install -t lib/ -b build --no-deps pynisher==0.4.1;                                                                 if [[ $? -ne 0 ]]; then	exit $?;	fi
pip install -t lib/ -b build --no-deps lockfile==0.10.2;																if [[ $? -ne 0 ]]; then	exit $?;	fi
pip install -t lib/ -b build git+ssh://git@bitbucket.org/aadfreiburg/smac3@development --no-deps; 						if [[ $? -ne 0 ]]; then	exit $?;	fi



# We download this, build the c extension and copy it directly
cd build
#git clone --depth 1 -b development --single-branch https://github.com/automl/auto-sklearn.git
git clone --depth 1 -b development --single-branch git@github.com:automl/auto-sklearn.git
cd auto-sklearn
python setup.py build_ext --inplace; 	if [[ $? -ne 0 ]]; then	exit $?;	fi
cd ../..
cp build/auto-sklearn/autosklearn lib/ -r

# ====== Download Stuff
#cd download/

#if [[ ! -e sklearn.tar.gz ]];	then
#    cp /mhome/aad/automl_2015/dependencies/sklearn.tar.gz .; 	if [[ $? -ne 0 ]]; then	exit $?;	fi
#fi

#tar -xf sklearn.tar.gz;																									if [[ $? -ne 0 ]]; then	exit $?;	fi
#cp sklearn ../lib -r
#cd ..

# ==== MOVE Libraries
cp /data/aad/automl_data/autotrack_dependencies/xgboost lib/ -r

# ==== MOVE scripts explicitly
cp score.py .zip/BeatAutosklearn/ -r
cp metadata .zip/BeatAutosklearn/ -r          # DO NOT DELETE THIS!!!!!!!!!
cp score .zip/BeatAutosklearn/ -r
# cp res .zip/BeatAutosklearn/ -r
cp ref .zip/BeatAutosklearn/ -r
cp ref_all .zip/BeatAutosklearn/ -r
cp lib .zip/BeatAutosklearn/ -r
cp data .zip/BeatAutosklearn/ -r

# === Clean up the submission directory
find . -name "*.egg-info" -exec rm -rf {} \;
find . -name "*.pyc" -exec rm -f {} \;
find . -name "*~" -exec rm -f {} \;

# === Create number of submission
if [ ! -e number_submission ]
then
    echo "0" > number_submission
fi
typeset -i NUMSUB=$(cat number_submission)
echo $((NUMSUB+1)) > number_submission

# === Zip it
rm .zip/BeatAutosklearn/lib/ -rf
cp lib .zip/BeatAutosklearn/ -rf
cd .zip/BeatAutosklearn
zip -q -r ../../BeatAuto-sklearn_${NUMSUB}_${USER}.zip *
cd ../..

echo "Submission is ready as BeatAuto-sklearn_${NUMSUB}_${USER}.zip"
