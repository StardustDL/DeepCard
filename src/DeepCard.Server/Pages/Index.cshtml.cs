using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using DeepCard.Client.SDK;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace DeepCard.Server.Pages
{
    [RequestSizeLimit(104857600)]
    public class IndexModel : PageModel
    {
        public class PostModel
        {
            public List<IFormFile> ImageFiles { get; set; }
        }

        public class RecResult
        {
            public string ImageSrc { get; set; }

            public string CardNumber { get; set; }
        }

        public string Message { get; set; }

        private readonly IHttpClientFactory _httpClientFactory;

        public IEnumerable<RecResult> Results { get; set; }

        [BindProperty]
        public PostModel PostData { get; set; }

        public IndexModel(IHttpClientFactory httpClientFactory)
        {
            _httpClientFactory = httpClientFactory;
        }

        public ActionResult OnGet()
        {
            return Page();
        }

        public async Task<ActionResult> OnPostAsync()
        {
            if (PostData.ImageFiles == null || PostData.ImageFiles.Count == 0)
            {
                Message = "请上传图片。";
                return Page();
            }

            var httpclient = _httpClientFactory.CreateClient();
            var client = new RecognitionClient(httpclient);
            try
            {
                List<RecResult> res = new List<RecResult>();
                List<string> imgs = new List<string>();
                foreach (var f in PostData.ImageFiles)
                {
                    string encoded = "";
                    using (var memoryStream = new MemoryStream())
                    {
                        await f.CopyToAsync(memoryStream);
                        var bytes = memoryStream.ToArray();
                        encoded = Convert.ToBase64String(bytes);
                    }
                    imgs.Add(encoded);
                }
                foreach (var encoded in imgs)
                {
                    string c = "";
                    try
                    {
                        c = await client.RecognizeAsync(encoded);
                    }
                    catch(Exception ex)
                    {
                        c = "识别失败";
                        Console.WriteLine(ex.ToString());
                    }
                    res.Add(new RecResult { ImageSrc = encoded, CardNumber = c });
                }
                Results = res;
            }
            catch
            {
                Message = "访问服务器失败。";
            }
            return Page();
        }
    }
}
