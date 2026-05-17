using Polyglot.DotNetService;
using Xunit;

public class ServiceMetadataTests
{
    [Fact]
    public void PayloadIncludesExpectedMetadata()
    {
        var payload = ServiceMetadata.Payload("ok");
        Assert.Equal("dotnet-service", payload["service"]);
        Assert.Equal("dotnet", payload["runtime"]);
        Assert.Equal("1.0.0", payload["version"]);
    }
}
