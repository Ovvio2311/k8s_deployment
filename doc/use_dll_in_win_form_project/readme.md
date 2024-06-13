# use dll in win form porject

ref project: https://192.168.64.188/bes/create_auto_pay_pending_win_form

1. copy `nuget.config`, `nuget.config` must place in same folder with `.sln` file
2. install package `Microsoft.Extensions.Hosting` and other dll you want to use.
   ```xml
     <ItemGroup>
       <PackageReference Include="FFTS.CentralDBServices.BP.BillingAndPaymentService" Version="1.0.458" />
       <PackageReference Include="Microsoft.Extensions.Hosting" Version="7.0.1" />
     </ItemGroup>
   ```
3. modify file `Program.cs`  
   ref: [CreateAutoPayPending/Program.cs](https://192.168.64.188/bes/create_auto_pay_pending_win_form/-/blob/master/CreateAutoPayPending/Program.cs)
4. add service to `Form1.cs` constructor  
   ref: [CreateAutoPayPending/Form1.cs](https://192.168.64.188/bes/create_auto_pay_pending_win_form/-/blob/master/CreateAutoPayPending/Form1.cs)

   ```csharp
        private readonly BillingAndPaymentService _billingService;
        private readonly BillingAndPaymentDBService _billingDBService;

        public Form1(IConfiguration config, BillingAndPaymentService paymentService, BillingAndPaymentDBService paymentDBService)
        {
            InitializeComponent();
            _config = config;
            _billingService = paymentService;
            _billingDBService = paymentDBService;
        }
   ```
