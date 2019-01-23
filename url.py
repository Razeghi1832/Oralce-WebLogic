connect('appsadmin','password','t3://intfadm001.tsa.aws.test.com:9306')
edit()
startEdit()
cd('JDBCSystemResources')
#getting user
mydatasources=cmo.getJDBCSystemResources()

for datasourcename in mydatasources:
         cd ('/JDBCSystemResources/'+datasourcename.getName()+'/JDBCResource/'+datasourcename.getName()+'/JDBCDriverParams/'+datasourcename.getName()+'/Properties/'+datasourcename.getName()+'/Properties/user')
         user = get('Value')
         print('User is: '+user)

#getting URL
domainConfig()
cd('JDBCSystemResources')
myurls=cmo.getJDBCSystemResources()
for urlname in myurls:
         cd('/JDBCSystemResources/'+urlname.getName()+'/JDBCResource/'+urlname.getName()+'/JDBCDriverParams/'+urlname.getName())
         url = get('Url')
         print('URLS are:------------------>> '+url)
