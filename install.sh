pip3 install virtualenv --user
virtualenv ./venv -p python3

# should enter venv python
source "$(find . -name activate)"

pip install -r ./requirements.txt

home="$PWD"

npm install

cd "$home"
clear

echo "Done... have fun :)"