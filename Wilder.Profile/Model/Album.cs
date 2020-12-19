using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;

namespace Wilder.Agency.Model
{
    public class Album
    {
        /// <summary>
        /// The name of the album.
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// The tracks on the album.
        /// </summary>
        public List<Track> Tracks { get; set; }

        /// <summary>
        /// The artist of the album.
        /// </summary>
        [ForeignKey("Name")]
        public Artist Artist { get; set; }
    }
}
