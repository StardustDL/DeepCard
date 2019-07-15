using System.Net.Http;
using System.Threading.Tasks;

namespace DeepCard.Client.Client.Helpers
{
    public static class HostServer
    {
        public static async Task<string> GetApiServerUrl(HttpClient http)
        {
            HttpResponseMessage response = await http.GetAsync("api/Server/ApiServer");
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                return null;
            }
        }
    }
}
