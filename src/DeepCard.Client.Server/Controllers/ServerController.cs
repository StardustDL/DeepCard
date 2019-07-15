using Microsoft.AspNetCore.Mvc;
using System;

namespace DeepCard.Client.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ServerController : Controller
    {
        public static string ApiServerUrl { get; set; }

        [HttpGet("[action]")]
        public string ApiServer()
        {
            return ApiServerUrl;
        }
    }
}
