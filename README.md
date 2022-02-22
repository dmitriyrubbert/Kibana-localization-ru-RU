# Kibana-localization-ru-RU

Discussion https://discuss.elastic.co/t/topic/228160/5

To translate kibana v6.8.20 run this steps:

Install google translator and build Kibana
```
pip3 install googletrans==4.0.0-rc1
git clone https://github.com/elastic/kibana.git
cd kibana
git checkout v6.8.20
git branch
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.zshrc
nvm use
nvm install 10.24.1
npm install --global yarn
yarn npm install -g yarn
yarn kbn bootstrap
```

Extract translations from Kibana
`node ./scripts/i18n_extract.js --output-dir ./`
Remove translator comments from file
`node scripts/i18n_integrate.js --source en.json --target en_integreted.json`

Run script `./translate_google.py` and wail 5-6 hours.

Then install translations in Kibana and restart service
```
cp ru-RU.json /usr/share/kibana/node_modules/x-pack/plugins/translations/translations/zh-CN.json
tee -a /etc/kibana/kibana.yml <<< 'i18n.locale: "zh-CN"'
systemctl restart kibana.service
```
For debug in console run this
```
systemctl stop kibana.service
/usr/share/kibana/bin/kibana "-c /etc/kibana/kibana.yml"
```
