mkdir tmp
curl http://repo.orix.oric.org/dists/official/tgz/6502/basic.tgz --output tmp/basic.tgz

#mv basic.tgz  tmp/
cd tmp && tar xvfz basic.tgz && cd ..

cat  tmp/etc/systemd/basic/2022.1/basic.cnf > ../build/etc/systemd/banks.cnf 
cat ../build/etc/systemd/bankstmp.cnf >> ../build/etc/systemd/banks.cnf && rm -f ../build/etc/systemd/bankstmp.cnf