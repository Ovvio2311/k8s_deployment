# config log to elastic (startup.cs)

1. install package

```xml
<PackageReference Include="Serilog.Extensions.Hosting" Version="5.0.1" />
<PackageReference Include="Serilog.Settings.Configuration" Version="3.4.0" />
<PackageReference Include="Serilog.Sinks.Console" Version="4.1.0" />
<PackageReference Include="Serilog.Sinks.Elasticsearch" Version="9.0.0" />
```

2. update `Program.cs` file

   add `using Serilog;` on top

   add `.UseSerilog((context, logger) => { logger.ReadFrom.Configuration(context.Configuration); })` after `Host.CreateDefaultBuilder(args)`

   ```C#
    static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .UseSerilog((context, logger) => { logger.ReadFrom.Configuration(context.Configuration); })
            .ConfigureWebHostDefaults(webBuilder =>
            {
                webBuilder.UseStartup<Startup>();
            });
   ```

3. update appsettings file  
    add serilog setion.

   ```json
   {
     "Serilog": {
       "MinimumLevel": {
         "Default": "Debug",
         "Override": {
           "Default": "Debug",
           "Microsoft": "Warning",
           "Microsoft.Hosting.Lifetime": "Warning"
         }
       },
       "WriteTo": [
         {
           "Name": "Logger",
           "Args": {
             "configureLogger": {
               "WriteTo": [
                 {
                   "Name": "Elasticsearch",
                   "Args": {
                     "nodeUris": "http://192.168.64.130:9200/",
                     "indexFormat": "logs-local-{0:yyyy.MM}",
                     "emitEventFailure": "WriteToSelfLog",
                     "autoRegisterTemplate": true,
                     "connectionTimeout": 2,
                     "connectionGlobalHeaders": "Authorization=Bearer SOME-TOKEN;"
                   }
                 }
               ]
             }
           }
         },
         {
           "Name": "Console",
           "Args": { "outputTemplate": "{Timestamp:o} [{Level:u3}] [{RequestId}] {Message:lj}{NewLine}{Exception}" }
         }
       ],
       "Enrich": ["FromLogContext", "WithMachineName"]
     }
   }
   ```

## Only for web api

4. Install package

```xml
<PackageReference Include="Serilog.AspNetCore" Version="6.1.0" />
```

5. Update `Startup.cs` file  
   Add `app.UseSerilogRequestLogging();` after `app.UseRouting();`

   ```C#
   public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
   {
       app.UseRouting();
       app.UseSerilogRequestLogging();

       app.UseEndpoints(endpoints =>
       {
           endpoints.MapControllers();
       });
   }
   ```
