using System.Collections.Generic;
using System.IO;
using Wilder.Common;
using Wilder.Common.Model;

namespace Wilder.FLP
{
    public class Project
    {
        /// <summary>
        /// The volume of the project.
        /// </summary>
        public int MainVolume { get; set; } = 300;

        /// <summary>
        /// The pitch of the project.
        /// </summary>
        public int MainPitch { get; set; } = 0;

        /// <summary>
        /// The pulses per quarter-beat of the project.
        /// </summary>
        public int Ppq { get; set; } = 0;

        /// <summary>
        /// The tempo of the project.
        /// </summary>
        public double Tempo { get; set; } = 140;

        /// <summary>
        /// The title of the project.
        /// </summary>
        public string Title { get; set; } = string.Empty;

        /// <summary>
        /// The comment attached to the project.
        /// </summary>
        public string Comment { get; set; } = string.Empty;

        /// <summary>
        /// The author of the project.
        /// </summary>
        public string Author { get; set; } = string.Empty;

        /// <summary>
        /// The genre of the project.
        /// </summary>
        public string Genre { get; set; } = string.Empty;

        /// <summary>
        /// The xx.xx.xx-formatted string of FL version.
        /// </summary>
        public string VersionString { get; set; } = string.Empty;

        /// <summary>
        /// The int format of the FL version.
        /// </summary>
        public int Version { get; set; } = 0x100;

        /// <summary>
        /// The list of the channels in the project.
        /// </summary>
        public List<Channel> Channels { get; set; } = new List<Channel>();

        /// <summary>
        /// The list of tracks in the project.
        /// </summary>
        public Track[] Tracks { get; set; } = new Track[Constants.MaxTrackCount];

        /// <summary>
        /// The list of patterns in the project.
        /// </summary>
        public List<Pattern> Patterns = new List<Pattern>();

        /// <summary>
        /// The set of inserts for the project (length is equal to Project.MaxInsertCount).
        /// </summary>
        public Insert[] Inserts { get; set; } = new Insert[Constants.MaxInsertCount];

        /// <summary>
        /// Whether the project is set to play truncated notes.
        /// </summary>
        public bool PlayTruncatedNotes { get; set; } = false;

        public Project()
        {
            for (var i = 0; i < Constants.MaxTrackCount; i++)
                Tracks[i] = new Track();

            for (var i = 0; i < Constants.MaxInsertCount; i++)
                Inserts[i] = new Insert { Id = i, Name = $"Insert {i}" };

            Inserts[0].Name = "Master";
        }

        /// <summary>
        /// Load a project from the path to the project file.
        /// </summary>
        /// <param name="projectFilePath"></param>
        /// <returns></returns>
        public static Project Load(string projectFilePath)
        {
            using var stream = File.OpenRead(projectFilePath);
            return Load(stream);
        }

        /// <summary>
        /// Load a project from a given project file stream.
        /// </summary>
        /// <param name="flpFileStream"></param>
        /// <returns></returns>
        private static Project Load(Stream flpFileStream)
        {
            using var reader = new BinaryReader(flpFileStream);
            return Load(reader);
        }

        /// <summary>
        /// Load a project from a given binary reader.
        /// </summary>
        /// <param name="flpReader"></param>
        /// <returns></returns>
        private static Project Load(BinaryReader flpReader)
        {
            var factory = new ProjectFactory();
            return factory.CreateProject(flpReader);
        }
    }
}
