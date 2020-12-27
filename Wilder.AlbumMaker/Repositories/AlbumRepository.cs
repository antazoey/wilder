using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Wilder.AlbumMaker.Model;
using Wilder.Common.Interfaces;

namespace Wilder.AlbumMaker.Repositories
{
    public class AlbumRepository : IAlbumRepository
    {
        private readonly DataContext _context = new DataContext();
        
        public List<Album> GetAllAlbums(string artistName) => _context.Albums.ToList();

        public List<Album> GetAlbumsForArtist(string artistName)
        {
            return _context.Albums.Where(album => album.Artist.Name == artistName).ToList();
        }
        
        public async Task CreateAlbum()
        {
            throw new System.NotImplementedException();
        }
    }
}