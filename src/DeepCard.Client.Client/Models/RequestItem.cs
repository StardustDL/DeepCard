using System;
using System.Linq;

namespace DeepCard.Client.Client.Models
{
    public class RequestItem
    {
        public string EncodedFile { get; set; }

        public BankCardInfo Result { get; set; }

        public string Name { get; set; }

        public int Size { get; set; }

        public TimeSpan? CostTime { get; set; }

        public string Message { get; set; }

        public string View
        {
            get
            {
                return $"{Name} ({(Size / 1024)} KB)";
            }
        }
    }
}
