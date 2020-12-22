using System;
using LibVLCSharp.Shared;
using Wilder.Common.Interfaces;

namespace Wilder.Player.VLC
{
    public class VLCPlayer : IPlayer
    {
        private readonly  LibVLC _libvlc;

        public VLCPlayer()
        {
            Core.Initialize();
            _libvlc = new LibVLC(enableDebugLogs: true);
        }

        public void Play(string songPath)
        {
            using var media = new Media(_libvlc, new Uri(songPath));
            using var mediaPlayer = new MediaPlayer(media);
            mediaPlayer.Play();
        }
    }
}
