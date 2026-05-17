using Polyglot.DotNetService;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/health", () => Results.Json(ServiceMetadata.Payload("ok")));
app.MapGet("/version", () => Results.Json(ServiceMetadata.Payload("ok")));

app.Run();

namespace Polyglot.DotNetService
{
    public static class ServiceMetadata
    {
        public static IDictionary<string, string> Payload(string status)
        {
            return new Dictionary<string, string>
            {
                ["service"] = "dotnet-service",
                ["version"] = "1.0.0",
                ["runtime"] = "dotnet",
                ["environment"] = Environment.GetEnvironmentVariable("ENVIRONMENT") ?? "local",
                ["build"] = Environment.GetEnvironmentVariable("BUILD_SHA") ?? "local",
                ["timestamp"] = DateTimeOffset.UtcNow.ToString("O"),
                ["status"] = status
            };
        }
    }
}
