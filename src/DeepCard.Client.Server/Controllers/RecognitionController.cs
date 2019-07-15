using DeepCard.Client.SDK;
using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Threading.Tasks;

namespace DeepCard.Client.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    [RequestSizeLimit(104857600)]
    public class RecognitionController : ControllerBase
    {
        private readonly IHttpClientFactory _httpClientFactory;

        public RecognitionController(IHttpClientFactory httpClientFactory)
        {
            _httpClientFactory = httpClientFactory;
        }

        [HttpPost]
        public async Task<string> Recognize([FromBody] string image)
        {
            var httpclient = _httpClientFactory.CreateClient();
            var client = new RecognitionClient(httpclient);
            string res;
            try
            {
                res = await client.RecognizeAsync(image);
            }
            catch
            {
                res = "识别失败";
            }
            return res;
        }
    }
}
