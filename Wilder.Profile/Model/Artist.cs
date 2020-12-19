using System.Collections.Generic;

namespace Wilder.Agency.Model
{
    public class Artist
    {
        /// <summary>
        /// The name of the artist.
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// All the albums by the artist.
        /// </summary>
        public List<Album> Discography { get; set; }

        /// <summary>
        /// All the genres that describe the artist.
        /// </summary>
        public List<string> Genre { get; set; }
    }
}
