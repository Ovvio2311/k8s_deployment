# How To Call Internal API

## Inject internal api client

### Startup.cs

```csharp
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using FFTS.InternalCommonModels.ApiClient.AnyInternalApi;
using FFTS.InternalCommonModels.ApiClient.TomsApi;
using FFTS.InternalCommonModels.ApiClient.AuthApi;
using FFTS.InternalCommonModels.ApiClient.ExampleTodoApi;
using System;
namespace TOMS_PORTAL
{
    public class Startup
    {
        public Startup(IWebHostEnvironment env, IConfiguration configuration)
        {
            Configuration = configuration;
            StaticConfig = configuration;
        }

        public IConfiguration Configuration { get; }
        public static IConfiguration StaticConfig { get; private set; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddHttpClient();
            services.AddHttpClient<AnyInternalApiClient>();
            services.AddHttpClient<TomsApiClient>(config => config.BaseAddress = new Uri(Configuration.GetSection("AppAPIHost").Value));
            services.AddHttpClient<AuthApiClient>(config => config.BaseAddress = new Uri(Configuration.GetSection("AuthAPIHost").Value));
            services.AddHttpClient<ExampleTodoApiClient>(config => config.BaseAddress = new Uri("http://192.168.64.170:31099/"));
        }
    }
}
```

## Call API In controller

### TestController.cs

```csharp
using FFTS.InternalCommonModels.ApiClient.ExampleTodoApi;
using FFTS.InternalCommonModels.ApiClient.AnyInternalApi;

using Microsoft.AspNetCore.Mvc;

using System.Collections.Generic;
using System.Net.Http.Json;
using System.Threading.Tasks;

using TOMS_PORTAL.Configuration;
using System;

namespace TOMS_PORTAL.Controllers
{
    public class TestController : Controller
    {
        private readonly Settings settings;
        private readonly AnyInternalApiClient anyInternalApiClient;
        private readonly ExampleTodoApiClient exampleTodoApiClient;

        public TestController(Settings settings, AnyInternalApiClient anyInternalApiClient, ExampleTodoApiClient exampleTodoApiClient)
        {
            this.settings = settings;
            this.anyInternalApiClient = anyInternalApiClient;
            this.exampleTodoApiClient = exampleTodoApiClient;
        }

        public async Task<IActionResult> CallInternalApi_1()
        {
            var param = new TodoItem() { Name = $"example item, created at : {DateTime.Now}" };
            TodoItem response = await exampleTodoApiClient.ApiTodoitemsPostAsync(param);
            return Json(response);
        }

        public async Task<IActionResult> CallInternalApi_2()
        {
            // Call multi api

            // get id 1 
            long id = 1;
            TodoItem response = await exampleTodoApiClient.ApiTodoitemsGetAsync(id);

            // get list
            ICollection<TodoItem> responseList = await exampleTodoApiClient.ApiTodoitemsGetAsync();

            return Json(new { response, responseList });
        }

        public IActionResult CallInternalApi_3()
        {
            // For non async function 
            ICollection<TodoItem> response = exampleTodoApiClient.ApiTodoitemsGetAsync().GetAwaiter().GetResult();
            return Json(response);
        }

        public async Task<IActionResult> CallInternalApi_4()
        {
            // call api that not existed in CommonModels
            var client = anyInternalApiClient.HttpClient;

            var param = new { id = 1 };
            var response = await client.PostAsync("http://192.168.64.170:31099/api/TodoItems", JsonContent.Create(param));
            return Json(response);
        }

        public async Task<IActionResult> CallApiInLoop()
        {
            // Call api in for loop
            var taskList = new List<Task<TodoItem>>();
            for (int i = 0; i < 10; i++)
            {
                long id = 1;
                var task = exampleTodoApiClient.ApiTodoitemsGetAsync(id);
                taskList.Add(task);
            }

            TodoItem[] responseList = await Task.WhenAll(taskList);
            return Json(responseList);
        }

        public IActionResult CallApiInView()
        {
            return View();
        }
    }
}

```

## Call API In View

### CallApiInView.cshtml

```csharp .cshtml
@{
    ViewBag.Title = "Call Api Testing";
    Layout = "~/Views/Shared/_Layout.cshtml";
}
@using FFTS.InternalCommonModels.ApiClient.ExampleTodoApi
@inject ExampleTodoApiClient exampleTodoApiClient
<!DOCTYPE html>
<html lang="en">
<body>
    @{
        var param = new TodoItem() { Name = $"example item, created at : {DateTime.Now}" };
        TodoItem response = await exampleTodoApiClient.ApiTodoitemsPostAsync(param);
    }
    <code>
        @Json.Serialize(response)
    </code>
</body>
</html>

```
