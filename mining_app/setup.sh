curl https://pyenv.run | bash &&
echo export PATH="/home/ubuntu/.pyenv/bin:$PATH" >> /home/ubuntu/.bashrc &&
echo 'eval "$(pyenv init -)"' >> /home/ubuntu/.bashrc &&
echo 'eval "$(pyenv virtualenv-init -)"' >> /home/ubuntu/.bashrc &&
source /home/ubuntu/.bashrc &&
pyenv install 3.8.0 &&
pyenv global 3.8.0 &&
pip install --upgrade pip &&
pip install awscli &&
aws s3 cp s3://inai-aixsw/src/app.zip . &&
unzip app.zip &&
cd minar-inai/ &&
pip install -r requirements.txt


aws s3 cp s3://inai-aixsw/src/minar.py minar.py &&
aws s3 cp s3://inai-aixsw/src/file_utils.py mining_utils/file_utils.py