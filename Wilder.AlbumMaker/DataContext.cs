using System.Diagnostics.CodeAnalysis;
using Microsoft.EntityFrameworkCore;
using Wilder.AlbumMaker.Model;

namespace Wilder.AlbumMaker
{
    [ExcludeFromCodeCoverage]
    internal class DataContext : DbContext
    {
        internal DbSet<Artist> Artists { get; set; }
        internal DbSet<Album> Albums { get; set; }
        internal DbSet<Album> Tracks { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder
                .UseSqlite(@"Data Source=WildDB.db;");
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Artist>().ToTable("Artists");
            modelBuilder.Entity<Album>().ToTable("Albums");
            modelBuilder.Entity<Track>().ToTable("Tracks");
        }
    }
}
