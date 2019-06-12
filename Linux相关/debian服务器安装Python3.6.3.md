### 1. 更新软件包
```shell
sudo apt-get update
sudo apt-get upgrade
```

### 2. 安装依赖包
```shell
sudo apt install gcc make zlib1g-dev libffi-dev libssl-dev
```

### 3. 下载Python3.6.3
```shell
cd /opt
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.3.tgz
```

### 4. 解压
```
tar -zxvf Pytho-3.6.3.tgz
```

### 5. 授权文件夹权限
```
chmod -R +x Python-3.6.3
```

### 6. 进入文件夹
```
./configure --enable-optimizations
```

### 7. 编译安装
```
make && make install
```

### 8. 安装setuptools
```
cd /opt

wget --no-check-certificate  https://pypi.python.org/packages/source/s/setuptools/setuptools-19.6.tar.gz#md5=c607dd118eae682c44ed146367a17e26

tar -zxvf setuptools-19.6.tar.gz

cd setuptools-19.6.tar.gz

python3 setup.py build

python3 setup.py install
```

### 9. 安装pip for python3.6.3
```
cd /opt

wget --no-check-certificate  https://pypi.python.org/packages/source/p/pip/pip-8.0.2.tar.gz#md5=3a73c4188f8dbad6a1e6f6d44d117eeb

tar -zxvf pip-8.0.2.tar.gz

cd pip-8.0.2

python3 setup.py build

python3 setup.py install
```


### 安装psycopg2失败后的解决方法
```
sudo apt-get install libpq-dev python-dev

sudo pip3 install psycopg2
```