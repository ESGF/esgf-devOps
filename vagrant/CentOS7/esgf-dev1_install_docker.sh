yum -y  update
yum install -y git wget vim ntpdate curl lsof

ntpdate pool.ntp.org

# systemctl start httpd
# systemctl enable httpd
# systemctl status httpd
#systemctl stop httpd

yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
docker run hello-world

sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

echo "export ESGF_CONFIG=/root/esgf_config" >> /etc/environment
source /etc/environment
mkdir -p $ESGF_CONFIG

touch "$ESGF_CONFIG/environment"
echo "ESGF_HOSTNAME=$(hostname)" >> $ESGF_CONFIG/environment
echo "ESGF_DATA=/root/esgf_data" >> $ESGF_CONFIG/environment

git clone https://github.com/ESGF/esgf-docker.git
cd esgf-docker

git checkout github_assets


./bin/esgf-setup generate-secrets
./bin/esgf-setup generate-test-certificates
./bin/esgf-setup create-trust-bundle

chmod +r "${ESGF_CONFIG}/certificates/hostcert/hostcert.key"
chmod +r "${ESGF_CONFIG}/certificates/slcsca/ca.key"

./bin/esgf-compose up -d
