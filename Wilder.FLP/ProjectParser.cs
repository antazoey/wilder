using System.IO;
using System.Text;
using Wilder.Common.Interfaces;
using Wilder.Common.Model;
using Wilder.FLP.Subparsers;

namespace Wilder.FLP
{
    public class ProjectParser : IProjectParser
    {
        private Channel _currentChannel;
        private Insert _currentInsert;
        private InsertSlot _currentSlot;
        private Pattern _currentPattern;
        private int _versionMajor;

        public ProjectParser()
        {
            Project = new Project();
            _currentInsert = Project.Inserts[0];
        }

        public IProject Parse(string projectFilePath)
        {
            using var stream = File.OpenRead(projectFilePath);
            return Load(stream);
        }

        public static IProject Load(Stream flpFileStream)
        {
            using var reader = new BinaryReader(flpFileStream);
            return Load(reader);
        }

        public static IProject Load(BinaryReader flpReader)
        {
            var factory = new ProjectFactory();
            return ProjectFactory.CreateProject(flpReader);
        }

        public Project Project { get; }

        public GeneratorData GeneratorData => _currentChannel?.Data as GeneratorData;

        public AutomationData AutomationData => _currentChannel?.Data as AutomationData;

        public void ParseAutomationChannels(BinaryReader reader, long dataEnd)
        {
            AutomationParser.ParseAutomationChannels(Project, reader, dataEnd);
        }

        public void ParseAutomationData(BinaryReader reader, AutomationData autData)
        {
            AutomationParser.ParseAutomationData(Project, reader, autData);
        }

        public int CurrentChannel
        {
            set => _currentChannel = Project.Channels[value];
        }

        public uint CurrentChannelColor
        {
            set
            {
                if (_currentChannel != null)
                    _currentChannel.Color = value;
            }
        }

        public uint CurrentChannelMiddleNote
        {
            set
            {
                if (_currentChannel?.Data is GeneratorData genData)
                    genData.BaseNote = value + 9;
            }
        }

        public string CurrentChannelName
        {
            set
            {
                if (_currentChannel != null)
                    _currentChannel.Name = value;
            }
        }

        public void AddChannelFromIndex(int index)
        {
            ChannelParser.AddNewChannelFromIndex(Project, index);
        }

        public ushort CurrentInsertIcon { set => _currentInsert.Icon = value; }

        public uint CurrentInsertColor { set => _currentInsert.Color = value; }

        public void ParseInsertParameters(BinaryReader reader, long dataEnd)
        {
            InsertParser.ParseInsertParameters(Project, reader, dataEnd);
        }

        public void ParseInsertRoutes(BinaryReader reader)
        {
            InsertParser.ParseInsertRoutes(reader, _currentInsert);
            var newIndex = _currentInsert.Id + 1;
            if (newIndex < Project.Inserts.Length)
                _currentInsert = Project.Inserts[newIndex];
        }

        public void ParseInsertFlags(BinaryReader reader)
        {
            InsertParser.ParseInsertFlags(reader, _currentInsert);
            _currentSlot = new InsertSlot();  // New insert route, create new slot
        }

        public static void ParseGeneratorName(GeneratorData genData, string name)
        {
            if (genData == null)
                return;
            genData.SampleFileName = name;
            genData.GeneratorName = "Sampler";
        }

        public string CurrentInsertName
        {
            set => _currentInsert.Name = value;
        }

        public int CurrentPattern
        {
            set => _currentPattern = Project.Patterns[value - 1];
        }

        public string CurrentPatternName
        {
            set
            {
                if (_currentPattern != null)
                    _currentPattern.Name = value;
            }
        }

        public int CurrentSlot
        {
            set
            {
                if (_currentSlot != null) // Current slot after plugin event, now re-arranged.
                {
                    _currentInsert.Slots[value] = _currentSlot;
                    _currentSlot = new InsertSlot();
                }
                _currentChannel = null;
            }
        }

        public void ParsePatternNotes(BinaryReader reader, long dataEnd)
        {
            PatternNotesParser.ParsePatternNotes(Project, reader, _currentPattern, dataEnd);
        }

        public int PatternsCount => Project.Patterns.Count;

        public void AddPatternFromCount()
            => Project.Patterns.Add(new Pattern { Id = PatternsCount });


        public void ParsePlayListItems(BinaryReader reader, long dataEnd)
        {
            PlaylistParser.ParsePlayListItems(Project, reader, _versionMajor, dataEnd);
        }

        public void InitSlotPlugins(BinaryReader reader, GeneratorData genData, int bufferLength)
        {
            SlotPluginsParser.InitSlotPlugins(reader, genData, _currentSlot, bufferLength);
        }

        public void ParseVersion(byte[] bytes)
        {
            Project.VersionString = Encoding.UTF8.GetString(bytes);
            if (Project.VersionString.EndsWith("\0"))
            {
                var endIndex = Project.VersionString.Length - 1;
                Project.VersionString = Project.VersionString.Substring(0, endIndex);
            }
            var numbers = Project.VersionString.Split('.');
            _versionMajor = int.Parse(numbers[0]);
            Project.Version = (int.Parse(numbers[0]) << 8) +
                               (int.Parse(numbers[1]) << 4) +
                               (int.Parse(numbers[2]) << 0);
        }
    }
}
