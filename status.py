
connect('admin','username','t3://domain.tsa.aws.test.com:9306')
cd ('AppDeployments')
myapps=cmo.getAppDeployments()

for appName in myapps:
       domainConfig()
       cd ('/AppDeployments/'+appName.getName()+'/Targets')
       mytargets = ls(returnMap='true')
       domainRuntime()
       cd('AppRuntimeStateRuntime')
       cd('AppRuntimeStateRuntime')
       for targetinst in mytargets:
             curstate4=cmo.getCurrentState(appName.getName(),targetinst)
             print '\t\t\t\t\t', curstate4, '\t\t\t\t\t', appName.getName()
