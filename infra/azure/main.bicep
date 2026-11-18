targetScope = 'resourceGroup'

param location string = resourceGroup().location
param databaseLocation string = location
@minLength(3)
@maxLength(35)
param appName string
param postgresName string
@secure()
param postgresAdminPassword string
@secure()
param appDatabasePassword string
@secure()
param djangoSecretKey string

resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: '${appName}-plan'
  location: location
  kind: 'linux'
  sku: { name: 'B1', tier: 'Basic', capacity: 1 }
  properties: { reserved: true }
}

resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2024-08-01' = {
  name: postgresName
  location: databaseLocation
  sku: { name: 'Standard_B1ms', tier: 'Burstable' }
  properties: {
    version: '16'
    administratorLogin: 'ecogest_admin'
    administratorLoginPassword: postgresAdminPassword
    storage: { storageSizeGB: 32, autoGrow: 'Disabled' }
    backup: { backupRetentionDays: 7, geoRedundantBackup: 'Disabled' }
    highAvailability: { mode: 'Disabled' }
    network: { publicNetworkAccess: 'Enabled' }
    authConfig: { activeDirectoryAuth: 'Disabled', passwordAuth: 'Enabled' }
  }
}

resource database 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2024-08-01' = {
  parent: postgres
  name: 'ecogest'
  properties: { charset: 'UTF8', collation: 'en_US.utf8' }
}

resource app 'Microsoft.Web/sites@2023-12-01' = {
  name: appName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.12'
      alwaysOn: true
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      scmMinTlsVersion: '1.2'
      appCommandLine: 'gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 60 config.wsgi_azure:application'
      appSettings: [
        { name: 'DJANGO_SETTINGS_MODULE', value: 'config.settings_azure' }
        { name: 'DJANGO_SECRET_KEY', value: djangoSecretKey }
        { name: 'DJANGO_DEBUG', value: '0' }
        { name: 'AZURE_APP_HOST', value: '${appName}.azurewebsites.net' }
        { name: 'DB_HOST', value: postgres.properties.fullyQualifiedDomainName }
        { name: 'DB_PORT', value: '5432' }
        { name: 'DB_NAME', value: database.name }
        { name: 'DB_USER', value: 'ecogest_app' }
        { name: 'DB_PASSWORD', value: appDatabasePassword }
        { name: 'SCM_DO_BUILD_DURING_DEPLOYMENT', value: 'true' }
        { name: 'DISABLE_COLLECTSTATIC', value: 'true' }
        { name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE', value: 'true' }
        { name: 'AI_ENABLED', value: '0' }
        { name: 'AI_BUDGET_AUTHORIZED', value: '0' }
        { name: 'OPENAI_SMOKE_TEST', value: '0' }
      ]
    }
  }
}

resource ftpAuth 'Microsoft.Web/sites/basicPublishingCredentialsPolicies@2023-12-01' = {
  parent: app
  name: 'ftp'
  properties: { allow: false }
}
resource scmAuth 'Microsoft.Web/sites/basicPublishingCredentialsPolicies@2023-12-01' = {
  parent: app
  name: 'scm'
  properties: { allow: false }
}

// Runtime-dependent IPs are applied in a separate step after inspecting the web app.
// No permissive Azure-wide or 0.0.0.0/0 firewall rule is created here.
output webAppName string = app.name
output databaseHost string = postgres.properties.fullyQualifiedDomainName
output webHost string = app.properties.defaultHostName
output outboundIps string = app.properties.outboundIpAddresses
