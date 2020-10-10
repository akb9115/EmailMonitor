import io, os

class Config:
    
    # Dictionary for environment variables
    env: dict = {
        'ENABLE_DB':'',
        'SMTP_SERVER':'',
        'SMTP_PORT':'',
        'MAIL_ACCOUNT':'',
        'IMAP_SREVER':'',
        'PASSWORD':'',
        'REFRESH':'',
        'WEBHOOK_URL':'',
        'API_ENDPOINT':'',
        'TENANT_ID':''
    }
    
    # Loading the environment variables from the .env
    def load_env(path: str) -> bool:
        try:
            with io.open(path) as stream:
                for line in stream:
                    parts = line.split('=')
                    Config.env[parts[0]] = parts[1].strip()
            return True
        except:
            return False   
    
    
    # Getters
    def get_smtpserver() -> str:
        return Config.env['SMTP_SERVER']
    
    def get_smtpport() -> int:
        return int(Config.env['SMTP_PORT'])
    
    def get_mailaccount() -> str:
        return Config.env['MAIL_ACCOUNT']
    
    def get_imapserver() -> str:
        return Config.env['IMAP_SREVER']
    
    def get_password() -> str:
        return Config.env['PASSWORD']
    
    def get_refresh() -> int:
        return int(Config.env['REFRESH'])
    
    def get_webhookurl() -> str:
        return Config.env['WEBHOOK_URL']

    def get_apiendpoint() -> str:
        return Config.env['API_ENDPOINT']

    def is_enabledb() -> bool:
        if Config.env['ENABLE_DB'] == 'True':
            return True
        else:
            return False

    def get_tenantid() -> str:
        return Config.env['TENANT_ID']

    # Class static initialization
    def static_init() -> bool:
        if os.path.isfile('.env'):
            return Config.load_env('.env')
        else:
            return Config.load_env('.env.default')
