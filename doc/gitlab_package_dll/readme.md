# gitlab dll package

generate group deploy tokens  
https://192.168.64.188/groups/bes/-/settings/repository/deploy_token/create#js-deploy-tokens

package repository  
https://192.168.64.188/bes/fftsinternalcommonpackage

```
cd E:\project_folder

dotnet build -c Release -p:Version=1.0.8 -p:VersionSuffix=release -p:IncludeSymbols=true -p:SymbolPackageFormat=snupkg
dotnet pack -c Release -p:Version=1.0.8 -p:VersionSuffix=release -p:IncludeSymbols=true -p:SymbolPackageFormat=snupkg
dotnet nuget add source "https://192.168.64.188/api/v4/projects/107/packages/nuget/index.json" --name gitlab --username "temp_deploy_token" --password "EEtRMvXzAyUiBWYMrtrs" --store-password-in-clear-text

dotnet nuget push "bin/Release/FFTS.InternalCommonCertAuth.1.0.8.nupkg" --source gitlab
```
